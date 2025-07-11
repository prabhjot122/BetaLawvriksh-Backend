#!/usr/bin/env python3
"""
MySQL Database initialization script for LawVriksh
This script creates the required tables in your MySQL database
"""

import os
import sys
import pymysql
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def get_db_config():
    """Get database configuration from environment variables"""
    return {
        'host': os.environ.get('DB_HOST', 'localhost'),
        'user': os.environ.get('DB_USER', 'myuser'),
        'password': os.environ.get('DB_PASSWORD', 'Sahil@123456'),
        'database': os.environ.get('DB_NAME', 'lawvriksh_db'),
        'port': int(os.environ.get('DB_PORT', '3306')),
        'charset': 'utf8mb4'
    }

def create_tables():
    """Create all required tables"""
    
    # SQL for creating user_registrations table
    user_registrations_sql = """
    CREATE TABLE IF NOT EXISTS user_registrations (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        email VARCHAR(255) NOT NULL,
        phone VARCHAR(20) NOT NULL,
        gender ENUM('Male', 'Female', 'Other', 'Prefer not to say') DEFAULT NULL,
        profession VARCHAR(255) DEFAULT NULL,
        user_type VARCHAR(50) NOT NULL,
        submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        ip_address VARCHAR(45) DEFAULT NULL,
        user_agent TEXT DEFAULT NULL,
        INDEX idx_email (email),
        INDEX idx_phone (phone),
        INDEX idx_submitted_at (submitted_at)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
    """
    
    # SQL for creating feedback table
    feedback_sql = """
    CREATE TABLE IF NOT EXISTS feedback (
        id INT AUTO_INCREMENT PRIMARY KEY,
        visual_design INT DEFAULT NULL CHECK (visual_design >= 1 AND visual_design <= 5),
        ease_of_navigation INT DEFAULT NULL CHECK (ease_of_navigation >= 1 AND ease_of_navigation <= 5),
        mobile_responsiveness INT DEFAULT NULL CHECK (mobile_responsiveness >= 1 AND mobile_responsiveness <= 5),
        overall_satisfaction INT DEFAULT NULL CHECK (overall_satisfaction >= 1 AND overall_satisfaction <= 5),
        ease_of_tasks INT DEFAULT NULL CHECK (ease_of_tasks >= 1 AND ease_of_tasks <= 5),
        quality_of_services INT DEFAULT NULL CHECK (quality_of_services >= 1 AND quality_of_services <= 5),
        visual_design_issue TEXT DEFAULT NULL,
        ease_of_navigation_issue TEXT DEFAULT NULL,
        mobile_responsiveness_issue TEXT DEFAULT NULL,
        overall_satisfaction_issue TEXT DEFAULT NULL,
        ease_of_tasks_issue TEXT DEFAULT NULL,
        quality_of_services_issue TEXT DEFAULT NULL,
        like_most TEXT DEFAULT NULL,
        improvements TEXT DEFAULT NULL,
        features TEXT DEFAULT NULL,
        legal_challenges TEXT DEFAULT NULL,
        additional_comments TEXT DEFAULT NULL,
        submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        ip_address VARCHAR(45) DEFAULT NULL,
        user_agent TEXT DEFAULT NULL,
        INDEX idx_submitted_at (submitted_at),
        INDEX idx_overall_satisfaction (overall_satisfaction)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
    """
    
    try:
        config = get_db_config()
        print(f"Connecting to MySQL database at {config['host']}:{config['port']}")
        
        connection = pymysql.connect(**config)
        cursor = connection.cursor()
        
        print("Creating user_registrations table...")
        cursor.execute(user_registrations_sql)
        
        print("Creating feedback table...")
        cursor.execute(feedback_sql)
        
        connection.commit()
        
        # Verify tables were created
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        
        print("\n✅ Database initialization successful!")
        print(f"Database: {config['database']}")
        print("Tables created:")
        for table in tables:
            print(f"  - {table[0]}")
            
        cursor.close()
        connection.close()
        
        return True
        
    except Exception as e:
        print(f"❌ Error initializing database: {str(e)}")
        return False

def main():
    """Main function"""
    print("🗄️ Initializing LawVriksh MySQL Database...")
    print("=" * 50)
    
    if create_tables():
        print("\n🎉 Database setup complete!")
        print("\nYou can now start your FastAPI application:")
        print("python main.py")
    else:
        print("\n💥 Database setup failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()
