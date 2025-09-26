from fastapi import FastAPI, Query, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, MetaData, inspect, text, select, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from typing import Optional, List, Dict, Any
from datetime import datetime, timedelta

import os
import json

app = FastAPI(title="MannBiome Customer Portal API", version="1.0.0")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with your actual domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database connection
DATABASE_URL = "postgresql://postgres:db_admin@vendor-portal-db.cszf6hop4o2t.us-east-2.rds.amazonaws.com:5432/mannbiome"
VECTORDB_URL = "postgresql://postgres:db_admin@vendor-portal-db.cszf6hop4o2t.us-east-2.rds.amazonaws.com:5432/vectordb"

try:
    vectordb_engine = create_engine(VECTORDB_URL)
    VectorDBSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=vectordb_engine)
    print("âœ… VectorDB connection configured successfully")
except Exception as e:
    print(f"âš ï¸ VectorDB connection error: {e}")
    vectordb_engine = None
    VectorDBSessionLocal = None

def get_vectordb():
    if VectorDBSessionLocal is None:
        yield None
        return
    
    db = VectorDBSessionLocal()
    try:
        yield db
    except Exception as e:
        print(f"VectorDB session error: {e}")
        db.rollback()
    finally:
        db.close()

try:
    engine = create_engine(DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base = declarative_base()
    metadata = MetaData()
    print("âœ… Database connection configured successfully")
except Exception as e:
    print(f"âš ï¸ Database connection error: {e}")
    engine = None
    SessionLocal = None

# Dependency to get DB session
def get_db():
    if SessionLocal is None:
        yield None
        return
    
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        print(f"Database session error: {e}")
        db.rollback()
    finally:
        db.close()

def group_bacteria_for_carousel(bacteria_analysis: List[Dict]) -> Dict:
    """Group bacteria by category with improved visualization metrics - FIXED for frontend compatibility"""
    try:
        # âœ… FIXED: Use the category names that frontend expects
        carousel_groups = {
            "bacteria": {  # â† Frontend expects this name
                "title": "Top Bacterial Species",
                "status": "Good", 
                "species": []
            },
            "probiotics": {  # â† Frontend expects this name
                "title": "Probiotic Organisms",
                "status": "Good",
                "species": []
            },
            "pathogens": {  # â† Frontend expects this name
                "title": "Pathogenic Bacteria",
                "status": "Monitor",
                "species": []
            },
            "virus": {  # â† Add categories frontend expects
                "title": "Viral Species",
                "status": "Normal",
                "species": []
            },
            "fungi": {  # â† Add categories frontend expects
                "title": "Fungal Species",
                "status": "Normal",
                "species": []
            },
            "protozoa": {  # â† Add categories frontend expects
                "title": "Protozoa Species",
                "status": "Normal",
                "species": []
            }
        }
        
        # Group bacteria by category with IMPROVED MAPPING
        for bacteria in bacteria_analysis:
            bacteria_name = bacteria["bacteria_name"].lower()
            category = bacteria["category"]
            
            # âœ… FIXED: Map your backend categories to frontend expected categories
            frontend_category = None
            
            if category == "beneficial":
                # Determine if it's a probiotic or general bacteria
                if any(probiotic in bacteria_name for probiotic in [
                    "lactobacillus", "bifidobacterium", "acidophilus", "plantarum", 
                    "rhamnosus", "casei", "longum", "saccharomyces"
                ]):
                    frontend_category = "probiotics"
                else:
                    frontend_category = "bacteria"
                    
            elif category == "pathogenic":
                frontend_category = "pathogens"
                
            elif category == "neutral":
                # Categorize neutral bacteria based on name patterns
                if any(virus in bacteria_name for virus in ["phage", "virus"]):
                    frontend_category = "virus"
                elif any(fungi in bacteria_name for fungi in ["candida", "saccharomyces", "malassezia"]):
                    frontend_category = "fungi"
                elif any(protozoa in bacteria_name for protozoa in ["blastocystis", "entamoeba", "giardia"]):
                    frontend_category = "protozoa"
                else:
                    frontend_category = "bacteria"  # Default neutral to bacteria
                    
            elif category == "unclassified":
                frontend_category = "bacteria"  # Put unclassified in bacteria category
            
            # Add to appropriate category
            if frontend_category and frontend_category in carousel_groups:
                # Calculate visualization metrics
                range_fill, marker_position = calculate_visualization_metrics(bacteria["percentage"])
                
                # Transform bacteria data with improved metrics
                species_data = {
                    "name": bacteria["bacteria_name"],
                    "scientific_name": bacteria["bacteria_name"],
                    "current_level": bacteria["abundance"],
                    "percentage": bacteria["percentage"],
                    "status": bacteria["status"],
                    "evidence_strength": bacteria["evidence_strength"],
                    "msp_id": bacteria["msp_id"],
                    "measurement_unit": "relative_abundance_fraction",
                    "is_beneficial": category == "beneficial",
                    "range_fill_width": range_fill,
                    "marker_position": marker_position,
                    # âœ… ADD: Frontend expected fields
                    "optimal_level": bacteria["abundance"] * 1.2,  # Mock optimal level
                    "range_min": "0.001%",
                    "range_max": "1.0%"
                }
                carousel_groups[frontend_category]["species"].append(species_data)
        
        # Sort species within each group by abundance (highest first)
        for group in carousel_groups.values():
            group["species"].sort(key=lambda x: x["current_level"], reverse=True)
            
            # Update group status based on species
            if group["species"]:
                good_count = len([s for s in group["species"] if s["status"] == "good"])
                normal_count = len([s for s in group["species"] if s["status"] == "normal"])
                low_count = len([s for s in group["species"] if s["status"] == "low"])
                high_count = len([s for s in group["species"] if s["status"] == "high"])
                
                # Determine overall group status
                if good_count > 0:
                    group["status"] = "Good"
                elif normal_count > low_count and normal_count > high_count:
                    group["status"] = "Normal"
                elif high_count > 0:
                    group["status"] = "Monitor"
                else:
                    group["status"] = "Low"
        
        return carousel_groups
        
    except Exception as e:
        print(f"Error grouping bacteria for carousel: {e}")
        return {}

# âœ… ALSO ADD: Update your categorize_bacteria_by_name function to be more comprehensive
def categorize_bacteria_by_name(bacteria_name: str) -> str:
    """Enhanced categorization with more comprehensive patterns"""
    bacteria_lower = bacteria_name.lower()
    
    # Beneficial bacteria patterns (expanded)
    beneficial_patterns = [
        'lactobacillus', 'bifidobacterium', 'akkermansia', 'faecalibacterium',
        'roseburia', 'eubacterium', 'butyrivibrio', 'coprococcus',
        'ruminococcus', 'bacteroides fragilis', 'streptococcus thermophilus',
        'lactococcus', 'enterococcus faecalis'  # Added more beneficial
    ]
    
    # Pathogenic bacteria patterns (expanded)
    pathogenic_patterns = [
        'clostridium difficile', 'salmonella', 'shigella', 'campylobacter',
        'helicobacter pylori', 'escherichia coli', 'klebsiella pneumoniae',
        'enterococcus faecium', 'staphylococcus aureus', 'pseudomonas',
        'vibrio', 'yersinia'  # Added more pathogens
    ]
    
    # Check for beneficial patterns
    for pattern in beneficial_patterns:
        if pattern in bacteria_lower:
            return "beneficial"
    
    # Check for pathogenic patterns
    for pattern in pathogenic_patterns:
        if pattern in bacteria_lower:
            return "pathogenic"
    
    # Check for unclassified
    if 'unclassified' in bacteria_lower or 'unknown' in bacteria_lower:
        return "unclassified"
    
    # Default to neutral
    return "neutral"
# =======================
# SCORE FORMATTING FUNCTION - FIXES FLOATING POINT ISSUES
# =======================

def format_score(score):
    """Format score to 1 decimal place - FIXES floating point errors"""
    try:
        return round(float(score), 1)
    except (TypeError, ValueError):
        return 0.0

def calculate_overall_average(scores):
    """Calculate the average of all domain scores and format it"""
    try:
        if not scores:
            return 0.0
        valid_scores = [score for score in scores if score is not None and score > 0]
        if not valid_scores:
            return 0.0
        average = sum(valid_scores) / len(valid_scores)
        return format_score(average)
    except Exception as e:
        print(f"Error calculating average: {e}")
        return 0.0
# Add these imports to your existing FastAPI file
from typing import Dict, List
import re
import math

# =======================
# BACTERIA CATEGORIZATION FUNCTIONS
# =======================

def categorize_bacteria_by_name(bacteria_name: str) -> str:
    """Categorize bacteria based on name patterns"""
    bacteria_lower = bacteria_name.lower()
    
    # Beneficial bacteria patterns
    beneficial_patterns = [
        'lactobacillus', 'bifidobacterium', 'akkermansia', 'faecalibacterium',
        'roseburia', 'eubacterium', 'butyrivibrio', 'coprococcus',
        'ruminococcus', 'bacteroides fragilis', 'streptococcus thermophilus'
    ]
    
    # Pathogenic bacteria patterns
    pathogenic_patterns = [
        'clostridium difficile', 'salmonella', 'shigella', 'campylobacter',
        'helicobacter pylori', 'escherichia coli', 'klebsiella pneumoniae',
        'enterococcus faecium', 'staphylococcus aureus', 'pseudomonas'
    ]
    
    # Check for beneficial patterns
    for pattern in beneficial_patterns:
        if pattern in bacteria_lower:
            return "beneficial"
    
    # Check for pathogenic patterns
    for pattern in pathogenic_patterns:
        if pattern in bacteria_lower:
            return "pathogenic"
    
    # Check for unclassified
    if 'unclassified' in bacteria_lower or 'unknown' in bacteria_lower:
        return "unclassified"
    
    # Default to neutral
    return "neutral"

def convert_abundance_to_percentage(abundance: float) -> float:
    """Convert relative abundance fraction to percentage with proper scaling"""
    try:
        # Your data appears to be relative abundance fractions
        # Convert to percentage with more precision for very small values
        percentage = abundance * 100
        
        # For very small values, show more decimal places
        if percentage < 0.001:
            return round(percentage, 6)  # Show 6 decimal places for tiny values
        elif percentage < 0.01:
            return round(percentage, 4)  # Show 4 decimal places for small values
        else:
            return round(percentage, 2)  # Show 2 decimal places for normal values
            
    except (TypeError, ValueError):
        return 0.0
def calculate_visualization_metrics(percentage: float) -> tuple:
    """Calculate range_fill_width and marker_position for visualization"""
    try:
        import math
        
        # Scale percentage for better visualization of small values
        if percentage <= 0:
            return 0.0, 0.0
        
        # For very small percentages, use log scaling
        if percentage < 0.001:
            # Log scale: map 1e-6% to 1e-1% to 10-90 range
            log_percentage = math.log10(percentage + 1e-8)  # Add small value to avoid log(0)
            scaled = max(5, min(85, (log_percentage + 8) * 10))  # Scale to 5-85 range
            range_fill = scaled
            marker_position = min(100, scaled + 5)
        
        # For small percentages (0.001% - 0.1%), linear scaling
        elif percentage < 0.1:
            scaled = 10 + (percentage / 0.1) * 70  # Scale to 10-80 range
            range_fill = scaled
            marker_position = min(100, scaled + 5)
        
        # For normal percentages (>0.1%), standard scaling
        else:
            range_fill = min(95, percentage * 10)  # Standard scaling
            marker_position = min(100, range_fill + 5)
        
        return round(range_fill, 1), round(marker_position, 1)
        
    except Exception as e:
        print(f"Error calculating visualization metrics: {e}")
        return 10.0, 15.0  # Default values


def calculate_bacteria_status(abundance: float, evidence_strength: str, category: str) -> str:
    """Calculate bacteria status with better thresholds for real data"""
    try:
        # Convert to percentage
        percentage = convert_abundance_to_percentage(abundance)
        
        # Evidence strength weights
        evidence_weights = {"A": 1.0, "B": 0.8, "C": 0.6}
        weight = evidence_weights.get(evidence_strength, 0.6)
        
        # Weighted percentage
        weighted_percentage = percentage * weight
        
        # Updated thresholds based on your real data patterns
        if category == "beneficial":
            # For beneficial bacteria - adjusted for microbiome data
            if weighted_percentage >= 0.0001:  # 0.0001% or higher
                return "good"
            elif weighted_percentage >= 0.00001:  # 0.00001% or higher  
                return "normal"
            else:
                return "low"
                
        elif category == "pathogenic":
            # For pathogenic bacteria - lower is better
            if weighted_percentage >= 0.001:  # 0.001% or higher is concerning
                return "high"
            elif weighted_percentage >= 0.0001:  # 0.0001% or higher is moderate
                return "normal" 
            else:
                return "good"  # Very low pathogenic bacteria
                
        else:  # neutral or unclassified
            # For neutral bacteria
            if weighted_percentage >= 0.001:
                return "high"
            elif weighted_percentage >= 0.00001:
                return "normal"
            else:
                return "low"
                
    except Exception as e:
        print(f"Error calculating bacteria status: {e}")
        return "normal"


def calculate_overall_health_score(bacteria_analysis: List[Dict]) -> Dict:
    """Calculate overall health scores based on bacteria analysis"""
    try:
        if not bacteria_analysis:
            return {"overall_score": 3.0, "diversity_score": 2.5}
        
        # Count bacteria by status and category
        beneficial_good = len([b for b in bacteria_analysis if b["category"] == "beneficial" and b["status"] == "good"])
        beneficial_total = len([b for b in bacteria_analysis if b["category"] == "beneficial"])
        pathogenic_high = len([b for b in bacteria_analysis if b["category"] == "pathogenic" and b["status"] == "high"])
        pathogenic_total = len([b for b in bacteria_analysis if b["category"] == "pathogenic"])
        total_bacteria = len(bacteria_analysis)
        
        # Calculate beneficial ratio (good beneficial / total beneficial)
        beneficial_ratio = beneficial_good / beneficial_total if beneficial_total > 0 else 0
        
        # Calculate pathogenic concern (high pathogenic / total pathogenic)
        pathogenic_concern = pathogenic_high / pathogenic_total if pathogenic_total > 0 else 0
        
        # Calculate diversity (more bacteria types = better)
        diversity_score = min(5.0, 2.0 + (total_bacteria / 10))  # Scale based on bacteria count
        
        # Calculate overall score
        base_score = 3.0  # Start with neutral
        base_score += beneficial_ratio * 1.5  # Boost for good beneficial bacteria
        base_score -= pathogenic_concern * 1.5  # Penalty for concerning pathogenic bacteria
        
        # Ensure scores are in valid range (1.0 - 5.0)
        overall_score = max(1.0, min(5.0, base_score))
        diversity_score = max(1.0, min(5.0, diversity_score))
        
        return {
            "overall_score": round(overall_score, 1),
            "diversity_score": round(diversity_score, 1)
        }
        
    except Exception as e:
        print(f"Error calculating health scores: {e}")
        return {"overall_score": 3.0, "diversity_score": 2.5}

def group_bacteria_for_carousel(bacteria_analysis: List[Dict]) -> Dict:
    """Group bacteria by category with improved visualization metrics"""
    try:
        carousel_groups = {
            "beneficial": {
                "title": "Beneficial Bacteria",
                "status": "Good", 
                "species": []
            },
            "pathogenic": {
                "title": "Pathogenic Bacteria",
                "status": "Monitor",
                "species": []
            },
            "neutral": {
                "title": "Neutral Bacteria", 
                "status": "Normal",
                "species": []
            },
            "unclassified": {
                "title": "Unclassified Bacteria",
                "status": "Unknown",
                "species": []
            }
        }
        
        # Group bacteria by category
        for bacteria in bacteria_analysis:
            category = bacteria["category"]
            if category in carousel_groups:
                # Calculate visualization metrics
                range_fill, marker_position = calculate_visualization_metrics(bacteria["percentage"])
                
                # Transform bacteria data with improved metrics
                species_data = {
                    "name": bacteria["bacteria_name"],
                    "scientific_name": bacteria["bacteria_name"],
                    "current_level": bacteria["abundance"],
                    "percentage": bacteria["percentage"],
                    "status": bacteria["status"],
                    "evidence_strength": bacteria["evidence_strength"],
                    "msp_id": bacteria["msp_id"],
                    "measurement_unit": "relative_abundance_fraction",
                    "is_beneficial": category == "beneficial",
                    "range_fill_width": range_fill,      # â† Improved scaling
                    "marker_position": marker_position   # â† Improved scaling
                }
                carousel_groups[category]["species"].append(species_data)
        
        # Sort species within each group by abundance (highest first)
        for group in carousel_groups.values():
            group["species"].sort(key=lambda x: x["current_level"], reverse=True)
            
            # Update group status based on species
            if group["species"]:
                good_count = len([s for s in group["species"] if s["status"] == "good"])
                normal_count = len([s for s in group["species"] if s["status"] == "normal"])
                low_count = len([s for s in group["species"] if s["status"] == "low"])
                high_count = len([s for s in group["species"] if s["status"] == "high"])
                
                # Determine overall group status
                if good_count > 0:
                    group["status"] = "Good"
                elif normal_count > low_count and normal_count > high_count:
                    group["status"] = "Normal"
                elif high_count > 0:
                    group["status"] = "Monitor"
                else:
                    group["status"] = "Low"
        
        return carousel_groups
        
    except Exception as e:
        print(f"Error grouping bacteria for carousel: {e}")
        return {}


# =======================
# HEALTH CHECK & BASIC ENDPOINTS
# =======================

@app.get("/")
def read_root():
    return {
        "message": "MannBiome Customer Portal API", 
        "status": "running",
        "version": "1.0.0",
        "docs_url": "/docs"
    }

@app.get("/api/health-check")
def health_check():
    """API health check endpoint with dual database status"""
    mannbiome_status = "connected" if engine is not None else "disconnected"
    vectordb_status = "connected" if vectordb_engine is not None else "disconnected"
    
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0",
        "databases": {
            "mannbiome": mannbiome_status,
            "vectordb": vectordb_status
        },
        "message": "MannBiome Customer Portal API with Real Bacteria Analysis"
    }

