"""
Database module for the dashboard
Handles connections to PostgreSQL and provides data access methods
"""

import os
import pandas as pd
import numpy as np
import streamlit as st
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Boolean, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime, timedelta

# Create SQLAlchemy engine and base
Base = declarative_base()

class Store(Base):
    """Store information table"""
    __tablename__ = 'stores'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    address = Column(String(255))
    city = Column(String(100))
    state = Column(String(50))
    zip_code = Column(String(20))
    phone = Column(String(20))
    manager = Column(String(100))
    opening_date = Column(DateTime)
    
    # Relationships
    theft_incidents = relationship("TheftIncident", back_populates="store")
    rewards_data = relationship("RewardsData", back_populates="store")
    traffic_data = relationship("TrafficData", back_populates="store")
    employee_data = relationship("EmployeeData", back_populates="store")
    business_health = relationship("BusinessHealth", back_populates="store")
    
    def __repr__(self):
        return f"<Store(name='{self.name}')>"

class TheftIncident(Base):
    """Theft incident table"""
    __tablename__ = 'theft_incidents'
    
    id = Column(Integer, primary_key=True)
    store_id = Column(Integer, ForeignKey('stores.id'))
    timestamp = Column(DateTime, nullable=False)
    day_of_week = Column(String(10))
    hour = Column(Integer)
    severity = Column(String(10))
    value = Column(Float)
    resolved = Column(Boolean, default=False)
    video_clip_url = Column(String(255), nullable=True)
    
    # Relationship
    store = relationship("Store", back_populates="theft_incidents")
    
    def __repr__(self):
        return f"<TheftIncident(timestamp='{self.timestamp}', store_id={self.store_id})>"

class RewardsData(Base):
    """Rewards program data table"""
    __tablename__ = 'rewards_data'
    
    id = Column(Integer, primary_key=True)
    store_id = Column(Integer, ForeignKey('stores.id'))
    date = Column(DateTime, nullable=False)
    total_members = Column(Integer)
    new_members = Column(Integer)
    campaign_engagement = Column(Float)
    active_campaigns = Column(Integer)
    
    # Relationship
    store = relationship("Store", back_populates="rewards_data")
    
    def __repr__(self):
        return f"<RewardsData(date='{self.date}', store_id={self.store_id})>"

class CampaignPerformance(Base):
    """Campaign performance data table"""
    __tablename__ = 'campaign_performance'
    
    id = Column(Integer, primary_key=True)
    store_id = Column(Integer, ForeignKey('stores.id'))
    campaign = Column(String(100))
    participation_rate = Column(Float)
    redemption_rate = Column(Float)
    roi = Column(Float)
    
    # Relationship
    store = relationship("Store")
    
    def __repr__(self):
        return f"<CampaignPerformance(campaign='{self.campaign}', store_id={self.store_id})>"

class TrafficData(Base):
    """Store traffic data table"""
    __tablename__ = 'traffic_data'
    
    id = Column(Integer, primary_key=True)
    store_id = Column(Integer, ForeignKey('stores.id'))
    date = Column(DateTime, nullable=False)
    total_visitors = Column(Integer)
    
    # Relationship
    store = relationship("Store", back_populates="traffic_data")
    
    def __repr__(self):
        return f"<TrafficData(date='{self.date}', store_id={self.store_id})>"

class TrafficPattern(Base):
    """Traffic pattern data table (for heatmaps)"""
    __tablename__ = 'traffic_patterns'
    
    id = Column(Integer, primary_key=True)
    store_id = Column(Integer, ForeignKey('stores.id'))
    day_of_week = Column(String(10))
    hour = Column(Integer)
    visitor_count = Column(Integer)
    
    # Relationship
    store = relationship("Store")
    
    def __repr__(self):
        return f"<TrafficPattern(day='{self.day_of_week}', hour={self.hour}, store_id={self.store_id})>"

