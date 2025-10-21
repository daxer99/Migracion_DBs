--En postgres
-- Conteo básico en PostgreSQL
SELECT 'PostgreSQL' as motor,
       COUNT(*) as total_estudiantes,
       (SELECT COUNT(*) FROM estudiante_lenguajes) as relaciones_lenguajes,
       (SELECT COUNT(*) FROM estudiante_sistemas_operativos) as relaciones_so
FROM estudiantes;

--En MySQL
-- Conteo básico en MySQL
SELECT 'MySQL' as motor,
       COUNT(*) as total_estudiantes,
       (SELECT COUNT(*) FROM estudiante_lenguajes) as relaciones_lenguajes,
       (SELECT COUNT(*) FROM estudiante_sistemas_operativos) as relaciones_so
FROM estudiantes;

--En mariaDB
-- Conteo básico en MariaDB
SELECT 'MariaDB' as motor,
       COUNT(*) as total_estudiantes,
       (SELECT COUNT(*) FROM estudiante_lenguajes) as relaciones_lenguajes,
       (SELECT COUNT(*) FROM estudiante_sistemas_operativos) as relaciones_so
FROM estudiantes;