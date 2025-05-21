-- Insert sample data for SceneIQ

-- Sample Stores
INSERT INTO stores (name, address, city, state, zip_code, phone, manager, opening_date)
VALUES
  ('Downtown Mart', '123 Main St', 'Springfield', 'IL', '62701', '555-123-4567', 'John Smith', '2020-05-15'),
  ('Riverside Convenience', '456 River Rd', 'Riverdale', 'IL', '62702', '555-234-5678', 'Sarah Johnson', '2021-03-10'),
  ('Oakwood Express', '789 Oak Ave', 'Oakville', 'IL', '62703', '555-345-6789', 'Michael Brown', '2022-01-20'),
  ('Sunset Shop & Go', '101 Sunset Blvd', 'Sunnydale', 'IL', '62704', '555-456-7890', 'Jennifer Davis', '2022-11-05')
ON CONFLICT DO NOTHING;

-- Sample Theft Incidents
INSERT INTO theft_incidents (store_id, timestamp, severity, value, resolved, video_clip_url)
VALUES
  (1, '2025-05-01 14:30:00', 'Medium', 125.50, false, 'https://example.com/clips/incident1.mp4'),
  (1, '2025-05-02 16:45:00', 'Low', 45.75, true, 'https://example.com/clips/incident2.mp4'),
  (2, '2025-05-03 10:15:00', 'High', 350.00, false, 'https://example.com/clips/incident3.mp4'),
  (3, '2025-05-04 12:30:00', 'Medium', 175.25, false, 'https://example.com/clips/incident4.mp4'),
  (4, '2025-05-05 18:20:00', 'Low', 50.00, true, 'https://example.com/clips/incident5.mp4'),
  (2, '2025-05-06 09:45:00', 'High', 425.50, false, 'https://example.com/clips/incident6.mp4'),
  (1, '2025-05-07 15:10:00', 'Medium', 150.00, true, 'https://example.com/clips/incident7.mp4'),
  (3, '2025-05-08 11:30:00', 'Low', 65.25, false, 'https://example.com/clips/incident8.mp4')
ON CONFLICT DO NOTHING;

-- Sample Rewards Data
INSERT INTO rewards_data (store_id, date, total_members, new_members, campaign_engagement, active_campaigns)
VALUES
  (1, '2025-05-01', 1250, 25, 45.8, 3),
  (1, '2025-05-02', 1260, 10, 46.2, 3),
  (2, '2025-05-01', 980, 15, 42.5, 2),
  (2, '2025-05-02', 990, 10, 43.0, 2),
  (3, '2025-05-01', 750, 8, 38.7, 2),
  (3, '2025-05-02', 758, 8, 39.2, 2),
  (4, '2025-05-01', 650, 12, 35.4, 1),
  (4, '2025-05-02', 662, 12, 36.1, 1)
ON CONFLICT DO NOTHING;

-- Sample Campaign Data
INSERT INTO campaigns (store_id, campaign, participation_rate, redemption_rate, roi)
VALUES
  (1, 'Summer Discount', 35.5, 22.8, 2.5),
  (1, 'Coffee Loyalty', 48.2, 35.5, 3.2),
  (1, 'Weekend Special', 42.1, 28.6, 2.1),
  (2, 'Summer Discount', 32.4, 20.5, 2.3),
  (2, 'Gas Rewards', 45.8, 30.2, 2.8),
  (3, 'Snack Bundle', 38.7, 25.4, 2.0),
  (3, 'Coffee Loyalty', 42.5, 31.8, 2.9),
  (4, 'Summer Discount', 30.2, 18.7, 1.9)
ON CONFLICT DO NOTHING;

-- Sample Traffic Patterns
INSERT INTO traffic_patterns (store_id, date, hour, foot_traffic, conversion_rate)
VALUES
  -- Store 1, May 1st
  (1, '2025-05-01', 8, 25, 35.5),
  (1, '2025-05-01', 9, 32, 40.2),
  (1, '2025-05-01', 10, 45, 42.5),
  (1, '2025-05-01', 11, 58, 45.8),
  (1, '2025-05-01', 12, 65, 47.2),
  (1, '2025-05-01', 13, 60, 46.5),
  (1, '2025-05-01', 14, 52, 44.1),
  (1, '2025-05-01', 15, 48, 43.5),
  (1, '2025-05-01', 16, 55, 45.0),
  (1, '2025-05-01', 17, 68, 48.2),
  (1, '2025-05-01', 18, 72, 50.5),
  (1, '2025-05-01', 19, 58, 48.0),
  (1, '2025-05-01', 20, 45, 43.2),
  
  -- Store 2, May 1st (just a few hours as example)
  (2, '2025-05-01', 8, 18, 32.5),
  (2, '2025-05-01', 12, 50, 42.8),
  (2, '2025-05-01', 18, 62, 47.5),
  
  -- Store 3, May 1st (just a few hours as example)
  (3, '2025-05-01', 8, 15, 30.2),
  (3, '2025-05-01', 12, 42, 40.5),
  (3, '2025-05-01', 18, 54, 45.2),
  
  -- Store 4, May 1st (just a few hours as example)
  (4, '2025-05-01', 8, 12, 28.4),
  (4, '2025-05-01', 12, 38, 37.5),
  (4, '2025-05-01', 18, 48, 42.8)
