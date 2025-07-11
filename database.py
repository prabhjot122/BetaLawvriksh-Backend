import os
import logging
import pymysql
from contextlib import contextmanager
from typing import Generator

logger = logging.getLogger(__name__)

# Database configuration
DB_HOST = os.environ.get('DB_HOST', 'localhost')
DB_USER = os.environ.get('DB_USER', 'root')
DB_PASSWORD = os.environ.get('DB_PASSWORD', 'Sahil@123456')
DB_NAME = os.environ.get('DB_NAME', 'lawvriksh_db')
DB_PORT = int(os.environ.get('DB_PORT', '3306'))

# SSL configuration for Aiven
SSL_REQUIRED = 'ssl-mode=REQUIRED' in os.environ.get('DATABASE_URL', '') or 'aiven' in os.environ.get('DB_HOST', '')

logger.info(f'Using MySQL database: {DB_HOST}:{DB_PORT}/{DB_NAME}')

def get_db_config():
    """Get database configuration"""
    config = {
        'host': DB_HOST,
        'user': DB_USER,
        'password': DB_PASSWORD,
        'database': DB_NAME,
        'port': DB_PORT,
        'autocommit': False,
        'charset': 'utf8mb4',
        'connect_timeout': 30,
    }

    # Add SSL configuration for production (Aiven)
    if SSL_REQUIRED:
        config['ssl'] = {'ssl_disabled': False}

    return config

@contextmanager
def get_db_connection() -> Generator[pymysql.Connection, None, None]:
    """Get database connection context manager"""
    connection = None
    try:
        config = get_db_config()
        logger.info(f"Connecting to MySQL at {config['host']}:{config['port']}")
        connection = pymysql.connect(**config)
        logger.info("Database connection established successfully")
        yield connection
    except Exception as e:
        logger.error(f"Database connection error: {e}")
        if connection:
            try:
                connection.rollback()
            except:
                pass
        raise
    finally:
        if connection:
            connection.close()
            logger.info("Database connection closed")

def get_db():
    """Dependency to get database connection for FastAPI"""
    with get_db_connection() as connection:
        yield connection

def verify_database_connection():
    """Verify database connection and tables exist"""
    try:
        with get_db_connection() as connection:
            cursor = connection.cursor()

            # Check if required tables exist
            cursor.execute("SHOW TABLES LIKE 'user_registrations'")
            if not cursor.fetchone():
                raise Exception("Table 'user_registrations' does not exist. Please run migrations first.")

            cursor.execute("SHOW TABLES LIKE 'feedback'")
            if not cursor.fetchone():
                raise Exception("Table 'feedback' does not exist. Please run migrations first.")

            logger.info('Database connection verified successfully')
            logger.info('Required tables exist: user_registrations, feedback')

    except Exception as e:
        logger.error(f'Database verification failed: {str(e)}')
        raise
