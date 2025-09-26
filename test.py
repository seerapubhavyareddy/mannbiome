#!/usr/bin/env python3
"""
Simple Customer Info API
Only extracts customer information using the exact SQL queries we tested
"""

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session
from datetime import datetime
import traceback

app = FastAPI(title="Simple Customer Info API", version="1.0.0")

# Database Configuration
DATABASE_URL = "postgresql://postgres:db_admin@vendor-portal-db.cszf6hop4o2t.us-east-2.rds.amazonaws.com:5432/mannbiome"

try:
    engine = create_engine(DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    print("✅ Database connected successfully")
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

@app.get("/api/health")
def health_check():
    return {
        "status": "healthy",
        "service": "Simple Customer Info API",
        "database_connected": engine is not None
    }

@app.get("/api/customer/{customer_id}/info")
def get_customer_info(customer_id: int, db: Session = Depends(get_db)):
    """
    Extract customer information using the exact SQL queries we tested
    Returns in the format:
    customer_info: {
        customer_id: 1,
        participant_id: "1",
        name: "Admin User",
        initials: "AU",
        email: "admin@mannbiome.com",
        age: 40,
        report_id: "MG1", 
        lab_name: "LabCorp Diagnostics",
        upload_date: "2024-08-12",
        last_updated: "May 23, 2025"
    }
    """
    try:
        print(f"🔍 Extracting customer info for customer_id: {customer_id}")
        
        if db is None:
            raise HTTPException(status_code=503, detail="Database connection not available")
        
        # Step 1: Check if customer exists and get user_id
        step1_query = text("SELECT user_id FROM customers.customer WHERE customer_id = :customer_id")
        step1_result = db.execute(step1_query, {"customer_id": customer_id}).fetchone()
        
        if not step1_result:
            raise HTTPException(status_code=404, detail=f"Customer {customer_id} not found")
        
        user_id = step1_result.user_id
        print(f"✅ Step 1: Found customer {customer_id} -> user_id {user_id}")
        
        # Step 2: Get complete customer info with JOIN
        step2_query = text("""
            SELECT 
                c.customer_id,
                c.user_id,
                c.date_of_birth,
                c.gender,
                c.phone,
                c.address,
                c.city,
                c.state,
                c.postal_code,
                c.country,
                c.medical_record_number,
                c.insurance_provider,
                c.created_at as customer_created_at,
                c.updated_at as customer_updated_at,
                u.username,
                u.email,
                u.first_name,
                u.last_name,
                u.created_at as user_created_at,
                u.role,
                u.status,
                u.age as user_age
            FROM customers.customer c
            JOIN public.user_account u ON c.user_id = u.user_id
            WHERE c.user_id = :user_id
        """)
        
        step2_result = db.execute(step2_query, {"user_id": user_id}).fetchone()
        
        if not step2_result:
            raise HTTPException(status_code=404, detail=f"User data not found for customer {customer_id}")
        
        print(f"✅ Step 2: Retrieved combined customer and user data")
        
        # Step 3: Check for patient reports (optional)
        participant_id = str(customer_id)
        step3_query = text("""
            SELECT 
                participant_id,
                lab_name,
                upload_date,
                total_bacteria_count,
                created_at
            FROM public.patient_reports
            WHERE participant_id = :participant_id
            ORDER BY upload_date DESC
            LIMIT 1
        """)
        
        step3_result = db.execute(step3_query, {"participant_id": participant_id}).fetchone()
        print(f"✅ Step 3: Patient reports - {'Found' if step3_result else 'Not found'}")
        
        # Step 4: Check for visits (optional)
        step4_query = text("""
            SELECT 
                v.visit_id,
                v.user_id,
                v.visit_date,
                v.report_id,
                v.status,
                v.created_at
            FROM microbiome.visits v
            WHERE v.user_id = :user_id
            ORDER BY v.visit_date DESC
            LIMIT 1
        """)
        
        step4_result = db.execute(step4_query, {"user_id": user_id}).fetchone()
        print(f"✅ Step 4: Visits - {'Found' if step4_result else 'Not found'}")
        
        # Build customer_info in exact format
        # Calculate age from date_of_birth
        age = None
        if step2_result.date_of_birth:
            today = datetime.now().date()
            birth_date = step2_result.date_of_birth
            age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
        
        # Extract names from database - no defaults
        first_name = step2_result.first_name
        last_name = step2_result.last_name
        
        # Only create full_name and initials if we have real data
        full_name = None
        initials = None
        if first_name and last_name:
            full_name = f"{first_name} {last_name}"
            initials = f"{first_name[0]}{last_name[0]}".upper()
        
        # Extract email from database - no defaults
        email = step2_result.email
        
        # Generate report_id - only from database, no defaults
        report_id = None
        if step4_result and step4_result.report_id:
            report_id = step4_result.report_id
        
        # Extract lab info - only from database, no defaults
        lab_name = None
        if step3_result and step3_result.lab_name:
            lab_name = step3_result.lab_name
        
        # Format dates - only real dates, no defaults
        upload_date = None
        if step3_result and step3_result.upload_date:
            upload_date = step3_result.upload_date.strftime("%Y-%m-%d")
            
        last_updated = None
        if step2_result.customer_updated_at:
            last_updated = step2_result.customer_updated_at.strftime("%B %d, %Y")
        elif step2_result.user_created_at:
            last_updated = step2_result.user_created_at.strftime("%B %d, %Y")
        
        # Build the exact format you specified
        customer_info = {
            "customer_id": customer_id,
            "participant_id": participant_id,
            "name": full_name,
            "initials": initials,
            "email": email,
            "age": age or step2_result.user_age,  # Use calculated age or database age, no default
            "report_id": report_id,
            "lab_name": lab_name,
            "upload_date": upload_date,
            "last_updated": last_updated
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

# Test endpoint to verify all steps work
@app.get("/api/customer/{customer_id}/debug-steps")
def debug_customer_steps(customer_id: int, db: Session = Depends(get_db)):
    """Debug endpoint to test each SQL step individually"""
    try:
        if db is None:
            return {"error": "Database connection not available"}
        
        results = {}
        
        # Step 1
        step1_query = text("SELECT user_id FROM customers.customer WHERE customer_id = :customer_id")
        step1_result = db.execute(step1_query, {"customer_id": customer_id}).fetchone()
        results["step1"] = {
            "query": "SELECT user_id FROM customers.customer WHERE customer_id = ?",
            "found": step1_result is not None,
            "data": dict(step1_result._mapping) if step1_result else None
        }
        
        if not step1_result:
            return {"success": False, "results": results, "stopped_at": "step1"}
        
        user_id = step1_result.user_id
        
        # Step 2  
        step2_query = text("""
            SELECT 
                c.customer_id, c.user_id, c.date_of_birth, c.gender,
                u.username, u.email, u.first_name, u.last_name, u.role, u.status, u.age
            FROM customers.customer c
            JOIN public.user_account u ON c.user_id = u.user_id
            WHERE c.user_id = :user_id
        """)
        step2_result = db.execute(step2_query, {"user_id": user_id}).fetchone()
        results["step2"] = {
            "query": "JOIN customers.customer with public.user_account",
            "found": step2_result is not None,
            "data": dict(step2_result._mapping) if step2_result else None
        }
        
        # Step 3
        participant_id = str(customer_id)
        step3_query = text("""
            SELECT participant_id, lab_name, upload_date, total_bacteria_count
            FROM public.patient_reports
            WHERE participant_id = :participant_id
            ORDER BY upload_date DESC LIMIT 1
        """)
        step3_result = db.execute(step3_query, {"participant_id": participant_id}).fetchone()
        results["step3"] = {
            "query": "SELECT from public.patient_reports",
            "found": step3_result is not None,
            "data": dict(step3_result._mapping) if step3_result else None
        }
        
        # Step 4
        step4_query = text("""
            SELECT visit_id, user_id, visit_date, report_id, status
            FROM microbiome.visits
            WHERE user_id = :user_id
            ORDER BY visit_date DESC LIMIT 1
        """)
        step4_result = db.execute(step4_query, {"user_id": user_id}).fetchone()
        results["step4"] = {
            "query": "SELECT from microbiome.visits",
            "found": step4_result is not None,
            "data": dict(step4_result._mapping) if step4_result else None
        }
        
        return {
            "success": True,
            "customer_id": customer_id,
            "user_id": user_id,
            "results": results
        }
        
    except Exception as e:
        return {"success": False, "error": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001, reload=True)