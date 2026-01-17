-- Create the target table
CREATE TABLE IF NOT EXISTS nessie.examples.target_table (
  id INTEGER,
  description VARCHAR
);

-- Create the source table
CREATE TABLE IF NOT EXISTS nessie.examples.source_table (
  id INTEGER,
  description_1 VARCHAR,
  description_2 VARCHAR
);

-- Insert initial data into the target table
INSERT INTO nessie.examples.target_table (id, description) VALUES
  (1, 'Original value 1'),
  (2, 'Original value 2');

-- Insert initial data into the source table
INSERT INTO nessie.examples.source_table (id, description_1, description_2) VALUES
  (1, 'Updated value 1', 'Updated value 2'),
  (3, 'New value 1', 'New value 2');

-- View Target table before merging
SELECT * FROM nessie.examples.target_table;

-- Perform the merge operation
MERGE INTO nessie.examples.target_table AS t
USING nessie.examples.source_table AS s
ON t.id = s.id
WHEN MATCHED THEN
  UPDATE SET description = s.description_2
WHEN NOT MATCHED THEN
  INSERT (id, description) VALUES (s.id, s.description_1);

-- View Target table before merging
SELECT * FROM nessie.examples.target_table;