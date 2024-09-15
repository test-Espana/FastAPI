CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    password VARCHAR(50) NOT NULL,
    admin BOOLEAN DEFAULT FALSE
);

INSERT INTO users (name, password, admin) VALUES ('John Doe', 'password123', TRUE), ('Jane Smith', 'password234', FALSE);
