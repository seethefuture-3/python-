DROP DATABASE IF EXISTS python_final_project;
CREATE DATABASE python_final_project CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE python_final_project;
CREATE TABLE users(username VARCHAR(100) NOT NULL PRIMARY KEY, password VARCHAR(100) NOT NULL);
INSERT INTO users (username, password) VALUES('lhl', '111');
INSERT INTO users (username, password) VALUES('admin', 'admin123');
CREATE TABLE IF NOT EXISTS listed_companies (
    id INT NOT NULL,
    Stock_code VARCHAR(20) NOT NULL,
    Stock_name VARCHAR(100) NOT NULL,
    Company_name VARCHAR(255),
    Province VARCHAR(100),
    City VARCHAR(100),
    IPO_date VARCHAR(50),
    Founded_date VARCHAR(50),
    Person VARCHAR(100),
    Reg_cap VARCHAR(100),
    Employ_num VARCHAR(50),
    Product TEXT,
    col13 VARCHAR(255),
    col14 VARCHAR(500),
    col15 VARCHAR(500),
    col16 VARCHAR(255)
);
LOAD DATA LOCAL INFILE 'C:/Users/liuha/WorkBuddy/2026-06-17-16-15-58/Python_Final_Project/static/data/SSGS.csv'
INTO TABLE listed_companies
CHARACTER SET utf8mb4
FIELDS TERMINATED BY ',' ENCLOSED BY '"'
LINES TERMINATED BY '\n';
