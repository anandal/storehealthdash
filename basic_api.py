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
    docs_url="/",  # Make docs the root endpoint for easy access
    redoc_url="/redoc"
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
    zip_code: Optional[str] = None
    phone: Optional[str] = None
    manager: Optional[str] = None
    opening_date: Optional[date] = None
    
    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "name": "Main Street Store",
                "address": "123 Main St",
                "city": "Springfield",
                "state": "IL",
                "zip_code": "62701",
                "phone": "555-123-4567",
                "manager": "John Smith",
                "opening_date": "2023-01-01"
            }
        }

class StoreCreate(StoreBase):
    pass

class StoreResponse(StoreBase):
    id: int

class TheftIncidentBase(BaseModel):
    store_id: int
    timestamp: datetime
    severity: str
    value: float
    video_clip_url: Optional[str] = None
    
    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "store_id": 1,
                "timestamp": "2025-05-18T14:32:15",
                "severity": "Medium", 
                "value": 125.50,
                "video_clip_url": "https://example.com/clip1.mp4"
            }
        }

class TheftIncidentCreate(TheftIncidentBase):
    pass

class TheftIncidentResponse(TheftIncidentBase):
    id: int
    resolved: bool
    
class RewardsBase(BaseModel):
    store_id: int
    date: date
    total_members: int
    new_members: int
    campaign_engagement: float
    active_campaigns: int
    
    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "store_id": 1,
                "date": "2025-05-01",
                "total_members": 1250,
                "new_members": 25,
                "campaign_engagement": 45.8,
                "active_campaigns": 3
            }
        }
        
class RewardsCreate(RewardsBase):
    pass

class RewardsResponse(RewardsBase):
    id: int

# API Endpoints
@app.get("/")
async def root():
    """Root endpoint that provides API information"""
    return {
        "name": "SceneIQ API",
        "version": "1.0.0",
        "description": "API for managing convenience store analytics data",
    }

# Store Endpoints
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

@app.post("/api/stores", response_model=StoreResponse, tags=["Stores"], status_code=201)
async def create_store(
    store: StoreCreate,
    db: Session = Depends(get_session)
):
    """
    Create a new store.
    
    This endpoint allows you to onboard a new store by providing the store details.
    """
    db_store = Store(**store.dict())
    db.add(db_store)
    db.commit()
    db.refresh(db_store)
    return db_store

@app.get("/api/stores/{store_id}", response_model=StoreResponse, tags=["Stores"])
async def get_store(
    store_id: int,
    db: Session = Depends(get_session)
):
    """
    Retrieve a specific store by ID.
    """
    store = db.query(Store).filter(Store.id == store_id).first()
    if not store:
        raise HTTPException(status_code=404, detail="Store not found")
    return store

@app.put("/api/stores/{store_id}", response_model=StoreResponse, tags=["Stores"])
async def update_store(
    store_id: int,
    store: StoreCreate,
    db: Session = Depends(get_session)
):
    """
    Update a store's information.
    """
    db_store = db.query(Store).filter(Store.id == store_id).first()
    if not db_store:
        raise HTTPException(status_code=404, detail="Store not found")
    
    store_data = store.dict(exclude_unset=True)
    for key, value in store_data.items():
        setattr(db_store, key, value)
    
    db.commit()
    db.refresh(db_store)
    return db_store

@app.delete("/api/stores/{store_id}", tags=["Stores"], status_code=204)
async def delete_store(
    store_id: int,
    db: Session = Depends(get_session)
):
    """
    Delete a store.
    """
    db_store = db.query(Store).filter(Store.id == store_id).first()
    if not db_store:
        raise HTTPException(status_code=404, detail="Store not found")
    
    db.delete(db_store)
    db.commit()
    return None

# Theft Incident Endpoints
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

@app.post("/api/theft-incidents", response_model=TheftIncidentResponse, tags=["Theft Analytics"], status_code=201)
async def create_theft_incident(
    incident: TheftIncidentCreate,
    db: Session = Depends(get_session)
):
    """
    Create a new theft incident.
    
    This endpoint allows you to record a new theft incident with details like store ID, timestamp, severity, and estimated value.
    """
    # Extract day of week and hour from timestamp
    day_of_week = incident.timestamp.strftime("%A")
    hour = incident.timestamp.hour
    
    db_incident = TheftIncident(
        **incident.dict(),
        day_of_week=day_of_week,
        hour=hour,
        resolved=False
    )
    
    db.add(db_incident)
    db.commit()
    db.refresh(db_incident)
    return db_incident

@app.put("/api/theft-incidents/{incident_id}/resolve", response_model=TheftIncidentResponse, tags=["Theft Analytics"])
async def resolve_theft_incident(
    incident_id: int,
    db: Session = Depends(get_session)
):
    """
    Mark a theft incident as resolved.
    """
    db_incident = db.query(TheftIncident).filter(TheftIncident.id == incident_id).first()
    if not db_incident:
        raise HTTPException(status_code=404, detail="Theft incident not found")
    
    db_incident.resolved = True
    db.commit()
    db.refresh(db_incident)
    return db_incident

# Rewards Program Endpoints
@app.get("/api/rewards", response_model=List[RewardsResponse], tags=["Rewards Analytics"])
async def get_rewards_data(
    db: Session = Depends(get_session),
    store_id: Optional[int] = Query(None, description="Filter by store ID"),
    skip: int = Query(0, description="Skip N records"),
    limit: int = Query(100, description="Limit to N records")
):
    """
    Retrieve rewards program data with optional filtering.
    """
    query = db.query(RewardsData)
    
    if store_id:
        query = query.filter(RewardsData.store_id == store_id)
    
    rewards_data = query.offset(skip).limit(limit).all()
    return rewards_data

@app.post("/api/rewards", response_model=RewardsResponse, tags=["Rewards Analytics"], status_code=201)
async def create_rewards_data(
    rewards: RewardsCreate,
    db: Session = Depends(get_session)
):
    """
    Create a new rewards program data entry.
    
    This endpoint allows you to add new rewards program data for a specific store and date.
    """
    db_rewards = RewardsData(**rewards.dict())
    db.add(db_rewards)
    db.commit()
    db.refresh(db_rewards)
    return db_rewards

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