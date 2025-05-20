"""
SceneIQ API - RESTful API implementation with Swagger UI
This module provides API endpoints for managing stores, rewards, theft incidents, users, and more.
"""

from fastapi import FastAPI, Depends, HTTPException, status, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, validator
from datetime import datetime, date, timedelta
import uvicorn
import json
from database import get_session, Store, TheftIncident, RewardsData, CampaignPerformance

# Create FastAPI app
app = FastAPI(
    title="SceneIQ API",
    description="API for managing convenience store analytics data",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, restrict to specific domains
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

    model_config = {
        "json_schema_extra": {
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
    }

class StoreCreate(StoreBase):
    pass

class StoreResponse(StoreBase):
    id: int
    
    model_config = {
        "from_attributes": True
    }

class TheftIncidentBase(BaseModel):
    store_id: int
    timestamp: datetime
    severity: str
    value: float
    resolved: bool = False
    video_clip_url: Optional[str] = None

    model_config = {
        "json_schema_extra": {
            "example": {
                "store_id": 1,
                "timestamp": "2025-05-18T14:32:15",
                "severity": "Medium",
                "value": 125.50,
                "resolved": False,
                "video_clip_url": "https://example.com/clip1.mp4"
            }
        }
    }

    @field_validator('severity')
    @classmethod
    def validate_severity(cls, v):
        if v not in ["Low", "Medium", "High"]:
            raise ValueError('Severity must be one of "Low", "Medium", or "High"')
        return v

class TheftIncidentCreate(TheftIncidentBase):
    pass

class TheftIncidentResponse(TheftIncidentBase):
    id: int
    day_of_week: str
    hour: int
    
    model_config = {
        "from_attributes": True
    }

class RewardsBase(BaseModel):
    store_id: int
    date: date
    total_members: int
    new_members: int
    campaign_engagement: float
    active_campaigns: int

    model_config = {
        "json_schema_extra": {
            "example": {
                "store_id": 1,
                "date": "2025-05-01",
                "total_members": 1250,
                "new_members": 25,
                "campaign_engagement": 45.8,
                "active_campaigns": 3
            }
        }
    }

class RewardsCreate(RewardsBase):
    pass

class RewardsResponse(RewardsBase):
    id: int
    
    model_config = {
        "from_attributes": True
    }

class CampaignBase(BaseModel):
    store_id: int
    campaign: str
    participation_rate: float
    redemption_rate: float
    roi: float

    model_config = {
        "json_schema_extra": {
            "example": {
                "store_id": 1,
                "campaign": "Summer Discount",
                "participation_rate": 35.5,
                "redemption_rate": 22.8,
                "roi": 2.5
            }
        }
    }

class CampaignCreate(CampaignBase):
    pass

class CampaignResponse(CampaignBase):
    id: int
    
    model_config = {
        "from_attributes": True
    }

class UserBase(BaseModel):
    username: str
    email: str
    full_name: str
    role: str
    store_id: Optional[int] = None

    model_config = {
        "json_schema_extra": {
            "example": {
                "username": "jsmith",
                "email": "jsmith@example.com",
                "full_name": "John Smith",
                "role": "Manager",
                "store_id": 1
            }
        }
    }

    @field_validator('role')
    @classmethod
    def validate_role(cls, v):
        if v not in ["Owner", "Manager", "Staff"]:
            raise ValueError('Role must be one of "Owner", "Manager", or "Staff"')
        return v

class UserCreate(UserBase):
    password: str

    model_config = {
        "json_schema_extra": {
            "example": {
                "username": "jsmith",
                "email": "jsmith@example.com",
                "full_name": "John Smith",
                "role": "Manager",
                "store_id": 1,
                "password": "securepassword"
            }
        }
    }

class UserResponse(UserBase):
    id: int
    created_at: datetime
    
    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "id": 1,
                "username": "jsmith",
                "email": "jsmith@example.com",
                "full_name": "John Smith",
                "role": "Manager",
                "store_id": 1,
                "created_at": "2025-05-01T10:00:00"
            }
        }
    }

