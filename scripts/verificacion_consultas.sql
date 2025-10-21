-- Consultas comparativas para ejecutar en los tres motores

-- 1. Conteo básico de estudiantes
SELECT 'PostgreSQL' as motor, COUNT(*) as total_estudiantes FROM estudiantes
UNION ALL
SELECT 'MySQL', COUNT(*) FROM encuesta_estudiantes.estudiantes
UNION ALL
SELECT 'MariaDB', COUNT(*) FROM encuesta_estudiantes.estudiantes;

-- 2. Lenguajes de programación más populares
SELECT
    lp.nombre_lenguaje,
    COUNT(el.estudiante_id) as total_estudiantes
FROM lenguajes_programacion lp
LEFT JOIN estudiante_lenguajes el ON lp.id = el.lenguaje_id
GROUP BY lp.id, lp.nombre_lenguaje
ORDER BY total_estudiantes DESC;

-- 3. Sistemas operativos más utilizados
SELECT
    so.nombre_so,
    COUNT(eso.estudiante_id) as total_estudiantes
FROM sistemas_operativos so
LEFT JOIN estudiante_sistemas_operativos eso ON so.id = eso.so_id
GROUP BY so.id, so.nombre_so
ORDER BY total_estudiantes DESC;

-- 4. Distribución por carreras
SELECT
    c.nombre_carrera,
    COUNT(e.id) as total_estudiantes,
    AVG(e.anos_experiencia) as experiencia_promedio
FROM carreras c
LEFT JOIN estudiantes e ON c.id = e.carrera_id
GROUP BY c.id, c.nombre_carrera
ORDER BY total_estudiantes DESC;

-- 5. Estudiantes por rangos de edad
SELECT
    CASE
        WHEN edad BETWEEN 16 AND 20 THEN '16-20'
        WHEN edad BETWEEN 21 AND 25 THEN '21-25'
        WHEN edad BETWEEN 26 AND 30 THEN '26-30'
        ELSE '31+'
    END as grupo_edad,
    COUNT(*) as cantidad
FROM estudiantes
GROUP BY grupo_edad
ORDER BY grupo_edad;

-- 6. Combinación más popular: Lenguaje + SO
SELECT
    lp.nombre_lenguaje,
    so.nombre_so,
    COUNT(DISTINCT e.id) as total_estudiantes
FROM estudiantes e
JOIN estudiante_lenguajes el ON e.id = el.estudiante_id
JOIN lenguajes_programacion lp ON el.lenguaje_id = lp.id
JOIN estudiante_sistemas_operativos eso ON e.id = eso.estudiante_id
JOIN sistemas_operativos so ON eso.so_id = so.id
GROUP BY lp.nombre_lenguaje, so.nombre_so
ORDER BY total_estudiantes DESC
LIMIT 10;

-- 7. Estudiantes con múltiples lenguajes
SELECT
    e.nombre_completo,
    COUNT(el.lenguaje_id) as total_lenguajes
FROM estudiantes e
JOIN estudiante_lenguajes el ON e.id = el.estudiante_id
GROUP BY e.id, e.nombre_completo
HAVING COUNT(el.lenguaje_id) > 1
ORDER BY total_lenguajes DESC;

-- 8. Experiencia por lenguaje preferido
SELECT
    lp.nombre_lenguaje,
    AVG(e.anos_experiencia) as experiencia_promedio,
    COUNT(DISTINCT e.id) as total_estudiantes
FROM lenguajes_programacion lp
JOIN estudiante_lenguajes el ON lp.id = el.lenguaje_id
JOIN estudiantes e ON el.estudiante_id = e.id
GROUP BY lp.id, lp.nombre_lenguaje
ORDER BY experiencia_promedio DESC;