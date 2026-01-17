-- Creating a namespace for organizing nessie catalog
CREATE FOLDER IF NOT EXISTS nessie.examples AT BRANCH main;

-- Creating a new table
CREATE TABLE IF NOT EXISTS nessie.examples.names (name VARCHAR);

-- Insert Data into the table
INSERT INTO nessie.examples.names VALUES ('Alex'),('Andrew'),('Read');

-- Query the Table
SELECT * FROM nessie.examples.names;