ON CONFLICT DO NOTHING;

-- Sample Employee Data
INSERT INTO employee_data (store_id, date, productivity_score, attendance_rate, training_compliance, customer_satisfaction)
VALUES
  (1, '2025-05-01', 82.5, 95.0, 90.5, 88.7),
  (1, '2025-05-02', 83.2, 94.5, 90.5, 89.1),
  (2, '2025-05-01', 78.4, 92.3, 85.7, 82.5),
  (2, '2025-05-02', 79.1, 93.0, 85.7, 83.2),
  (3, '2025-05-01', 81.2, 94.5, 88.2, 85.4),
  (3, '2025-05-02', 82.0, 95.0, 88.2, 86.0),
  (4, '2025-05-01', 75.8, 91.2, 82.5, 80.3),
  (4, '2025-05-02', 76.5, 92.0, 83.0, 81.0)
ON CONFLICT DO NOTHING;

-- Sample Business Health Data
INSERT INTO business_health (store_id, date, overall_health, theft_score, rewards_score, traffic_score, employee_score, alerts)
VALUES
  (1, '2025-05-01', 85.5, 75.0, 90.5, 82.3, 88.7, '{"alert1": "Check high-value merchandise security", "alert2": "Review employee schedule"}'),
  (1, '2025-05-02', 86.2, 76.5, 91.0, 83.0, 89.1, '{"alert1": "Check high-value merchandise security"}'),
  (2, '2025-05-01', 80.2, 68.5, 85.3, 78.4, 82.5, '{"alert1": "High theft trend detected", "alert2": "Rewards program participation decreasing"}'),
  (2, '2025-05-02', 81.0, 69.2, 86.0, 79.1, 83.2, '{"alert1": "High theft trend detected"}'),
  (3, '2025-05-01', 83.5, 72.8, 88.2, 80.5, 85.4, '{"alert1": "Review security camera placement"}'),
  (3, '2025-05-02', 84.2, 73.5, 88.8, 81.2, 86.0, NULL),
  (4, '2025-05-01', 78.5, 65.4, 82.7, 76.8, 80.3, '{"alert1": "Review employee training program", "alert2": "Low rewards program engagement"}'),
  (4, '2025-05-02', 79.2, 66.0, 83.5, 77.5, 81.0, '{"alert1": "Low rewards program engagement"}')
ON CONFLICT DO NOTHING;

-- Sample Users
INSERT INTO users (username, email, full_name, role, store_id, password_hash)
VALUES
  ('admin', 'admin@sceneiq.com', 'Admin User', 'Admin', NULL, '$2b$12$JQJzTt3YwEWJxCDLE1pF1eU.3KPQtcPQ9eTmU6NDX.gvCjXxqQJMW'), -- password: admin123
  ('jsmith', 'jsmith@sceneiq.com', 'John Smith', 'Manager', 1, '$2b$12$v/FGdXjE8AhWWh1N8.PcluytsMz4KIXW/9XH1JQtULgzO0nYDpcw.'), -- password: password123
  ('sjohnson', 'sjohnson@sceneiq.com', 'Sarah Johnson', 'Manager', 2, '$2b$12$v/FGdXjE8AhWWh1N8.PcluytsMz4KIXW/9XH1JQtULgzO0nYDpcw.'), -- password: password123
  ('mbrown', 'mbrown@sceneiq.com', 'Michael Brown', 'Manager', 3, '$2b$12$v/FGdXjE8AhWWh1N8.PcluytsMz4KIXW/9XH1JQtULgzO0nYDpcw.'), -- password: password123
  ('jdavis', 'jdavis@sceneiq.com', 'Jennifer Davis', 'Manager', 4, '$2b$12$v/FGdXjE8AhWWh1N8.PcluytsMz4KIXW/9XH1JQtULgzO0nYDpcw.'), -- password: password123
  ('owner', 'owner@sceneiq.com', 'Store Owner', 'Owner', NULL, '$2b$12$JQJzTt3YwEWJxCDLE1pF1eU.3KPQtcPQ9eTmU6NDX.gvCjXxqQJMW') -- password: admin123
ON CONFLICT DO NOTHING;