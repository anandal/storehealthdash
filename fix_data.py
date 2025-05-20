"""
This script will populate the database with additional data 
to fix dashboard visualization issues
"""

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
from data_generator import generate_date_range
from database import get_session, Store, TheftIncident, RewardsData, CampaignPerformance, TrafficData, TrafficPattern, EmployeeData, MobileUsagePattern, BusinessHealth, save_data_to_db

def generate_enhanced_data():
    """Generate more comprehensive data for all stores"""
    # List of store names
    stores = [
        "Downtown Mart", 
        "Riverside Convenience", 
        "Oakwood Express", 
        "Sunset Shop & Go",
        "Hillside Corner Store"
    ]
    
    # Make sure we have stores in the database
    db = get_session()
    db_stores = []
    
    for store_name in stores:
        # Check if store exists first
        store = db.query(Store).filter(Store.name == store_name).first()
        if not store:
            # Create new store with additional information
            store = Store(
                name=store_name,
                address=f"{random.randint(100, 999)} {random.choice(['Main', 'Oak', 'Maple', 'River', 'Hill'])} St",
                city=random.choice(['Springfield', 'Riverside', 'Oakwood', 'Hillside', 'Maplewood']),
                state="IL",
                zip_code=f"{random.randint(60000, 62999)}",
                phone=f"555-{random.randint(100, 999)}-{random.randint(1000, 9999)}",
                manager=random.choice(['John Smith', 'Jane Doe', 'Robert Johnson', 'Emily Wilson', 'Michael Brown']),
                opening_date=datetime.now() - timedelta(days=random.randint(30, 1000))
            )
            db.add(store)
            db.commit()
            db.refresh(store)
        
        db_stores.append(store)
    
    # Generate theft incidents (more comprehensive data)
    dates = [datetime.now() - timedelta(days=i) for i in range(90)]
    
    for store in db_stores:
        # Add 20-30 theft incidents per store
        for _ in range(random.randint(20, 30)):
            # Random date within the range
            incident_date = random.choice(dates)
            
            # Random time during store hours
            hour = random.randint(6, 23)
            incident_time = incident_date.replace(hour=hour, minute=random.randint(0, 59))
            
            # Severity and value
            severity = random.choice(["Low", "Medium", "High"])
            if severity == "Low":
                value = round(random.uniform(10, 50), 2)
            elif severity == "Medium":
                value = round(random.uniform(50, 200), 2)
            else:  # High
                value = round(random.uniform(200, 1000), 2)
            
            # Resolution status - older incidents more likely to be resolved
            days_ago = (datetime.now() - incident_time).days
            resolution_prob = min(0.9, days_ago / 30)
            resolved = random.random() < resolution_prob
            
            # Create theft incident
            theft = TheftIncident(
                store_id=store.id,
                timestamp=incident_time,
                severity=severity,
                value=value,
                resolved=resolved,
                day_of_week=incident_time.strftime("%A"),
                hour=hour,
                video_clip_url=f"https://example.com/clip{random.randint(1000, 9999)}.mp4" if random.random() > 0.3 else None
            )
            db.add(theft)
        
        # Add rewards data for each day
        member_count = random.randint(500, 2000)  # Starting member count
        for date in dates:
            # New members per day (with some randomness)
            new_members = random.randint(1, 15)
            member_count += new_members
            
            # Create rewards data
            rewards = RewardsData(
                store_id=store.id,
                date=date,
                total_members=member_count,
                new_members=new_members,
                campaign_engagement=round(random.uniform(20, 80), 1),
                active_campaigns=random.randint(1, 4)
            )
            db.add(rewards)
            
            # Create business health data for each day
            health = BusinessHealth(
                store_id=store.id,
                date=date,
                overall_health=round(random.uniform(60, 95), 1),
                theft_score=round(random.uniform(50, 100), 1),
                rewards_score=round(random.uniform(60, 95), 1),
                traffic_score=round(random.uniform(65, 90), 1),
                employee_score=round(random.uniform(55, 95), 1),
                alerts=None  # No alerts for now
            )
            db.add(health)
        
        # Add campaign performance data
        for campaign in ["Summer Discount", "Coffee Club", "Weekend Deals", "Loyalty Bonus"]:
            campaign_perf = CampaignPerformance(
                store_id=store.id,
                campaign=campaign,
                participation_rate=round(random.uniform(20, 80), 1),
                redemption_rate=round(random.uniform(10, 50), 1),
                roi=round(random.uniform(1.1, 3.5), 2)
            )
            db.add(campaign_perf)
        
        # Add traffic data entries (hourly traffic for each day of week)
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        for day in days:
            for hour in range(24):
                # Traffic patterns by time of day
                if 7 <= hour <= 9:  # Morning rush
                    traffic = random.randint(40, 80)
                elif 11 <= hour <= 13:  # Lunch
                    traffic = random.randint(50, 90)
                elif 16 <= hour <= 19:  # Evening rush
                    traffic = random.randint(60, 100)
                elif 0 <= hour <= 5:  # Late night
                    traffic = random.randint(5, 20)
                else:  # Normal hours
                    traffic = random.randint(20, 50)
                
                # Weekends have different patterns
                if day in ["Saturday", "Sunday"]:
                    traffic = int(traffic * random.uniform(0.8, 1.2))
                
                # Add traffic pattern data
                traffic_pattern = TrafficPattern(
                    store_id=store.id,
                    day_of_week=day,
                    hour=hour,
                    visitor_count=traffic
                )
                db.add(traffic_pattern)
        
        # Add daily traffic data
        for date in dates:
            # Daily traffic with some randomness
            daily_traffic = random.randint(400, 1200)
            
            # Create traffic data
            traffic = TrafficData(
                store_id=store.id,
                date=date,
                total_visits=daily_traffic,
                conversion_rate=round(random.uniform(20, 40), 1),
                avg_time_spent=round(random.uniform(5, 15), 1),
                repeat_visits=int(daily_traffic * random.uniform(0.1, 0.3))
            )
            db.add(traffic)
        
        # Add employee productivity data
        for date in dates:
            employee = EmployeeData(
                store_id=store.id,
                date=date,
                total_employees=random.randint(3, 8),
                productivity_score=round(random.uniform(60, 95), 1),
                mobile_usage_minutes=random.randint(30, 120),
                register_scans_per_hour=round(random.uniform(20, 50), 1)
            )
            db.add(employee)
    
    # Commit all changes
    db.commit()
    return True

# Run this function to fix data issues
if __name__ == "__main__":
    print("Generating enhanced data...")
    success = generate_enhanced_data()
    print(f"Data generation {'successful' if success else 'failed'}")