-- Drop table if exists
DROP TABLE IF EXISTS users;

-- Create table
CREATE TABLE users (
    id BIGSERIAL PRIMARY KEY,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    email VARCHAR(100),
    gender VARCHAR(10),
    ip_address VARCHAR(45)
);

-- Insert 1,000,000 mock users
INSERT INTO users (first_name, last_name, email, gender, ip_address)
SELECT
    fn AS first_name,
    ln AS last_name,
    LOWER(fn || '.' || ln || gs.i || '@example.com') AS email,
    g AS gender,
    (floor(random()*256)::int || '.' || floor(random()*256)::int || '.' ||
     floor(random()*256)::int || '.' || floor(random()*256)::int) AS ip_address
FROM generate_series(1, 1000000) AS gs(i)
CROSS JOIN LATERAL (
    SELECT
        (ARRAY['James','Mary','John','Patricia','Robert','Jennifer','Michael','Linda',
               'William','Elizabeth','David','Barbara','Richard','Susan','Joseph',
               'Jessica','Thomas','Sarah','Charles','Karen'])[floor(random()*20+1)::int] AS fn,
        (ARRAY['Smith','Johnson','Williams','Brown','Jones','Garcia','Miller','Davis',
               'Rodriguez','Martinez','Hernandez','Lopez','Gonzalez','Wilson','Anderson',
               'Thomas','Taylor','Moore','Jackson','Martin'])[floor(random()*20+1)::int] AS ln,
        (ARRAY['Male','Female','Other'])[floor(random()*3+1)::int] AS g
) AS t;

-- Check total rows
SELECT COUNT(*) FROM users;

-- Preview 10 rows
SELECT * FROM users LIMIT 10;