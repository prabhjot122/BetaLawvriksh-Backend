-- Migration script to add missing columns to feedback table
-- Run this script on your MySQL database to fix the feedback form issues

USE lawvriksh_db;

-- Check if contact_willing column exists, if not add it
SET @column_exists = (
    SELECT COUNT(*) 
    FROM INFORMATION_SCHEMA.COLUMNS 
    WHERE TABLE_SCHEMA = DATABASE() 
    AND TABLE_NAME = 'feedback' 
    AND COLUMN_NAME = 'contact_willing'
);

SET @sql = IF(@column_exists = 0, 
    'ALTER TABLE feedback ADD COLUMN contact_willing VARCHAR(10) DEFAULT NULL AFTER additional_comments;',
    'SELECT "contact_willing column already exists" AS message;'
);

PREPARE stmt FROM @sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

-- Check if contact_email column exists, if not add it
SET @column_exists = (
    SELECT COUNT(*) 
    FROM INFORMATION_SCHEMA.COLUMNS 
    WHERE TABLE_SCHEMA = DATABASE() 
    AND TABLE_NAME = 'feedback' 
    AND COLUMN_NAME = 'contact_email'
);

SET @sql = IF(@column_exists = 0, 
    'ALTER TABLE feedback ADD COLUMN contact_email VARCHAR(255) DEFAULT NULL AFTER contact_willing;',
    'SELECT "contact_email column already exists" AS message;'
);

PREPARE stmt FROM @sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

-- Show the updated table structure
DESCRIBE feedback;

-- Show success message
SELECT 'Migration completed successfully! The feedback table now has contact_willing and contact_email columns.' AS result;