class LoginRequest(BaseModel):
    username: str
    password: str

    model_config = {
        "json_schema_extra": {
            "example": {
                "username": "jsmith",
                "password": "securepassword"
            }
        }
    }

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

    model_config = {
        "json_schema_extra": {
            "example": {
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "token_type": "bearer"
            }
        }
    }

class BusinessHealthBase(BaseModel):
    store_id: int
    date: date
    overall_health: float
    theft_score: float
    rewards_score: float
    traffic_score: float
    employee_score: float
    alerts: Optional[str] = None

    model_config = {
        "json_schema_extra": {
            "example": {
                "store_id": 1,
                "date": "2025-05-01",
                "overall_health": 85.5,
                "theft_score": 75.0,
                "rewards_score": 90.5,
                "traffic_score": 82.3,
                "employee_score": 78.9,
                "alerts": '{"alert1": "Low stock on item X", "alert2": "High theft rate"}'
            }
        }
    }

class BusinessHealthCreate(BusinessHealthBase):
    pass

class BusinessHealthResponse(BusinessHealthBase):
    id: int
    
    model_config = {
        "from_attributes": True
    }

# API Endpoints
@app.get("/", response_class=JSONResponse)
async def root():
    """Root endpoint that provides API information"""
    return {
        "name": "SceneIQ API",
        "version": "1.0.0",
        "description": "API for managing convenience store analytics data",
        "documentation": "/api/docs"
    }

# Store Endpoints
@app.get("/api/stores", response_model=List[StoreResponse], tags=["Stores"], summary="Get all stores")
async def get_stores(
    db: Session = Depends(get_session),
    skip: int = Query(0, description="Skip N records"),
    limit: int = Query(100, description="Limit to N records")
):
    """
    Retrieve a list of all stores.
    
    - **skip**: Number of records to skip (pagination)
    - **limit**: Maximum number of records to return (pagination)
    """
    stores = db.query(Store).offset(skip).limit(limit).all()
    return stores

@app.get("/api/stores/{store_id}", response_model=StoreResponse, tags=["Stores"], summary="Get store by ID")
async def get_store(
    store_id: int = Path(..., description="The ID of the store to retrieve"),
    db: Session = Depends(get_session)
):
    """
    Retrieve a specific store by its ID.
    
    - **store_id**: The unique identifier of the store
    """
    store = db.query(Store).filter(Store.id == store_id).first()
    if not store:
        raise HTTPException(status_code=404, detail="Store not found")
    return store

@app.post("/api/stores", response_model=StoreResponse, status_code=status.HTTP_201_CREATED, tags=["Stores"], summary="Create a new store")
async def create_store(
    store: StoreCreate,
    db: Session = Depends(get_session)
):
    """
    Create a new store.
    
    - **store**: Store information to create
    """
    db_store = Store(**store.dict())
    db.add(db_store)
    db.commit()
    db.refresh(db_store)
    return db_store

@app.put("/api/stores/{store_id}", response_model=StoreResponse, tags=["Stores"], summary="Update a store")
async def update_store(
    store_id: int = Path(..., description="The ID of the store to update"),
    store: StoreBase = None,
    db: Session = Depends(get_session)
):
    """
    Update a store's information.
    
    - **store_id**: The unique identifier of the store to update
    - **store**: Updated store information
    """
    db_store = db.query(Store).filter(Store.id == store_id).first()
    if not db_store:
        raise HTTPException(status_code=404, detail="Store not found")
    
    for key, value in store.dict().items():
        setattr(db_store, key, value)
    
    db.commit()
    db.refresh(db_store)
    return db_store

@app.delete("/api/stores/{store_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Stores"], summary="Delete a store")
async def delete_store(
    store_id: int = Path(..., description="The ID of the store to delete"),
    db: Session = Depends(get_session)
):
    """
    Delete a store.
    
    - **store_id**: The unique identifier of the store to delete
    """
    db_store = db.query(Store).filter(Store.id == store_id).first()
    if not db_store:
        raise HTTPException(status_code=404, detail="Store not found")
    
    db.delete(db_store)
    db.commit()
    return None