class EmployeeData(Base):
    """Employee mobile usage data table"""
    __tablename__ = 'employee_data'
    
    id = Column(Integer, primary_key=True)
    store_id = Column(Integer, ForeignKey('stores.id'))
    date = Column(DateTime, nullable=False)
    shift = Column(String(50))
    mobile_usage_incidents = Column(Integer)
    avg_duration_minutes = Column(Float)
    total_usage_minutes = Column(Integer)
    
    # Relationship
    store = relationship("Store", back_populates="employee_data")
    
    def __repr__(self):
        return f"<EmployeeData(date='{self.date}', store_id={self.store_id})>"

class MobileUsagePattern(Base):
    """Mobile usage pattern data table (for heatmaps)"""
    __tablename__ = 'mobile_usage_patterns'
    
    id = Column(Integer, primary_key=True)
    store_id = Column(Integer, ForeignKey('stores.id'))
    day_of_week = Column(String(10))
    hour = Column(Integer)
    mobile_usage_incidents = Column(Integer)
    
    # Relationship
    store = relationship("Store")
    
    def __repr__(self):
        return f"<MobileUsagePattern(day='{self.day_of_week}', hour={self.hour}, store_id={self.store_id})>"

class BusinessHealth(Base):
    """Business health metrics table"""
    __tablename__ = 'business_health'
    
    id = Column(Integer, primary_key=True)
    store_id = Column(Integer, ForeignKey('stores.id'))
    date = Column(DateTime, nullable=False)
    overall_health = Column(Float)
    theft_score = Column(Float)
    rewards_score = Column(Float)
    traffic_score = Column(Float)
    employee_score = Column(Float)
    alerts = Column(Text)  # Stored as JSON string
    
    # Relationship
    store = relationship("Store", back_populates="business_health")
    
    def __repr__(self):
        return f"<BusinessHealth(date='{self.date}', store_id={self.store_id})>"

# Database connection and session management
def get_engine():
    """Get SQLAlchemy engine for database connection"""
    DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/postgres")
    return create_engine(DATABASE_URL)

def init_db():
    """Initialize database schema"""
    engine = get_engine()
    Base.metadata.create_all(engine)
    return engine

def get_session():
    """Get database session"""
    engine = get_engine()
    Session = sessionmaker(bind=engine)
    return Session()

