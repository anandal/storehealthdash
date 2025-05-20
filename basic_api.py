"""
SceneIQ API - Basic RESTful API implementation with Swagger UI
This module provides core API endpoints for the SceneIQ dashboard.
"""

from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime, date
import uvicorn
from database import get_session, Store, TheftIncident, RewardsData

# Create FastAPI app
app = FastAPI(
    title="SceneIQ API",
    description="API for managing convenience store analytics data",
    version="1.0.0",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define Pydantic models for request/response
class StoreBase(BaseModel):
    name: str
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    
    class Config:
        orm_mode = True

class StoreResponse(StoreBase):
    id: int

class TheftIncidentBase(BaseModel):
    store_id: int
    timestamp: datetime
    severity: str
    value: float
    
    class Config:
        orm_mode = True

class TheftIncidentResponse(TheftIncidentBase):
    id: int
    resolved: bool

# API Endpoints
@app.get("/")
async def root():
    """Root endpoint that provides API information"""
    return {
        "name": "SceneIQ API",
        "version": "1.0.0",
        "description": "API for managing convenience store analytics data",
    }

@app.get("/api/stores", response_model=List[StoreResponse], tags=["Stores"])
async def get_stores(
    db: Session = Depends(get_session),
    skip: int = Query(0, description="Skip N records"),
    limit: int = Query(100, description="Limit to N records")
):
    """
    Retrieve a list of all stores.
    """
    stores = db.query(Store).offset(skip).limit(limit).all()
    return stores

@app.get("/api/theft-incidents", response_model=List[TheftIncidentResponse], tags=["Theft Analytics"])
async def get_theft_incidents(
    db: Session = Depends(get_session),
    store_id: Optional[int] = Query(None, description="Filter by store ID"),
    skip: int = Query(0, description="Skip N records"),
    limit: int = Query(100, description="Limit to N records")
):
    """
    Retrieve a list of theft incidents with optional filtering.
    """
    query = db.query(TheftIncident)
    
    if store_id:
        query = query.filter(TheftIncident.store_id == store_id)
    
    incidents = query.offset(skip).limit(limit).all()
    return incidents

@app.get("/api/dashboard/summary", tags=["Dashboard"])
async def get_dashboard_summary(
    db: Session = Depends(get_session),
    store_id: Optional[int] = Query(None, description="Filter by store ID")
):
    """
    Retrieve a summary of dashboard data.
    """
    # Define the base queries
    theft_query = db.query(TheftIncident)
    rewards_query = db.query(RewardsData)
    
    # Apply store filter if provided
    if store_id:
        theft_query = theft_query.filter(TheftIncident.store_id == store_id)
        rewards_query = rewards_query.filter(RewardsData.store_id == store_id)
    
    # Execute queries with limits to avoid performance issues
    theft_incidents = theft_query.limit(1000).all()
    rewards_data = rewards_query.limit(1000).all()
    
    # Calculate summary metrics
    total_theft_incidents = len(theft_incidents)
    resolved_incidents = sum(1 for incident in theft_incidents if incident.resolved)
    resolution_rate = (resolved_incidents / total_theft_incidents * 100) if total_theft_incidents > 0 else 0
    
    total_members = 0
    new_members = 0
    if rewards_data:
        total_members = sum(data.total_members for data in rewards_data) // len(rewards_data)  # Average
        new_members = sum(data.new_members for data in rewards_data)
    
    # Build the summary response
    summary = {
        "theft_analytics": {
            "total_incidents": total_theft_incidents,
            "resolved_incidents": resolved_incidents,
            "resolution_rate": resolution_rate
        },
        "rewards_program": {
            "total_members": total_members,
            "new_members": new_members
        }
    }
    
    return summary

if __name__ == "__main__":
    uvicorn.run("basic_api:app", host="0.0.0.0", port=5001, reload=True)