# Theft Incident Endpoints
@app.get("/api/theft-incidents", response_model=List[TheftIncidentResponse], tags=["Theft Analytics"], summary="Get all theft incidents")
async def get_theft_incidents(
    db: Session = Depends(get_session),
    store_id: Optional[int] = Query(None, description="Filter by store ID"),
    start_date: Optional[date] = Query(None, description="Filter by start date"),
    end_date: Optional[date] = Query(None, description="Filter by end date"),
    severity: Optional[str] = Query(None, description="Filter by severity (Low, Medium, High)"),
    resolved: Optional[bool] = Query(None, description="Filter by resolution status"),
    skip: int = Query(0, description="Skip N records"),
    limit: int = Query(100, description="Limit to N records")
):
    """
    Retrieve a list of theft incidents with optional filtering.
    
    - **store_id**: Filter by store ID
    - **start_date**: Filter by incidents on or after this date
    - **end_date**: Filter by incidents on or before this date
    - **severity**: Filter by incident severity
    - **resolved**: Filter by resolved status
    - **skip**: Number of records to skip (pagination)
    - **limit**: Maximum number of records to return (pagination)
    """
    query = db.query(TheftIncident)
    
    if store_id:
        query = query.filter(TheftIncident.store_id == store_id)
    if start_date:
        query = query.filter(TheftIncident.timestamp >= start_date)
    if end_date:
        query = query.filter(TheftIncident.timestamp <= end_date)
    if severity:
        query = query.filter(TheftIncident.severity == severity)
    if resolved is not None:
        query = query.filter(TheftIncident.resolved == resolved)
    
    incidents = query.offset(skip).limit(limit).all()
    return incidents

@app.post("/api/theft-incidents", response_model=TheftIncidentResponse, status_code=status.HTTP_201_CREATED, tags=["Theft Analytics"], summary="Create a new theft incident")
async def create_theft_incident(
    incident: TheftIncidentCreate,
    db: Session = Depends(get_session)
):
    """
    Create a new theft incident.
    
    - **incident**: Theft incident information to create
    """
    # Extract day of week and hour from timestamp
    day_of_week = incident.timestamp.strftime("%A")
    hour = incident.timestamp.hour
    
    db_incident = TheftIncident(
        **incident.dict(),
        day_of_week=day_of_week,
        hour=hour
    )
    
    db.add(db_incident)
    db.commit()
    db.refresh(db_incident)
    return db_incident

@app.put("/api/theft-incidents/{incident_id}/resolve", response_model=TheftIncidentResponse, tags=["Theft Analytics"], summary="Mark a theft incident as resolved")
async def resolve_theft_incident(
    incident_id: int = Path(..., description="The ID of the incident to resolve"),
    db: Session = Depends(get_session)
):
    """
    Mark a theft incident as resolved.
    
    - **incident_id**: The unique identifier of the incident to resolve
    """
    db_incident = db.query(TheftIncident).filter(TheftIncident.id == incident_id).first()
    if not db_incident:
        raise HTTPException(status_code=404, detail="Theft incident not found")
    
    db_incident.resolved = True
    db.commit()
    db.refresh(db_incident)
    return db_incident

# Rewards Program Endpoints
@app.get("/api/rewards", response_model=List[RewardsResponse], tags=["Rewards Analytics"], summary="Get rewards program data")
async def get_rewards_data(
    db: Session = Depends(get_session),
    store_id: Optional[int] = Query(None, description="Filter by store ID"),
    start_date: Optional[date] = Query(None, description="Filter by start date"),
    end_date: Optional[date] = Query(None, description="Filter by end date"),
    skip: int = Query(0, description="Skip N records"),
    limit: int = Query(100, description="Limit to N records")
):
    """
    Retrieve rewards program data with optional filtering.
    
    - **store_id**: Filter by store ID
    - **start_date**: Filter by data on or after this date
    - **end_date**: Filter by data on or before this date
    - **skip**: Number of records to skip (pagination)
    - **limit**: Maximum number of records to return (pagination)
    """
    query = db.query(RewardsData)
    
    if store_id:
        query = query.filter(RewardsData.store_id == store_id)
    if start_date:
        query = query.filter(RewardsData.date >= start_date)
    if end_date:
        query = query.filter(RewardsData.date <= end_date)
    
    rewards_data = query.offset(skip).limit(limit).all()
    return rewards_data

