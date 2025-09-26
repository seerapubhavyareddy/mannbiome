# report_generator.py
"""
PDF Report Generation Module for MannBiome Health Analysis
"""

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.units import inch
import io
from datetime import datetime
from typing import List, Dict, Any, Optional

class MannBiomePDFGenerator:
    """PDF Generator for MannBiome Health Reports"""
    
    def __init__(self):
        self.buffer = None
        self.canvas = None
        self.width = letter[0]
        self.height = letter[1]
        
    def create_full_report(self, user_data: Dict, health_data: Dict) -> bytes:
        """Generate a comprehensive full health report"""
        try:
            self.buffer = io.BytesIO()
            p = canvas.Canvas(self.buffer, pagesize=letter)
            
            # Title Page
            self._add_title_page(p, user_data)
            
            # Health Summary
            self._add_health_summary(p, health_data)
            
            # Domain Analysis
            self._add_domain_analysis(p, health_data)
            
            # Recommendations
            self._add_recommendations(p, health_data)
            
            # Disclaimers
            self._add_disclaimers(p)
            
            p.save()
            self.buffer.seek(0)
            return self.buffer.getvalue()
            
        except Exception as e:
            return self._create_error_pdf(f"Error generating full report: {str(e)}")
    
    def create_domain_report(self, user_data: Dict, health_data: Dict, domains: List[str]) -> bytes:
        """Generate a domain-specific health report"""
        try:
            self.buffer = io.BytesIO()
            p = canvas.Canvas(self.buffer, pagesize=letter)
            
            # Title Page
            self._add_title_page(p, user_data, report_type="Domain-Specific")
            
            # Domain-specific analysis
            self._add_domain_specific_analysis(p, health_data, domains)
            
            # Domain-specific recommendations
            self._add_domain_recommendations(p, domains)
            
            # Disclaimers
            self._add_disclaimers(p)
            
            p.save()
            self.buffer.seek(0)
            return self.buffer.getvalue()
            
        except Exception as e:
            return self._create_error_pdf(f"Error generating domain report: {str(e)}")
    
    def _add_title_page(self, p: canvas.Canvas, user_data: Dict, report_type: str = "Comprehensive"):
        """Add title page with patient information"""
        user = user_data.get("user", {})
        
        # Main title
        p.setFont("Helvetica-Bold", 24)
        p.drawString(50, self.height - 80, "🧬 MannBiome Health Analysis")
        
        # Subtitle
        p.setFont("Helvetica", 18)
        p.drawString(50, self.height - 110, f"{report_type} Report")
        
        # Patient info box
        y_pos = self.height - 160
        p.setFont("Helvetica-Bold", 14)
        p.drawString(50, y_pos, "Patient Information")
        
        # Draw box around patient info
        p.rect(50, y_pos - 120, 500, 110)
        
        y_pos -= 25
        p.setFont("Helvetica", 12)
        p.drawString(60, y_pos, f"Name: {user.get('full_name', 'N/A')}")
        y_pos -= 20
        p.drawString(60, y_pos, f"Report ID: {user.get('report_id', 'N/A')}")
        y_pos -= 20
        p.drawString(60, y_pos, f"Generated: {datetime.now().strftime('%B %d, %Y')}")
        y_pos -= 20
        p.drawString(60, y_pos, f"Last Updated: {user.get('last_updated', 'N/A')}")
        
        # Add generation timestamp
        p.setFont("Helvetica", 10)
        p.drawString(50, 50, f"Report generated on {datetime.now().strftime('%B %d, %Y at %I:%M %p')}")
        
        p.showPage()
    
    def _add_health_summary(self, p: canvas.Canvas, health_data: Dict):
        """Add health summary section"""
        health = health_data.get("health_data", {})
        y_pos = self.height - 80
        
        # Section title
        p.setFont("Helvetica-Bold", 20)
        p.drawString(50, y_pos, "📊 Executive Summary")
        y_pos -= 40
        
        # Overall scores
        p.setFont("Helvetica-Bold", 16)
        p.drawString(50, y_pos, "Your Health Scores")
        y_pos -= 30
        
        p.setFont("Helvetica", 12)
        overall_score = health.get('overall_score', 'N/A')
        diversity_score = health.get('diversity_score', 'N/A')
        
        p.drawString(50, y_pos, f"Overall Health Score: {overall_score}/5.0")
        y_pos -= 20
        p.drawString(50, y_pos, f"Microbiome Diversity: {diversity_score}/5.0")
        y_pos -= 30
        
        # Diversity explanation
        p.setFont("Helvetica-Bold", 14)
        p.drawString(50, y_pos, "Understanding Your Microbiome Diversity")
        y_pos -= 25
        
        p.setFont("Helvetica", 11)
        explanation_lines = [
            f"Your microbiome diversity score of {diversity_score} reflects the variety and balance",
            "of microbial species in your gut ecosystem. Higher diversity is generally associated",
            "with better health outcomes, improved immune function, and enhanced resilience",
            "against digestive issues and inflammation.",
            "",
            "Score Interpretation:",
            "• 4.0-5.0: Excellent diversity - Continue current practices",
            "• 3.0-3.9: Good diversity - Minor optimizations recommended", 
            "• 2.0-2.9: Moderate diversity - Targeted improvements needed",
            "• Below 2.0: Low diversity - Comprehensive intervention recommended"
        ]
        
        for line in explanation_lines:
            p.drawString(50, y_pos, line)
            y_pos -= 15
            if y_pos < 100:
                p.showPage()
                y_pos = self.height - 50
        
        p.showPage()
    
    def _add_domain_analysis(self, p: canvas.Canvas, health_data: Dict):
        """Add comprehensive domain analysis"""
        health = health_data.get("health_data", {})
        domains = health.get("domains", {})
        y_pos = self.height - 80
        
        # Section title
        p.setFont("Helvetica-Bold", 20)
        p.drawString(50, y_pos, "🎯 Health Domain Analysis")
        y_pos -= 50
        
        # Categorize domains
        needs_attention = []
        good_domains = []
        moderate_domains = []
        
        for domain_name, domain_data in domains.items():
            if domain_name == "overall":
                continue
            
            score = float(domain_data.get('score', 0))
            if score >= 3.5:
                good_domains.append((domain_name, domain_data))
            elif score >= 2.5:
                moderate_domains.append((domain_name, domain_data))
            else:
                needs_attention.append((domain_name, domain_data))
        
        # Areas needing attention
        if needs_attention:
            p.setFont("Helvetica-Bold", 16)
            p.setFillColor(colors.red)
            p.drawString(50, y_pos, "🔴 Areas Needing Attention")
            p.setFillColor(colors.black)
            y_pos -= 30
            
            for domain_name, domain_data in needs_attention:
                y_pos = self._add_domain_detail(p, domain_name, domain_data, y_pos)
                y_pos -= 15
        
        # Moderate performing areas
        if moderate_domains:
            if y_pos < 200:
                p.showPage()
                y_pos = self.height - 50
            
            p.setFont("Helvetica-Bold", 16)
            p.setFillColor(colors.orange)
            p.drawString(50, y_pos, "🟡 Areas for Improvement")
            p.setFillColor(colors.black)
            y_pos -= 30
            
            for domain_name, domain_data in moderate_domains:
                y_pos = self._add_domain_detail(p, domain_name, domain_data, y_pos)
                y_pos -= 15
        
        # Strong performing areas
        if good_domains:
            if y_pos < 200:
                p.showPage()
                y_pos = self.height - 50
            
            p.setFont("Helvetica-Bold", 16)
            p.setFillColor(colors.green)
            p.drawString(50, y_pos, "🟢 Strong Performing Areas")
            p.setFillColor(colors.black)
            y_pos -= 30
            
            for domain_name, domain_data in good_domains:
                y_pos = self._add_domain_detail(p, domain_name, domain_data, y_pos)
                y_pos -= 15
        
        p.showPage()
    
    def _add_domain_detail(self, p: canvas.Canvas, domain_name: str, domain_data: Dict, y_pos: int) -> int:
        """Add detailed information for a single domain"""
        if y_pos < 100:
            p.showPage()
            y_pos = self.height - 50
        
        p.setFont("Helvetica-Bold", 12)
        p.drawString(70, y_pos, f"{domain_name.title()} Health")
        y_pos -= 18
        
        p.setFont("Helvetica", 10)
        score = domain_data.get('score', 'N/A')
        diversity = domain_data.get('diversity', 'N/A')
        status = domain_data.get('status', 'unknown').title()
        
        p.drawString(85, y_pos, f"Score: {score}/5.0  |  Diversity: {diversity}/5.0  |  Status: {status}")
        
        return y_pos - 18
    
    def _add_domain_specific_analysis(self, p: canvas.Canvas, health_data: Dict, domains: List[str]):
        """Add detailed analysis for specific domains"""
        health = health_data.get("health_data", {})
        domain_data = health.get("domains", {})
        y_pos = self.height - 80
        
        # Section title
        p.setFont("Helvetica-Bold", 20)
        p.drawString(50, y_pos, f"Domain Analysis: {', '.join([d.title() for d in domains])}")
        y_pos -= 50
        
        for domain in domains:
            if domain in domain_data:
                if y_pos < 150:
                    p.showPage()
                    y_pos = self.height - 50
                
                data = domain_data[domain]
                
                # Domain header
                p.setFont("Helvetica-Bold", 16)
                p.drawString(50, y_pos, f"{domain.title()} Health Analysis")
                y_pos -= 30
                
                # Scores
                p.setFont("Helvetica", 12)
                p.drawString(50, y_pos, f"Health Score: {data.get('score', 'N/A')}/5.0")
                y_pos -= 18
                p.drawString(50, y_pos, f"Diversity Score: {data.get('diversity', 'N/A')}/5.0")
                y_pos -= 18
                p.drawString(50, y_pos, f"Current Status: {data.get('status', 'Unknown').title()}")
                y_pos -= 35
                
                # Domain-specific insights
                insights = self._get_domain_insights(domain, data)
                if insights:
                    p.setFont("Helvetica-Bold", 12)
                    p.drawString(50, y_pos, "Key Insights:")
                    y_pos -= 20
                    
                    p.setFont("Helvetica", 10)
                    for insight in insights:
                        p.drawString(60, y_pos, f"• {insight}")
                        y_pos -= 15
                        if y_pos < 50:
                            p.showPage()
                            y_pos = self.height - 50
                
                y_pos -= 20
        
        p.showPage()
    
    def _add_recommendations(self, p: canvas.Canvas, health_data: Dict):
        """Add general recommendations section"""
        y_pos = self.height - 80
        
        # Section title
        p.setFont("Helvetica-Bold", 20)
        p.drawString(50, y_pos, "💊 Personalized Recommendations")
        y_pos -= 40
        
        # General recommendations
        general_recs = [
            "Increase dietary fiber through a variety of vegetables and whole grains",
            "Include fermented foods like yogurt, kimchi, kefir, and sauerkraut daily",
            "Consider high-quality probiotic supplementation with multiple strains",
            "Maintain regular moderate exercise (30+ minutes daily)",
            "Prioritize sleep quality (7-9 hours per night with consistent schedule)",
            "Practice stress management through meditation, yoga, or deep breathing",
            "Stay well-hydrated with 8-10 glasses of clean water daily",
            "Limit processed foods, refined sugars, and artificial additives",
            "Include prebiotic foods like garlic, onions, and Jerusalem artichokes",
            "Consider omega-3 supplementation for anti-inflammatory support"
        ]
        
        p.setFont("Helvetica-Bold", 14)
        p.drawString(50, y_pos, "General Health Optimization")
        y_pos -= 25
        
        p.setFont("Helvetica", 11)
        for rec in general_recs:
            if y_pos < 50:
                p.showPage()
                y_pos = self.height - 50
            p.drawString(50, y_pos, f"• {rec}")
            y_pos -= 16
        
        p.showPage()
    
    def _add_domain_recommendations(self, p: canvas.Canvas, domains: List[str]):
        """Add domain-specific recommendations"""
        y_pos = self.height - 80
        
        # Section title
        p.setFont("Helvetica-Bold", 20)
        p.drawString(50, y_pos, "🎯 Domain-Specific Recommendations")
        y_pos -= 40
        
        for domain in domains:
            if y_pos < 200:
                p.showPage()
                y_pos = self.height - 50
            
            # Domain header
            p.setFont("Helvetica-Bold", 16)
            p.drawString(50, y_pos, f"{domain.title()} Health Optimization")
            y_pos -= 30
            
            # Get domain-specific recommendations
            recs = self._get_domain_recommendations(domain)
            
            p.setFont("Helvetica", 11)
            for rec in recs:
                if y_pos < 50:
                    p.showPage()
                    y_pos = self.height - 50
                p.drawString(50, y_pos, f"• {rec}")
                y_pos -= 16
            
            y_pos -= 20
        
        p.showPage()
    
    def _add_disclaimers(self, p: canvas.Canvas):
        """Add disclaimers and footer information"""
        y_pos = self.height - 80
        
        # Section title
        p.setFont("Helvetica-Bold", 18)
        p.drawString(50, y_pos, "⚖️ Important Information")
        y_pos -= 40
        
        # Medical disclaimer
        p.setFont("Helvetica-Bold", 12)
        p.drawString(50, y_pos, "Medical Disclaimer")
        y_pos -= 20
        
        disclaimer_text = [
            "This report is for informational and educational purposes only and is not intended",
            "as medical advice, diagnosis, or treatment. The information provided should not be",
            "used for diagnosing or treating a health condition or disease. Always consult with",
            "a qualified healthcare provider before making any changes to your diet, supplements,",
            "or treatment regimen."
        ]
        
        p.setFont("Helvetica", 10)
        for line in disclaimer_text:
            p.drawString(50, y_pos, line)
            y_pos -= 15
        
        y_pos -= 20
        
        # Data interpretation
        p.setFont("Helvetica-Bold", 12)
        p.drawString(50, y_pos, "Data Interpretation")
        y_pos -= 20
        
        interpretation_text = [
            "Microbiome analysis results are based on current scientific understanding and may",
            "be subject to interpretation. Individual results may vary, and optimal ranges are",
            "based on population studies. This analysis represents a snapshot in time and may",
            "change based on diet, lifestyle, medications, and other factors."
        ]
        
        p.setFont("Helvetica", 10)
        for line in interpretation_text:
            p.drawString(50, y_pos, line)
            y_pos -= 15
        
        # Footer
        p.setFont("Helvetica", 8)
        p.drawString(50, 50, "MannBiome Health Analysis Platform - Confidential Patient Report")
        p.drawString(50, 35, f"Generated: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}")
    
    def _get_domain_insights(self, domain: str, domain_data: Dict) -> List[str]:
        """Get domain-specific insights based on scores"""
        score = float(domain_data.get('score', 0))
        
        insights_map = {
            "liver": [
                "Your liver health markers indicate the efficiency of detoxification pathways",
                "Consider supporting Phase I and Phase II liver detoxification",
                "Bile acid metabolism may benefit from targeted interventions"
            ],
            "gut": [
                "Gut microbiome diversity directly impacts overall health outcomes",
                "Beneficial bacteria levels influence immune system function", 
                "Intestinal barrier integrity affects nutrient absorption"
            ],
            "heart": [
                "Cardiovascular health markers reflect systemic inflammation levels",
                "Heart-healthy bacteria influence cholesterol metabolism",
                "Vascular health correlates with microbial diversity"
            ],
            "cognitive": [
                "Brain-gut axis communication affects neurotransmitter production",
                "Cognitive function benefits from optimal microbiome balance",
                "Neuroinflammation markers indicate brain health status"
            ],
            "skin": [
                "Skin microbiome diversity reflects internal health status",
                "Collagen synthesis markers indicate aging and repair processes",
                "Inflammatory skin conditions link to gut health imbalances"
            ],
            "aging": [
                "Cellular regeneration markers indicate biological aging rate",
                "Antioxidant defense systems reflect longevity potential",
                "Metabolic efficiency impacts healthy aging processes"
            ]
        }
        
        return insights_map.get(domain, [])
    
    def _get_domain_recommendations(self, domain: str) -> List[str]:
        """Get specific recommendations for each domain"""
        recommendations_map = {
            "liver": [
                "Increase cruciferous vegetables (broccoli, kale, Brussels sprouts)",
                "Consider milk thistle or NAC (N-Acetyl Cysteine) supplementation",
                "Reduce alcohol consumption and processed food intake",
                "Include sulfur-rich foods like garlic, onions, and eggs",
                "Support glutathione production with selenium and vitamin C",
                "Practice intermittent fasting to support liver regeneration"
            ],
            "gut": [
                "Increase prebiotic fiber intake through diverse plant foods",
                "Include fermented foods like kimchi, sauerkraut, and kefir daily",
                "Consider targeted probiotic supplementation with multiple strains",
                "Support gut lining with L-glutamine and zinc carnosine",
                "Minimize antibiotic use unless medically necessary",
                "Reduce stress through mindfulness and relaxation techniques"
            ],
            "heart": [
                "Include omega-3 rich foods like fatty fish and walnuts",
                "Increase soluble fiber through oats, beans, and berries",
                "Regular cardiovascular exercise (150+ minutes per week)",
                "Limit sodium intake and increase potassium-rich foods",
                "Consider CoQ10 and magnesium supplementation",
                "Manage stress through meditation and adequate sleep"
            ],
            "cognitive": [
                "Include brain-healthy fats like DHA and omega-3 fatty acids",
                "Prioritize quality sleep (7-9 hours with consistent schedule)",
                "Engage in regular mental challenges and learning activities",
                "Support neurotransmitter production with B-vitamins",
                "Practice stress reduction and mindfulness meditation",
                "Maintain social connections and meaningful relationships"
            ],
            "skin": [
                "Stay well-hydrated with 8-10 glasses of water daily",
                "Include vitamin C rich foods for collagen synthesis",
                "Consider collagen peptide supplementation",
                "Protect skin from UV damage with sunscreen and antioxidants",
                "Reduce sugar intake to prevent glycation damage",
                "Support skin microbiome with gentle, pH-balanced products"
            ],
            "aging": [
                "Include antioxidant-rich foods like berries and dark chocolate",
                "Practice regular strength training to maintain muscle mass",
                "Support mitochondrial health with CoQ10 and PQQ",
                "Consider resveratrol and other longevity compounds",
                "Maintain optimal vitamin D levels through sun and supplementation",
                "Practice caloric restriction or intermittent fasting protocols"
            ]
        }
        
        return recommendations_map.get(domain, [])
    
    def _create_error_pdf(self, error_message: str) -> bytes:
        """Create a simple error PDF when generation fails"""
        buffer = io.BytesIO()
        p = canvas.Canvas(buffer, pagesize=letter)
        
        # Header
        p.setFont("Helvetica-Bold", 20)
        p.drawString(50, self.height - 100, "MannBiome Report Generation Error")
        
        # Error message
        p.setFont("Helvetica", 12)
        p.drawString(50, self.height - 150, "An error occurred while generating your report:")
        p.drawString(50, self.height - 180, error_message)
        p.drawString(50, self.height - 210, "Please contact support for assistance.")
        
        # Contact info
        p.setFont("Helvetica", 10)
        p.drawString(50, self.height - 250, "Support Email: support@mannbiome.com")
        p.drawString(50, self.height - 270, f"Error reported on: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}")
        
        # Footer
        p.setFont("Helvetica", 8)
        p.drawString(50, 50, "MannBiome Health Analysis Platform - Error Report")
        
        p.save()
        buffer.seek(0)
        return buffer.getvalue()

def generate_filename(report_type: str, domains: List[str] = None, customer_id: int = None) -> str:
    """Generate appropriate filename for the report"""
    timestamp = datetime.now().strftime('%Y-%m-%d')
    
    if report_type == "full":
        return f"MannBiome-Full-Report-{customer_id or 'unknown'}-{timestamp}.pdf"
    else:
        domains_str = "-".join(domains) if domains else "custom"
        return f"MannBiome-Domain-Report-{domains_str}-{customer_id or 'unknown'}-{timestamp}.pdf"