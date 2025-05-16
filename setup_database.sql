-- Create the database if it doesn't exist
CREATE DATABASE IF NOT EXISTS aa_pilot;

-- Use the database
USE aa_pilot;

-- Create tables
CREATE TABLE IF NOT EXISTS user (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id VARCHAR(50) NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS user_answer (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id VARCHAR(50) NOT NULL,
    page_number INT NOT NULL,
    answers JSON NOT NULL,
    embeddings JSON,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS user_result (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id VARCHAR(50) NOT NULL UNIQUE,
    result_data JSON NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create a user with necessary permissions
CREATE USER IF NOT EXISTS 'aa_user'@'localhost' IDENTIFIED BY 'aa_password';
GRANT ALL PRIVILEGES ON aa_pilot.* TO 'aa_user'@'localhost';
FLUSH PRIVILEGES;