@app.post("/api/rewards", response_model=RewardsResponse, status_code=status.HTTP_201_CREATED, tags=["Rewards Analytics"], summary="Create rewards program data entry")
async def create_rewards_data(
    rewards: RewardsCreate,
    db: Session = Depends(get_session)
):
    """
    Create a new rewards program data entry.
    
    - **rewards**: Rewards program data to create
    """
    db_rewards = RewardsData(**rewards.dict())
    db.add(db_rewards)
    db.commit()
    db.refresh(db_rewards)
    return db_rewards

@app.get("/api/campaigns", response_model=List[CampaignResponse], tags=["Rewards Analytics"], summary="Get campaign performance data")
async def get_campaign_data(
    db: Session = Depends(get_session),
    store_id: Optional[int] = Query(None, description="Filter by store ID"),
    campaign: Optional[str] = Query(None, description="Filter by campaign name"),
    skip: int = Query(0, description="Skip N records"),
    limit: int = Query(100, description="Limit to N records")
):
    """
    Retrieve campaign performance data with optional filtering.
    
    - **store_id**: Filter by store ID
    - **campaign**: Filter by campaign name
    - **skip**: Number of records to skip (pagination)
    - **limit**: Maximum number of records to return (pagination)
    """
    query = db.query(CampaignPerformance)
    
    if store_id:
        query = query.filter(CampaignPerformance.store_id == store_id)
    if campaign:
        query = query.filter(CampaignPerformance.campaign == campaign)
    
    campaign_data = query.offset(skip).limit(limit).all()
    return campaign_data

@app.post("/api/campaigns", response_model=CampaignResponse, status_code=status.HTTP_201_CREATED, tags=["Rewards Analytics"], summary="Create campaign performance data entry")
async def create_campaign_data(
    campaign: CampaignCreate,
    db: Session = Depends(get_session)
):
    """
    Create a new campaign performance data entry.
    
    - **campaign**: Campaign performance data to create
    """
    db_campaign = CampaignPerformance(**campaign.dict())
    db.add(db_campaign)
    db.commit()
    db.refresh(db_campaign)
    return db_campaign

# Business Health Endpoints
@app.get("/api/business-health", response_model=List[BusinessHealthResponse], tags=["Business Health"], summary="Get business health data")
async def get_business_health(
    db: Session = Depends(get_session),
    store_id: Optional[int] = Query(None, description="Filter by store ID"),
    start_date: Optional[date] = Query(None, description="Filter by start date"),
    end_date: Optional[date] = Query(None, description="Filter by end date"),
    skip: int = Query(0, description="Skip N records"),
    limit: int = Query(100, description="Limit to N records")
):
    """
    Retrieve business health data with optional filtering.
    
    - **store_id**: Filter by store ID
    - **start_date**: Filter by data on or after this date
    - **end_date**: Filter by data on or before this date
    - **skip**: Number of records to skip (pagination)
    - **limit**: Maximum number of records to return (pagination)
    """
    query = db.query(BusinessHealth)
    
    if store_id:
        query = query.filter(BusinessHealth.store_id == store_id)
    if start_date:
        query = query.filter(BusinessHealth.date >= start_date)
    if end_date:
        query = query.filter(BusinessHealth.date <= end_date)
    
    health_data = query.offset(skip).limit(limit).all()
    return health_data

@app.post("/api/business-health", response_model=BusinessHealthResponse, status_code=status.HTTP_201_CREATED, tags=["Business Health"], summary="Create business health data entry")
async def create_business_health(
    health: BusinessHealthCreate,
    db: Session = Depends(get_session)
):
    """
    Create a new business health data entry.
    
    - **health**: Business health data to create
    """
    db_health = BusinessHealth(**health.dict())
    db.add(db_health)
    db.commit()
    db.refresh(db_health)
    return db_health

