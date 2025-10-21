-- Tabla de carreras
CREATE TABLE carreras (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre_carrera VARCHAR(50) UNIQUE NOT NULL
);

-- Tabla de lenguajes de programacion
CREATE TABLE lenguajes_programacion (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre_lenguaje VARCHAR(30) UNIQUE NOT NULL
);

-- Tabla de sistemas operativos
CREATE TABLE sistemas_operativos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre_so VARCHAR(50) UNIQUE NOT NULL
);

-- Tabla principal de estudiantes
CREATE TABLE estudiantes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre_completo VARCHAR(100) NOT NULL,
    edad INT,
    carrera_id INT,
    anos_experiencia INT DEFAULT 0,
    proyecto_favorito TEXT,
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (carrera_id) REFERENCES carreras(id),
    CHECK (edad >= 16 AND edad <= 60)
);

-- Tabla de relacion estudiantes-lenguajes
CREATE TABLE estudiante_lenguajes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    estudiante_id INT,
    lenguaje_id INT,
    FOREIGN KEY (estudiante_id) REFERENCES estudiantes(id) ON DELETE CASCADE,
    FOREIGN KEY (lenguaje_id) REFERENCES lenguajes_programacion(id) ON DELETE CASCADE,
    UNIQUE(estudiante_id, lenguaje_id)
);

-- Tabla de relacion estudiantes-sistemas operativos
CREATE TABLE estudiante_sistemas_operativos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    estudiante_id INT,
    so_id INT,
    FOREIGN KEY (estudiante_id) REFERENCES estudiantes(id) ON DELETE CASCADE,
    FOREIGN KEY (so_id) REFERENCES sistemas_operativos(id) ON DELETE CASCADE,
    UNIQUE(estudiante_id, so_id)
);

-- Insertar datos de referencia
INSERT INTO lenguajes_programacion (nombre_lenguaje) VALUES
('Python'), ('Java'), ('C++'), ('PHP'), ('JavaScript'),
('R'), ('Perl'), ('SQL'), ('Rust'), ('Go');

INSERT INTO sistemas_operativos (nombre_so) VALUES
('Windows 7'), ('Windows 10'), ('Windows 11'),
('Linux Mint'), ('Ubuntu'), ('Debian'), ('OpenSUSE'), ('Fedora'),
('macOS'), ('Chrome OS');

INSERT INTO carreras (nombre_carrera) VALUES
('Ingenieria de Software'),
('Ciencias de la Computacion'),
('Sistemas de Informacion'),
('Tecnologias de la Informacion'),
('Ingenieria en Computacion'),
('Otra');