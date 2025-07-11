-- =====================================================
-- LawVriksh Complete Database Setup
-- This file contains all migrations and schema setup
-- For use with local MySQL installation
-- =====================================================

-- Create database if it doesn't exist
CREATE DATABASE IF NOT EXISTS lawvriksh_db 
CHARACTER SET utf8mb4 
COLLATE utf8mb4_unicode_ci;

-- Use the database
USE lawvriksh_db;

-- =====================================================
-- DROP EXISTING TABLES (if they exist)
-- =====================================================
SET FOREIGN_KEY_CHECKS = 0;
DROP TABLE IF EXISTS feedback;
DROP TABLE IF EXISTS user_registrations;
SET FOREIGN_KEY_CHECKS = 1;

-- =====================================================
-- USER REGISTRATIONS TABLE
-- =====================================================
CREATE TABLE user_registrations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL COMMENT 'Full name of the user',
    email VARCHAR(255) NOT NULL COMMENT 'Email address',
    phone VARCHAR(20) NOT NULL COMMENT 'Phone number',
    gender VARCHAR(50) NULL COMMENT 'Gender (optional)',
    profession VARCHAR(255) NULL COMMENT 'Profession/occupation (optional)',
    user_type VARCHAR(20) NOT NULL COMMENT 'USER or Creator',
    submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT 'Registration timestamp',
    ip_address VARCHAR(45) NULL COMMENT 'IP address (supports IPv4 and IPv6)',
    user_agent TEXT NULL COMMENT 'Browser user agent string',
    
    -- Indexes for better performance
    INDEX idx_name (name),
    INDEX idx_email (email),
    INDEX idx_user_type (user_type),
    INDEX idx_submitted_at (submitted_at),
    INDEX idx_email_user_type (email, user_type)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
COMMENT='User registration data for LawVriksh platform';

