-- LawVriksh Database Schema
-- Initial migration for user registrations and feedback system

-- Create database if it doesn't exist
CREATE DATABASE IF NOT EXISTS lawvriksh_db 
CHARACTER SET utf8mb4 
COLLATE utf8mb4_unicode_ci;

USE lawvriksh_db;

-- User Registrations Table
CREATE TABLE IF NOT EXISTS user_registrations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    phone VARCHAR(20) NOT NULL,
    gender VARCHAR(50) NULL,
    profession VARCHAR(255) NULL,
    user_type VARCHAR(20) NOT NULL COMMENT 'USER or Creator',
    submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ip_address VARCHAR(45) NULL COMMENT 'Support IPv4 and IPv6',
    user_agent TEXT NULL,
    
    -- Indexes for better performance
    INDEX idx_name (name),
    INDEX idx_email (email),
    INDEX idx_user_type (user_type),
    INDEX idx_submitted_at (submitted_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Feedback Table
CREATE TABLE IF NOT EXISTS feedback (
    id INT AUTO_INCREMENT PRIMARY KEY,
    
    -- Rating questions (1-5 scale)
    visual_design INT NULL CHECK (visual_design >= 1 AND visual_design <= 5),
    ease_of_navigation INT NULL CHECK (ease_of_navigation >= 1 AND ease_of_navigation <= 5),
    mobile_responsiveness INT NULL CHECK (mobile_responsiveness >= 1 AND mobile_responsiveness <= 5),
    overall_satisfaction INT NULL CHECK (overall_satisfaction >= 1 AND overall_satisfaction <= 5),
    ease_of_tasks INT NULL CHECK (ease_of_tasks >= 1 AND ease_of_tasks <= 5),
    quality_of_services INT NULL CHECK (quality_of_services >= 1 AND quality_of_services <= 5),
    
    -- Conditional fields for low ratings
    visual_design_issue TEXT NULL,
    ease_of_navigation_issue TEXT NULL,
    mobile_responsiveness_issue TEXT NULL,
    overall_satisfaction_issue TEXT NULL,
    ease_of_tasks_issue TEXT NULL,
    quality_of_services_issue TEXT NULL,
    
    -- Text area questions
    like_most TEXT NULL,
    improvements TEXT NULL,
    features TEXT NULL,
    legal_challenges TEXT NULL,
    additional_comments TEXT NULL,
    
    -- Follow-up questions
    contact_willing VARCHAR(10) NULL COMMENT 'yes or no',
    contact_email VARCHAR(255) NULL,
    
    -- Metadata
    submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ip_address VARCHAR(45) NULL COMMENT 'Support IPv6',
    user_agent TEXT NULL,
    
    -- Indexes
    INDEX idx_submitted_at (submitted_at),
    INDEX idx_contact_willing (contact_willing)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Insert some sample data for testing (optional)
-- INSERT INTO user_registrations (name, email, phone, user_type) 
-- VALUES ('Test User', 'test@example.com', '1234567890', 'USER');

-- Show tables to verify creation
SHOW TABLES;

-- Show table structures
DESCRIBE user_registrations;
DESCRIBE feedback;
