-- Create the table with initial partitioning on 'name'
CREATE TABLE nessie.examples.partitioned_table (
  id INTEGER,
  name VARCHAR,
  "count" INTEGER,
  ts TIMESTAMP
)
PARTITION BY (name);

-- Insert initial data into the partitioned table
INSERT INTO nessie.examples.partitioned_table VALUES
  (1, 'Alice', NULL, TIMESTAMP '2024-07-02 12:00:00'),
  (2, 'Bob', 5, TIMESTAMP '2024-07-02 12:05:00'),
  (3, 'Catherine', 10, TIMESTAMP '2024-07-02 12:10:00');

-- Query the table before updating partitioning
SELECT * FROM nessie.examples.partitioned_table;

-- Add a new partition field to the table
ALTER TABLE nessie.examples.partitioned_table
  ADD PARTITION FIELD bucket(4, ts);

-- Insert additional data into the updated partitioned table
INSERT INTO nessie.examples.partitioned_table VALUES
  (4, 'David', 15, TIMESTAMP '2024-07-02 12:15:00'),
  (5, 'Eve', 20, TIMESTAMP '2024-07-02 12:20:00');

-- Query the table after updating partitioning
SELECT * FROM nessie.examples.partitioned_table;