# =======================
# USER AUTHENTICATION & PROFILE APIs
# =======================

@app.get("/api/user/{user_id}/profile")
def get_user_profile(user_id: int, db: Session = Depends(get_db)):
    """Get user profile information with customer details"""
    try:
        if db is None:
            # Return mock data if no database connection
            return {
                "success": True,
                "user": {
                    "user_id": user_id,
                    "username": f"user_{user_id}",
                    "email": f"user{user_id}@mannbiome.com",
                    "first_name": "John",
                    "last_name": "Doe",
                    "full_name": "John Doe",
                    "initials": "JD",
                    "report_id": f"MG{user_id:04d}",
                    "created_at": "January 15, 2024",
                    "last_updated": "March 12, 2025",
                    "status": "active",
                    "age": 35
                },
                "message": "Using mock data - database not available"
            }
        
        query = text("""
            SELECT 
                ua.user_id,
                ua.username,
                ua.email,
                ua.first_name,
                ua.last_name,
                ua.created_at,
                ua.last_login,
                ua.status,
                ua.age
            FROM public.user_account ua
            WHERE ua.user_id = :user_id AND ua.role = 'patient'
        """)
        
        result = db.execute(query, {"user_id": user_id}).fetchone()
        
        if not result:
            # Return mock data if user not found
            return {
                "success": True,
                "user": {
                    "user_id": user_id,
                    "username": f"user_{user_id}",
                    "email": f"user{user_id}@mannbiome.com", 
                    "first_name": "John",
                    "last_name": "Doe",
                    "full_name": "John Doe",
                    "initials": "JD",
                    "report_id": f"MG{user_id:04d}",
                    "created_at": "January 15, 2024",
                    "last_updated": "March 12, 2025",
                    "status": "active",
                    "age": 35
                },
                "message": "User not found in database, using mock data"
            }
        
        user = dict(result._mapping)
        
        # Format dates
        if user.get('created_at'):
            user['created_at'] = user['created_at'].strftime('%B %d, %Y') if user['created_at'] else "January 15, 2024"
        if user.get('last_login'):
            user['last_updated'] = user['last_login'].strftime('%B %d, %Y') if user['last_login'] else "March 12, 2025"
        
        # Generate initials
        initials = ""
        if user.get('first_name'):
            initials += user['first_name'][0].upper()
        if user.get('last_name'):
            initials += user['last_name'][0].upper()
        user['initials'] = initials or "JD"
        
        # Generate report ID (format: MG + user_id padded to 4 digits)
        user['report_id'] = f"MG{user_id:04d}"
        
        # Generate full name
        first_name = user.get('first_name') or 'John'
        last_name = user.get('last_name') or 'Doe'
        user['full_name'] = f"{first_name} {last_name}".strip()
        
        return {
            "success": True,
            "user": user
        }
        
    except Exception as e:
        print(f"Error in get_user_profile: {e}")
        # Return mock data on any error
        return {
            "success": True,
            "user": {
                "user_id": user_id,
                "username": f"user_{user_id}",
                "email": f"user{user_id}@mannbiome.com",
                "first_name": "John",
                "last_name": "Doe", 
                "full_name": "John Doe",
                "initials": "JD",
                "report_id": f"MG{user_id:04d}",
                "created_at": "January 15, 2024",
                "last_updated": "March 12, 2025",
                "status": "active",
                "age": 35
            },
            "message": f"Database error, using mock data: {str(e)}"
        }
# =======================
# BACTERIA ANALYSIS HELPER FUNCTIONS (ADD THESE)
# =======================

def map_customer_to_participant(customer_id: int) -> str:
    """Map customer_id to participant_id format"""
    return str(customer_id)

def determine_bacteria_status(patient_abundance: float, ideal_min: float, ideal_max: float) -> str:
    """Determine if bacteria abundance is HIGH, LOW, or NORMAL"""
    try:
        if patient_abundance < ideal_min:
            return "LOW"
        elif patient_abundance > ideal_max:
            return "HIGH"
        else:
            return "NORMAL"
    except Exception as e:
        print(f"Error determining bacteria status: {e}")
        return "UNKNOWN"

def analyze_patient_bacteria_real(bacteria_data: list, vectordb):
    """Analyze patient bacteria against computed_bacteria_metadata ranges"""
    try:
        if not vectordb:
            return []
            
        bacteria_analysis = []
        
        # Get bacteria metadata from VectorDB
        metadata_query = text("""
            SELECT 
                bacteria_name,
                genus,
                ideal_min,
                ideal_max,
                units,
                evidence_strength
            FROM public.computed_bacteria_metadata
            WHERE ideal_min IS NOT NULL AND ideal_max IS NOT NULL
        """)
        
        metadata_results = vectordb.execute(metadata_query).fetchall()
        
        # Create lookup dictionary
        metadata_dict = {}
        for row in metadata_results:
            metadata_dict[row.bacteria_name.lower()] = {
                "bacteria_name": row.bacteria_name,
                "genus": row.genus,
                "ideal_min": row.ideal_min,
                "ideal_max": row.ideal_max,
                "units": row.units,
                "evidence_strength": row.evidence_strength
            }
        
        # Analyze each bacteria
        for bacteria_item in bacteria_data:
            bacteria_name = bacteria_item.get('bacteria_name', '').strip()
            patient_abundance = float(bacteria_item.get('abundance', 0))
            
            metadata = metadata_dict.get(bacteria_name.lower())
            
            if metadata:
                status = determine_bacteria_status(
                    patient_abundance, 
                    metadata["ideal_min"], 
                    metadata["ideal_max"]
                )
                
                bacteria_analysis.append({
                    "bacteria_name": bacteria_name,
                    "current_level": patient_abundance,
                    "optimal_min": metadata["ideal_min"],
                    "optimal_max": metadata["ideal_max"],
                    "status": status.lower(),
                    "genus": metadata["genus"],
                    "evidence_strength": metadata["evidence_strength"]
                })
        
        return bacteria_analysis
        
    except Exception as e:
        print(f"Error in analyze_patient_bacteria_real: {e}")
        return []

def calculate_domain_scores_from_bacteria(bacteria_analysis: list) -> dict:
    """Calculate domain scores based on real bacteria analysis"""
    try:
        # Count bacteria status
        total_bacteria = len(bacteria_analysis)
        if total_bacteria == 0:
            return {}
        
        normal_count = len([b for b in bacteria_analysis if b["status"] == "normal"])
        concerning_count = total_bacteria - normal_count
        
        # Calculate base score (higher normal bacteria = better score)
        normal_ratio = normal_count / total_bacteria
        base_score = 2.0 + (normal_ratio * 2.5)  # Score between 2.0-4.5
        
        # Calculate diversity score (slight variation)
        diversity_score = base_score - 0.3
        
        # Ensure scores are in valid range
        base_score = max(1.0, min(5.0, base_score))
        diversity_score = max(1.0, min(5.0, diversity_score))
        
        return {
            "overall_score": format_score(base_score),
            "diversity_score": format_score(diversity_score),
            "normal_bacteria_count": normal_count,
            "concerning_bacteria_count": concerning_count,
            "total_bacteria_analyzed": total_bacteria
        }
        
    except Exception as e:
        print(f"Error calculating domain scores: {e}")
        return {}
# =======================
# MICROBIOME DATA APIs
# =======================

# @app.get("/api/customer/{customer_id}/microbiome-data")
# def get_customer_microbiome_data(customer_id: int, db: Session = Depends(get_db)):
#     """Get customer's microbiome analysis data from most recent visit"""
#     try:
#         if db is None:
#             # Return mock data if no database connection
#             return get_mock_microbiome_data()
        
#         # Try to get real data from your schema
#         query = text("""
#             SELECT 
#                 hr.report_id,
#                 hr.overall_score,
#                 hr.diversity_score,
#                 hr.created_at,
#                 v.visit_date,
#                 v.user_id
#             FROM microbiome.health_reports hr
#             JOIN microbiome.visits v ON hr.visit_id = v.visit_id
#             WHERE v.user_id = :customer_id
#             ORDER BY v.visit_date DESC
#             LIMIT 1
#         """)
        
#         result = db.execute(query, {"customer_id": customer_id}).fetchone()
        
#         if not result:
#             # Return mock data if no visit data exists
#             return get_mock_microbiome_data()
        
#         report_data = dict(result._mapping)
        
#         # Get domain reports
#         domain_query = text("""
#             SELECT 
#                 dr.domain_report_id,
#                 dr.score,
#                 dr.diversity,
#                 dr.status,
#                 dr.comment,
#                 hd.domain_name
#             FROM microbiome.domain_reports dr
#             JOIN microbiome.health_domains hd ON dr.domain_id = hd.domain_id
#             WHERE dr.report_id = :report_id
#         """)
        
#         domain_results = db.execute(domain_query, {"report_id": report_data['report_id']}).fetchall()
        
#         # Process domain data with formatting
#         domains = {}
#         for row in domain_results:
#             domain = dict(row._mapping)
#             domain_name = domain['domain_name'].lower()
#             domains[domain_name] = {
#                 "score": format_score(domain['score']),  # âœ… FORMATTED
#                 "diversity": format_score(domain['diversity']),  # âœ… FORMATTED
#                 "status": domain['status']
#             }
        
#         # Fill in missing domains with calculated values
#         base_score = format_score(report_data.get('overall_score', 3.5))  # âœ… FORMATTED
#         diversity = format_score(report_data.get('diversity_score', 2.8))  # âœ… FORMATTED
        
#         default_domains = {
#             "liver": {"score": max(1.0, base_score - 0.7), "diversity": max(1.0, diversity - 0.3)},
#             "aging": {"score": max(1.0, base_score - 0.9), "diversity": max(1.0, diversity - 0.4)},
#             "skin": {"score": max(1.0, base_score - 0.6), "diversity": max(1.0, diversity - 0.1)},
#             "cognitive": {"score": min(5.0, base_score + 0.3), "diversity": min(5.0, diversity + 0.4)},
#             "gut": {"score": max(1.0, base_score - 0.3), "diversity": max(1.0, diversity + 0.2)},
#             "heart": {"score": base_score, "diversity": diversity + 0.2}
#         }
        
#         # âœ… UPDATED SECTION WITH FORMATTING
#         for domain_name, values in default_domains.items():
#             if domain_name not in domains:
#                 score = format_score(values["score"])  # âœ… FORMATTED
#                 domains[domain_name] = {
#                     "score": score,
#                     "diversity": format_score(values["diversity"]),  # âœ… FORMATTED
#                     "status": get_status_from_score(score)
#                 }
        
#         # Calculate overall averages from all domains (excluding overall itself)
#         domain_scores = [d["score"] for k, d in domains.items() if k != "overall"]
#         domain_diversities = [d["diversity"] for k, d in domains.items() if k != "overall"]
        
#         calculated_overall_score = calculate_overall_average(domain_scores)
#         calculated_diversity_score = calculate_overall_average(domain_diversities)
        
#         # Add overall domain with calculated averages
#         domains["overall"] = {
#             "score": calculated_overall_score,
#             "diversity": calculated_diversity_score,
#             "status": get_status_from_score(calculated_overall_score)
#         }
        
#         # Format the response with calculated averages
#         health_data = {
#             "diversity_score": calculated_diversity_score,  # Use calculated average
#             "overall_score": calculated_overall_score,      # Use calculated average
#             "last_updated": report_data['visit_date'].strftime('%B %d, %Y') if report_data.get('visit_date') else "March 12, 2025",
#             "domains": domains
#         }
        
#         return {
#             "success": True,
#             "health_data": health_data,
#             "message": "Data retrieved from database"
#         }
        
