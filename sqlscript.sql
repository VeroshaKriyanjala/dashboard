CREATE DATABASE sensor_db;
USE sensor_db;

CREATE TABLE sensor_data (
    id INT AUTO_INCREMENT PRIMARY KEY,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    value FLOAT
);