# Dashboard Data Summary Endpoint
@app.get("/api/dashboard/summary", tags=["Dashboard"], summary="Get dashboard summary data")
async def get_dashboard_summary(
    store_id: Optional[int] = Query(None, description="Filter by store ID"),
    days: int = Query(30, description="Number of days to include in the summary"),
    db: Session = Depends(get_session)
):
    """
    Retrieve a summary of dashboard data for the specified period.
    This endpoint aggregates data from various sources for dashboard display.
    
    - **store_id**: Filter by store ID (optional)
    - **days**: Number of days to include in the summary (defaults to 30)
    """
    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=days)
    
    # Define the base queries
    theft_query = db.query(TheftIncident).filter(TheftIncident.timestamp >= start_date)
    rewards_query = db.query(RewardsData).filter(RewardsData.date >= start_date)
    health_query = db.query(BusinessHealth).filter(BusinessHealth.date >= start_date)
    
    # Apply store filter if provided
    if store_id:
        theft_query = theft_query.filter(TheftIncident.store_id == store_id)
        rewards_query = rewards_query.filter(RewardsData.store_id == store_id)
        health_query = health_query.filter(BusinessHealth.store_id == store_id)
    
    # Execute queries
    theft_incidents = theft_query.all()
    rewards_data = rewards_query.all()
    health_data = health_query.all()
    
    # Calculate summary metrics
    total_theft_incidents = len(theft_incidents)
    resolved_incidents = sum(1 for incident in theft_incidents if incident.resolved)
    resolution_rate = (resolved_incidents / total_theft_incidents * 100) if total_theft_incidents > 0 else 0
    
    latest_health = None
    if health_data:
        latest_health = sorted(health_data, key=lambda x: x.date)[-1]
    
    total_members = 0
    new_members = 0
    if rewards_data:
        latest_rewards = sorted(rewards_data, key=lambda x: x.date)[-1]
        total_members = latest_rewards.total_members
        new_members = sum(data.new_members for data in rewards_data)
    
    # Build the summary response
    summary = {
        "time_period": {
            "start_date": start_date.isoformat(),
            "end_date": end_date.isoformat(),
            "days": days
        },
        "theft_analytics": {
            "total_incidents": total_theft_incidents,
            "resolved_incidents": resolved_incidents,
            "resolution_rate": resolution_rate
        },
        "rewards_program": {
            "total_members": total_members,
            "new_members": new_members
        },
        "business_health": {
            "latest_overall_health": latest_health.overall_health if latest_health else None,
            "latest_theft_score": latest_health.theft_score if latest_health else None,
            "latest_rewards_score": latest_health.rewards_score if latest_health else None,
            "latest_traffic_score": latest_health.traffic_score if latest_health else None,
            "latest_employee_score": latest_health.employee_score if latest_health else None
        }
    }
    
    return summary

# User Management Endpoints (simplified without actual auth implementation)
@app.post("/api/users", response_model=UserResponse, status_code=status.HTTP_201_CREATED, tags=["User Management"], summary="Create a new user")
async def create_user(user: UserCreate):
    """
    Create a new user.
    
    - **user**: User information to create
    
    Note: In a real implementation, you would hash the password and store it securely.
    """
    # This is a simplified mock implementation
    # In a real application, you would hash the password and store in the database
    user_dict = user.dict()
    password = user_dict.pop("password")  # Don't include the password in the response
    
    # Mock user creation
    user_response = UserResponse(
        id=999,  # Mock ID
        created_at=datetime.now(),
        **user_dict
    )
    
    return user_response

@app.post("/api/login", response_model=TokenResponse, tags=["User Management"], summary="User login")
async def login(login_request: LoginRequest):
    """
    User login endpoint.
    
    - **login_request**: Login credentials
    
    Returns a JWT token for authentication if credentials are valid.
    """
    # This is a simplified mock implementation
    # In a real application, you would validate credentials against the database
    
    # Mock token response
    return TokenResponse(
        access_token="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c",
        token_type="bearer"
    )

# Start the server when run directly
if __name__ == "__main__":
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)