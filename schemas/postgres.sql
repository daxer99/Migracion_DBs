-- Tabla de carreras
CREATE TABLE carreras (
    id SERIAL PRIMARY KEY,
    nombre_carrera VARCHAR(50) UNIQUE NOT NULL
);

-- Tabla de lenguajes de programación (opciones múltiples)
CREATE TABLE lenguajes_programacion (
    id SERIAL PRIMARY KEY,
    nombre_lenguaje VARCHAR(30) UNIQUE NOT NULL
);

-- Tabla de sistemas operativos (opciones múltiples)
CREATE TABLE sistemas_operativos (
    id SERIAL PRIMARY KEY,
    nombre_so VARCHAR(50) UNIQUE NOT NULL
);

-- Tabla principal de estudiantes
CREATE TABLE estudiantes (
    id SERIAL PRIMARY KEY,
    nombre_completo VARCHAR(100) NOT NULL,
    edad INTEGER CHECK (edad >= 16 AND edad <= 60),
    carrera_id INTEGER REFERENCES carreras(id),
    anos_experiencia INTEGER DEFAULT 0,
    proyecto_favorito TEXT,
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de relación estudiantes-lenguajes (muchos a muchos)
CREATE TABLE estudiante_lenguajes (
    id SERIAL PRIMARY KEY,
    estudiante_id INTEGER REFERENCES estudiantes(id) ON DELETE CASCADE,
    lenguaje_id INTEGER REFERENCES lenguajes_programacion(id) ON DELETE CASCADE,
    UNIQUE(estudiante_id, lenguaje_id)
);

-- Tabla de relación estudiantes-sistemas operativos (muchos a muchos)
CREATE TABLE estudiante_sistemas_operativos (
    id SERIAL PRIMARY KEY,
    estudiante_id INTEGER REFERENCES estudiantes(id) ON DELETE CASCADE,
    so_id INTEGER REFERENCES sistemas_operativos(id) ON DELETE CASCADE,
    UNIQUE(estudiante_id, so_id)
);

-- Insertar datos de referencia para lenguajes
INSERT INTO lenguajes_programacion (nombre_lenguaje) VALUES
('Python'), ('Java'), ('C++'), ('PHP'), ('JavaScript'),
('R'), ('Perl'), ('SQL'), ('Rust'), ('Go');

-- Insertar datos de referencia para sistemas operativos
INSERT INTO sistemas_operativos (nombre_so) VALUES
('Windows 7'), ('Windows 10'), ('Windows 11'),
('Linux Mint'), ('Ubuntu'), ('Debian'), ('OpenSUSE'), ('Fedora'),
('macOS'), ('Chrome OS');

-- Insertar datos de referencia para carreras
INSERT INTO carreras (nombre_carrera) VALUES
('Ingeniería de Software'),
('Ciencias de la Computación'),
('Sistemas de Información'),
('Tecnologías de la Información'),
('Ingeniería en Computación'),
('Otra');