# Data import/export functions
def save_data_to_db():
    """Save session state data to database"""
    # Initialize database if needed
    init_db()
    session = get_session()
    
    try:
        # First check if we have data in the session state
        if 'store_info' not in st.session_state:
            st.warning("No store data available to save to database")
            return False
        
        # Add stores
        for _, store_row in st.session_state.store_info.iterrows():
            store = Store(
                name=store_row['store_name'],
                address=store_row.get('address', ''),
                city=store_row.get('city', ''),
                state=store_row.get('state', ''),
                zip_code=store_row.get('zip_code', ''),
                phone=store_row.get('phone', ''),
                manager=store_row.get('manager', ''),
                opening_date=store_row.get('opening_date', datetime.now())
            )
            session.add(store)
        
        # Commit to get store IDs
        session.commit()
        
        # Get store ID mapping
        stores = {store.name: store.id for store in session.query(Store).all()}
        
        # Add theft incidents
        if 'theft_data' in st.session_state:
            for _, incident in st.session_state.theft_data.iterrows():
                store_id = stores.get(incident['store'])
                if store_id:
                    theft = TheftIncident(
                        store_id=store_id,
                        timestamp=incident['timestamp'],
                        day_of_week=incident['day_of_week'],
                        hour=incident['hour'],
                        severity=incident['severity'],
                        value=float(incident['value']),
                        resolved=bool(incident['resolved'])
                    )
                    session.add(theft)
        
        # Add rewards data
        if 'rewards_data' in st.session_state:
            for _, reward in st.session_state.rewards_data.iterrows():
                store_id = stores.get(reward['store'])
                if store_id:
                    reward_data = RewardsData(
                        store_id=store_id,
                        date=reward['date'],
                        total_members=int(reward['total_members']),
                        new_members=int(reward['new_members']),
                        campaign_engagement=float(reward['campaign_engagement']),
                        active_campaigns=int(reward['active_campaigns'])
                    )
                    session.add(reward_data)
        
        # Add campaign performance
        if 'campaign_performance' in st.session_state:
            for _, campaign in st.session_state.campaign_performance.iterrows():
                store_id = stores.get(campaign['store'])
                if store_id:
                    camp_perf = CampaignPerformance(
                        store_id=store_id,
                        campaign=campaign['campaign'],
                        participation_rate=float(campaign['participation_rate']),
                        redemption_rate=float(campaign['redemption_rate']),
                        roi=float(campaign['roi'])
                    )
                    session.add(camp_perf)
        
        # Add traffic data
        if 'daily_traffic' in st.session_state:
            for _, traffic in st.session_state.daily_traffic.iterrows():
                store_id = stores.get(traffic['store'])
                if store_id:
                    traffic_data = TrafficData(
                        store_id=store_id,
                        date=traffic['date'],
                        total_visitors=int(traffic['total_visitors'])
                    )
                    session.add(traffic_data)
        
        # Add traffic patterns
        if 'traffic_patterns' in st.session_state:
            for _, pattern in st.session_state.traffic_patterns.iterrows():
                store_id = stores.get(pattern['store'])
                if store_id:
                    traffic_pattern = TrafficPattern(
                        store_id=store_id,
                        day_of_week=pattern['day_of_week'],
                        hour=int(pattern['hour']),
                        visitor_count=int(pattern['visitor_count'])
                    )
                    session.add(traffic_pattern)
        
        # Add employee data
        if 'shift_usage_data' in st.session_state:
            for _, employee in st.session_state.shift_usage_data.iterrows():
                store_id = stores.get(employee['store'])
                if store_id:
                    emp_data = EmployeeData(
                        store_id=store_id,
                        date=employee['date'],
                        shift=employee['shift'],
                        mobile_usage_incidents=int(employee['mobile_usage_incidents']),
                        avg_duration_minutes=float(employee['avg_duration_minutes']),
                        total_usage_minutes=int(employee['total_usage_minutes'])
                    )
                    session.add(emp_data)
        
        # Add mobile usage patterns
        if 'mobile_usage_patterns' in st.session_state:
            for _, pattern in st.session_state.mobile_usage_patterns.iterrows():
                store_id = stores.get(pattern['store'])
                if store_id:
                    mobile_pattern = MobileUsagePattern(
                        store_id=store_id,
                        day_of_week=pattern['day_of_week'],
                        hour=int(pattern['hour']),
                        mobile_usage_incidents=int(pattern['mobile_usage_incidents'])
                    )
                    session.add(mobile_pattern)
        
        # Add business health
        if 'business_health' in st.session_state:
            for _, health in st.session_state.business_health.iterrows():
                store_id = stores.get(health['store'])
                if store_id:
                    # Convert alerts list to string if needed
                    alerts = str(health['alerts']) if 'alerts' in health else ''
                    
                    health_data = BusinessHealth(
                        store_id=store_id,
                        date=health['date'],
                        overall_health=float(health['overall_health']),
                        theft_score=float(health['theft_score']),
                        rewards_score=float(health['rewards_score']),
                        traffic_score=float(health['traffic_score']),
                        employee_score=float(health['employee_score']),
                        alerts=alerts
                    )
                    session.add(health_data)
        
        # Commit all changes
        session.commit()
        return True
    
    except Exception as e:
        session.rollback()
        st.error(f"Error saving data to database: {str(e)}")
        return False
    
    finally:
        session.close()

