-- Migration to add last_login column to allow_list table
ALTER TABLE allow_list ADD COLUMN last_login DATETIME;