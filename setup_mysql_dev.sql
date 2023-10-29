-- a script that prepares a MySQL server for the project

-- Create the database if it doesn't exist
CREATE DATABASE IF NOT EXISTS hbnb_dev_db;

-- Create the user if it doesn't exist and set the password
CREATE USER IF NOT EXISTS 'hbnb_dev'@'localhost' IDENTIFIED BY 'hbnb_dev_pwd';

-- Grant all privileges on the database
GRANT ALL PRIVILEGES ON hbnb_dev_db.* TO 'hbnb_dev'@'localhost';

-- Grant SELECT privilege on performance_schema (if not already granted)
GRANT SELECT ON performance_schema.* TO 'hbnb_dev'@'localhost';
