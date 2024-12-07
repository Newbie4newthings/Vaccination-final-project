-- 1. Create Database
CREATE DATABASE IF NOT EXISTS vaccination_tracker;

-- Switch to the created database
USE vaccination_tracker;

-- 2. Create Individuals table
CREATE TABLE IF NOT EXISTS Individuals (
    id INT AUTO_INCREMENT PRIMARY KEY,  -- Auto-increment primary key
    patient_number INT(6) UNIQUE NOT NULL,  -- Random 6-digit number
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    birth_date DATE,
    gender VARCHAR(10),
    contact_info VARCHAR(100)
);

-- 3. Create VaccinationTypes table
CREATE TABLE IF NOT EXISTS VaccinationTypes (
    vaccination_type_id INT AUTO_INCREMENT PRIMARY KEY,
    vaccination_name VARCHAR(100),
    manufacturer VARCHAR(100),
    description TEXT
);

-- 4. Create VaccinationHistory table
CREATE TABLE IF NOT EXISTS VaccinationHistory (
    history_id INT AUTO_INCREMENT PRIMARY KEY,
    individual_id INT,  -- Foreign key referencing Individuals table
    patient_number INT(6),  -- 6 digit individual ID (for reference)
    vaccination_type_id INT,  -- References vaccination type
    vaccination_date DATE,
    vaccination_status VARCHAR(20),
    FOREIGN KEY (individual_id) REFERENCES Individuals(id),  -- Link to Individuals table
	FOREIGN KEY (patient_number) REFERENCES Individuals(patient_number),  -- Link to patient_number in Individuals table
    FOREIGN KEY (vaccination_type_id) REFERENCES VaccinationTypes(vaccination_type_id)  -- Link to VaccinationTypes table
);

-- 5. Create Admin table
CREATE TABLE IF NOT EXISTS Admin (
    admin_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,  -- Password field with hashed values
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    contact_info VARCHAR(100),
    role VARCHAR(50)  -- Can be 'super_admin', 'admin', or other roles
);
