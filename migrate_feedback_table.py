#!/usr/bin/env python3
"""
Migration script to add missing columns to the feedback table.
This script adds contact_willing and contact_email columns to the existing feedback table.
"""

import os
import sys
import logging
from database import get_db_connection, get_db_config

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def check_column_exists(cursor, table_name, column_name):
    """Check if a column exists in a table"""
    cursor.execute(f"""
        SELECT COUNT(*) 
        FROM INFORMATION_SCHEMA.COLUMNS 
        WHERE TABLE_SCHEMA = DATABASE() 
        AND TABLE_NAME = '{table_name}' 
        AND COLUMN_NAME = '{column_name}'
    """)
    return cursor.fetchone()[0] > 0

def migrate_feedback_table():
    """Add missing columns to feedback table"""
    try:
        with get_db_connection() as connection:
            cursor = connection.cursor()
            
            # Check if feedback table exists
            cursor.execute("SHOW TABLES LIKE 'feedback'")
            if not cursor.fetchone():
                logger.error("Feedback table does not exist. Please run init_mysql.py first.")
                return False
            
            logger.info("Checking existing feedback table structure...")
            
            # Check if contact_willing column exists
            if not check_column_exists(cursor, 'feedback', 'contact_willing'):
                logger.info("Adding contact_willing column...")
                cursor.execute("""
                    ALTER TABLE feedback 
                    ADD COLUMN contact_willing VARCHAR(10) DEFAULT NULL 
                    AFTER additional_comments
                """)
                logger.info("✓ contact_willing column added successfully")
            else:
                logger.info("✓ contact_willing column already exists")
            
            # Check if contact_email column exists
            if not check_column_exists(cursor, 'feedback', 'contact_email'):
                logger.info("Adding contact_email column...")
                cursor.execute("""
                    ALTER TABLE feedback 
                    ADD COLUMN contact_email VARCHAR(255) DEFAULT NULL 
                    AFTER contact_willing
                """)
                logger.info("✓ contact_email column added successfully")
            else:
                logger.info("✓ contact_email column already exists")
            
            # Commit the changes
            connection.commit()
            
            # Verify the table structure
            logger.info("Verifying updated table structure...")
            cursor.execute("DESCRIBE feedback")
            columns = cursor.fetchall()
            
            logger.info("Current feedback table structure:")
            for column in columns:
                logger.info(f"  - {column[0]}: {column[1]} {column[2] if column[2] == 'NO' else 'NULL'}")
            
            logger.info("✅ Migration completed successfully!")
            return True
            
    except Exception as e:
        logger.error(f"❌ Migration failed: {str(e)}")
        return False

def main():
    """Main function"""
    logger.info("Starting feedback table migration...")
    
    # Show database configuration
    config = get_db_config()
    logger.info(f"Database: {config['host']}:{config['port']}/{config['database']}")
    
    # Run migration
    success = migrate_feedback_table()
    
    if success:
        logger.info("🎉 Migration completed successfully!")
        sys.exit(0)
    else:
        logger.error("💥 Migration failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()
