import anthropic
import os
import re
from typing import Dict, List, Optional
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import text
import json

class CachedRecommendationService:
    def __init__(self):
        api_key = os.environ.get("ANTHROPIC_API_KEY")
        if not api_key:
            print("❌ ANTHROPIC_API_KEY not found in environment variables!")
            raise ValueError("ANTHROPIC_API_KEY environment variable is required")
        else:
            print(f"✅ ANTHROPIC_API_KEY loaded: {api_key[:10]}...")
        
        self.client = anthropic.Anthropic(api_key=api_key)
        self.cache_duration_days = 7  # Recommendations valid for 7 days
        
    def get_recommendations(
        self,
        customer_id: int,
        domain_name: str,
        db: Session,
        force_regenerate: bool = False
    ) -> Dict:
        """
        Get recommendations - from cache if available and fresh, 
        otherwise generate new ones
        """
        domain_id = self._get_domain_id(domain_name, db)
        
        if not force_regenerate:
            # Try to get from cache first
            cached = self._get_cached_recommendations(customer_id, domain_id, db)
            if cached:
                return {
                    "success": True,
                    "source": "cache",
                    "recommendations": cached["recommendations"],
                    "generated_at": cached["generated_at"],
                    "expires_at": cached["expires_at"],
                    "model": cached["model_version"]
                }
        
        # Generate new recommendations
        return self._generate_and_store_recommendations(
            customer_id, domain_name, domain_id, db
        )
    
    def _get_domain_id(self, domain_name: str, db: Session) -> int:
        """Get domain_id from domain name"""
        domain_map = {
            "gut": 1,
            "liver": 2,
            "heart": 3,
            "skin": 4,
            "cognitive": 5,
            "aging": 6
        }
        return domain_map.get(domain_name.lower())
    
    def _get_cached_recommendations(
        self,
        customer_id: int,
        domain_id: int,
        db: Session
    ) -> Optional[Dict]:
        """Retrieve valid cached recommendations"""
        try:
            query = text("""
                SELECT 
                    dietary_recommendations,
                    lifestyle_recommendations,
                    probiotic_recommendations,
                    prebiotic_recommendations,
                    summary,
                    generated_at,
                    expires_at,
                    model_version
                FROM microbiome.customer_recommendations
                WHERE customer_id = :customer_id
                  AND domain_id = :domain_id
                  AND is_active = TRUE
                  AND expires_at > NOW()
                ORDER BY generated_at DESC
                LIMIT 1
            """)
            
            result = db.execute(query, {
                "customer_id": customer_id,
                "domain_id": domain_id
            }).fetchone()
            
            if result:
                return {
                    "recommendations": {
                        "dietary_recommendations": result.dietary_recommendations,
                        "lifestyle_recommendations": result.lifestyle_recommendations,
                        "probiotic_recommendations": result.probiotic_recommendations,
                        "prebiotic_recommendations": result.prebiotic_recommendations,
                        "summary": result.summary
                    },
                    "generated_at": result.generated_at.isoformat(),
                    "expires_at": result.expires_at.isoformat(),
                    "model_version": result.model_version
                }
            
            return None
            
        except Exception as e:
            print(f"Error retrieving cached recommendations: {e}")
            return None
    
    def _generate_and_store_recommendations(
        self,
        customer_id: int,
        domain_name: str,
        domain_id: int,
        db: Session
    ) -> Dict:
        """Generate new recommendations and store in database"""
        try:
            # Get customer data (reuse existing functions)
            from DBCustomerPortal import get_customer_info, get_customer_bacteria_domains
            
            customer_info = get_customer_info(customer_id, db)
            domain_bacteria = get_customer_bacteria_domains(customer_id, db)
            
            if not customer_info.get("success") or not domain_bacteria.get("success"):
                raise Exception("Failed to fetch customer data")
            
            domain_data = domain_bacteria["domain_bacteria"].get(domain_name.lower())
            if not domain_data:
                raise Exception(f"Domain '{domain_name}' not found")
            
            # Generate recommendations using Claude
            customer_context = self._build_customer_context(
                customer_info["customer_info"],
                domain_bacteria["overall_health"]
            )
            domain_context = self._build_domain_context(domain_name, domain_data)
            
            recommendations = self._call_claude_api(customer_context, domain_context, domain_name)
            
            # Store in database
            self._store_recommendations(
                customer_id=customer_id,
                domain_id=domain_id,
                recommendations=recommendations,
                customer_age=customer_info["customer_info"].get("age"),
                domain_score=domain_data.get("score"),
                domain_diversity=domain_data.get("diversity"),
                db=db
            )
            
            return {
                "success": True,
                "source": "generated",
                "recommendations": recommendations,
                "generated_at": datetime.now().isoformat(),
                "expires_at": (datetime.now() + timedelta(days=self.cache_duration_days)).isoformat(),
                "model": "claude-sonnet-4.5"
            }
            
        except Exception as e:
            print(f"Error generating recommendations: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def _build_customer_context(self, customer_info: Dict, overall_health: Dict) -> str:
        """Build customer context string"""
        return f"""
Customer Profile:
- Age: {customer_info.get('age', 'N/A')}
- Gender: {customer_info.get('gender', 'N/A')}
- Location: {customer_info.get('city', '')}, {customer_info.get('state', '')}

Overall Health Metrics:
- Overall Health Score: {overall_health.get('overall_score', 'N/A')}/5.0
- Diversity Score: {overall_health.get('diversity_score', 'N/A')}/5.0
- Total Bacteria Analyzed: {overall_health.get('total_bacteria_analyzed', 'N/A')}
- Beneficial Bacteria: {overall_health.get('beneficial_bacteria', 'N/A')}
- Concerning Bacteria: {overall_health.get('concerning_bacteria', 'N/A')}
"""
    
    def _build_domain_context(self, domain_name: str, domain_data: Dict) -> str:
        """Build domain-specific context"""
        bacteria_list = domain_data.get('bacteria', [])
        beneficial = [b for b in bacteria_list if b.get('category') == 'beneficial']
        concerning = [b for b in bacteria_list if b.get('category') == 'concerning']
        
        context = f"""
{domain_name.upper()} Health Domain Analysis:
- Domain Score: {domain_data.get('score', 'N/A')}/5.0
- Diversity: {domain_data.get('diversity', 'N/A')}/5.0
- Status: {domain_data.get('status', 'N/A')}

Microbiome Composition:
- Total Species: {len(bacteria_list)}
- Beneficial: {len(beneficial)} species
- Concerning: {len(concerning)} species
"""
        
        if beneficial:
            context += "\nTop Beneficial Bacteria:\n"
            for b in beneficial[:5]:
                context += f"  • {b.get('species_name')}: {b.get('abundance', 'N/A')}% abundance\n"
        
        if concerning:
            context += "\nConcerning Bacteria Detected:\n"
            for b in concerning[:3]:
                context += f"  • {b.get('species_name')}: {b.get('abundance', 'N/A')}% abundance\n"
        
        return context
    
    def _call_claude_api(self, customer_context: str, domain_context: str, domain_name: str) -> Dict:
        """Call Claude API to generate recommendations"""
        prompt = f"""{customer_context}

{domain_context}

Based on this customer's profile and their {domain_name} health data, provide highly personalized, evidence-based recommendations.

Requirements:
1. **Dietary Recommendations** (5-7 items):
   - Specific foods that support beneficial bacteria
   - Foods to avoid that feed concerning bacteria
   - Include reasoning based on the bacteria present

2. **Lifestyle Modifications** (3-5 items):
   - Practical, actionable changes
   - Specific to this domain (e.g., stress management for gut, sleep for cognitive)
   - Consider the customer's age and location

3. **Probiotic Recommendations** (2-3 items):
   - Specific strains that address the bacterial imbalances
   - Recommended CFU counts
   - Scientific rationale for each strain

4. **Prebiotic Recommendations** (3-4 items):
   - Fiber sources to feed beneficial bacteria
   - Daily amounts
   - Best food sources

5. **Summary** (2-3 sentences):
   - Most critical interventions
   - Expected timeline for improvement

Format as JSON:
{{
  "dietary_recommendations": [
    {{
      "item": "Food name",
      "rationale": "Why this helps based on bacteria present",
      "frequency": "Daily/Weekly",
      "priority": "high/medium/low"
    }}
  ],
  "lifestyle_recommendations": [
    {{
      "activity": "Specific activity",
      "rationale": "How this impacts the microbiome",
      "implementation": "Practical how-to",
      "priority": "high/medium/low"
    }}
  ],
  "probiotic_recommendations": [
    {{
      "strain": "Specific probiotic strain",
      "dosage": "CFU amount",
      "rationale": "Why this strain for this customer",
      "duration": "Recommended duration"
    }}
  ],
  "prebiotic_recommendations": [
    {{
      "source": "Prebiotic food",
      "amount": "Daily amount in grams",
      "rationale": "Benefits for this customer",
      "food_sources": ["food1", "food2"]
    }}
  ],
  "summary": "Concise action plan summary"
}}

Be specific and actionable. Prioritize interventions that address the concerning bacteria while supporting beneficial strains."""

        try:
            message = self.client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=2500,
                temperature=0.3,
                messages=[{"role": "user", "content": prompt}]
            )
            
            response_text = message.content[0].text
            
            # Extract JSON
            if "```json" in response_text:
                json_str = response_text.split("```json")[1].split("```")[0].strip()
            elif "```" in response_text:
                json_str = response_text.split("```")[1].split("```")[0].strip()
            else:
                json_str = response_text.strip()
            
            # Clean up the JSON string - remove any trailing content after the closing brace
            import re
            json_match = re.search(r'\{.*\}', json_str, re.DOTALL)
            if json_match:
                json_str = json_match.group()
            
            return json.loads(json_str)
            
        except Exception as e:
            print(f"Error calling Claude API: {e}")
            raise
    
    def _store_recommendations(
        self,
        customer_id: int,
        domain_id: int,
        recommendations: Dict,
        customer_age: int,
        domain_score: float,
        domain_diversity: float,
        db: Session
    ):
        """Store recommendations in database"""
        try:
            # Deactivate old recommendations
            deactivate_query = text("""
                UPDATE microbiome.customer_recommendations
                SET is_active = FALSE
                WHERE customer_id = :customer_id
                  AND domain_id = :domain_id
                  AND is_active = TRUE
            """)
            db.execute(deactivate_query, {
                "customer_id": customer_id,
                "domain_id": domain_id
            })
            
            # Insert new recommendations
            insert_query = text("""
                INSERT INTO microbiome.customer_recommendations (
                    customer_id,
                    domain_id,
                    dietary_recommendations,
                    lifestyle_recommendations,
                    probiotic_recommendations,
                    prebiotic_recommendations,
                    summary,
                    generated_at,
                    expires_at,
                    model_version,
                    customer_age,
                    domain_score,
                    domain_diversity,
                    is_active
                ) VALUES (
                    :customer_id,
                    :domain_id,
                    CAST(:dietary AS jsonb),
                    CAST(:lifestyle AS jsonb),
                    CAST(:probiotic AS jsonb),
                    CAST(:prebiotic AS jsonb),
                    :summary,
                    NOW(),
                    NOW() + CAST(:days_str AS INTERVAL),
                    :model,
                    :age,
                    :score,
                    :diversity,
                    TRUE
                )
            """)
            
            db.execute(insert_query, {
                "customer_id": customer_id,
                "domain_id": domain_id,
                "dietary": json.dumps(recommendations.get("dietary_recommendations", [])),
                "lifestyle": json.dumps(recommendations.get("lifestyle_recommendations", [])),
                "probiotic": json.dumps(recommendations.get("probiotic_recommendations", [])),
                "prebiotic": json.dumps(recommendations.get("prebiotic_recommendations", [])),
                "summary": recommendations.get("summary", ""),
                "days_str": f"{self.cache_duration_days} days",
                "model": "claude-3-5-sonnet",
                "age": customer_age,
                "score": domain_score,
                "diversity": domain_diversity
            })
            
            db.commit()
            print(f"✅ Stored recommendations for customer {customer_id}, domain {domain_id}")
            
        except Exception as e:
            db.rollback()
            print(f"Error storing recommendations: {e}")
            raise
    
    def generate_all_domains_on_login(
        self,
        customer_id: int,
        db: Session
    ) -> Dict:
        """
        Generate recommendations for ALL domains when customer logs in
        Use this on login event
        """
        domains = ["gut", "liver", "heart", "skin", "cognitive", "aging"]
        results = {}
        
        for domain in domains:
            try:
                result = self.get_recommendations(
                    customer_id=customer_id,
                    domain_name=domain,
                    db=db,
                    force_regenerate=False  # Only generate if expired
                )
                results[domain] = result
            except Exception as e:
                print(f"Error generating recommendations for {domain}: {e}")
                results[domain] = {"success": False, "error": str(e)}
        
        return {
            "success": True,
            "customer_id": customer_id,
            "domains_processed": len(results),
            "results": results
        }
    
    def get_cache_status(self, customer_id: int, db: Session) -> Dict:
        """Get cache status for all domains for a customer"""
        try:
            query = text("""
                SELECT 
                    hd.domain_name,
                    cr.generated_at,
                    cr.expires_at,
                    cr.model_version,
                    CASE 
                        WHEN cr.expires_at > NOW() THEN 'valid'
                        WHEN cr.expires_at IS NULL THEN 'none'
                        ELSE 'expired'
                    END as cache_status
                FROM microbiome.health_domains hd
                LEFT JOIN microbiome.customer_recommendations cr
                    ON hd.domain_id = cr.domain_id
                    AND cr.customer_id = :customer_id
                    AND cr.is_active = TRUE
                ORDER BY hd.domain_id
            """)
            
            result = db.execute(query, {"customer_id": customer_id}).fetchall()
            
            status = {}
            for row in result:
                status[row.domain_name] = {
                    "cache_status": row.cache_status,
                    "generated_at": row.generated_at.isoformat() if row.generated_at else None,
                    "expires_at": row.expires_at.isoformat() if row.expires_at else None,
                    "model_version": row.model_version
                }
            
            return {
                "success": True,
                "customer_id": customer_id,
                "cache_status": status
            }
            
        except Exception as e:
            print(f"Error getting cache status: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def cleanup_expired_recommendations(self, db: Session) -> Dict:
        """Clean up expired recommendations (maintenance function)"""
        try:
            cleanup_query = text("""
                DELETE FROM microbiome.customer_recommendations
                WHERE expires_at < NOW() - INTERVAL '30 days'
            """)
            
            result = db.execute(cleanup_query)
            db.commit()
            
            return {
                "success": True,
                "deleted_count": result.rowcount,
                "message": f"Cleaned up {result.rowcount} expired recommendations"
            }
            
        except Exception as e:
            db.rollback()
            print(f"Error cleaning up expired recommendations: {e}")
            return {
                "success": False,
                "error": str(e)
            }