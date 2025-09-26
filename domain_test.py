#!/usr/bin/env python3
"""
Complete Patient Bacteria Domain System - Using Existing patient_reports Table
Uses your existing patient_reports table with JSONB bacteria_data instead of creating new tables
"""

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session
from datetime import datetime
import traceback
import json
from typing import Dict, List, Optional
import random
import math

app = FastAPI(title="Patient Bacteria Domain API - Reports Integration", version="3.0.0")

# Database Configuration - Your existing database
DATABASE_URL = "postgresql://postgres:db_admin@vendor-portal-db.cszf6hop4o2t.us-east-2.rds.amazonaws.com:5432/mannbiome"

# Create engine for mannbiome database (which has both local tables and foreign vectordb tables)
try:
    engine = create_engine(DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    print("✅ Database connection established")
except Exception as e:
    print(f"⚠️ Database connection error: {e}")
    engine = None
    SessionLocal = None

def get_db():
    if SessionLocal is None:
        yield None
        return
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ===============================================================
# Data Extraction from patient_reports JSONB
# ===============================================================

def get_bacteria_domain_data_from_reports(participant_id: str, db: Session) -> Dict:
    """
    Extract bacteria domain data using your existing patient_reports table
    """
    try:
        print(f"🔬 Extracting bacteria data for participant {participant_id}")
        
        # First, get the patient's bacteria data from patient_reports
        patient_query = text("""
            SELECT 
                upload_id,
                participant_id,
                lab_name,
                upload_date,
                bacteria_data,
                total_bacteria_count
            FROM patient_reports
            WHERE participant_id = :participant_id
            ORDER BY upload_date DESC
            LIMIT 1
        """)
        
        patient_result = db.execute(patient_query, {"participant_id": participant_id}).fetchone()
        
        if not patient_result:
            print(f"❌ No patient reports found for participant {participant_id}")
            return {}
        
        if not patient_result.bacteria_data:
            print(f"❌ No bacteria data found in report for participant {participant_id}")
            return {}
        
        print(f"✅ Found {patient_result.total_bacteria_count} bacteria records for participant {participant_id}")
        
        # Parse the JSONB bacteria data
        bacteria_list = patient_result.bacteria_data
        if isinstance(bacteria_list, str):
            bacteria_list = json.loads(bacteria_list)
        
        # Get domain associations and metadata from foreign tables with case-insensitive msp_id matching
        domain_query = text("""
            SELECT DISTINCT
                bda.domain,
                bda.bacteria_name,
                bda.association_type,
                bda.confidence_score,
                bda.diseases_beneficial,
                bda.diseases_harmful,
                COALESCE(cbm.msp_id, hcbm.msp_id) as msp_id,
                COALESCE(cbm.ideal_min, hcbm.ideal_min) as ideal_min,
                COALESCE(cbm.ideal_max, hcbm.ideal_max) as ideal_max,
                COALESCE(cbm.units, hcbm.units) as units,
                COALESCE(cbm.clinical_context, hcbm.clinical_context) as clinical_context,
                COALESCE(cbm.evidence_strength, hcbm.evidence_strength) as evidence_strength
            FROM vectordb.bacteria_domain_associations bda
            LEFT JOIN vectordb.computed_bacteria_metadata cbm ON bda.bacteria_name = cbm.bacteria_name
            LEFT JOIN vectordb."Healthy_Cohort_Bacteria_Metadata" hcbm ON bda.bacteria_name = hcbm.bacteria_name
            WHERE COALESCE(cbm.msp_id, hcbm.msp_id) IS NOT NULL
            ORDER BY bda.domain, bda.confidence_score DESC
        """)
        
        domain_results = db.execute(domain_query).fetchall()
        
        if not domain_results:
            print("❌ No domain associations found in vectordb foreign tables")
            return {}
        
        print(f"✅ Found {len(domain_results)} bacteria-domain associations")
        
        # Create lookup dictionary for patient bacteria by msp_id
        patient_bacteria_lookup = {}
        for bacteria_item in bacteria_list:
            msp_id = bacteria_item.get('msp_id')
            if msp_id:
                patient_bacteria_lookup[msp_id] = bacteria_item
        
        print(f"✅ Created lookup for {len(patient_bacteria_lookup)} patient bacteria records")
        
        # Organize data by domain
        domain_data = {
            "aging": {"bacteria": [], "scores": {"diversity": 0, "overall": 0, "status": "poor"}},
            "gut": {"bacteria": [], "scores": {"diversity": 0, "overall": 0, "status": "poor"}},
            "liver": {"bacteria": [], "scores": {"diversity": 0, "overall": 0, "status": "poor"}},
            "heart": {"bacteria": [], "scores": {"diversity": 0, "overall": 0, "status": "poor"}},
            "skin": {"bacteria": [], "scores": {"diversity": 0, "overall": 0, "status": "poor"}},
            "cognitive": {"bacteria": [], "scores": {"diversity": 0, "overall": 0, "status": "poor"}},
            "immune": {"bacteria": [], "scores": {"diversity": 0, "overall": 0, "status": "poor"}},
            "oral": {"bacteria": [], "scores": {"diversity": 0, "overall": 0, "status": "poor"}},
            "vaginal": {"bacteria": [], "scores": {"diversity": 0, "overall": 0, "status": "poor"}},
            "overall": {"bacteria": [], "scores": {"diversity": 0, "overall": 0, "status": "poor"}}
        }
        
        # Process each bacteria from domain associations
        for row in domain_results:
            domain = row.domain.lower()
            if domain not in domain_data:
                domain_data[domain] = {"bacteria": [], "scores": {"diversity": 0, "overall": 0, "status": "poor"}}
            
            # Find matching patient bacteria data
            patient_bacteria = patient_bacteria_lookup.get(row.msp_id)
            
            if not patient_bacteria:
                # Skip bacteria not found in patient report
                continue
            
            # Extract abundance from patient data
            abundance = float(patient_bacteria.get('abundance', 0))
            optimal_min = float(row.ideal_min) if row.ideal_min else 0.000001
            optimal_max = float(row.ideal_max) if row.ideal_max else 0.00001
            
            # Determine status based on ideal ranges
            if abundance < optimal_min * 0.8:
                status = "LOW"
            elif abundance > optimal_max * 1.2:
                status = "HIGH"
            else:
                status = "NORMAL"
            
            # Calculate current level and percentage
            current_level = f"{abundance * 1000000:.2f} units"
            
            # Calculate percentage relative to optimal range midpoint
            optimal_mid = (optimal_min + optimal_max) / 2
            percentage = min((abundance / optimal_mid) * 100, 999.9) if optimal_mid > 0 else 0.1
            
            # Determine category based on association type
            if row.association_type == "beneficial":
                category = "beneficial"
            elif row.association_type == "harmful":
                category = "concerning"
            else:
                category = "neutral"
            
            # Create bacteria entry in format.js structure
            bacteria_entry = {
                "msp_id": row.msp_id,
                "bacteria_name": row.bacteria_name.split()[-1] if " " in row.bacteria_name else row.bacteria_name,
                "full_name": row.bacteria_name,
                "abundance": abundance,
                "current_level": current_level,
                "percentage": round(percentage, 3),
                "confidence_level": patient_bacteria.get('evidence_strength', 'C'),
                "status": status,
                "optimal_range": [optimal_min, optimal_max],
                "category": category,
                "description": row.clinical_context or f"Associated with {domain} health",
                "units": patient_bacteria.get('units', 'relative_abundance_fraction')
            }
            
            domain_data[domain]["bacteria"].append(bacteria_entry)
        
        # Calculate domain scores based on bacteria status
        for domain in domain_data:
            bacteria_in_domain = domain_data[domain]["bacteria"]
            if bacteria_in_domain:
                normal_count = sum(1 for b in bacteria_in_domain if b["status"] == "NORMAL")
                total_count = len(bacteria_in_domain)
                
                diversity_score = min(4.0, total_count / 3.0)  # Diversity based on count
                overall_score = (normal_count / total_count) * 4.0 if total_count > 0 else 1.0
                
                if overall_score >= 3.5:
                    status = "excellent"
                elif overall_score >= 2.5:
                    status = "good"
                elif overall_score >= 1.5:
                    status = "warning"
                else:
                    status = "poor"
                
                domain_data[domain]["scores"] = {
                    "diversity": round(diversity_score, 1),
                    "overall": round(overall_score, 1),
                    "status": status
                }
        
        # Limit bacteria per domain for cleaner API responses
        for domain in domain_data:
            if len(domain_data[domain]["bacteria"]) > 15:
                # Keep the most significant ones (sorted by confidence score implicit in query)
                domain_data[domain]["bacteria"] = domain_data[domain]["bacteria"][:15]
        
        print(f"✅ Successfully processed data for {len([d for d in domain_data if domain_data[d]['bacteria']])} domains")
        
        return domain_data
        
    except Exception as e:
        print(f"❌ Error extracting bacteria domain data: {e}")
        traceback.print_exc()
        return {}

# ===============================================================
# API Endpoints
# ===============================================================

@app.get("/api/health")
def health_check():
    return {
        "status": "healthy",
        "service": "Patient Bacteria Domain API - Reports Integration",
        "database_connected": engine is not None,
        "using_table": "patient_reports (JSONB bacteria_data)"
    }

@app.get("/api/customer/{customer_id}/info")
def get_customer_info(customer_id: int, db: Session = Depends(get_db)):
    """Get customer information using your existing customer tables"""
    try:
        if db is None:
            raise HTTPException(status_code=503, detail="Database not available")
        
        print(f"🔍 Extracting customer info for customer_id: {customer_id}")
        
        # Step 1: Get user_id from customers table
        step1_query = text("SELECT user_id FROM customers.customer WHERE customer_id = :customer_id")
        step1_result = db.execute(step1_query, {"customer_id": customer_id}).fetchone()
        
        if not step1_result:
            raise HTTPException(status_code=404, detail=f"Customer {customer_id} not found")
        
        user_id = step1_result.user_id
        
        # Step 2: Get detailed customer and user information
        step2_query = text("""
            SELECT 
                c.customer_id, c.user_id, c.date_of_birth, c.gender, c.phone,
                c.address, c.city, c.state, c.postal_code, c.country,
                c.created_at as customer_created_at, c.updated_at as customer_updated_at,
                u.username, u.email, u.first_name, u.last_name,
                u.created_at as user_created_at, u.role, u.status, u.age as user_age
            FROM customers.customer c
            JOIN public.user_account u ON c.user_id = u.user_id
            WHERE c.user_id = :user_id
        """)
        
        step2_result = db.execute(step2_query, {"user_id": user_id}).fetchone()
        
        if not step2_result:
            raise HTTPException(status_code=404, detail=f"User data not found for customer {customer_id}")
        
        # Calculate age if date_of_birth is available
        age = None
        if step2_result.date_of_birth:
            today = datetime.now().date()
            birth_date = step2_result.date_of_birth
            age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
        
        # Build name and initials
        first_name = step2_result.first_name
        last_name = step2_result.last_name
        
        full_name = None
        initials = None
        if first_name and last_name:
            full_name = f"{first_name} {last_name}"
            initials = f"{first_name[0]}{last_name[0]}".upper()
        
        customer_info = {
            "customer_id": customer_id,
            "participant_id": str(customer_id),
            "name": full_name,
            "initials": initials,
            "email": step2_result.email,
            "age": age or step2_result.user_age,
            "report_id": f"MG{customer_id}",
            "lab_name": "LabCorp Diagnostics",
            "upload_date": datetime.now().strftime("%Y-%m-%d"),
            "last_updated": step2_result.customer_updated_at.strftime("%B %d, %Y") if step2_result.customer_updated_at else None
        }
        
        return {
            "success": True,
            "customer_info": customer_info
        }
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Error extracting customer info: {e}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@app.get("/api/customer/{customer_id}/bacteria-domains")
def get_customer_bacteria_domains(customer_id: int, db: Session = Depends(get_db)):
    """Get bacteria domain data using existing patient_reports table"""
    try:
        if db is None:
            raise HTTPException(status_code=503, detail="Database not available")
        
        participant_id = str(customer_id)  # Convert customer_id to participant_id format
        print(f"🔬 Extracting bacteria domain data for customer {customer_id} (participant {participant_id})")
        
        # Get bacteria domain data from patient_reports
        domain_bacteria = get_bacteria_domain_data_from_reports(participant_id, db)
        
        if not domain_bacteria:
            raise HTTPException(
                status_code=404, 
                detail=f"No bacteria data found for customer {customer_id}. Make sure patient reports exist in the database."
            )
        
        # Calculate overall health metrics
        total_bacteria = sum(len(domain_data["bacteria"]) for domain_data in domain_bacteria.values())
        beneficial_count = 0
        concerning_count = 0
        
        for domain_data in domain_bacteria.values():
            for bacteria in domain_data["bacteria"]:
                if bacteria["category"] == "beneficial":
                    beneficial_count += 1
                elif bacteria["category"] == "concerning":
                    concerning_count += 1
        
        overall_health = {
            "diversity_score": round(min(4.0, total_bacteria / 15.0), 1),
            "overall_score": round(max(1.0, 4.0 - (concerning_count / max(total_bacteria, 1)) * 3), 1),
            "status": "excellent" if concerning_count < beneficial_count * 0.3 else "good" if concerning_count < beneficial_count else "warning" if concerning_count < total_bacteria * 0.6 else "poor",
            "total_bacteria_analyzed": total_bacteria,
            "concerning_bacteria": concerning_count,
            "beneficial_bacteria": beneficial_count,
            "neutral_bacteria": total_bacteria - beneficial_count - concerning_count
        }
        
        return {
            "success": True,
            "customer_id": customer_id,
            "participant_id": participant_id,
            "domain_bacteria": domain_bacteria,
            "overall_health": overall_health,
            "generated_at": datetime.now().isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Error extracting bacteria domain data: {e}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@app.get("/api/customer/{customer_id}/complete-profile")
def get_complete_customer_profile(customer_id: int, db: Session = Depends(get_db)):
    """Get complete customer profile including both info and bacteria domains"""
    try:
        # Get customer info
        customer_info_response = get_customer_info(customer_id, db)
        
        # Get bacteria domain data
        bacteria_response = get_customer_bacteria_domains(customer_id, db)
        
        # Combine into complete profile
        complete_profile = {
            "success": True,
            "customer_info": customer_info_response["customer_info"],
            "domain_bacteria": bacteria_response["domain_bacteria"],
            "overall_health": bacteria_response["overall_health"],
            "generated_at": datetime.now().isoformat()
        }
        
        return complete_profile
        
    except Exception as e:
        print(f"❌ Error creating complete profile: {e}")
        raise HTTPException(status_code=500, detail=f"Error creating complete profile: {str(e)}")

# ===============================================================
# Validation and Debug Endpoints
# ===============================================================

@app.get("/api/debug/patient-reports/{participant_id}")
def debug_patient_reports(participant_id: str, db: Session = Depends(get_db)):
    """Debug endpoint to check patient reports data"""
    try:
        if db is None:
            raise HTTPException(status_code=503, detail="Database not available")
        
        query = text("""
            SELECT 
                upload_id,
                participant_id,
                lab_name,
                upload_date,
                total_bacteria_count,
                bacteria_data
            FROM patient_reports
            WHERE participant_id = :participant_id
            ORDER BY upload_date DESC
        """)
        
        results = db.execute(query, {"participant_id": participant_id}).fetchall()
        
        if not results:
            return {"error": f"No patient reports found for participant {participant_id}"}
        
        debug_info = []
        for result in results:
            bacteria_preview = []
            if result.bacteria_data:
                bacteria_list = result.bacteria_data
                if isinstance(bacteria_list, str):
                    bacteria_list = json.loads(bacteria_list)
                
                # Show first 3 bacteria for preview
                bacteria_preview = bacteria_list[:3] if len(bacteria_list) > 3 else bacteria_list
            
            debug_info.append({
                "upload_id": str(result.upload_id),
                "participant_id": result.participant_id,
                "lab_name": result.lab_name,
                "upload_date": result.upload_date.isoformat() if result.upload_date else None,
                "total_bacteria_count": result.total_bacteria_count,
                "bacteria_preview": bacteria_preview
            })
        
        return {
            "participant_id": participant_id,
            "reports_found": len(debug_info),
            "reports": debug_info
        }
        
    except Exception as e:
        return {"error": str(e)}

@app.get("/api/debug/vectordb-tables")
def debug_vectordb_tables(db: Session = Depends(get_db)):
    """Debug endpoint to check vectordb foreign tables"""
    try:
        if db is None:
            raise HTTPException(status_code=503, detail="Database not available")
        
        checks = {}
        
        # Check each foreign table
        tables_to_check = [
            "vectordb.bacteria_domain_associations",
            "vectordb.computed_bacteria_metadata",
            'vectordb."Healthy_Cohort_Bacteria_Metadata"',
            "vectordb.bacteria_disease_associate",
            "vectordb.rules_mappings"
        ]
        
        for table in tables_to_check:
            try:
                count_query = text(f"SELECT COUNT(*) FROM {table}")
                count = db.execute(count_query).scalar()
                checks[table] = {"status": "OK", "count": count}
                
                # Get sample data
                if count > 0:
                    sample_query = text(f"SELECT * FROM {table} LIMIT 1")
                    sample = db.execute(sample_query).fetchone()
                    if sample:
                        checks[table]["sample_columns"] = list(sample._mapping.keys())
                
            except Exception as e:
                checks[table] = {"status": "ERROR", "error": str(e)}
        
        return {"vectordb_tables": checks}
        
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting Patient Bacteria Domain API (Reports Integration)...")
    print("📋 Available endpoints:")
    print("   GET  /api/health - Health check")
    print("   GET  /api/customer/{id}/info - Customer information")
    print("   GET  /api/customer/{id}/bacteria-domains - Bacteria domain data from patient_reports")
    print("   GET  /api/customer/{id}/complete-profile - Complete profile")
    print("   GET  /api/debug/patient-reports/{participant_id} - Debug patient reports")
    print("   GET  /api/debug/vectordb-tables - Debug vectordb foreign tables")
    print("")
    print("💡 This version uses your existing patient_reports table with JSONB bacteria_data")
    print("💡 Test with participant_id '3091' which has real data")
    
    uvicorn.run(app, host="0.0.0.0", port=8001, reload=True)