CREATE TABLE videojuegos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    titulo VARCHAR(100) NOT NULL,
    genero VARCHAR(100) NOT NULL,
    anio INT NOT NULL,
    desarrollador VARCHAR(100) NOT NULL
);