-- =====================================================
-- FEEDBACK TABLE
-- =====================================================
CREATE TABLE feedback (
    id INT AUTO_INCREMENT PRIMARY KEY,
    
    -- Rating questions (1-5 scale)
    visual_design INT NULL COMMENT 'Rating for visual design (1-5)',
    ease_of_navigation INT NULL COMMENT 'Rating for ease of navigation (1-5)',
    mobile_responsiveness INT NULL COMMENT 'Rating for mobile responsiveness (1-5)',
    overall_satisfaction INT NULL COMMENT 'Rating for overall satisfaction (1-5)',
    ease_of_tasks INT NULL COMMENT 'Rating for ease of completing tasks (1-5)',
    quality_of_services INT NULL COMMENT 'Rating for quality of services (1-5)',
    
    -- Conditional fields for low ratings (when rating < 3)
    visual_design_issue TEXT NULL COMMENT 'Issues with visual design',
    ease_of_navigation_issue TEXT NULL COMMENT 'Issues with navigation',
    mobile_responsiveness_issue TEXT NULL COMMENT 'Issues with mobile experience',
    overall_satisfaction_issue TEXT NULL COMMENT 'Issues with overall satisfaction',
    ease_of_tasks_issue TEXT NULL COMMENT 'Issues with completing tasks',
    quality_of_services_issue TEXT NULL COMMENT 'Issues with service quality',
    
    -- Open-ended feedback questions
    like_most TEXT NULL COMMENT 'What users like most about the platform',
    improvements TEXT NULL COMMENT 'Suggested improvements',
    features TEXT NULL COMMENT 'Requested new features',
    legal_challenges TEXT NULL COMMENT 'Legal challenges users face',
    additional_comments TEXT NULL COMMENT 'Any additional comments',
    
    -- Follow-up contact information
    contact_willing VARCHAR(10) NULL COMMENT 'Willing to be contacted (yes/no)',
    contact_email VARCHAR(255) NULL COMMENT 'Email for follow-up contact',
    
    -- Metadata
    submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT 'Feedback submission timestamp',
    ip_address VARCHAR(45) NULL COMMENT 'IP address (supports IPv6)',
    user_agent TEXT NULL COMMENT 'Browser user agent string',
    
    -- Indexes for better performance
    INDEX idx_submitted_at (submitted_at),
    INDEX idx_contact_willing (contact_willing),
    INDEX idx_visual_design (visual_design),
    INDEX idx_overall_satisfaction (overall_satisfaction),
    INDEX idx_contact_email (contact_email),
    
    -- Constraints for rating values
    CONSTRAINT chk_visual_design CHECK (visual_design IS NULL OR (visual_design >= 1 AND visual_design <= 5)),
    CONSTRAINT chk_ease_of_navigation CHECK (ease_of_navigation IS NULL OR (ease_of_navigation >= 1 AND ease_of_navigation <= 5)),
    CONSTRAINT chk_mobile_responsiveness CHECK (mobile_responsiveness IS NULL OR (mobile_responsiveness >= 1 AND mobile_responsiveness <= 5)),
    CONSTRAINT chk_overall_satisfaction CHECK (overall_satisfaction IS NULL OR (overall_satisfaction >= 1 AND overall_satisfaction <= 5)),
    CONSTRAINT chk_ease_of_tasks CHECK (ease_of_tasks IS NULL OR (ease_of_tasks >= 1 AND ease_of_tasks <= 5)),
    CONSTRAINT chk_quality_of_services CHECK (quality_of_services IS NULL OR (quality_of_services >= 1 AND quality_of_services <= 5)),
    CONSTRAINT chk_contact_willing CHECK (contact_willing IS NULL OR contact_willing IN ('yes', 'no'))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
COMMENT='User feedback data for LawVriksh platform';

-- =====================================================
-- SAMPLE DATA (Optional - for testing)
-- =====================================================

-- Insert sample user registrations
INSERT INTO user_registrations (name, email, phone, gender, profession, user_type, ip_address) VALUES
('John Doe', 'john.doe@example.com', '+1234567890', 'Male', 'Lawyer', 'USER', '192.168.1.100'),
('Jane Smith', 'jane.smith@example.com', '+1234567891', 'Female', 'Legal Consultant', 'Creator', '192.168.1.101'),
('Alex Johnson', 'alex.johnson@example.com', '+1234567892', 'Non-binary', 'Paralegal', 'USER', '192.168.1.102');

-- Insert sample feedback
INSERT INTO feedback (
    visual_design, ease_of_navigation, mobile_responsiveness, overall_satisfaction, 
    ease_of_tasks, quality_of_services, like_most, improvements, features, 
    legal_challenges, contact_willing, contact_email, ip_address
) VALUES
(5, 4, 5, 4, 4, 5, 
 'Clean and professional interface', 
 'Could use better search functionality', 
 'Document templates would be helpful',
 'Finding reliable legal precedents quickly',
 'yes', 'john.doe@example.com', '192.168.1.100'),
 
(3, 2, 4, 3, 3, 4,
 'Good content quality',
 'Navigation could be more intuitive',
 'Mobile app would be great',
 'Cost of legal services',
 'no', NULL, '192.168.1.103');

-- Disable safe update mode temporarily for sample data updates
SET SQL_SAFE_UPDATES = 0;

-- Update sample feedback with issue descriptions for low ratings
UPDATE feedback
SET ease_of_navigation_issue = 'Menu structure is confusing, hard to find specific legal topics'
WHERE ease_of_navigation < 3 AND ease_of_navigation_issue IS NULL;

UPDATE feedback
SET overall_satisfaction_issue = 'Some features are hard to find and use'
WHERE overall_satisfaction < 3 AND overall_satisfaction_issue IS NULL;

-- Re-enable safe update mode
SET SQL_SAFE_UPDATES = 1;

-- =====================================================
-- VIEWS FOR REPORTING (Optional)
-- =====================================================

-- View for user registration summary
CREATE OR REPLACE VIEW user_registration_summary AS
SELECT 
    user_type,
    COUNT(*) as total_registrations,
    COUNT(CASE WHEN gender = 'Male' THEN 1 END) as male_count,
    COUNT(CASE WHEN gender = 'Female' THEN 1 END) as female_count,
    COUNT(CASE WHEN gender NOT IN ('Male', 'Female') OR gender IS NULL THEN 1 END) as other_gender_count,
    DATE(submitted_at) as registration_date
FROM user_registrations 
GROUP BY user_type, DATE(submitted_at)
ORDER BY registration_date DESC;

-- View for feedback ratings summary
CREATE OR REPLACE VIEW feedback_ratings_summary AS
SELECT 
    AVG(visual_design) as avg_visual_design,
    AVG(ease_of_navigation) as avg_ease_of_navigation,
    AVG(mobile_responsiveness) as avg_mobile_responsiveness,
    AVG(overall_satisfaction) as avg_overall_satisfaction,
    AVG(ease_of_tasks) as avg_ease_of_tasks,
    AVG(quality_of_services) as avg_quality_of_services,
    COUNT(*) as total_feedback,
    COUNT(CASE WHEN contact_willing = 'yes' THEN 1 END) as willing_to_contact,
    DATE(submitted_at) as feedback_date
FROM feedback 
GROUP BY DATE(submitted_at)
ORDER BY feedback_date DESC;

-- =====================================================
-- STORED PROCEDURES (Optional)
-- =====================================================

DELIMITER //

-- Procedure to get user statistics
CREATE PROCEDURE GetUserStats()
BEGIN
    SELECT 
        COUNT(*) as total_users,
        COUNT(CASE WHEN user_type = 'USER' THEN 1 END) as regular_users,
        COUNT(CASE WHEN user_type = 'Creator' THEN 1 END) as creators,
        COUNT(CASE WHEN submitted_at >= DATE_SUB(NOW(), INTERVAL 30 DAY) THEN 1 END) as recent_registrations
    FROM user_registrations;
END //

-- Procedure to get feedback statistics
CREATE PROCEDURE GetFeedbackStats()
BEGIN
    SELECT 
        COUNT(*) as total_feedback,
        AVG(overall_satisfaction) as avg_satisfaction,
        COUNT(CASE WHEN overall_satisfaction >= 4 THEN 1 END) as satisfied_users,
        COUNT(CASE WHEN overall_satisfaction <= 2 THEN 1 END) as unsatisfied_users,
        COUNT(CASE WHEN contact_willing = 'yes' THEN 1 END) as contact_willing_count
    FROM feedback;
END //

DELIMITER ;

-- =====================================================
-- VERIFICATION QUERIES
-- =====================================================

-- Show all tables
SHOW TABLES;

-- Show table structures
DESCRIBE user_registrations;
DESCRIBE feedback;

-- Show table row counts
SELECT 'user_registrations' as table_name, COUNT(*) as row_count FROM user_registrations
UNION ALL
SELECT 'feedback' as table_name, COUNT(*) as row_count FROM feedback;

-- Show sample data
SELECT 'Sample User Registrations:' as info;
SELECT id, name, email, user_type, submitted_at FROM user_registrations LIMIT 5;

SELECT 'Sample Feedback:' as info;
SELECT id, overall_satisfaction, like_most, submitted_at FROM feedback LIMIT 5;

-- =====================================================
-- COMPLETION MESSAGE
-- =====================================================
SELECT 'Database setup completed successfully!' as status;
