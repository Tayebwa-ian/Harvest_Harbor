-- Create database + user if doesn't exist
CREATE DATABASE IF NOT EXISTS hh_dev_db;
CREATE USER IF NOT EXISTS 'hh_dev'@'localhost';
SET PASSWORD FOR 'hh_dev'@'localhost' = 'hh_dev_pwd';
GRANT ALL ON hh_dev_db.* TO 'hh_dev'@'localhost';
GRANT SELECT ON performance_schema.* TO 'hh_dev'@'localhost';
FLUSH PRIVILEGES;
