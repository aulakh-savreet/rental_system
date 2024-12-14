-- db/schema.sql

-- Create Database
CREATE DATABASE IF NOT EXISTS rental_system_db;
USE rental_system_db;

-- Create Categories Table
CREATE TABLE IF NOT EXISTS categories (
    category_id INT PRIMARY KEY,
    name VARCHAR(100) NOT NULL
);

-- Create Equipment Table
CREATE TABLE IF NOT EXISTS equipment (
    equipment_id INT PRIMARY KEY,
    category_id INT,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    daily_rate DECIMAL(10,2) DEFAULT 0.00,
    contact_phone VARCHAR(20),
    email VARCHAR(100),
    available BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (category_id) REFERENCES categories(category_id)
);

-- Create Customers Table
CREATE TABLE IF NOT EXISTS customers (
    customer_id INT PRIMARY KEY,
    last_name VARCHAR(100) NOT NULL,
    first_name VARCHAR(100) NOT NULL,
    contact_phone VARCHAR(20),
    email VARCHAR(100)
);

-- Create Rentals Table
CREATE TABLE IF NOT EXISTS rentals (
    rental_id INT PRIMARY KEY,
    rental_date DATE NOT NULL,
    customer_id INT,
    equipment_id INT,
    return_date DATE,
    cost DECIMAL(10,2) DEFAULT 0.00,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
    FOREIGN KEY (equipment_id) REFERENCES equipment(equipment_id)
);