def load_data_from_db():
    """Load data from database to session state"""
    # Initialize database if needed
    init_db()
    session = get_session()
    
    try:
        # Load stores
        stores = session.query(Store).all()
        if not stores:
            return False
        
        # Create store_info dataframe
        store_data = []
        for store in stores:
            store_data.append({
                'store_name': store.name,
                'address': store.address,
                'city': store.city,
                'state': store.state,
                'zip_code': store.zip_code,
                'phone': store.phone,
                'manager': store.manager,
                'opening_date': store.opening_date
            })
        st.session_state.store_info = pd.DataFrame(store_data)
        
        # Load theft incidents
        theft_data = []
        for incident in session.query(TheftIncident).all():
            store = session.query(Store).filter_by(id=incident.store_id).first()
            theft_data.append({
                'store': store.name,
                'timestamp': incident.timestamp,
                'day_of_week': incident.day_of_week,
                'hour': incident.hour,
                'severity': incident.severity,
                'value': incident.value,
                'resolved': incident.resolved
            })
        if theft_data:
            st.session_state.theft_data = pd.DataFrame(theft_data)
        
        # Load rewards data
        rewards_data = []
        for reward in session.query(RewardsData).all():
            store = session.query(Store).filter_by(id=reward.store_id).first()
            rewards_data.append({
                'store': store.name,
                'date': reward.date,
                'total_members': reward.total_members,
                'new_members': reward.new_members,
                'campaign_engagement': reward.campaign_engagement,
                'active_campaigns': reward.active_campaigns
            })
        if rewards_data:
            st.session_state.rewards_data = pd.DataFrame(rewards_data)
        
        # Load campaign performance
        campaign_data = []
        for campaign in session.query(CampaignPerformance).all():
            store = session.query(Store).filter_by(id=campaign.store_id).first()
            campaign_data.append({
                'store': store.name,
                'campaign': campaign.campaign,
                'participation_rate': campaign.participation_rate,
                'redemption_rate': campaign.redemption_rate,
                'roi': campaign.roi
            })
        if campaign_data:
            st.session_state.campaign_performance = pd.DataFrame(campaign_data)
        
        # Load traffic data
        traffic_data = []
        for traffic in session.query(TrafficData).all():
            store = session.query(Store).filter_by(id=traffic.store_id).first()
            traffic_data.append({
                'store': store.name,
                'date': traffic.date,
                'total_visitors': traffic.total_visitors
            })
        if traffic_data:
            st.session_state.daily_traffic = pd.DataFrame(traffic_data)
        
        # Load traffic patterns
        pattern_data = []
        for pattern in session.query(TrafficPattern).all():
            store = session.query(Store).filter_by(id=pattern.store_id).first()
            pattern_data.append({
                'store': store.name,
                'day_of_week': pattern.day_of_week,
                'hour': pattern.hour,
                'visitor_count': pattern.visitor_count
            })
        if pattern_data:
            st.session_state.traffic_patterns = pd.DataFrame(pattern_data)
        
        # Load employee data
        employee_data = []
        for employee in session.query(EmployeeData).all():
            store = session.query(Store).filter_by(id=employee.store_id).first()
            employee_data.append({
                'store': store.name,
                'date': employee.date,
                'shift': employee.shift,
                'mobile_usage_incidents': employee.mobile_usage_incidents,
                'avg_duration_minutes': employee.avg_duration_minutes,
                'total_usage_minutes': employee.total_usage_minutes
            })
        if employee_data:
            st.session_state.shift_usage_data = pd.DataFrame(employee_data)
        
        # Load mobile usage patterns
        mobile_pattern_data = []
        for pattern in session.query(MobileUsagePattern).all():
            store = session.query(Store).filter_by(id=pattern.store_id).first()
            mobile_pattern_data.append({
                'store': store.name,
                'day_of_week': pattern.day_of_week,
                'hour': pattern.hour,
                'mobile_usage_incidents': pattern.mobile_usage_incidents
            })
        if mobile_pattern_data:
            st.session_state.mobile_usage_patterns = pd.DataFrame(mobile_pattern_data)
        
        # Load business health
        health_data = []
        for health in session.query(BusinessHealth).all():
            store = session.query(Store).filter_by(id=health.store_id).first()
            # Convert alerts string back to list if needed
            alerts = eval(health.alerts) if health.alerts else []
            
            health_data.append({
                'store': store.name,
                'date': health.date,
                'overall_health': health.overall_health,
                'theft_score': health.theft_score,
                'rewards_score': health.rewards_score,
                'traffic_score': health.traffic_score,
                'employee_score': health.employee_score,
                'alerts': alerts
            })
        if health_data:
            st.session_state.business_health = pd.DataFrame(health_data)
        
        return True
    
    except Exception as e:
        st.error(f"Error loading data from database: {str(e)}")
        return False
    
    finally:
        session.close()