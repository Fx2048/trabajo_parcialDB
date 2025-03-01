CREATE DATABASE snake_voting;
USE snake_voting;
CREATE TABLE votos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    direccion VARCHAR(10),
    procesado TINYINT DEFAULT 0
);
