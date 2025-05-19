"""
This module handles the generation of structured data for our dashboard.
It's responsible for creating consistent datasets for each analytics module.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import streamlit as st

def generate_demo_data():
    """Generate all necessary data for the dashboard"""
    # List of store names
    stores = [
        "Downtown Mart", 
        "Riverside Convenience", 
        "Oakwood Express", 
        "Sunset Shop & Go",
        "Hillside Corner Store"
    ]
    
    # Generate data for each module
    try:
        generate_theft_data(stores)
        generate_rewards_data(stores)
        generate_traffic_data(stores)
        generate_employee_data(stores)
        generate_business_health_data(stores)
        
        # Store information for each store
        generate_store_info(stores)
    except Exception as e:
        st.error(f"Error generating demo data: {str(e)}")
        import traceback
        st.error(traceback.format_exc())

def generate_date_range(days=60):
    """Generate a date range for the past number of days"""
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    return pd.date_range(start=start_date, end=end_date, freq='h')

def generate_theft_data(stores):
    """Generate theft incident data for all stores"""
    date_range = generate_date_range()
    
    # Create an empty list to store records
    theft_records = []
    
    # For each store, generate varying numbers of theft incidents
    for store in stores:
        # Number of incidents varies by store
        store_factor = 0.5 if "Downtown" in store else 0.3 if "Riverside" in store else 0.2
        
        # Generate random timestamps for incidents
        for _ in range(int(len(date_range) * store_factor * 0.03)):
            # Select a random timestamp
            timestamp = pd.Timestamp(np.random.choice(date_range))
            
            # Higher probability during specific hours (e.g., evening)
            if 17 <= timestamp.hour <= 22:
                if np.random.random() < 0.7:  # 70% more likely during evening
                    severity = np.random.choice(["Low", "Medium", "High"], 
                                               p=[0.4, 0.4, 0.2])
                    value = np.random.randint(5, 100)
                    
                    theft_records.append({
                        "store": store,
                        "timestamp": timestamp,
                        "day_of_week": timestamp.day_name(),
                        "hour": timestamp.hour,
                        "severity": severity,
                        "value": value,
                        "resolved": np.random.choice([True, False], p=[0.7, 0.3])
                    })
    
    # Create DataFrame
    theft_data = pd.DataFrame(theft_records)
    
    # Store in session state
    st.session_state.theft_data = theft_data

def generate_rewards_data(stores):
    """Generate rewards program data for all stores"""
    date_range = generate_date_range()
    
    # Generate member data
    members_records = []
    
    # Starting member counts by store
    base_members = {
        "Downtown Mart": 2500, 
        "Riverside Convenience": 1800, 
        "Oakwood Express": 1500, 
        "Sunset Shop & Go": 900,
        "Hillside Corner Store": 600
    }
    
    # Get start and end dates as datetime objects
    start_date = datetime.now() - timedelta(days=60)
    end_date = datetime.now()
    
    # Daily growth rate varies by store
    for store in stores:
        members = base_members.get(store, 1000)
        
        # Specific campaigns
        campaigns = [
            {"name": "Double Points Weekend", "start": start_date + timedelta(days=10), "end": start_date + timedelta(days=12), "engagement": 0.4},
            {"name": "Free Coffee Month", "start": start_date + timedelta(days=20), "end": start_date + timedelta(days=50), "engagement": 0.6},
            {"name": "Summer Savings", "start": start_date + timedelta(days=40), "end": end_date, "engagement": 0.5}
        ]
        
        # Generate daily member and campaign data
        for date in pd.date_range(start_date.date(), end_date.date()):
            # Growth rate varies by store and has some randomness
            growth_rate = np.random.normal(0.005, 0.002) if "Downtown" in store or "Riverside" in store else np.random.normal(0.003, 0.001)
            new_members = int(members * growth_rate)
            members += new_members
            
            # Check if any campaigns are active
            active_campaigns = [c for c in campaigns if c["start"].date() <= date.date() <= c["end"].date()]
            campaign_engagement = sum(c["engagement"] for c in active_campaigns) if active_campaigns else 0
            
            members_records.append({
                "store": store,
                "date": date,
                "total_members": int(members),
                "new_members": new_members,
                "campaign_engagement": campaign_engagement,
                "active_campaigns": len(active_campaigns)
            })
    
    # Create DataFrame
    rewards_data = pd.DataFrame(members_records)
    
    # Create campaign performance data
    campaign_data = []
    for store in stores:
        for campaign in ["Double Points Weekend", "Free Coffee Month", "Summer Savings", "Birthday Rewards"]:
            participation = np.random.uniform(20, 80)
            redemption = participation * np.random.uniform(0.3, 0.8)
            campaign_data.append({
                "store": store,
                "campaign": campaign,
                "participation_rate": participation,
                "redemption_rate": redemption,
                "roi": np.random.uniform(1.1, 3.5)
            })
    
    campaign_performance = pd.DataFrame(campaign_data)
    
    # Store in session state
    st.session_state.rewards_data = rewards_data
    st.session_state.campaign_performance = campaign_performance

def generate_traffic_data(stores):
    """Generate store visit and traffic data for all stores"""
    hours = range(24)
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    
    # Create traffic patterns data (for heatmaps)
    traffic_patterns = []
    
    for store in stores:
        # Different traffic patterns for different stores
        is_busy_store = "Downtown" in store or "Riverside" in store
        
        # Generate hourly traffic for each day of week
        for day in days:
            for hour in hours:
                # Base traffic by time of day - morning and evening peaks
                if 7 <= hour <= 9:  # Morning rush
                    base_traffic = np.random.normal(70, 15) if is_busy_store else np.random.normal(40, 10)
                elif 11 <= hour <= 13:  # Lunch
                    base_traffic = np.random.normal(60, 10) if is_busy_store else np.random.normal(35, 8)
                elif 16 <= hour <= 19:  # Evening rush
                    base_traffic = np.random.normal(80, 20) if is_busy_store else np.random.normal(50, 15)
                elif 20 <= hour <= 22:  # Evening
                    base_traffic = np.random.normal(40, 10) if is_busy_store else np.random.normal(30, 8)
                elif 0 <= hour <= 5:  # Late night/early morning
                    base_traffic = np.random.normal(15, 5) if is_busy_store else np.random.normal(8, 3)
                else:  # Other times
                    base_traffic = np.random.normal(30, 8) if is_busy_store else np.random.normal(20, 5)
                
                # Weekend vs. weekday adjustment
                is_weekend = day in ["Saturday", "Sunday"]
                if is_weekend:
                    if 9 <= hour <= 18:  # Daytime weekend
                        base_traffic *= 1.3
                    elif hour >= 21 or hour <= 2:  # Late night weekend
                        base_traffic *= 1.5
                
                traffic_patterns.append({
                    "store": store,
                    "day_of_week": day,
                    "hour": hour,
                    "visitor_count": max(int(base_traffic), 0)  # Ensure no negative values
                })
    
    # Convert to DataFrame
    traffic_data = pd.DataFrame(traffic_patterns)
    
    # Also generate daily traffic data for trend lines
    date_range = pd.date_range(datetime.now() - timedelta(days=60), datetime.now())
    daily_traffic = []
    
    for store in stores:
        is_busy_store = "Downtown" in store or "Riverside" in store
        base_visitors = 650 if is_busy_store else 350
        
        for date in date_range:
            # Weekend boost
            is_weekend = date.weekday() >= 5
            day_factor = 1.3 if is_weekend else 1.0
            
            # Add some seasonality and trends
            seasonal_factor = 1 + 0.2 * np.sin(date.dayofyear / 365 * 2 * np.pi)
            trend_factor = 1 + 0.001 * (date - date_range[0]).days  # Slight upward trend
            
            # Random variations
            random_factor = np.random.normal(1, 0.1)
            
            visitors = int(base_visitors * day_factor * seasonal_factor * trend_factor * random_factor)
            
            daily_traffic.append({
                "store": store,
                "date": date,
                "total_visitors": max(visitors, 0)  # Ensure no negative values
            })
    
    daily_traffic_data = pd.DataFrame(daily_traffic)
    
    # Store in session state
    st.session_state.traffic_patterns = traffic_data
    st.session_state.daily_traffic = daily_traffic_data

def generate_employee_data(stores):
    """Generate employee productivity and mobile phone usage data"""
    hours = range(24)
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    
    # Create mobile usage patterns data (for heatmaps)
    mobile_usage = []
    
    for store in stores:
        # Different staffing and compliance levels for different stores
        high_compliance = "Oakwood" in store or "Sunset" in store
        
        # Generate hourly mobile usage for each day of week
        for day in days:
            for hour in hours:
                # Base mobile usage by time of day
                if 0 <= hour <= 5:  # Very early morning - lower staffing, possibly more usage
                    base_usage = np.random.normal(4, 2) if high_compliance else np.random.normal(8, 3)
                elif 11 <= hour <= 14 or 17 <= hour <= 20:  # Lunch and dinner - busier, less time for phones
                    base_usage = np.random.normal(2, 1) if high_compliance else np.random.normal(5, 2)
                else:  # Other times
                    base_usage = np.random.normal(3, 1.5) if high_compliance else np.random.normal(6, 2.5)
                
                # Weekend adjustment - generally busier with more staff
                is_weekend = day in ["Saturday", "Sunday"]
                if is_weekend:
                    base_usage *= 0.8  # Less usage due to being busier
                
                mobile_usage.append({
                    "store": store,
                    "day_of_week": day,
                    "hour": hour,
                    "mobile_usage_incidents": max(int(base_usage), 0)  # Ensure no negative values
                })
    
    # Convert to DataFrame
    mobile_usage_data = pd.DataFrame(mobile_usage)
    
    # Generate shift-based data for deeper analysis
    date_range = pd.date_range(datetime.now() - timedelta(days=60), datetime.now())
    shifts = ["Morning (6AM-2PM)", "Afternoon (2PM-10PM)", "Night (10PM-6AM)"]
    
    shift_data = []
    
    for store in stores:
        high_compliance = "Oakwood" in store or "Sunset" in store
        
        for date in date_range:
            for shift in shifts:
                # Base incidents vary by shift
                if "Morning" in shift:
                    base_incidents = np.random.normal(12, 4) if high_compliance else np.random.normal(20, 6)
                elif "Afternoon" in shift:
                    base_incidents = np.random.normal(15, 5) if high_compliance else np.random.normal(25, 8)
                else:  # Night shift
                    base_incidents = np.random.normal(8, 3) if high_compliance else np.random.normal(18, 5)
                
                # Weekend adjustment
                is_weekend = date.weekday() >= 5
                if is_weekend:
                    base_incidents *= 0.8  # Less usage on weekends
                
                # Total duration of usage
                avg_duration = np.random.normal(1.5, 0.5) if high_compliance else np.random.normal(2.5, 0.8)
                
                shift_data.append({
                    "store": store,
                    "date": date,
                    "shift": shift,
                    "mobile_usage_incidents": max(int(base_incidents), 0),
                    "avg_duration_minutes": max(avg_duration, 0.5),
                    "total_usage_minutes": max(int(base_incidents * avg_duration), 0)
                })
    
    shift_usage_data = pd.DataFrame(shift_data)
    
    # Store in session state
    st.session_state.mobile_usage_patterns = mobile_usage_data
    st.session_state.shift_usage_data = shift_usage_data

def generate_business_health_data(stores):
    """Generate overall business health data"""
    date_range = pd.date_range(datetime.now() - timedelta(days=60), datetime.now())
    
    # Create business health metrics
    health_data = []
    
    for store in stores:
        # Base metrics vary by store
        if "Downtown" in store:
            base_health = 85  # Generally high-performing store
        elif "Riverside" in store:
            base_health = 75  # Good performance
        elif "Oakwood" in store:
            base_health = 70  # Average performance
        elif "Sunset" in store:
            base_health = 65  # Below average
        else:
            base_health = 60  # Struggling store
        
        for date in date_range:
            # Add some trends and variations
            seasonal_factor = 1 + 0.05 * np.sin(date.dayofyear / 365 * 2 * np.pi)
            trend_factor = 1 + 0.0005 * (date - date_range[0]).days  # Slight improvement trend
            
            # Random daily variation
            random_factor = np.random.normal(1, 0.05)
            
            # Calculate scores for each key metric
            theft_score = np.random.normal(base_health, 10) * seasonal_factor * random_factor
            rewards_score = np.random.normal(base_health + 5, 8) * seasonal_factor * trend_factor * random_factor
            traffic_score = np.random.normal(base_health - 2, 9) * seasonal_factor * trend_factor * random_factor
            employee_score = np.random.normal(base_health + 3, 7) * random_factor
            
            # Overall health score is weighted average
            overall_score = (
                0.25 * theft_score + 
                0.25 * rewards_score + 
                0.3 * traffic_score + 
                0.2 * employee_score
            )
            
            # Create alert if any metric is very low
            alerts = []
            if theft_score < 50:
                alerts.append("High theft incidents")
            if rewards_score < 50:
                alerts.append("Low rewards program performance")
            if traffic_score < 40:
                alerts.append("Concerning drop in store traffic")
            if employee_score < 45:
                alerts.append("Excessive employee mobile usage")
            
            health_data.append({
                "store": store,
                "date": date,
                "overall_health": min(max(overall_score, 0), 100),  # Clamp between 0-100
                "theft_score": min(max(theft_score, 0), 100),
                "rewards_score": min(max(rewards_score, 0), 100),
                "traffic_score": min(max(traffic_score, 0), 100),
                "employee_score": min(max(employee_score, 0), 100),
                "alerts": alerts
            })
    
    # Convert to DataFrame
    business_health = pd.DataFrame(health_data)
    
    # Store in session state
    st.session_state.business_health = business_health

def generate_store_info(stores):
    """Generate static information about each store"""
    store_info = []
    
    for i, store in enumerate(stores):
        # Create varied store profiles
        if "Downtown" in store:
            size = "Large"
            employees = 15
            opened = "2017-03-15"
            revenue_tier = "High"
        elif "Riverside" in store:
            size = "Medium"
            employees = 10
            opened = "2018-09-22"
            revenue_tier = "High"
        elif "Oakwood" in store:
            size = "Medium"
            employees = 8
            opened = "2019-05-10"
            revenue_tier = "Medium"
        elif "Sunset" in store:
            size = "Small"
            employees = 6
            opened = "2020-11-05"
            revenue_tier = "Medium"
        else:
            size = "Small"
            employees = 5
            opened = "2021-07-30"
            revenue_tier = "Low"
            
        store_info.append({
            "store_id": i + 1,
            "store_name": store,
            "size": size,
            "employees": employees,
            "opened_date": opened,
            "revenue_tier": revenue_tier,
            "address": f"{100 + i*100} Main St, Anytown, USA",
            "manager": f"Manager {i+1}"
        })
    
    # Convert to DataFrame
    store_info_data = pd.DataFrame(store_info)
    
    # Store in session state
    st.session_state.store_info = store_info_data
