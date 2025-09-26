# report_models.py
"""
Pydantic models for report generation API
"""

from pydantic import BaseModel, Field
from typing import Optional, List
from enum import Enum

class ReportType(str, Enum):
    """Enum for report types"""
    FULL = "full"
    DOMAIN = "domain"

class ReportFormat(str, Enum):
    """Enum for report formats"""
    PDF = "pdf"
    # Future: Could add XLSX, HTML, etc.

class ReportRequest(BaseModel):
    """Request model for report generation"""
    type: ReportType = Field(..., description="Type of report to generate")
    domains: Optional[List[str]] = Field(None, description="List of domains for domain-specific reports")
    format: ReportFormat = Field(ReportFormat.PDF, description="Output format for the report")
    customer_id: Optional[int] = Field(None, description="Customer ID for personalized data")
    include_recommendations: bool = Field(True, description="Include recommendations section")
    include_detailed_analysis: bool = Field(True, description="Include detailed domain analysis")
    
    class Config:
        """Pydantic configuration"""
        schema_extra = {
            "example": {
                "type": "full",
                "format": "pdf",
                "customer_id": 3,
                "include_recommendations": True,
                "include_detailed_analysis": True
            }
        }

class DomainReportRequest(ReportRequest):
    """Specific request model for domain reports"""
    type: ReportType = Field(ReportType.DOMAIN, description="Must be 'domain' for this endpoint")
    domains: List[str] = Field(..., min_items=1, description="At least one domain must be specified")
    
    class Config:
        """Pydantic configuration"""
        schema_extra = {
            "example": {
                "type": "domain",
                "domains": ["gut", "liver"],
                "format": "pdf",
                "customer_id": 3,
                "include_recommendations": True,
                "include_detailed_analysis": True
            }
        }

class ReportResponse(BaseModel):
    """Response model for successful report generation"""
    success: bool = Field(True, description="Whether the report was generated successfully")
    message: str = Field(..., description="Success message")
    filename: str = Field(..., description="Generated filename")
    generated_at: str = Field(..., description="Timestamp when report was generated")
    report_type: str = Field(..., description="Type of report generated")
    customer_id: Optional[int] = Field(None, description="Customer ID used for the report")

class ReportErrorResponse(BaseModel):
    """Response model for report generation errors"""
    success: bool = Field(False, description="Always false for error responses")
    error: str = Field(..., description="Error message")
    error_code: Optional[str] = Field(None, description="Error code for debugging")
    timestamp: str = Field(..., description="Timestamp when error occurred")