#     except Exception as e:
#         print(f"Error in get_customer_microbiome_data: {e}")
#         return get_mock_microbiome_data()


# =======================
# FRONTEND-COMPATIBLE ENDPOINTS (ADD THESE)
# =======================
@app.get("/api/microbiome-data/{customer_id}")
def get_microbiome_data(customer_id: int, db: Session = Depends(get_db)):
    """Get real microbiome data with improved abundance scaling"""
    try:
        if db is None:
            raise HTTPException(status_code=500, detail="Database connection not available")
        
        participant_id = str(customer_id)
        
        # Get microbiome data from database
        query = text("""
            SELECT 
                participant_id,
                lab_name,
                upload_date,
                bacteria_data,
                total_bacteria_count
            FROM public.patient_reports 
            WHERE participant_id = :participant_id
            ORDER BY upload_date DESC
            LIMIT 1
        """)
        
        result = db.execute(query, {"participant_id": participant_id}).fetchone()
        
        if not result:
            raise HTTPException(
                status_code=404, 
                detail=f"No microbiome data found for customer {customer_id}"
            )
        
        report_data = dict(result._mapping)
        bacteria_data = report_data['bacteria_data']
        
        print(f"Processing real microbiome data for customer {customer_id}: {len(bacteria_data)} bacteria found")
        
        # Process each bacteria entry with improved functions
        bacteria_analysis = []
        for bacteria_item in bacteria_data:
            try:
                bacteria_name = bacteria_item.get('bacteria_name', '').strip()
                abundance = float(bacteria_item.get('abundance', 0))
                evidence_strength = bacteria_item.get('evidence_strength', 'C')
                msp_id = bacteria_item.get('msp_id', '')
                units = bacteria_item.get('units', 'relative_abundance_fraction')
                
                # Categorize bacteria
                category = categorize_bacteria_by_name(bacteria_name)
                
                # Convert abundance to percentage with improved scaling
                percentage = convert_abundance_to_percentage(abundance)
                
                # Calculate status with updated thresholds
                status = calculate_bacteria_status(abundance, evidence_strength, category)
                
                bacteria_analysis.append({
                    "bacteria_name": bacteria_name,
                    "msp_id": msp_id,
                    "abundance": abundance,
                    "percentage": percentage,
                    "evidence_strength": evidence_strength,
                    "category": category,
                    "status": status,
                    "units": units
                })
                
            except Exception as e:
                print(f"Error processing bacteria {bacteria_item}: {e}")
                continue
        
        # Calculate overall health scores
        health_scores = calculate_overall_health_score(bacteria_analysis)
        
        # Group bacteria for carousel display
        species_carousel = group_bacteria_for_carousel(bacteria_analysis)
        
        # Create hardcoded domain information (since no domain tables exist)
        domain_info = {
            "domain_id": "microbiome",
            "domain_name": "Microbiome Analysis",
            "description": "Comprehensive analysis of your gut microbiome based on bacteria abundance and diversity",
            "score": health_scores["overall_score"],
            "diversity": health_scores["diversity_score"],
            "status": "good" if health_scores["overall_score"] >= 3.5 else "warning" if health_scores["overall_score"] >= 2.5 else "poor",
            "comment": f"Analysis of {len(bacteria_analysis)} bacteria species from {report_data.get('lab_name', 'laboratory')}"
        }
        
        # Create response in expected frontend format
        response_data = {
            "success": True,
            "domain_info": domain_info,
            "health_metrics": [
                {
                    "label": "Overall Health Score",
                    "value": health_scores["overall_score"],
                    "unit": "score",
                    "description": "Overall microbiome health based on bacteria analysis"
                },
                {
                    "label": "Diversity Score", 
                    "value": health_scores["diversity_score"],
                    "unit": "index",
                    "description": "Bacterial diversity and richness indicator"
                },
                {
                    "label": "Bacteria Analyzed",
                    "value": len(bacteria_analysis),
                    "unit": "count",
                    "description": "Total number of bacteria species identified"
                }
            ],
            "species_carousel": species_carousel,
            "metadata": {
                "lab_name": report_data.get('lab_name', 'Unknown Lab'),
                "upload_date": report_data['upload_date'].strftime('%Y-%m-%d') if report_data.get('upload_date') else None,
                "total_bacteria_count": report_data.get('total_bacteria_count', 0),
                "analyzed_count": len(bacteria_analysis),
                "data_source": "REAL_MICROBIOME_DATA"
            }
        }
        
        print(f"Successfully processed microbiome data: {len(bacteria_analysis)} bacteria analyzed")
        return response_data
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error in get_microbiome_data: {e}")
        raise HTTPException(status_code=500, detail=f"Error processing microbiome data: {str(e)}")

@app.get("/api/customer/{customer_id}/microbiome-data")
def get_customer_microbiome_data_frontend(customer_id: int, db: Session = Depends(get_db)):
    """Frontend-compatible endpoint that returns real microbiome data"""
    print(f"ðŸ”„ Frontend requesting microbiome data for customer {customer_id}")
    
    # Use your new real microbiome data function
    return get_microbiome_data(customer_id, db)
    
def get_status_from_score(score):
    """Helper function to determine status based on score"""
    if score >= 3.5:
        return "good"
    elif score >= 2.5:
        return "warning"
    else:
        return "poor"

def get_mock_microbiome_data():
    """Return mock microbiome data with properly formatted numbers - FIXES floating point errors"""
    # Define individual domain scores first
    domains_data = {
        "liver": {
            "score": format_score(2.8),      # âœ… Will show 2.8
            "diversity": format_score(2.5),  # âœ… Will show 2.5 instead of 1.9999999999999998
            "status": "poor"
        },
        "aging": {
            "score": format_score(2.6),      # âœ… Will show 2.6
            "diversity": format_score(2.4),  # âœ… Will show 2.4
            "status": "poor"
        },
        "skin": {
            "score": format_score(2.9),      # âœ… Will show 2.9
            "diversity": format_score(2.7),  # âœ… Will show 2.7
            "status": "warning"
        },
        "cognitive": {
            "score": format_score(3.8),      # âœ… Will show 3.8
            "diversity": format_score(3.2),  # âœ… Will show 3.2
            "status": "good"
        },
        "gut": {
            "score": format_score(3.2),      # âœ… Will show 3.2
            "diversity": format_score(3.0),  # âœ… Will show 3.0
            "status": "good"
        },
        "heart": {
            "score": format_score(3.5),      # âœ… Will show 3.5
            "diversity": format_score(3.0),  # âœ… Will show 3.0
            "status": "good"
        }
    }
    
    # Calculate overall scores as averages of all domains (excluding overall)
    overall_score_avg = calculate_overall_average([d["score"] for d in domains_data.values()])
    overall_diversity_avg = calculate_overall_average([d["diversity"] for d in domains_data.values()])
    
    # Add overall domain with calculated averages
    domains_data["overall"] = {
        "score": overall_score_avg,
        "diversity": overall_diversity_avg,
        "status": get_status_from_score(overall_score_avg)
    }
    
    return {
        "success": True,
        "health_data": {
            "diversity_score": overall_diversity_avg,  # Use calculated average
            "overall_score": overall_score_avg,        # Use calculated average
            "last_updated": "March 12, 2025",
            "domains": domains_data
        },
        "message": "Using mock data for demonstration"
    }

# =======================
# DASHBOARD DATA AGGREGATION
# =======================

@app.get("/api/customer/{customer_id}/dashboard-data")
def get_customer_dashboard_data(
    customer_id: int, 
    db: Session = Depends(get_db),
    vectordb = Depends(get_vectordb)
):
    """Get dashboard data with real microbiome integration"""
    try:
        print(f"ðŸ”„ Getting dashboard data for customer {customer_id}")
        
        # Get user profile
        user_response = get_user_profile(customer_id, db)
        
        # Try to get real microbiome data first
        try:
            real_microbiome_response = get_microbiome_data(customer_id, db)
            
            if real_microbiome_response["success"]:
                print(f"âœ… Using real microbiome data for customer {customer_id}")
                
                # Convert microbiome data to dashboard health_data format
                microbiome_data = real_microbiome_response["domain_info"]
                
                health_data = {
                    "diversity_score": microbiome_data["diversity"],
                    "overall_score": microbiome_data["score"],
                    "last_updated": real_microbiome_response["metadata"]["upload_date"] or "March 12, 2025",
                    "domains": {
                        "overall": {
                            "score": microbiome_data["score"],
                            "diversity": microbiome_data["diversity"],
                            "status": microbiome_data["status"]
                        },
                        "gut": {
                            "score": microbiome_data["score"],
                            "diversity": microbiome_data["diversity"],
                            "status": microbiome_data["status"]
                        },
                        "liver": {
                            "score": format_score(max(1.0, microbiome_data["score"] - 0.5)),
                            "diversity": format_score(max(1.0, microbiome_data["diversity"] - 0.3)),
                            "status": "warning" if microbiome_data["score"] - 0.5 < 2.5 else "good"
                        },
                        "heart": {
                            "score": format_score(min(5.0, microbiome_data["score"] + 0.2)),
                            "diversity": format_score(min(5.0, microbiome_data["diversity"] + 0.1)),
                            "status": "good"
                        },
                        "cognitive": {
                            "score": format_score(min(5.0, microbiome_data["score"] + 0.3)),
                            "diversity": format_score(min(5.0, microbiome_data["diversity"] + 0.2)),
                            "status": "good"
                        },
                        "skin": {
                            "score": format_score(max(1.0, microbiome_data["score"] - 0.1)),
                            "diversity": format_score(max(1.0, microbiome_data["diversity"] - 0.2)),
                            "status": "warning"
                        },
                        "aging": {
                            "score": format_score(max(1.0, microbiome_data["score"] - 0.4)),
                            "diversity": format_score(max(1.0, microbiome_data["diversity"] - 0.5)),
                            "status": "poor"
                        }
                    },
                    "bacteria_analyzed": real_microbiome_response["metadata"]["analyzed_count"],
                    "data_source": "REAL_MICROBIOME_DATA"
                }
                
                return {
                    "success": True,
                    "dashboard_data": {
                        "user": user_response["user"],
                        "health_data": health_data,
                        "customer_id": customer_id,
                        "user_id": customer_id
                    }
                }
                
        except Exception as e:
            print(f"âš ï¸ Could not get real microbiome data for customer {customer_id}: {e}")
        
        # Fallback to mock data if real data fails
        print(f"ðŸ“Š Using mock data for customer {customer_id}")
        health_response = get_mock_microbiome_data()
        
        return {
            "success": True,
            "dashboard_data": {
                "user": user_response["user"],
                "health_data": health_response["health_data"],
                "customer_id": customer_id,
                "user_id": customer_id
            }
        }
        
    except Exception as e:
        print(f"Error in get_customer_dashboard_data: {e}")
        raise HTTPException(status_code=500, detail=f"Error retrieving dashboard data: {str(e)}")# =======================
# ENHANCED HEALTH DOMAIN DETAILS (NEW)
# =======================

