create database bookstore;
use bookstore;

CREATE USER 'dbadmin'@'localhost' IDENTIFIED WITH mysql_native_password BY 'admin123';
create user dbadmin identified by 'admin123';
grant all on bookstore.* to 'dbadmin'@'%';
flush privileges;

show tables;
