-- db/seed_data.sql

USE rental_system_db;

-- Insert Categories
INSERT INTO categories (category_id, name) VALUES
(1, 'Audio Equipment'),
(2, 'Visual Equipment'),
(3, 'Lighting Equipment');

-- Insert Equipment
INSERT INTO equipment (equipment_id, category_id, name, description, daily_rate, contact_phone, email, available) VALUES
(101, 1, 'Microphone', 'High-quality condenser microphone.', 15.00, '123-456-7890', 'audio@example.com', TRUE),
(102, 2, 'Projector', 'HD projector suitable for presentations.', 50.00, '123-456-7891', 'visual@example.com', TRUE),
(103, 3, 'Stage Lights', 'LED stage lighting kit.', 30.00, '123-456-7892', 'lighting@example.com', TRUE);

-- Insert Customers
INSERT INTO customers (customer_id, last_name, first_name, contact_phone, email) VALUES
(201, 'Doe', 'John', '555-1234', 'john.doe@example.com'),
(202, 'Smith', 'Jane', '555-5678', 'jane.smith@example.com');