@app.get("/api/health-domains/{domain_id}/details")
def get_domain_details_enhanced(domain_id: str, customer_id: Optional[int] = None, db: Session = Depends(get_db)):
    """Get detailed information for a specific health domain with enhanced data"""
    try:
        # Domain information mapping with detailed content
        domain_info = {
            "liver": {
                "title": "Liver Health Analysis",
                "description": "Your liver health markers indicate areas for improvement. The liver plays a crucial role in detoxification, metabolism, and overall health.",
                "current_status": "Needs Attention",
                "icon": "ðŸ«€",
                "key_indicators": [
                    "Bile acid metabolism efficiency",
                    "Phase I & II detoxification pathways", 
                    "Metabolic function markers",
                    "Inflammatory response indicators"
                ],
                "recommendations": [
                    "Increase cruciferous vegetables (broccoli, kale, Brussels sprouts)",
                    "Reduce processed foods and alcohol consumption",
                    "Consider milk thistle or NAC supplementation",
                    "Implement intermittent fasting protocols"
                ],
                "foods_to_include": [
                    "Leafy greens", "Beets", "Carrots", "Avocados", 
                    "Walnuts", "Green tea", "Turmeric", "Garlic"
                ]
            },
            "cognitive": {
                "title": "Cognitive Health Analysis",
                "description": "Excellent cognitive health markers! Your brain-gut axis is functioning well. Continue current practices to maintain this status.",
                "current_status": "Excellent",
                "icon": "ðŸ§ ",
                "key_indicators": [
                    "Neurotransmitter balance",
                    "Brain-gut axis communication",
                    "Neuroinflammation levels",
                    "Cognitive performance markers"
                ],
                "recommendations": [
                    "Continue current dietary patterns",
                    "Maintain regular mental challenges",
                    "Keep up social engagement",
                    "Sustain current sleep schedule"
                ],
                "foods_to_include": [
                    "Fatty fish", "Blueberries", "Nuts and seeds", "Dark chocolate",
                    "Leafy greens", "Eggs", "Turmeric", "Broccoli"
                ]
            },
            "aging": {
                "title": "Aging & Longevity Analysis",
                "description": "Your aging markers suggest opportunities for interventions that support healthy aging and longevity.",
                "current_status": "Needs Improvement",
                "icon": "â³",
                "key_indicators": [
                    "Cellular regeneration markers",
                    "Antioxidant defense systems",
                    "Inflammatory aging (inflammaging)",
                    "Metabolic efficiency metrics"
                ],
                "recommendations": [
                    "Increase antioxidant-rich foods (berries, dark chocolate)",
                    "Implement regular strength training",
                    "Practice stress reduction techniques",
                    "Optimize sleep quality and duration"
                ],
                "foods_to_include": [
                    "Blueberries", "Pomegranates", "Dark leafy greens", "Fatty fish",
                    "Nuts and seeds", "Green tea", "Dark chocolate", "Olive oil"
                ]
            },
            "skin": {
                "title": "Skin Health Analysis",
                "description": "Your skin health markers show moderate status with opportunities for improvement through targeted interventions.",
                "current_status": "Moderate",
                "icon": "ðŸ§´",
                "key_indicators": [
                    "Skin microbiome diversity",
                    "Collagen synthesis markers",
                    "Hydration and barrier function",
                    "Inflammatory skin conditions"
                ],
                "recommendations": [
                    "Increase omega-3 fatty acid intake",
                    "Stay well-hydrated (8-10 glasses water daily)",
                    "Consider collagen supplementation",
                    "Reduce sugar and dairy intake"
                ],
                "foods_to_include": [
                    "Fatty fish", "Avocados", "Sweet potatoes", "Bell peppers",
                    "Tomatoes", "Bone broth", "Citrus fruits", "Green tea"
                ]
            },
            "gut": {
                "title": "Gut Health Analysis",
                "description": "Good gut health foundation with opportunities to enhance microbial diversity and optimize digestive function.",
                "current_status": "Good",
                "icon": "ðŸ¦ ",
                "key_indicators": [
                    "Microbial diversity index",
                    "Beneficial bacteria levels",
                    "Digestive enzyme activity",
                    "Intestinal barrier integrity"
                ],
                "recommendations": [
                    "Increase dietary fiber variety",
                    "Include fermented foods regularly",
                    "Consider rotating prebiotic sources",
                    "Minimize unnecessary antibiotic use"
                ],
                "foods_to_include": [
                    "Fermented vegetables", "Kefir", "Yogurt", "Kombucha",
                    "Diverse fiber sources", "Bone broth", "Prebiotic foods", "Herbs and spices"
                ]
            },
            "heart": {
                "title": "Cardiovascular Health Analysis",
                "description": "Your cardiovascular health markers show good status with opportunities for optimization through targeted lifestyle interventions.",
                "current_status": "Good",
                "icon": "â¤ï¸",
                "key_indicators": [
                    "Cholesterol metabolism",
                    "Blood pressure regulation",
                    "Inflammatory markers",
                    "Vascular health metrics"
                ],
                "recommendations": [
                    "Include more heart-healthy fats",
                    "Regular cardiovascular exercise",
                    "Reduce sodium intake",
                    "Stress management practices"
                ],
                "foods_to_include": [
                    "Fatty fish", "Olive oil", "Nuts", "Seeds",
                    "Berries", "Oats", "Beans", "Dark chocolate"
                ]
            }
        }
        
        if domain_id not in domain_info:
            raise HTTPException(status_code=404, detail="Health domain not found")
        
        domain_data = domain_info[domain_id]
        
        # If customer_id is provided, try to get personalized data
        if customer_id:
            try:
                microbiome_response = get_customer_microbiome_data(customer_id, db)
                health_data = microbiome_response["health_data"]
                
                if domain_id in health_data["domains"]:
                    domain_score = health_data["domains"][domain_id]
                    domain_data["current_score"] = round(float(domain_score["score"]), 1)
                    domain_data["diversity_score"] = round(float(domain_score["diversity"]), 1)
                    domain_data["status"] = domain_score["status"]
                    
                    # Update status based on score
                    score = float(domain_score["score"])
                    if score >= 3.5:
                        domain_data["current_status"] = "Excellent"
                    elif score >= 2.5:
                        domain_data["current_status"] = "Moderate" 
                    else:
                        domain_data["current_status"] = "Needs Attention"
            except Exception as e:
                print(f"Warning: Could not get personalized data for {domain_id}: {str(e)}")
                # Continue with general info
                pass
        
        # Try to get recommendations from database if available
        if customer_id and db is not None:
            try:
                recommendations_response = get_customer_recommendations_for_domain(customer_id, domain_id, db)
                if recommendations_response.get("success"):
                    domain_data["personalized_recommendations"] = recommendations_response["recommendations"]
            except Exception as e:
                print(f"Warning: Could not get personalized recommendations: {str(e)}")
                # If no personalized recommendations, use default ones
                pass
        
        return {
            "success": True,
            "domain": domain_data
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving domain details: {str(e)}")

def get_customer_recommendations_for_domain(customer_id: int, domain_id: str, db: Session):
    """Helper function to get recommendations for a specific customer and domain"""
    try:
        # Map domain names to domain IDs (you may need to adjust this based on your data)
        domain_name_to_id = {
            "liver": 2,
            "aging": 6, 
            "skin": 4,
            "cognitive": 5,
            "gut": 1,
            "heart": 3
        }
        
        domain_db_id = domain_name_to_id.get(domain_id)
        if not domain_db_id:
            return {"success": False, "message": "Domain not found"}
        
        # Get the latest domain report for this customer and domain
        domain_report_query = text("""
            SELECT dr.domain_report_id
            FROM microbiome.domain_reports dr
            JOIN microbiome.health_reports hr ON dr.report_id = hr.report_id
            JOIN microbiome.visits v ON hr.visit_id = v.visit_id
            JOIN customers.customer c ON v.user_id = c.user_id
            WHERE dr.domain_id = :domain_db_id 
            AND c.customer_id = :customer_id
            ORDER BY hr.created_at DESC
            LIMIT 1
        """)
        
        domain_report = db.execute(domain_report_query, {
            "domain_db_id": domain_db_id,
            "customer_id": customer_id
        }).fetchone()
        
        if not domain_report:
            return {"success": False, "message": "No domain report found"}
        
        # Try to get detailed recommendations first
        detailed_query = text("""
            SELECT recommendation_category, item_name, description,
                   priority, dosage, duration, reason, evidence_level
            FROM microbiome.detailed_recommendations
            WHERE domain_report_id = :domain_report_id
            AND is_recommended = true
            ORDER BY recommendation_category, display_order, priority DESC
            LIMIT 10
        """)
        
        detailed_recs = db.execute(detailed_query, {"domain_report_id": domain_report.domain_report_id}).fetchall()
        
        if detailed_recs:
            recommendations_by_category = {}
            for rec in detailed_recs:
                category = rec.recommendation_category
                if category not in recommendations_by_category:
                    recommendations_by_category[category] = []
                
                priority_map = {1: "high", 2: "medium", 3: "low"}
                priority = priority_map.get(rec.priority, "medium")
                
                recommendations_by_category[category].append({
                    "title": rec.item_name,
                    "description": rec.description,
                    "reason": rec.reason,
                    "priority": priority,
                    "dosage": rec.dosage,
                    "duration": rec.duration,
                    "evidence_level": rec.evidence_level
                })
            
            return {
                "success": True,
                "recommendations": recommendations_by_category
            }
        
        return {"success": False, "message": "No recommendations found"}
        
    except Exception as e:
        print(f"Error getting recommendations for domain {domain_id}: {str(e)}")
        return {"success": False, "message": str(e)}

@app.get("/api/health-domains/{domain_id}/metrics/{customer_id}")
def get_domain_health_metrics(domain_id: str, customer_id: int, db: Session = Depends(get_db)):
    """Get health metrics for a specific domain and customer"""
    try:
        # Map domain names to domain IDs
        domain_name_to_id = {
            "liver": 2,
            "aging": 6, 
            "skin": 4,
            "cognitive": 5,
            "gut": 1,
            "heart": 3
        }
        
        domain_db_id = domain_name_to_id.get(domain_id)
        if not domain_db_id:
            raise HTTPException(status_code=404, detail="Domain not found")
        
        # Get the latest domain report
        domain_report_query = text("""
            SELECT dr.domain_report_id, dr.score, dr.diversity, dr.status
            FROM microbiome.domain_reports dr
            JOIN microbiome.health_reports hr ON dr.report_id = hr.report_id
            JOIN microbiome.visits v ON hr.visit_id = v.visit_id
            JOIN customers.customer c ON v.user_id = c.user_id
            WHERE dr.domain_id = :domain_db_id 
            AND c.customer_id = :customer_id
            ORDER BY hr.created_at DESC
            LIMIT 1
        """)
        
        domain_report = db.execute(domain_report_query, {
            "domain_db_id": domain_db_id,
            "customer_id": customer_id
        }).fetchone()
        
        if not domain_report:
            # Return default metrics if no data found
            return {
                "success": True,
                "metrics": [
                    {
                        "metric_name": "Health Score",
                        "metric_value": 3.0,
                        "metric_unit": "score",
                        "metric_description": "Overall health assessment for this domain"
                    },
                    {
                        "metric_name": "Diversity Index", 
                        "metric_value": 2.8,
                        "metric_unit": "index",
                        "metric_description": "Microbial diversity measurement"
                    }
                ]
            }
        
        # Get health metrics summary
        metrics_query = text("""
            SELECT metric_name, metric_value, metric_unit, metric_description
            FROM microbiome.health_metrics_summary
            WHERE domain_report_id = :domain_report_id
            ORDER BY display_order
        """)
        
        metrics = db.execute(metrics_query, {
            "domain_report_id": domain_report.domain_report_id
        }).fetchall()
        
        metrics_list = []
        for metric in metrics:
            metrics_list.append({
                "metric_name": metric.metric_name,
                "metric_value": float(metric.metric_value),
                "metric_unit": metric.metric_unit,
                "metric_description": metric.metric_description
            })
        
        # If no metrics found, add basic ones
        if not metrics_list:
            metrics_list = [
                {
                    "metric_name": "Health Score",
                    "metric_value": float(domain_report.score),
                    "metric_unit": "score",
                    "metric_description": "Overall health assessment for this domain"
                },
                {
                    "metric_name": "Diversity Index",
                    "metric_value": float(domain_report.diversity),
                    "metric_unit": "index", 
                    "metric_description": "Microbial diversity measurement"
                },
                {
                    "metric_name": "Status Level",
                    "metric_value": {"good": 4, "warning": 2, "poor": 1}.get(domain_report.status, 3),
                    "metric_unit": "level",
                    "metric_description": "Current health status indicator"
                }
            ]
        
        return {
            "success": True,
            "metrics": metrics_list
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving health metrics: {str(e)}")

# =======================
# CLINICAL TRIALS APIs (Database-Powered)
# =======================

@app.get("/api/clinical-trials")
def get_clinical_trials(
    domain: Optional[str] = None,
    status: Optional[str] = None,
    clinical_status: Optional[str] = None,
    limit: Optional[int] = 20,
    offset: Optional[int] = 0,
    db: Session = Depends(get_db)
):
    """Get clinical trials from database, optionally filtered by domain and status"""
    try:
        if db is None:
            # Return mock data if no database connection
            return get_mock_clinical_trials()
        
        # Base query joining clinical trials with health domains
        base_query = text("""
            SELECT 
                ct.trial_id,
                ct.trial_code,
                ct.name,
                ct.vendor,
                ct.domain_id,
                hd.domain_name as domain,
                ct.description,
                ct.status,
                ct.clinical_status,
                ct.duration,
                ct.participants,
                ct.max_participants,
                ct.image_path as image,
                ct.is_eligible,
                ct.key_findings,
                ct.publication,
                ct.publication_date,
                ct.created_at,
                ct.updated_at
            FROM microbiome.clinical_trials_new ct
            JOIN microbiome.health_domains hd ON ct.domain_id = hd.domain_id
            WHERE 1=1
        """)
        
        # Build dynamic WHERE clause
        where_conditions = []
        params = {}
        
        if domain:
            where_conditions.append("hd.domain_name = :domain")
            params["domain"] = domain
        
        if status:
            where_conditions.append("ct.status = :status")
            params["status"] = status
            
        if clinical_status:
            where_conditions.append("ct.clinical_status = :clinical_status")
            params["clinical_status"] = clinical_status
        
        # Add WHERE conditions if any
        if where_conditions:
            query_text = base_query.text + " AND " + " AND ".join(where_conditions)
        else:
            query_text = base_query.text
            
        # Add ORDER BY and LIMIT
        query_text += " ORDER BY ct.created_at DESC"
        
        if limit:
            query_text += f" LIMIT :limit"
            params["limit"] = limit
            
        if offset:
            query_text += f" OFFSET :offset"
            params["offset"] = offset
        
        final_query = text(query_text)
        
        # Execute query
        result = db.execute(final_query, params).fetchall()
        
        # Convert to list of dictionaries
        trials = []
        for row in result:
            trial = dict(row._mapping)
            
            # Format dates
            if trial['publication_date']:
                trial['publication_date'] = trial['publication_date'].strftime('%Y-%m-%d')
            if trial['created_at']:
                trial['created_at'] = trial['created_at'].strftime('%Y-%m-%d %H:%M:%S')
            if trial['updated_at']:
                trial['updated_at'] = trial['updated_at'].strftime('%Y-%m-%d %H:%M:%S')
            
            # Calculate completion percentage
            if trial['participants'] and trial['max_participants']:
                trial['completion_percentage'] = round((trial['participants'] / trial['max_participants']) * 100, 1)
            else:
                trial['completion_percentage'] = 0
            
            trials.append(trial)
        
        # Get total count for pagination
        count_query = text("""
            SELECT COUNT(*) as total
            FROM microbiome.clinical_trials_new ct
            JOIN microbiome.health_domains hd ON ct.domain_id = hd.domain_id
            WHERE 1=1
        """)
        
        if where_conditions:
            count_query_text = count_query.text + " AND " + " AND ".join(where_conditions)
        else:
            count_query_text = count_query.text
            
        count_result = db.execute(text(count_query_text), params).fetchone()
        total_trials = count_result[0] if count_result else 0
        
        return {
            "success": True,
            "total_trials": total_trials,
            "showing": len(trials),
            "limit": limit,
            "offset": offset,
            "filters": {
                "domain": domain,
                "status": status,
                "clinical_status": clinical_status
            },
            "trials": trials
        }
        
    except Exception as e:
        print(f"Error in get_clinical_trials: {e}")
        return get_mock_clinical_trials()

def get_mock_clinical_trials():
    """Return mock clinical trials data"""
    mock_trials = [
        {
            "trial_id": 1,
            "trial_code": "CT001",
            "name": "Advanced Gut Microbiome Restoration Protocol",
            "vendor": "BioHealth Labs",
            "domain_id": 1,
            "domain": "gut",
            "description": "A comprehensive 12-week clinical trial studying the effects of personalized probiotic therapy on gut microbiome diversity and digestive health outcomes.",
            "status": "open",
            "clinical_status": "ongoing",
            "duration": "12 weeks",
            "participants": 145,
            "max_participants": 200,
            "completion_percentage": 72.5,
            "image": "/assets/images/probiotics_images/Gut Health Pro Clinical.jpeg",
            "key_findings": "Significant increase in beneficial bacteria (45% improvement in Bifidobacterium levels) and reduction in inflammatory markers (30% decrease in IL-6).",
            "publication": "Journal of Microbiome Research",
            "publication_date": "2024-03-15",
            "created_at": "2025-06-03"
        },
        {
            "trial_id": 2,
            "trial_code": "CT006",
            "name": "Liver Function Enhancement Protocol",
            "vendor": "HepatoHealth Institute",
            "domain_id": 2,
            "domain": "liver",
            "description": "Clinical study investigating natural liver support compounds for improving detoxification pathways and overall liver function.",
            "status": "open",
            "clinical_status": "ongoing",
            "duration": "16 weeks",
            "participants": 78,
            "max_participants": 120,
            "completion_percentage": 65.0,
            "image": "/assets/images/probiotics_images/Liver Support Complex.jpeg",
            "key_findings": "Improved liver enzyme profiles (ALT and AST levels decreased by 22% on average) and enhanced detoxification markers.",
            "publication": "Hepatology Research",
            "publication_date": "2024-01-12",
            "created_at": "2025-06-03"
        }
    ]
    
    return {
        "success": True,
        "total_trials": len(mock_trials),
        "showing": len(mock_trials),
        "trials": mock_trials,
        "message": "Using mock data - database not available"
    }


# =======================
# ENHANCED MODAL DATA ENDPOINTS
# =======================

@app.get("/api/health-domains/{domain_id}/modal-data/{customer_id}")
def get_domain_modal_data(domain_id: int, customer_id: int, db: Session = Depends(get_db)):
    """
    Get complete modal data for a health domain
    domain_id: integer (1=gut, 2=liver, 3=heart, 4=skin, 5=cognitive, 6=aging)
    """
    try:
        if db is None:
            return get_mock_modal_data(f"domain_{domain_id}")
        
        # Get the latest domain report for this customer
        domain_report_query = text("""
            SELECT dr.domain_report_id, dr.score, dr.diversity, dr.status, dr.comment,
                   hd.domain_name, hd.description
            FROM microbiome.domain_reports dr
            JOIN microbiome.health_reports hr ON dr.report_id = hr.report_id
            JOIN microbiome.visits v ON hr.visit_id = v.visit_id
            JOIN microbiome.health_domains hd ON dr.domain_id = hd.domain_id
            WHERE dr.domain_id = :domain_id 
            AND v.user_id = :user_id
            ORDER BY hr.created_at DESC
            LIMIT 1
        """)
        
        domain_report = db.execute(domain_report_query, {
            "domain_id": domain_id,
            "user_id": customer_id
        }).fetchone()
        
        if not domain_report:
            return get_mock_modal_data(f"domain_{domain_id}")
        
        # Get all the data components
        species_data = get_species_carousel_data(domain_report.domain_report_id, db)
        pathway_data = get_pathway_carousel_data(domain_report.domain_report_id, db)
        recommendations_data = get_recommendations_modal_data(domain_report.domain_report_id, db)
        health_metrics = get_health_metrics_modal_data(domain_report.domain_report_id, db)
        
        return {
            "success": True,
            "domain_info": {
                "domain_id": domain_id,
                "domain_name": domain_report.domain_name,
                "description": domain_report.description,
                "score": format_score(domain_report.score),
                "diversity": format_score(domain_report.diversity),
                "status": domain_report.status,
                "comment": domain_report.comment
            },
            "health_metrics": health_metrics,
            "species_carousel": species_data,
            "pathway_carousel": pathway_data,
            "recommendations": recommendations_data
        }
        
    except Exception as e:
        print(f"Error in get_domain_modal_data: {e}")
        return get_mock_modal_data(f"domain_{domain_id}")

@app.get("/api/health-domains/{domain_id}/species-carousel/{customer_id}")
def get_species_carousel_only(domain_id: int, customer_id: int, db: Session = Depends(get_db)):
    """Get only species carousel data for a domain"""
    try:
        modal_data = get_domain_modal_data(domain_id, customer_id, db)
        return {
            "success": modal_data["success"],
            "species_carousel": modal_data["species_carousel"],
            "domain_info": modal_data["domain_info"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving species data: {str(e)}")

@app.get("/api/health-domains/{domain_id}/pathway-carousel/{customer_id}")
def get_pathway_carousel_only(domain_id: int, customer_id: int, db: Session = Depends(get_db)):
    """Get only pathway carousel data for a domain"""
    try:
        modal_data = get_domain_modal_data(domain_id, customer_id, db)
        return {
            "success": modal_data["success"],
            "pathway_carousel": modal_data["pathway_carousel"],
            "domain_info": modal_data["domain_info"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving pathway data: {str(e)}")

@app.get("/api/health-domains/{domain_id}/recommendations-only/{customer_id}")
def get_recommendations_only(domain_id: int, customer_id: int, db: Session = Depends(get_db)):
    """Get only recommendations data for a domain"""
    try:
        modal_data = get_domain_modal_data(domain_id, customer_id, db)
        return {
            "success": modal_data["success"],
            "recommendations": modal_data["recommendations"],
            "domain_info": modal_data["domain_info"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving recommendations: {str(e)}")

# Optional: Keep this one debug endpoint for production monitoring
@app.get("/api/debug/domain-reports")
def debug_domain_reports(db: Session = Depends(get_db)):
    """Debug endpoint to check available domain reports - useful for monitoring"""
    try:
        if db is None:
            return {"error": "No database connection"}
        
        query = text("""
            SELECT dr.domain_report_id, dr.report_id, dr.domain_id, dr.score, dr.diversity, dr.status,
                   hd.domain_name, hr.created_at
            FROM microbiome.domain_reports dr
            JOIN microbiome.health_domains hd ON dr.domain_id = hd.domain_id
            JOIN microbiome.health_reports hr ON dr.report_id = hr.report_id
            ORDER BY hr.created_at DESC
            LIMIT 10
        """)
        
        results = db.execute(query).fetchall()
        
        domain_reports = []
        for row in results:
            domain_reports.append({
                "domain_report_id": row.domain_report_id,
                "report_id": row.report_id,
                "domain_id": row.domain_id,
                "domain_name": row.domain_name,
                "score": float(row.score),
                "diversity": float(row.diversity),
                "status": row.status,
                "created_at": str(row.created_at)
            })
        
        return {
            "success": True,
            "total_reports": len(domain_reports),
            "domain_reports": domain_reports
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }
    
    
def get_species_carousel_data(domain_report_id: int, db: Session):
    """Get species data with REAL bacteria analysis when available"""
    try:
        # Try to get real bacteria data first if we have vectordb
        if hasattr(db, '_vectordb_session'):
            vectordb = db._vectordb_session
            # Get real bacteria analysis here
            # This would need the customer_id to work properly
            pass
        
        # For now, return enhanced mock data that looks more realistic
        return get_enhanced_mock_species_data()
        
    except Exception as e:
        print(f"Error fetching species carousel data: {e}")
        return get_mock_species_data()

def get_enhanced_mock_species_data():
    """Enhanced mock data that mimics real bacteria analysis structure"""
    return {
        "bacteria": {
            "title": "Top Bacterial Species",
            "status": "Excellent", 
            "species": [
                {
                    "name": "Bacteroides fragilis",
                    "scientific_name": "Bacteroides fragilis",
                    "current_level": 0.045,  # More realistic abundance values
                    "optimal_level": 0.050,
                    "range_min": "0.02",
                    "range_max": "0.08",
                    "measurement_unit": "relative_abundance_fraction",
                    "status": "normal",  # Use lowercase to match real data
                    "is_beneficial": True,
                    "percentage": 90.0,
                    "range_fill_width": 75.0,
                    "marker_position": 80.0
                },
                {
                    "name": "Escherichia coli",
                    "scientific_name": "Escherichia coli",
                    "current_level": 0.028,
                    "optimal_level": 0.035,
                    "range_min": "0.015",
                    "range_max": "0.055",
                    "measurement_unit": "relative_abundance_fraction",
                    "status": "low",  # Some showing as low
                    "is_beneficial": True,
                    "percentage": 80.0,
                    "range_fill_width": 65.0,
                    "marker_position": 70.0
                },
                {
                    "name": "Faecalibacterium prausnitzii",
                    "scientific_name": "Faecalibacterium prausnitzii",
                    "current_level": 0.062,
                    "optimal_level": 0.060,
                    "range_min": "0.040",
                    "range_max": "0.080",
                    "measurement_unit": "relative_abundance_fraction",
                    "status": "high",  # Some showing as high
                    "is_beneficial": True,
                    "percentage": 103.3,
                    "range_fill_width": 85.0,
                    "marker_position": 90.0
                },
                {
                    "name": "Bifidobacterium bifidum",
                    "scientific_name": "Bifidobacterium bifidum",
                    "current_level": 0.038,
                    "optimal_level": 0.040,
                    "range_min": "0.020",
                    "range_max": "0.060",
                    "measurement_unit": "relative_abundance_fraction",
                    "status": "normal",
                    "is_beneficial": True,
                    "percentage": 95.0,
                    "range_fill_width": 78.0,
                    "marker_position": 82.0
                },
                {
                    "name": "Akkermansia muciniphila",
                    "scientific_name": "Akkermansia muciniphila",
                    "current_level": 0.022,
                    "optimal_level": 0.030,
                    "range_min": "0.015",
                    "range_max": "0.045",
                    "measurement_unit": "relative_abundance_fraction",
                    "status": "low",
                    "is_beneficial": True,
                    "percentage": 73.3,
                    "range_fill_width": 60.0,
                    "marker_position": 65.0
                }
            ]
        },
        "probiotics": {
            "title": "Probiotic Organisms",
            "status": "Good",
            "species": [
                {
                    "name": "Lactobacillus acidophilus", 
                    "scientific_name": "Lactobacillus acidophilus",
                    "current_level": 0.032,
                    "optimal_level": 0.040,
                    "range_min": "0.025",
                    "range_max": "0.055",
                    "measurement_unit": "relative_abundance_fraction",
                    "status": "low",  # Some bacteria showing issues
                    "is_beneficial": True,
                    "percentage": 80.0,
                    "range_fill_width": 65.0,
                    "marker_position": 70.0
                },
                {
                    "name": "Bifidobacterium longum",
                    "scientific_name": "Bifidobacterium longum",
                    "current_level": 0.048,
                    "optimal_level": 0.045,
                    "range_min": "0.030",
                    "range_max": "0.060",
                    "measurement_unit": "relative_abundance_fraction",
                    "status": "normal",
                    "is_beneficial": True,
                    "percentage": 106.7,
                    "range_fill_width": 85.0,
                    "marker_position": 88.0
                },
                {
                    "name": "Lactobacillus rhamnosus",
                    "scientific_name": "Lactobacillus rhamnosus",
                    "current_level": 0.029,
                    "optimal_level": 0.035,
                    "range_min": "0.020",
                    "range_max": "0.050",
                    "measurement_unit": "relative_abundance_fraction",
                    "status": "low",
                    "is_beneficial": True,
                    "percentage": 82.9,
                    "range_fill_width": 68.0,
                    "marker_position": 72.0
                },
                {
                    "name": "Lactobacillus plantarum",
                    "scientific_name": "Lactobacillus plantarum",
                    "current_level": 0.041,
                    "optimal_level": 0.038,
                    "range_min": "0.025",
                    "range_max": "0.055",
                    "measurement_unit": "relative_abundance_fraction",
                    "status": "normal",
                    "is_beneficial": True,
                    "percentage": 107.9,
                    "range_fill_width": 87.0,
                    "marker_position": 90.0
                },
                {
                    "name": "Lactobacillus casei",
                    "scientific_name": "Lactobacillus casei",
                    "current_level": 0.035,
                    "optimal_level": 0.040,
                    "range_min": "0.022",
                    "range_max": "0.058",
                    "measurement_unit": "relative_abundance_fraction",
                    "status": "normal",
                    "is_beneficial": True,
                    "percentage": 87.5,
                    "range_fill_width": 72.0,
                    "marker_position": 76.0
                }
            ]
        },
        "virus": {
            "title": "Viral Species",
            "status": "Normal",
            "species": [
                {
                    "name": "Bacteriophage T4",
                    "scientific_name": "Bacteriophage T4",
                    "current_level": 0.012,
                    "optimal_level": 0.015,
                    "range_min": "0.008",
                    "range_max": "0.025",
                    "measurement_unit": "relative_abundance_fraction",
                    "status": "low",
                    "is_beneficial": True,
                    "percentage": 80.0,
                    "range_fill_width": 65.0,
                    "marker_position": 70.0
                },
                {
                    "name": "CrAssphage",
                    "scientific_name": "CrAssphage",
                    "current_level": 0.018,
                    "optimal_level": 0.020,
                    "range_min": "0.010",
                    "range_max": "0.030",
                    "measurement_unit": "relative_abundance_fraction",
                    "status": "normal",
                    "is_beneficial": True,
                    "percentage": 90.0,
                    "range_fill_width": 75.0,
                    "marker_position": 78.0
                },
                {
                    "name": "Microviridae",
                    "scientific_name": "Microviridae",
                    "current_level": 0.014,
                    "optimal_level": 0.016,
                    "range_min": "0.009",
                    "range_max": "0.024",
                    "measurement_unit": "relative_abundance_fraction",
                    "status": "normal",
                    "is_beneficial": True,
                    "percentage": 87.5,
                    "range_fill_width": 72.0,
                    "marker_position": 75.0
                }
            ]
        },
        "fungi": {
            "title": "Fungal Species",
            "status": "Good",
            "species": [
                {
                    "name": "Saccharomyces boulardii",
                    "scientific_name": "Saccharomyces boulardii",
                    "current_level": 0.025,
                    "optimal_level": 0.028,
                    "range_min": "0.015",
                    "range_max": "0.040",
                    "measurement_unit": "relative_abundance_fraction",
                    "status": "normal",
                    "is_beneficial": True,
                    "percentage": 89.3,
                    "range_fill_width": 74.0,
                    "marker_position": 77.0
                },
                {
                    "name": "Candida albicans",
                    "scientific_name": "Candida albicans",
                    "current_level": 0.018,
                    "optimal_level": 0.012,
                    "range_min": "0.005",
                    "range_max": "0.020",
                    "measurement_unit": "relative_abundance_fraction",
                    "status": "high",  # Candida is concerning when high
                    "is_beneficial": False,
                    "percentage": 150.0,
                    "range_fill_width": 95.0,
                    "marker_position": 98.0
                },
                {
                    "name": "Malassezia restricta",
                    "scientific_name": "Malassezia restricta",
                    "current_level": 0.008,
                    "optimal_level": 0.010,
                    "range_min": "0.004",
                    "range_max": "0.016",
                    "measurement_unit": "relative_abundance_fraction",
                    "status": "low",
                    "is_beneficial": True,
                    "percentage": 80.0,
                    "range_fill_width": 65.0,
                    "marker_position": 68.0
                }
            ]
        },
        "pathogens": {
            "title": "Pathogenic Species",
            "status": "Low (Good)",
            "species": [
                {
                    "name": "Clostridium difficile",
                    "scientific_name": "Clostridium difficile",
                    "current_level": 0.003,
                    "optimal_level": 0.005,
                    "range_min": "0.001",
                    "range_max": "0.008",
                    "measurement_unit": "relative_abundance_fraction",
                    "status": "normal",  # Low levels are good for pathogens
                    "is_beneficial": False,
                    "percentage": 60.0,
                    "range_fill_width": 50.0,
                    "marker_position": 52.0
                },
                {
                    "name": "Salmonella enterica",
                    "scientific_name": "Salmonella enterica",
                    "current_level": 0.001,
                    "optimal_level": 0.002,
                    "range_min": "0.000",
                    "range_max": "0.004",
                    "measurement_unit": "relative_abundance_fraction",
                    "status": "low",  # Very low is excellent for pathogens
                    "is_beneficial": False,
                    "percentage": 50.0,
                    "range_fill_width": 40.0,
                    "marker_position": 42.0
                },
                {
                    "name": "Klebsiella pneumoniae",
                    "scientific_name": "Klebsiella pneumoniae",
                    "current_level": 0.007,
                    "optimal_level": 0.004,
                    "range_min": "0.001",
                    "range_max": "0.006",
                    "measurement_unit": "relative_abundance_fraction",
                    "status": "high",  # Concerning when high
                    "is_beneficial": False,
                    "percentage": 175.0,
                    "range_fill_width": 98.0,
                    "marker_position": 100.0
                }
            ]
        },
        "protozoa": {
            "title": "Protozoa Species",
            "status": "Low",
            "species": [
                {
                    "name": "Blastocystis hominis",
                    "scientific_name": "Blastocystis hominis",
                    "current_level": 0.006,
                    "optimal_level": 0.008,
                    "range_min": "0.002",
                    "range_max": "0.012",
                    "measurement_unit": "relative_abundance_fraction",
                    "status": "low",
                    "is_beneficial": False,
                    "percentage": 75.0,
                    "range_fill_width": 62.0,
                    "marker_position": 65.0
                },
                {
                    "name": "Entamoeba histolytica",
                    "scientific_name": "Entamoeba histolytica",
                    "current_level": 0.002,
                    "optimal_level": 0.003,
                    "range_min": "0.001",
                    "range_max": "0.005",
                    "measurement_unit": "relative_abundance_fraction",
                    "status": "low",
                    "is_beneficial": False,
                    "percentage": 66.7,
                    "range_fill_width": 55.0,
                    "marker_position": 58.0
                },
                {
                    "name": "Giardia lamblia",
                    "scientific_name": "Giardia lamblia",
                    "current_level": 0.001,
                    "optimal_level": 0.002,
                    "range_min": "0.000",
                    "range_max": "0.004",
                    "measurement_unit": "relative_abundance_fraction",
                    "status": "low",
                    "is_beneficial": False,
                    "percentage": 50.0,
                    "range_fill_width": 42.0,
                    "marker_position": 45.0
                }
            ]
        },
        "neurotransmitter": {
            "title": "Neurotransmitter Pathway",
            "status": "Good",
            "metrics": [
                {
                    "name": "Serotonin Production",
                    "current_level": 75.0,
                    "optimal_level": 80.0,
                    "range_low": "Low",
                    "range_high": "High",
                    "status": "good",
                    "description": "Level of serotonin production",
                    "percentage": 75.0,
                    "range_fill_width": 75.0,
                    "marker_position": 80.0
                },
                {
                    "name": "GABA Synthesis",
                    "current_level": 65.0,
                    "optimal_level": 70.0,
                    "range_low": "Low",
                    "range_high": "High",
                    "status": "good",
                    "description": "Synthesis of gamma-aminobutyric acid",
                    "percentage": 65.0,
                    "range_fill_width": 65.0,
                    "marker_position": 70.0
                },
                {
                    "name": "Dopamine Pathway",
                    "current_level": 70.0,
                    "optimal_level": 75.0,
                    "range_low": "Low",
                    "range_high": "High",
                    "status": "good",
                    "description": "Function of dopamine pathway",
                    "percentage": 70.0,
                    "range_fill_width": 70.0,
                    "marker_position": 75.0
                },
                {
                    "name": "Glutamate Balance",
                    "current_level": 60.0,
                    "optimal_level": 65.0,
                    "range_low": "Low",
                    "range_high": "High",
                    "status": "normal",
                    "description": "Balance of glutamate levels",
                    "percentage": 60.0,
                    "range_fill_width": 60.0,
                    "marker_position": 65.0
                },
                {
                    "name": "Norepinephrine Levels",
                    "current_level": 55.0,
                    "optimal_level": 60.0,
                    "range_low": "Low",
                    "range_high": "High",
                    "status": "normal",
                    "description": "Levels of norepinephrine",
                    "percentage": 55.0,
                    "range_fill_width": 55.0,
                    "marker_position": 60.0
                }
            ]
        }
    }
def get_mock_recommendations_data():
    """Return mock recommendations data"""
    return {
        "probiotics": [
            {
                "name": "Lactobacillus plantarum",
                "description": "Supports gut barrier integrity",
                "reason": "Low levels detected in analysis",
                "dosage": "10 billion CFU daily",
                "duration": "3 months",
                "priority": 1,
                "evidence_level": "strong",
                "recommended": True
            },
            {
                "name": "Lactobacillus acidophilus",
                "description": "Support overall gut health",
                "reason": "Enhance beneficial bacteria diversity",
                "dosage": "5 billion CFU daily",
                "duration": "Ongoing",
                "priority": 2,
                "evidence_level": "strong",
                "recommended": True
            }
        ],
        "supplements": [
            {
                "name": "L-Glutamine",
                "description": "Supports gut lining integrity",
                "reason": "Maintain healthy gut lining",
                "dosage": "5g daily",
                "duration": "As needed",
                "priority": 2,
                "evidence_level": "moderate",
                "recommended": True
            },
            {
                "name": "Immunoglobulin",
                "description": "Supports immune function in the gut",
                "reason": "Support immune function",
                "dosage": "4g daily",
                "duration": "2 months",
                "priority": 1,
                "evidence_level": "moderate",
                "recommended": True
            },
            {
                "name": "Zinc Carnosine",
                "description": "Helps protect and heal the gut lining",
                "reason": "Support mucosal repair",
                "dosage": "150mg daily",
                "duration": "6-8 weeks",
                "priority": 1,
                "evidence_level": "moderate",
                "recommended": True
            },
            {
                "name": "Inulin",
                "description": "Prebiotic fiber that feeds beneficial bacteria",
                "reason": "Feed beneficial bacteria",
                "dosage": "5-10g daily",
                "duration": "Ongoing",
                "priority": 2,
                "evidence_level": "strong",
                "recommended": True
            },
            {
                "name": "Arabinoglactin",
                "description": "Supports immune function and gut health",
                "reason": "Support immune function",
                "dosage": "4-8g daily",
                "duration": "Ongoing",
                "priority": 3,
                "evidence_level": "moderate",
                "recommended": True
            },
            {
                "name": "Licorice Root Extract",
                "description": "Soothes and protects the digestive tract",
                "reason": "Soothe digestive tract",
                "dosage": "400mg daily",
                "duration": "2-3 months",
                "priority": 3,
                "evidence_level": "moderate",
                "recommended": True
            }
        ],
        "diet": [
            {
                "name": "Increase Fiber-Rich Foods",
                "description": "Include more whole grains, legumes, and vegetables",
                "reason": "Support beneficial bacteria growth",
                "dosage": "25-35g daily",
                "duration": "Ongoing",
                "priority": 1,
                "evidence_level": "strong",
                "recommended": True
            },
            {
                "name": "Add Fermented Foods",
                "description": "Include kimchi, sauerkraut, kefir",
                "reason": "Introduce beneficial bacteria naturally",
                "dosage": "Daily servings",
                "duration": "Ongoing",
                "priority": 1,
                "evidence_level": "strong",
                "recommended": True
            }
        ],
        "lifestyle": [
            {
                "name": "Regular Exercise",
                "description": "Moderate intensity cardiovascular exercise",
                "reason": "Improve microbial diversity",
                "dosage": "30 min daily",
                "duration": "Ongoing",
                "priority": 1,
                "evidence_level": "strong",
                "recommended": True
            },
            {
                "name": "Stress Management",
                "description": "Meditation, yoga, or deep breathing",
                "reason": "Support gut-brain axis",
                "dosage": "15-20 min daily",
                "duration": "Ongoing",
                "priority": 2,
                "evidence_level": "moderate",
                "recommended": True
            }
        ]
    }

def get_mock_health_metrics():
    """Return mock health metrics"""
    return [
        {
            "label": "Status Level",
            "value": "Excellent",
            "unit": "level",
            "description": "Your health markers show strong indicators"
        },
        {
            "label": "Score",
            "value": 3.8,
            "unit": "score", 
            "description": "Above average health score"
        },
        {
            "label": "Diversity",
            "value": 3.2,
            "unit": "index",
            "description": "High microbial diversity observed"
        }
    ]

# =======================
# ADDITIONAL HELPER ENDPOINTS
# =======================

@app.get("/api/health-domains/{domain_id}/species-carousel/{customer_id}")
def get_species_carousel_only(domain_id: str, customer_id: int, db: Session = Depends(get_db)):
    """Get only species carousel data for a domain"""
    try:
        modal_data = get_domain_modal_data(domain_id, customer_id, db)
        return {
            "success": modal_data["success"],
            "species_carousel": modal_data["species_carousel"],
            "domain_info": modal_data["domain_info"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving species data: {str(e)}")

@app.get("/api/health-domains/{domain_id}/pathway-carousel/{customer_id}")
def get_pathway_carousel_only(domain_id: str, customer_id: int, db: Session = Depends(get_db)):
    """Get only pathway carousel data for a domain"""
    try:
        modal_data = get_domain_modal_data(domain_id, customer_id, db)
        return {
            "success": modal_data["success"],
            "pathway_carousel": modal_data["pathway_carousel"],
            "domain_info": modal_data["domain_info"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving pathway data: {str(e)}")

@app.get("/api/health-domains/{domain_id}/recommendations-only/{customer_id}")
def get_recommendations_only(domain_id: str, customer_id: int, db: Session = Depends(get_db)):
    """Get only recommendations data for a domain"""
    try:
        modal_data = get_domain_modal_data(domain_id, customer_id, db)
        return {
            "success": modal_data["success"],
            "recommendations": modal_data["recommendations"],
            "domain_info": modal_data["domain_info"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving recommendations: {str(e)}")

# =======================
# DEBUG ENDPOINTS FOR TESTING
# =======================

@app.get("/api/debug/domain-reports")
def debug_domain_reports(db: Session = Depends(get_db)):
    """Debug endpoint to check available domain reports"""
    try:
        if db is None:
            return {"error": "No database connection"}
        
        query = text("""
            SELECT dr.domain_report_id, dr.report_id, dr.domain_id, dr.score, dr.diversity, dr.status,
                   hd.domain_name, hr.created_at
            FROM microbiome.domain_reports dr
            JOIN microbiome.health_domains hd ON dr.domain_id = hd.domain_id
            JOIN microbiome.health_reports hr ON dr.report_id = hr.report_id
            ORDER BY hr.created_at DESC
            LIMIT 10
        """)
        
        results = db.execute(query).fetchall()
        
        domain_reports = []
        for row in results:
            domain_reports.append({
                "domain_report_id": row.domain_report_id,
                "report_id": row.report_id,
                "domain_id": row.domain_id,
                "domain_name": row.domain_name,
                "score": float(row.score),
                "diversity": float(row.diversity),
                "status": row.status,
                "created_at": str(row.created_at)
            })
        
        return {
            "success": True,
            "total_reports": len(domain_reports),
            "domain_reports": domain_reports
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

# =======================
# TESTING & VALIDATION ENDPOINTS
# =======================

@app.get("/api/test/modal-data/{domain_id}")
def test_modal_data_structure(domain_id: str):
    """Test endpoint to validate modal data structure without database"""
    try:
        mock_data = get_mock_modal_data(domain_id)
        
        # Validate structure
        validation_result = {
            "success": True,
            "domain_id": domain_id,
            "structure_validation": {
                "has_domain_info": "domain_info" in mock_data,
                "has_health_metrics": "health_metrics" in mock_data,
                "has_species_carousel": "species_carousel" in mock_data,
                "has_pathway_carousel": "pathway_carousel" in mock_data,
                "has_recommendations": "recommendations" in mock_data,
                "species_categories_count": len(mock_data.get("species_carousel", {})),
                "pathway_categories_count": len(mock_data.get("pathway_carousel", {})),
                "recommendation_categories_count": len(mock_data.get("recommendations", {}))
            },
            "sample_data": mock_data
        }
        
        return validation_result
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "domain_id": domain_id
        }

@app.get("/api/test/all-domains-mock")
def test_all_domains_mock():
    """Test all domain mock data generation"""
    domains = ["liver", "aging", "skin", "cognitive", "gut", "heart"]
    results = {}
    
    for domain in domains:
        try:
            results[domain] = {
                "success": True,
                "basic_info": get_mock_modal_data(domain)["domain_info"],
                "species_categories": list(get_mock_modal_data(domain)["species_carousel"].keys()),
                "pathway_categories": list(get_mock_modal_data(domain)["pathway_carousel"].keys())
            }
        except Exception as e:
            results[domain] = {
                "success": False,
                "error": str(e)
            }
    
    return {
        "success": True,
        "tested_domains": domains,
        "results": results
    }


def get_pathway_carousel_data(domain_report_id: int, db: Session):
    """Get pathway data organized by carousel categories"""
    try:
        query = text("""
            SELECT pa.pathway_category, pa.pathway_title, pa.metric_name,
                   pa.current_level, pa.optimal_level, pa.range_label_low,
                   pa.range_label_high, pa.status, pa.description
            FROM microbiome.pathway_analysis pa
            WHERE pa.domain_report_id = :domain_report_id
            ORDER BY pa.pathway_category, pa.metric_name
        """)
        
        pathway_data = db.execute(query, {"domain_report_id": domain_report_id}).fetchall()
        
        # Organize by pathway category
        carousel_data = {
            "LPS": {
                "title": "LPS (Lipopolysaccharide) Pathway",
                "status": "Normal",
                "metrics": []
            },
            "neurotransmitter": {
                "title": "Neurotransmitter Pathway", 
                "status": "Good",
                "metrics": []
            }
        }
        
        for pathway in pathway_data:
            category = pathway.pathway_category
            if category in carousel_data:
                current = float(pathway.current_level)
                optimal = float(pathway.optimal_level)
                
                # Calculate range fill and marker position
                percentage = (current / 100) * 100  # Current level is already a percentage
                range_fill = min(100, percentage)
                marker_position = min(100, percentage + 5)  # Marker slightly ahead
                
                carousel_data[category]["metrics"].append({
                    "name": pathway.metric_name,
                    "current_level": current,
                    "optimal_level": optimal,
                    "range_low": pathway.range_label_low,
                    "range_high": pathway.range_label_high,
                    "status": pathway.status,
                    "description": pathway.description,
                    "percentage": round(percentage, 1),
                    "range_fill_width": round(range_fill, 1),
                    "marker_position": round(marker_position, 1)
                })
        
        # Update status based on overall pathway performance
        for category, data in carousel_data.items():
            if data["metrics"]:
                # For LPS: lower is better, for neurotransmitter: higher is better
                if category == "LPS":
                    avg_level = sum(m["current_level"] for m in data["metrics"]) / len(data["metrics"])
                    data["status"] = "Good" if avg_level < 40 else "Normal" if avg_level < 60 else "Poor"
                else:  # neurotransmitter
                    avg_level = sum(m["current_level"] for m in data["metrics"]) / len(data["metrics"])
                    data["status"] = "Excellent" if avg_level >= 75 else "Good" if avg_level >= 60 else "Normal"
        
        return carousel_data
        
    except Exception as e:
        print(f"Error getting pathway carousel data: {e}")
        return get_mock_pathway_data()

def get_recommendations_modal_data(domain_report_id: int, db: Session):
    """Get recommendations data for modal display"""
    try:
        # Try detailed recommendations first
        detailed_query = text("""
            SELECT recommendation_category, item_name, description,
                   priority, dosage, duration, reason, evidence_level
            FROM microbiome.detailed_recommendations
            WHERE domain_report_id = :domain_report_id
            AND is_recommended = true
            ORDER BY recommendation_category, display_order, priority DESC
            LIMIT 20
        """)
        
        detailed_recs = db.execute(detailed_query, {"domain_report_id": domain_report_id}).fetchall()
        
        recommendations = {
            "probiotics": [],
            "supplements": [],
            "diet": [],
            "lifestyle": []
        }
        
        for rec in detailed_recs:
            category = rec.recommendation_category
            if category in recommendations:
                recommendations[category].append({
                    "name": rec.item_name,
                    "description": rec.description,
                    "reason": rec.reason,
                    "dosage": rec.dosage,
                    "duration": rec.duration,
                    "priority": rec.priority,
                    "evidence_level": rec.evidence_level,
                    "recommended": True
                })
        
        return recommendations
        
    except Exception as e:
        print(f"Error getting recommendations data: {e}")
        return get_mock_recommendations_data()

def get_health_metrics_modal_data(domain_report_id: int, db: Session):
    """Get health metrics for modal header display"""
    try:
        query = text("""
            SELECT metric_name, metric_value, metric_unit, metric_description
            FROM microbiome.health_metrics_summary
            WHERE domain_report_id = :domain_report_id
            ORDER BY display_order
            LIMIT 3
        """)
        
        metrics = db.execute(query, {"domain_report_id": domain_report_id}).fetchall()
        
        health_metrics = []
        for metric in metrics:
            health_metrics.append({
                "label": metric.metric_name,
                "value": format_score(metric.metric_value) if metric.metric_name in ["Score", "Diversity"] else metric.metric_value,
                "unit": metric.metric_unit,
                "description": metric.metric_description
            })
        
        return health_metrics
        
    except Exception as e:
        print(f"Error getting health metrics: {e}")
        return get_mock_health_metrics()

# =======================
# MOCK DATA FUNCTIONS
# =======================

def get_mock_modal_data(domain_id: str):
    """Return comprehensive mock data for modal"""
    
    # Determine status and scores based on domain
    domain_configs = {
        "liver": {"score": 2.8, "diversity": 2.5, "status": "poor", "main_status": "Needs Attention"},
        "aging": {"score": 2.6, "diversity": 2.4, "status": "poor", "main_status": "Needs Improvement"},
        "skin": {"score": 2.9, "diversity": 2.7, "status": "warning", "main_status": "Moderate"},
        "cognitive": {"score": 3.8, "diversity": 3.2, "status": "good", "main_status": "Excellent"},
        "gut": {"score": 3.2, "diversity": 3.0, "status": "good", "main_status": "Good"},
        "heart": {"score": 3.5, "diversity": 3.0, "status": "good", "main_status": "Good"}
    }
    
    config = domain_configs.get(domain_id, {"score": 3.0, "diversity": 2.8, "status": "warning", "main_status": "Moderate"})
    
    return {
        "success": True,
        "domain_info": {
            "domain_id": domain_id,
            "domain_name": domain_id.title(),
            "description": f"Your {domain_id} health analysis based on microbiome data",
            "score": config["score"],
            "diversity": config["diversity"],
            "status": config["status"],
            "comment": f"{domain_id.title()} health markers analysis"
        },
        "health_metrics": [
            {"label": "Status Level", "value": config["main_status"], "unit": "level", "description": f"Your {domain_id} markers show health indicators"},
            {"label": "Score", "value": config["score"], "unit": "score", "description": f"Above average {domain_id} health score"},
            {"label": "Diversity", "value": config["diversity"], "unit": "index", "description": "Microbial diversity observed"}
        ],
        "species_carousel": get_mock_species_data(),
        "pathway_carousel": get_mock_pathway_data(),
        "recommendations": get_mock_recommendations_data(),
        "message": "Using mock data for demonstration"
    }

def get_mock_species_data():
    """Return mock species carousel data"""
    return {
        "bacteria": {
            "title": "Top Bacterial Species",
            "status": "Excellent",
            "species": [
                {
                    "name": "Bacteroides fragilis",
                    "scientific_name": "Bacteroides fragilis",
                    "current_level": 75.0,
                    "optimal_level": 80.0,
                    "range_min": "10â´ CFU/g",
                    "range_max": "10â¸ CFU/g",
                    "measurement_unit": "CFU/g",
                    "status": "good",
                    "is_beneficial": True,
                    "percentage": 93.8,
                    "range_fill_width": 75.0,
                    "marker_position": 80.0
                },
                {
                    "name": "Escherichia coli",
                    "scientific_name": "Escherichia coli",
                    "current_level": 65.0,
                    "optimal_level": 70.0,
                    "range_min": "10Â³ CFU/g",
                    "range_max": "10â· CFU/g",
                    "measurement_unit": "CFU/g",
                    "status": "good",
                    "is_beneficial": True,
                    "percentage": 92.9,
                    "range_fill_width": 65.0,
                    "marker_position": 70.0
                },
                {
                    "name": "Lactobacillus plantarum",
                    "scientific_name": "Lactobacillus plantarum",
                    "current_level": 80.0,
                    "optimal_level": 85.0,
                    "range_min": "10âµ CFU/g",
                    "range_max": "10â¹ CFU/g",
                    "measurement_unit": "CFU/g",
                    "status": "good",
                    "is_beneficial": True,
                    "percentage": 94.1,
                    "range_fill_width": 80.0,
                    "marker_position": 85.0
                },
                {
                    "name": "Bifidobacterium bifidum",
                    "scientific_name": "Bifidobacterium bifidum",
                    "current_level": 70.0,
                    "optimal_level": 75.0,
                    "range_min": "10â´ CFU/g",
                    "range_max": "10â¸ CFU/g",
                    "measurement_unit": "CFU/g",
                    "status": "good",
                    "is_beneficial": True,
                    "percentage": 93.3,
                    "range_fill_width": 70.0,
                    "marker_position": 75.0
                },
                {
                    "name": "Streptococcus thermophilus",
                    "scientific_name": "Streptococcus thermophilus",
                    "current_level": 85.0,
                    "optimal_level": 90.0,
                    "range_min": "10â´ CFU/g",
                    "range_max": "10â¸ CFU/g",
                    "measurement_unit": "CFU/g",
                    "status": "good",
                    "is_beneficial": True,
                    "percentage": 94.4,
                    "range_fill_width": 85.0,
                    "marker_position": 90.0
                }
            ]
        },
        "probiotics": {
            "title": "Probiotic Organisms",
            "status": "Excellent",
            "species": [
                {
                    "name": "Lactobacillus acidophilus",
                    "scientific_name": "Lactobacillus acidophilus",
                    "current_level": 85.0,
                    "optimal_level": 90.0,
                    "range_min": "10â¶ CFU/g",
                    "range_max": "10â¸ CFU/g",
                    "measurement_unit": "CFU/g",
                    "status": "good",
                    "is_beneficial": True,
                    "percentage": 94.4,
                    "range_fill_width": 85.0,
                    "marker_position": 90.0
                },
                {
                    "name": "Bifidobacterium longum",
                    "scientific_name": "Bifidobacterium longum",
                    "current_level": 75.0,
                    "optimal_level": 80.0,
                    "range_min": "10âµ CFU/g",
                    "range_max": "10â· CFU/g",
                    "measurement_unit": "CFU/g",
                    "status": "good",
                    "is_beneficial": True,
                    "percentage": 93.8,
                    "range_fill_width": 75.0,
                    "marker_position": 80.0
                },
                {
                    "name": "Lactobacillus rhamnosus",
                    "scientific_name": "Lactobacillus rhamnosus",
                    "current_level": 80.0,
                    "optimal_level": 85.0,
                    "range_min": "10â¶ CFU/g",
                    "range_max": "10â¸ CFU/g",
                    "measurement_unit": "CFU/g",
                    "status": "good",
                    "is_beneficial": True,
                    "percentage": 94.1,
                    "range_fill_width": 80.0,
                    "marker_position": 85.0
                },
                {
                    "name": "Bifidobacterium bifidum",
                    "scientific_name": "Bifidobacterium bifidum",
                    "current_level": 70.0,
                    "optimal_level": 75.0,
                    "range_min": "10âµ CFU/g",
                    "range_max": "10â· CFU/g",
                    "measurement_unit": "CFU/g",
                    "status": "good",
                    "is_beneficial": True,
                    "percentage": 93.3,
                    "range_fill_width": 70.0,
                    "marker_position": 75.0
                },
                {
                    "name": "Lactobacillus casei",
                    "scientific_name": "Lactobacillus casei",
                    "current_level": 90.0,
                    "optimal_level": 95.0,
                    "range_min": "10â¶ CFU/g",
                    "range_max": "10â¸ CFU/g",
                    "measurement_unit": "CFU/g",
                    "status": "good",
                    "is_beneficial": True,
                    "percentage": 94.7,
                    "range_fill_width": 90.0,
                    "marker_position": 95.0
                }
            ]
        },
        "virus": {
            "title": "Viral Species",
            "status": "Normal",
            "species": [
                {
                    "name": "Bacteriophage T4",
                    "scientific_name": "Bacteriophage T4",
                    "current_level": 60.0,
                    "optimal_level": 65.0,
                    "range_min": "10Â² PFU/g",
                    "range_max": "10â´ PFU/g",
                    "measurement_unit": "PFU/g",
                    "status": "normal",
                    "is_beneficial": True,
                    "percentage": 92.3,
                    "range_fill_width": 60.0,
                    "marker_position": 65.0
                },
                {
                    "name": "CrAssphage",
                    "scientific_name": "CrAssphage",
                    "current_level": 55.0,
                    "optimal_level": 60.0,
                    "range_min": "10Â¹ PFU/g",
                    "range_max": "10Â³ PFU/g",
                    "measurement_unit": "PFU/g",
                    "status": "normal",
                    "is_beneficial": True,
                    "percentage": 91.7,
                    "range_fill_width": 55.0,
                    "marker_position": 60.0
                },
                {
                    "name": "Microviridae",
                    "scientific_name": "Microviridae",
                    "current_level": 70.0,
                    "optimal_level": 75.0,
                    "range_min": "10Â² PFU/g",
                    "range_max": "10â´ PFU/g",
                    "measurement_unit": "PFU/g",
                    "status": "normal",
                    "is_beneficial": True,
                    "percentage": 93.3,
                    "range_fill_width": 70.0,
                    "marker_position": 75.0
                }
            ]
        },
        "fungi": {
            "title": "Fungal Species",
            "status": "Good",
            "species": [
                {
                    "name": "Saccharomyces boulardii",
                    "scientific_name": "Saccharomyces boulardii",
                    "current_level": 80.0,
                    "optimal_level": 85.0,
                    "range_min": "10Â³ CFU/g",
                    "range_max": "10âµ CFU/g",
                    "measurement_unit": "CFU/g",
                    "status": "good",
                    "is_beneficial": True,
                    "percentage": 94.1,
                    "range_fill_width": 80.0,
                    "marker_position": 85.0
                },
                {
                    "name": "Candida albicans",
                    "scientific_name": "Candida albicans",
                    "current_level": 40.0,
                    "optimal_level": 45.0,
                    "range_min": "10Â² CFU/g",
                    "range_max": "10â´ CFU/g",
                    "measurement_unit": "CFU/g",
                    "status": "normal",
                    "is_beneficial": False,
                    "percentage": 88.9,
                    "range_fill_width": 40.0,
                    "marker_position": 45.0
                }
            ]
        },
        "pathogens": {
            "title": "Pathogenic Species",
            "status": "Low (Good)",
            "species": [
                {
                    "name": "Clostridium difficile",
                    "scientific_name": "Clostridium difficile",
                    "current_level": 20.0,
                    "optimal_level": 25.0,
                    "range_min": "10Â¹ CFU/g",
                    "range_max": "10Â³ CFU/g",
                    "measurement_unit": "CFU/g",
                    "status": "good",
                    "is_beneficial": False,
                    "percentage": 80.0,
                    "range_fill_width": 20.0,
                    "marker_position": 25.0
                },
                {
                    "name": "Salmonella enterica",
                    "scientific_name": "Salmonella enterica",
                    "current_level": 15.0,
                    "optimal_level": 20.0,
                    "range_min": "10Â¹ CFU/g",
                    "range_max": "10Â³ CFU/g",
                    "measurement_unit": "CFU/g",
                    "status": "good",
                    "is_beneficial": False,
                    "percentage": 75.0,
                    "range_fill_width": 15.0,
                    "marker_position": 20.0
                }
            ]
        },
        "protozoa": {
            "title": "Protozoa Species",
            "status": "Low",
            "species": [
                {
                    "name": "Blastocystis hominis",
                    "scientific_name": "Blastocystis hominis",
                    "current_level": 30.0,
                    "optimal_level": 35.0,
                    "range_min": "10Â¹ Cells/g",
                    "range_max": "10Â³ Cells/g",
                    "measurement_unit": "Cells/g",
                    "status": "normal",
                    "is_beneficial": False,
                    "percentage": 85.7,
                    "range_fill_width": 30.0,
                    "marker_position": 35.0
                },
                {
                    "name": "Entamoeba histolytica",
                    "scientific_name": "Entamoeba histolytica",
                    "current_level": 20.0,
                    "optimal_level": 25.0,
                    "range_min": "10Â¹ Cells/g",
                    "range_max": "10Â³ Cells/g",
                    "measurement_unit": "Cells/g",
                    "status": "normal",
                    "is_beneficial": False,
                    "percentage": 80.0,
                    "range_fill_width": 20.0,
                    "marker_position": 25.0
                }
            ]
        }
    }

def get_mock_pathway_data():
    """Return mock pathway carousel data"""
    return {
        "LPS": {
            "title": "LPS (Lipopolysaccharide) Pathway",
            "status": "Normal",
            "metrics": [
                {
                    "name": "Endotoxin Production",
                    "current_level": 45.0,
                    "optimal_level": 50.0,
                    "range_low": "Low",
                    "range_high": "High",
                    "status": "normal",
                    "description": "Level of bacterial endotoxin production",
                    "percentage": 45.0,
                    "range_fill_width": 45.0,
                    "marker_position": 50.0
                },
                {
                    "name": "Inflammatory Response",
                    "current_level": 35.0,
                    "optimal_level": 40.0,
                    "range_low": "Low",
                    "range_high": "High",
                    "status": "good",
                    "description": "Inflammatory response to endotoxins",
                    "percentage": 35.0,
                    "range_fill_width": 35.0,
                    "marker_position": 40.0
                },
                {
                    "name": "Barrier Function",
                    "current_level": 70.0,
                    "optimal_level": 75.0,
                    "range_low": "Weak",
                    "range_high": "Strong",
                    "status": "good",
                    "description": "Intestinal barrier integrity",
                    "percentage": 70.0,
                    "range_fill_width": 70.0,
                    "marker_position": 75.0
                },
                {
                    "name": "Immune Activation",
                    "current_level": 50.0,
                    "optimal_level": 55.0,
                    "range_low": "Low",
                    "range_high": "High",
                    "status": "normal",
                    "description": "Level of immune system activation",
                    "percentage": 50.0,
                    "range_fill_width": 50.0,
                    "marker_position": 55.0
                },
                {
                    "name": "Metabolic Stress",
                    "current_level": 40.0,
                    "optimal_level": 45.0,
                    "range_low": "Low",
                    "range_high": "High",
                    "status": "good",
                    "description": "Level of metabolic stress due to endotoxins",
                    "percentage": 40.0,
                    "range_fill_width": 40.0,
                    "marker_position": 45.0
                }
            ]
        },
        "neurotransmitter": {
            "title": "Neurotransmitter Pathway",
            "status": "Good",
            "metrics": [
                {
                    "name": "Serotonin Production",
                    "current_level": 75.0,
                    "optimal_level": 80.0,
                    "range_low": "Low",
                    "range_high": "High",
                    "status": "good",
                    "description": "Level of serotonin production",
                    "percentage": 75.0,
                    "range_fill_width": 75.0,
                    "marker_position": 80.0
                },
                {
                    "name": "GABA Synthesis",
                    "current_level": 65.0,
                    "optimal_level": 70.0,
                    "range_low": "Low",
                    "range_high": "High",
                    "status": "good",
                    "description": "Synthesis of gamma-aminobutyric acid",
                    "percentage": 65.0,
                    "range_fill_width": 65.0,
                    "marker_position": 70.0
                },
                {
                    "name": "Dopamine Pathway",
                    "current_level": 70.0,
                    "optimal_level": 75.0,
                    "range_low": "Low",
                    "range_high": "High",
                    "status": "good",
                    "description": "Function of dopamine pathway",
                    "percentage": 70.0,
                    "range_fill_width": 70.0,
                    "marker_position": 75.0
                },
                {
                    "name": "Glutamate Balance",
                    "current_level": 60.0,
                    "optimal_level": 65.0,
                    "range_low": "Low",
                    "range_high": "High",
                    "status": "normal",
                    "description": "Balance of glutamate levels",
                    "percentage": 60.0,
                    "range_fill_width": 60.0,
                    "marker_position": 65.0
                },
                {
                    "name": "Norepinephrine Levels",
                    "current_level": 55.0,
                    "optimal_level": 60.0,
                    "range_low": "Low",
                    "range_high": "High",
                    "status": "normal",
                    "description": "Levels of norepinephrine",
                    "percentage": 55.0,
                    "range_fill_width": 55.0,
                    "marker_position": 60.0
                }
            ]
        }
    }

    # Add this endpoint to your DBCustomerPortal.py file
# Place it with your other health domain endpoints

@app.get("/api/health-domains/{domain_id}/clinical-trials")
def get_domain_clinical_trials(
    domain_id: str, 
    customer_id: Optional[int] = Query(None), 
    limit: Optional[int] = Query(5), 
    db: Session = Depends(get_db)
):
    """Get clinical trials specific to a health domain with customer eligibility"""
    try:
        # Map domain IDs to domain names for filtering
        domain_mapping = {
            "1": "gut",      # Added numeric mappings to match your system
            "2": "liver",
            "3": "heart", 
            "4": "skin",
            "5": "cognitive",
            "6": "aging",
            "gut": "gut",    # Keep string mappings for flexibility
            "liver": "liver",
            "aging": "aging", 
            "skin": "skin",
            "cognitive": "cognitive",
            "heart": "heart",
            "immune": "immune"
        }
        
        domain_name = domain_mapping.get(str(domain_id))
        if not domain_name:
            raise HTTPException(status_code=404, detail="Health domain not found")
        
        # If no database connection, return mock data
        if db is None:
            return get_mock_clinical_trials_data(domain_name, customer_id, limit)
        
        # Query for domain-specific trials with eligibility info if customer_id provided
        if customer_id:
            query = text("""
                SELECT 
                    ct.trial_id,
                    ct.trial_code,
                    ct.name,
                    ct.vendor,
                    ct.domain_id,
                    hd.domain_name as domain,
                    ct.description,
                    ct.status,
                    ct.clinical_status,
                    ct.duration,
                    ct.participants,
                    ct.max_participants,
                    ct.image_path as image,
                    COALESCE(te.is_eligible, ct.is_eligible) as is_eligible,
                    te.eligibility_reason,
                    ct.key_findings,
                    ct.publication,
                    ct.publication_date,
                    CASE 
                        WHEN en.enrollment_id IS NOT NULL THEN en.status
                        ELSE NULL 
                    END as enrollment_status
                FROM microbiome.clinical_trials_new ct
                JOIN microbiome.health_domains hd ON ct.domain_id = hd.domain_id
                LEFT JOIN microbiome.trial_eligibility te ON ct.trial_id = te.trial_id AND te.customer_id = :customer_id
                LEFT JOIN microbiome.trial_enrollments en ON ct.trial_id = en.trial_id AND en.customer_id = :customer_id
                WHERE hd.domain_name = :domain_name
                ORDER BY ct.status ASC, ct.created_at DESC
                LIMIT :limit
            """)
            
            params = {
                "domain_name": domain_name,
                "customer_id": customer_id,
                "limit": limit
            }
        else:
            query = text("""
                SELECT 
                    ct.trial_id,
                    ct.trial_code,
                    ct.name,
                    ct.vendor,
                    ct.domain_id,
                    hd.domain_name as domain,
                    ct.description,
                    ct.status,
                    ct.clinical_status,
                    ct.duration,
                    ct.participants,
                    ct.max_participants,
                    ct.image_path as image,
                    ct.is_eligible,
                    ct.key_findings,
                    ct.publication,
                    ct.publication_date
                FROM microbiome.clinical_trials_new ct
                JOIN microbiome.health_domains hd ON ct.domain_id = hd.domain_id
                WHERE hd.domain_name = :domain_name
                ORDER BY ct.status ASC, ct.created_at DESC
                LIMIT :limit
            """)
            
            params = {
                "domain_name": domain_name,
                "limit": limit
            }
        
        result = db.execute(query, params).fetchall()
        
        # Convert to list of dictionaries
        trials = []
        for row in result:
            trial = dict(row._mapping)
            
            # Format dates
            if trial['publication_date']:
                trial['publication_date'] = trial['publication_date'].strftime('%Y-%m-%d')
            
            trials.append(trial)
        
        # Get total count for this domain
        count_query = text("""
            SELECT COUNT(*) as total
            FROM microbiome.clinical_trials_new ct
            JOIN microbiome.health_domains hd ON ct.domain_id = hd.domain_id
            WHERE hd.domain_name = :domain_name
        """)
        
        count_result = db.execute(count_query, {"domain_name": domain_name}).fetchone()
        total_trials = count_result[0] if count_result else 0
        
        return {
            "success": True,
            "domain_id": domain_id,
            "domain_name": domain_name,
            "total_trials": total_trials,
            "showing": len(trials),
            "customer_id": customer_id,
            "trials": trials
        }
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error in get_domain_clinical_trials: {e}")
        # Return mock data on error
        return get_mock_clinical_trials_data(domain_mapping.get(str(domain_id), domain_id), customer_id, limit)


# Add this helper function for mock data
def get_mock_clinical_trials_data(domain_name: str, customer_id: Optional[int] = None, limit: int = 5):
    """Return mock clinical trials data for testing"""
    
    # Mock trials data - you can customize this
    mock_trials = [
        {
            "trial_id": 1,
            "trial_code": f"{domain_name.upper()}-2025-001",
            "name": f"Advanced {domain_name.title()} Health Study",
            "vendor": "Research Institute",
            "domain_id": 1,
            "domain": domain_name,
            "description": f"A comprehensive study examining microbiome interventions for {domain_name} health optimization using personalized probiotic therapy.",
            "status": "open",
            "clinical_status": "recruiting",
            "duration": "12 weeks",
            "participants": 45,
            "max_participants": 100,
            "image": f"/assets/images/trials/{domain_name}_trial.jpeg",
            "is_eligible": True,
            "eligibility_reason": "Good candidate based on current health markers",
            "key_findings": f"Preliminary results show 25% improvement in {domain_name} health markers.",
            "publication": "Journal of Microbiome Research",
            "publication_date": "2024-11-15",
            "enrollment_status": None
        },
        {
            "trial_id": 2,
            "trial_code": f"{domain_name.upper()}-2025-002", 
            "name": f"{domain_name.title()} Optimization Protocol",
            "vendor": "BioHealth Labs",
            "domain_id": 1,
            "domain": domain_name,
            "description": f"Investigating targeted nutritional interventions for {domain_name} health enhancement.",
            "status": "open",
            "clinical_status": "ongoing",
            "duration": "16 weeks",
            "participants": 32,
            "max_participants": 80,
            "image": f"/assets/images/trials/{domain_name}_study.jpeg",
            "is_eligible": True,
            "eligibility_reason": "Meets inclusion criteria for intervention study",
            "key_findings": f"Significant improvements observed in {domain_name} function markers.",
            "publication": "Clinical Nutrition Journal",
            "publication_date": "2024-10-20",
            "enrollment_status": None
        }
    ]
    
    # Filter to limit
    limited_trials = mock_trials[:limit]
    
    return {
        "success": True,
        "domain_id": domain_name,
        "domain_name": domain_name,
        "total_trials": len(mock_trials),
        "showing": len(limited_trials),
        "customer_id": customer_id,
        "trials": limited_trials,
        "message": "Using mock data - database not available"
    }

# Add these imports at the top with your other imports
from fastapi.responses import StreamingResponse
import io
from report_generator import MannBiomePDFGenerator, generate_filename
from report_models import ReportRequest, DomainReportRequest

# Add this endpoint anywhere with your other @app.post endpoints
@app.post("/api/reports/generate")
async def generate_report(request: ReportRequest, db: Session = Depends(get_db)):
    """Generate comprehensive microbiome health reports"""
    try:
        # Use customer_id from request or default to 3 (as seen in your logs)
        customer_id = request.customer_id or 3
        
        # Get data using your existing functions
        user_data = get_user_profile(customer_id, db)
        health_data = get_customer_microbiome_data(customer_id, db)
        
        # Initialize PDF generator
        pdf_generator = MannBiomePDFGenerator()
        
        # Generate appropriate report
        if request.type == "full":
            pdf_content = pdf_generator.create_full_report(user_data, health_data)
            filename = generate_filename("full", customer_id=customer_id)
        elif request.type == "domain":
            if not request.domains:
                raise HTTPException(status_code=400, detail="Domains required for domain-specific report")
            pdf_content = pdf_generator.create_domain_report(user_data, health_data, request.domains)
            filename = generate_filename("domain", domains=request.domains, customer_id=customer_id)
        else:
            raise HTTPException(status_code=400, detail="Invalid report type")
        
        # Return PDF as streaming response
        return StreamingResponse(
            io.BytesIO(pdf_content),
            media_type="application/pdf",
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Report generation error: {e}")
        raise HTTPException(status_code=500, detail=f"Error generating report: {str(e)}")

# Optional: Add a separate endpoint for domain-specific reports
@app.post("/api/reports/generate/domain")
async def generate_domain_report(request: DomainReportRequest, db: Session = Depends(get_db)):
    """Generate domain-specific health reports"""
    # Convert to general request and use the main endpoint
    general_request = ReportRequest(
        type="domain",
        domains=request.domains,
        format=request.format,
        customer_id=request.customer_id,
        include_recommendations=request.include_recommendations,
        include_detailed_analysis=request.include_detailed_analysis
    )
    
    return await generate_report(general_request, db)
@app.get("/api/debug/check-data")
def check_what_data_exists():
    """Simple check to see what customer data exists"""
    try:
        if engine is None:
            return {"error": "No database connection"}
        
        db = SessionLocal()
        
        # Check what participant IDs exist in your database
        query = text("SELECT participant_id FROM public.patient_reports LIMIT 10")
        results = db.execute(query).fetchall()
        
        participant_list = [row.participant_id for row in results]
        
        db.close()
        
        return {
            "participants_in_database": participant_list,
            "total_found": len(participant_list),
            "note": "These are the participant IDs that have real data"
        }
        
    except Exception as e:
        return {"error": str(e)}
# =======================
# MAIN API ENDPOINT
# =======================

# =======================
# HELPER ENDPOINT FOR DEBUGGING
# =======================

@app.get("/api/microbiome-data/{customer_id}/debug")
def debug_microbiome_data(customer_id: int, db: Session = Depends(get_db)):
    """Debug endpoint to see raw bacteria data and processing steps"""
    try:
        if db is None:
            return {"error": "Database connection not available"}
        
        participant_id = str(customer_id)
        
        # Get raw data
        query = text("""
            SELECT bacteria_data, lab_name, upload_date, total_bacteria_count
            FROM public.patient_reports 
            WHERE participant_id = :participant_id
            ORDER BY upload_date DESC
            LIMIT 1
        """)
        
        result = db.execute(query, {"participant_id": participant_id}).fetchone()
        
        if not result:
            return {"error": f"No data found for customer {customer_id}"}
        
        bacteria_data = result.bacteria_data
        
        # Show sample processing
        sample_bacteria = bacteria_data[:5] if len(bacteria_data) > 5 else bacteria_data
        processed_samples = []
        
        for bacteria in sample_bacteria:
            category = categorize_bacteria_by_name(bacteria.get('bacteria_name', ''))
            percentage = convert_abundance_to_percentage(bacteria.get('abundance', 0))
            status = calculate_bacteria_status(
                bacteria.get('abundance', 0), 
                bacteria.get('evidence_strength', 'C'), 
                category
            )
            
            processed_samples.append({
                "original": bacteria,
                "processed": {
                    "category": category,
                    "percentage": percentage,
                    "status": status
                }
            })
        
        return {
            "success": True,
            "raw_count": len(bacteria_data),
            "lab_info": {
                "lab_name": result.lab_name,
                "upload_date": str(result.upload_date),
                "total_count": result.total_bacteria_count
            },
            "sample_processing": processed_samples
        }
        
    except Exception as e:
        return {"success": False, "error": str(e)}
if __name__ == "__main__":
    import uvicorn
    print("ðŸš€ Starting MannBiome Customer Portal API...")
    print("ðŸ“š API Documentation: http://localhost:8001/docs")
    print("ðŸ” Health Check: http://localhost:8001/api/health-check")
    print("âœ… Enhanced health domain APIs added!")
    uvicorn.run(app, host="0.0.0.0", port=8000)