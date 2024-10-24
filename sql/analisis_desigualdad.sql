SELECT * FROM indices;


-- ANÁLISIS INVERSIÓN

-- Calcular la inversión media anual por habitante en cada distrito
WITH inversion_total_anual AS (
    SELECT 
        cod_distrito,
        SUM(total_invertido) AS inversion_total_anual,
        COUNT(DISTINCT año) AS num_años
    FROM presupuestos
    GROUP BY cod_distrito
),
inversion_media_por_distrito AS (
    SELECT 
        cod_distrito,
        (inversion_total_anual / num_años) AS inversion_media_anual
    FROM inversion_total_anual
)
SELECT 
    i.cod_distrito,
    i.inversion_media_anual,
    (i.inversion_media_anual / p.numero_habitantes) AS inversion_per_capita
FROM inversion_media_por_distrito i
JOIN poblacion p ON i.cod_distrito = p.cod_distrito
ORDER BY inversion_per_capita DESC;


-- Inversión media anual en cada área por cada distrito
SELECT 
    cod_distrito,
    area_inversion,
    AVG(total_invertido) AS inversion_media_anual_area
FROM presupuestos
GROUP BY cod_distrito, area_inversion
ORDER BY cod_distrito, inversion_media_anual_area DESC;


-- Inversión total de cada año en cada distrito
SELECT 
    cod_distrito,
    año,
    SUM(total_invertido) AS inversion_total_anual
FROM presupuestos
GROUP BY cod_distrito, año
ORDER BY cod_distrito, año;


-- Porcentaje de inversión en cada área respecto al total del distrito
WITH total_inversion_por_distrito AS (
    SELECT 
        cod_distrito,
        SUM(total_invertido) AS inversion_total_distrito
    FROM presupuestos
    GROUP BY cod_distrito
)
SELECT 
    p.cod_distrito,
    p.area_inversion,
    SUM(p.total_invertido) AS inversion_total_area,
    (SUM(p.total_invertido) / t.inversion_total_distrito) * 100 AS porcentaje_inversion_area
FROM presupuestos p
JOIN total_inversion_por_distrito t ON p.cod_distrito = t.cod_distrito
GROUP BY p.cod_distrito, p.area_inversion
ORDER BY p.cod_distrito, porcentaje_inversion_area DESC;


-- Aumento o disminución de la inversión cada año:
-- Agrupar la inversión total por distrito y año
WITH inversion_total_anual AS (
    SELECT 
        cod_distrito,
        año,
        SUM(total_invertido) AS total_invertido_anual
    FROM presupuestos
    GROUP BY cod_distrito, año
),
-- Calcular la variación anual en porcentaje
variacion_anual AS (
    SELECT 
        cod_distrito,
        año,
        total_invertido_anual,
        LAG(total_invertido_anual, 1) OVER (PARTITION BY cod_distrito ORDER BY año) AS inversion_anterior,
        ((total_invertido_anual - LAG(total_invertido_anual, 1) OVER (PARTITION BY cod_distrito ORDER BY año)) / LAG(total_invertido_anual, 1) OVER (PARTITION BY cod_distrito ORDER BY año)) * 100 AS variacion_inversion_anual_porcentaje
    FROM inversion_total_anual
)
-- Seleccionar la variación en porcentaje para cada año y distrito
SELECT 
    cod_distrito,
    año,
    variacion_inversion_anual_porcentaje
FROM variacion_anual
WHERE inversion_anterior IS NOT NULL
ORDER BY cod_distrito, año;


-- Calcular el total de inversión en 2012 y 2022 para cada distrito
WITH inversion_por_anio AS (
    SELECT 
        cod_distrito,
        año,
        SUM(total_invertido) AS total_invertido_anual
    FROM presupuestos
    WHERE año IN (2012, 2022)
    GROUP BY cod_distrito, año
),
-- Obtener la inversión en 2012 y 2022 para cada distrito
inversion_2012_2022 AS (
    SELECT 
        cod_distrito,
        MAX(CASE WHEN año = 2012 THEN total_invertido_anual ELSE NULL END) AS inversion_2012,
        MAX(CASE WHEN año = 2022 THEN total_invertido_anual ELSE NULL END) AS inversion_2022
    FROM inversion_por_anio
    GROUP BY cod_distrito
)
-- Calcular la variación en porcentaje entre 2012 y 2022
SELECT 
    cod_distrito,
    inversion_2012,
    inversion_2022,
    CASE
        WHEN inversion_2012 = 0 THEN NULL
        ELSE ((inversion_2022 - inversion_2012) / inversion_2012) * 100
    END AS variacion_porcentaje
FROM inversion_2012_2022
ORDER BY variacion_porcentaje DESC;


------------------------------------------------------------------------------------
-- ANÁLISIS ECONÓMICO

-- Relación entre la inversión en sectores productivos y la tasa de paro
WITH inversion_sectores_productivos AS (
    SELECT 
        cod_distrito,
        AVG(total_invertido) AS inversion_media_sectores_productivos
    FROM presupuestos
    WHERE area_inversion = 'Sectores productivos'
    GROUP BY cod_distrito
)
SELECT 
    i.cod_distrito,
    i.inversion_media_sectores_productivos,
    eco.tasa_paro_joven,
    eco.tasa_paro
FROM inversion_sectores_productivos i
JOIN economia eco ON i.cod_distrito = eco.cod_distrito
ORDER BY i.inversion_media_sectores_productivos DESC;


-- Relación entre inversión per cápita y renta media
WITH inversion_media_anual AS (
    SELECT 
        cod_distrito,
        SUM(total_invertido) / COUNT(DISTINCT año) AS inversion_media_anual
    FROM presupuestos
    GROUP BY cod_distrito
)
SELECT 
    i.cod_distrito,
    p.numero_habitantes,
    (i.inversion_media_anual / p.numero_habitantes) AS inversion_per_capita,
    e.renta_media
FROM inversion_media_anual i
JOIN poblacion p ON i.cod_distrito = p.cod_distrito
JOIN economia e ON i.cod_distrito = e.cod_distrito
ORDER BY inversion_per_capita DESC;


-- Relación entre la inversión en áreas económicas y el paro
WITH inversion_areas_economicas AS (
    SELECT 
        cod_distrito,
        AVG(total_invertido) AS inversion_media_area_economica
    FROM presupuestos
    WHERE area_inversion IN ('Urbanismo', 'Sectores productivos')
    GROUP BY cod_distrito
)
SELECT 
    i.cod_distrito,
    i.inversion_media_area_economica,
    e.tasa_paro,
    e.tasa_paro_larga_duracion,
    e.tasa_paro_joven
FROM inversion_areas_economicas i
JOIN economia e ON i.cod_distrito = e.cod_distrito
ORDER BY inversion_media_area_economica DESC;


-- Relación entre la inversión en áreas económicas y tasa de comercios
WITH inversion_areas_economicas AS (
    SELECT 
        cod_distrito,
        AVG(total_invertido) AS inversion_media_area_economica
    FROM presupuestos
    WHERE area_inversion IN ('Urbanismo', 'Sectores productivos', 'Infraestructuras')
    GROUP BY cod_distrito
)
SELECT 
    i.cod_distrito,
    i.inversion_media_area_economica,
    e.tasa_comercios
FROM inversion_areas_economicas i
JOIN economia e ON i.cod_distrito = e.cod_distrito
ORDER BY inversion_media_area_economica DESC;


-- Correlación entre inversión per cápita y tasas de paro 
WITH inversion_media_anual AS (
    SELECT 
        cod_distrito,
        SUM(total_invertido) / COUNT(DISTINCT año) AS inversion_media_anual
    FROM presupuestos
    GROUP BY cod_distrito
),
inversion_per_capita AS (
    SELECT 
        i.cod_distrito,
        (i.inversion_media_anual / p.numero_habitantes) AS inversion_per_capita
    FROM inversion_media_anual i
    JOIN poblacion p ON i.cod_distrito = p.cod_distrito
)
SELECT 
    i.cod_distrito,
    i.inversion_per_capita,
    e.tasa_paro,
    e.tasa_paro_larga_duracion,
    e.tasa_paro_joven
FROM inversion_per_capita i
JOIN economia e ON i.cod_distrito = e.cod_distrito
ORDER BY i.inversion_per_capita DESC;


-- Relación entre la inversión en áreas económicas y la renta media
WITH inversion_areas_economicas AS (
    SELECT 
        cod_distrito,
        AVG(total_invertido) AS inversion_media_area_economica
    FROM presupuestos
    WHERE area_inversion IN ('Urbanismo', 'Sectores productivos', 'Infraestructuras')
    GROUP BY cod_distrito
)
SELECT 
    i.cod_distrito,
    i.inversion_media_area_economica,
    e.renta_media
FROM inversion_areas_economicas i
JOIN economia e ON i.cod_distrito = e.cod_distrito
ORDER BY i.inversion_media_area_economica DESC;


-- Relación entre la inversión en educación y la tasa de empleo juvenil:
WITH inversion_educacion AS (
    SELECT 
        cod_distrito,
        AVG(total_invertido) AS inversion_media_educacion
    FROM presupuestos
    WHERE area_inversion = 'Educación'
    GROUP BY cod_distrito
)
SELECT 
    i.cod_distrito,
    i.inversion_media_educacion,
    eco.tasa_paro_joven
FROM inversion_educacion i
JOIN economia eco ON i.cod_distrito = eco.cod_distrito
ORDER BY eco.tasa_paro_joven ASC;


-- Relación entre la tasa de paro y la proporción de población con educación superior:
SELECT 
    e.cod_distrito,
    e.tasa_poblacion_educacion_superior,
    eco.tasa_paro
FROM educacion e
JOIN economia eco ON e.cod_distrito = eco.cod_distrito
ORDER BY eco.tasa_paro DESC;


-- Relación entre el índice de envejecimiento, la renta media y pensión media:
SELECT 
    p.cod_distrito,
    p.proporcion_envejecimiento,
    e.pension_media,
    e.renta_media
FROM poblacion p
JOIN economia e ON p.cod_distrito = e.cod_distrito
ORDER BY p.proporcion_envejecimiento DESC;


-- Relación entre la renta media y el paro de larga duración
SELECT 
    e.cod_distrito,
    e.renta_media,
    eco.tasa_paro_larga_duracion
FROM economia e
JOIN economia eco ON e.cod_distrito = eco.cod_distrito
ORDER BY eco.tasa_paro_larga_duracion DESC;



------------------------------------------------------------------------------------
-- ANÁLISIS SOCIAL

-- Relación entre la tasa de riesgo de pobreza infantil y la inversión en protección social
WITH inversion_proteccion_social AS (
    SELECT 
        cod_distrito,
        AVG(total_invertido) AS inversion_media_proteccion_social
    FROM presupuestos
    WHERE area_inversion = 'Protección y promoción social'
    GROUP BY cod_distrito
)
SELECT 
    i.cod_distrito,
    i.inversion_media_proteccion_social,
    s.tasa_riesgo_pobreza_infantil
FROM inversion_proteccion_social i
JOIN social s ON i.cod_distrito = s.cod_distrito
ORDER BY s.tasa_riesgo_pobreza_infantil DESC;


-- Relación entre la tasa de envejecimiento y la inversión social:
WITH inversion_residencias AS (
    SELECT 
        cod_distrito,
        AVG(total_invertido) AS inversion_media_residencias
    FROM presupuestos
    WHERE area_inversion = 'Protección y promoción social'
    GROUP BY cod_distrito
)
SELECT 
    i.cod_distrito,
    i.inversion_media_residencias,
    s.tasa_residencias,
    p.proporcion_envejecimiento
FROM inversion_residencias i
JOIN social s ON i.cod_distrito = s.cod_distrito
JOIN poblacion p ON i.cod_distrito = p.cod_distrito
ORDER BY p.proporcion_envejecimiento DESC;

-- Relación entre tasa de intervenciones policiales y percepción de seguridad:
SELECT 
    s.cod_distrito,
    s.tasa_intervenciones_policia,
    s.percepcion_seguridad,
    s.calidad_vida
FROM social s
ORDER BY s.tasa_intervenciones_policia DESC;


-- Relación entre la tasa de personas atendidas por los servicios sociales y la inversión en servicios sociales
WITH inversion_servicios_sociales AS (
    SELECT 
        cod_distrito,
        AVG(total_invertido) AS inversion_media_servicios_sociales
    FROM presupuestos
    WHERE area_inversion = 'Protección y promoción social'
    GROUP BY cod_distrito
)
SELECT 
    i.cod_distrito,
    i.inversion_media_servicios_sociales,
    s.tasa_personas_atendidas_ss
FROM inversion_servicios_sociales i
JOIN social s ON i.cod_distrito = s.cod_distrito
ORDER BY s.tasa_personas_atendidas_ss DESC;


-- Relación entre la inversión en áreas de bienestar social y la calidad de vida:
WITH inversion_bienestar_social AS (
    SELECT 
        cod_distrito,
        AVG(total_invertido) AS inversion_media_bienestar
    FROM presupuestos
    WHERE area_inversion IN ('Protección y promoción social', 'Otros bienes públicos de carácter social')
    GROUP BY cod_distrito
)
SELECT 
    i.cod_distrito,
    i.inversion_media_bienestar,
    s.calidad_vida
FROM inversion_bienestar_social i
JOIN social s ON i.cod_distrito = s.cod_distrito
ORDER BY s.calidad_vida DESC;


-- Relación entre tasa de migrantes y tasa de personas atendidas por servicios sociales:
SELECT 
    p.cod_distrito,
    p.proporcion_migrantes,
    s.tasa_personas_atendidas_ss
FROM poblacion p
JOIN social s ON p.cod_distrito = s.cod_distrito
ORDER BY p.proporcion_migrantes DESC;


-- Relación entre la inversión en protección social y la calidad de vida
WITH inversion_proteccion_social AS (
    SELECT 
        cod_distrito,
        AVG(total_invertido) AS inversion_media_proteccion_social
    FROM presupuestos
    WHERE area_inversion = 'Protección y promoción social'
    GROUP BY cod_distrito
)
SELECT 
    i.cod_distrito,
    i.inversion_media_proteccion_social,
    s.calidad_vida
FROM inversion_proteccion_social i
JOIN social s ON i.cod_distrito = s.cod_distrito
ORDER BY s.calidad_vida DESC;


-- Relación entre el índice de envejecimiento y servicios sociales para mayores:
SELECT 
    p.cod_distrito,
    p.proporcion_envejecimiento,
    s.tasa_ayuda_domicilio,
    s.tasa_residencias
FROM poblacion p
JOIN social s ON p.cod_distrito = s.cod_distrito
ORDER BY p.proporcion_envejecimiento DESC;


-- Relación entre la tasa de migrantes y la percepción de seguridad:
SELECT 
    p.cod_distrito,
    p.proporcion_migrantes,
    s.percepcion_seguridad,
    s.tasa_intervenciones_policia
FROM poblacion p
JOIN social s ON p.cod_distrito = s.cod_distrito
ORDER BY p.proporcion_migrantes DESC;


-- Relación entre la tasa de intervenciones policiales y la percepción de seguridad según áreas de inversión en seguridad:
WITH inversion_seguridad AS (
    SELECT 
        cod_distrito,
        AVG(total_invertido) AS inversion_media_seguridad
    FROM presupuestos
    WHERE area_inversion = 'Protección Civil y seguridad ciudadana'
    GROUP BY cod_distrito
)
SELECT 
    i.cod_distrito,
    i.inversion_media_seguridad,
    s.tasa_intervenciones_policia,
    s.percepcion_seguridad
FROM inversion_seguridad i
JOIN social s ON i.cod_distrito = s.cod_distrito
ORDER BY s.percepcion_seguridad DESC;


-- Relación entre tasa de riesgo de pobreza infantil y tasas de personas atendidas por servicios sociales:
SELECT 
    s.cod_distrito,
    s.tasa_riesgo_pobreza_infantil,
    s.tasa_personas_atendidas_ss
FROM social s
ORDER BY s.tasa_riesgo_pobreza_infantil DESC;


-- Relación entre la inversión en infraestructuras sociales y la percepción de seguridad:
WITH inversion_infraestructura_social AS (
    SELECT 
        cod_distrito,
        AVG(total_invertido) AS inversion_media_social
    FROM presupuestos
    WHERE area_inversion = 'Protección y promoción social'
    GROUP BY cod_distrito
)
SELECT 
    i.cod_distrito,
    i.inversion_media_social,
    s.percepcion_seguridad
FROM inversion_infraestructura_social i
JOIN social s ON i.cod_distrito = s.cod_distrito
ORDER BY s.percepcion_seguridad DESC;


-- Relación entre la tasa de personas atendidas por servicios sociales y el índice de dependencia:
SELECT 
    p.cod_distrito,
    p.indice_dependencia,
    s.tasa_personas_atendidas_ss
FROM poblacion p
JOIN social s ON p.cod_distrito = s.cod_distrito
ORDER BY p.indice_dependencia DESC;


-- Relación entre la percepción de seguridad y la satisfacción con el barrio
SELECT 
    s.cod_distrito,
    s.percepcion_seguridad,
    s.satisfaccion_vivir_distrito,
    s.calidad_vida
FROM social s
ORDER BY s.percepcion_seguridad DESC;



------------------------------------------------------------------------------------
-- ANÁLISIS EDUCACIÓN Y CULTURA

-- Relación entre la inversión en educación y la tasa de absentismo escolar:
WITH inversion_educacion AS (
    SELECT 
        cod_distrito,
        AVG(total_invertido) AS inversion_media_educacion
    FROM presupuestos
    WHERE area_inversion = 'Educación'
    GROUP BY cod_distrito
)
SELECT 
    i.cod_distrito,
    i.inversion_media_educacion,
    e.tasa_absentismo
FROM inversion_educacion i
JOIN educacion e ON i.cod_distrito = e.cod_distrito
ORDER BY e.tasa_absentismo DESC;


-- Relación entre la tasa de centros de enseñanza y población que llega a educación superior:
SELECT 
    e.cod_distrito,
    e.tasa_centros_enseñanza,
    e.tasa_poblacion_educacion_superior
FROM educacion e
ORDER BY e.tasa_centros_enseñanza DESC;


-- Relación entre renta media y proporción de población con estudios superiores:
SELECT 
    e.cod_distrito,
    eco.renta_media,
    e.tasa_poblacion_educacion_superior
FROM educacion e
JOIN economia eco ON e.cod_distrito = eco.cod_distrito
ORDER BY eco.renta_media DESC;


-- Relación entre la inversión en cultura y la satisfacción con los centros culturales:
WITH inversion_cultura AS (
    SELECT 
        cod_distrito,
        AVG(total_invertido) AS inversion_media_cultura
    FROM presupuestos
    WHERE area_inversion = 'Cultura'
    GROUP BY cod_distrito
)
SELECT 
    i.cod_distrito,
    i.inversion_media_cultura,
    e.satisfaccion_centros_culturales
FROM inversion_cultura i
JOIN educacion e ON i.cod_distrito = e.cod_distrito
ORDER BY e.satisfaccion_centros_culturales DESC;


-- Relación entre la tasa de bibliotecas y el nivel de estudios:
SELECT 
    e.cod_distrito,
    e.tasa_bibliotecas,
    e.tasa_poblacion_educacion_obligatoria,
    e.tasa_poblacion_educacion_superior
FROM educacion e
ORDER BY e.tasa_bibliotecas DESC;


-- Relación entre absentismo escolar y riesgo de pobreza infantil:
SELECT 
    e.cod_distrito,
    e.tasa_absentismo,
    s.tasa_riesgo_pobreza_infantil
FROM educacion e
JOIN social s ON e.cod_distrito = s.cod_distrito
ORDER BY e.tasa_absentismo DESC;


-- Relación entre la inversión en deportes y la satisfacción con las instalaciones deportivas:
WITH inversion_deportes AS (
    SELECT 
        cod_distrito,
        AVG(total_invertido) AS inversion_media_deportes
    FROM presupuestos
    WHERE area_inversion = 'Deportes, juventud y esparcimiento'
    GROUP BY cod_distrito
)
SELECT 
    i.cod_distrito,
    i.inversion_media_deportes,
    e.satisfaccion_instalaciones_deportivas
FROM inversion_deportes i
JOIN educacion e ON i.cod_distrito = e.cod_distrito
ORDER BY e.satisfaccion_instalaciones_deportivas DESC;


-- Relación entre la tasa de personas sin estudios y la tasa de absentismo escolar:
SELECT 
    e.cod_distrito,
    e.tasa_sin_estudios,
    e.tasa_absentismo
FROM educacion e
ORDER BY e.tasa_sin_estudios DESC;


-- Relación entre la tasa de absentismo y la de población con educación superior
SELECT 
    e.cod_distrito,
    e.tasa_absentismo,
    e.tasa_poblacion_educacion_superior
FROM educacion e
ORDER BY e.tasa_absentismo DESC;


-- Relación entre el índice de migrantes y la tasa de población sin estudios:
SELECT 
    p.cod_distrito,
    p.proporcion_migrantes,
    e.tasa_sin_estudios
FROM poblacion p
JOIN educacion e ON p.cod_distrito = e.cod_distrito
ORDER BY p.proporcion_migrantes DESC;


-- Relación entre la inversión en educación y la tasa de personas sin estudios:
WITH inversion_educacion AS (
    SELECT 
        cod_distrito,
        AVG(total_invertido) AS inversion_media_educacion
    FROM presupuestos
    WHERE area_inversion = 'Educación'
    GROUP BY cod_distrito
)
SELECT 
    i.cod_distrito,
    i.inversion_media_educacion,
    e.tasa_sin_estudios
FROM inversion_educacion i
JOIN educacion e ON i.cod_distrito = e.cod_distrito
ORDER BY e.tasa_sin_estudios DESC;


-- Relación entre la inversión en cultura y la satisfacción general de los residentes:
WITH inversion_cultura AS (
    SELECT 
        cod_distrito,
        AVG(total_invertido) AS inversion_media_cultura
    FROM presupuestos
    WHERE area_inversion = 'Cultura'
    GROUP BY cod_distrito
)
SELECT 
    i.cod_distrito,
    i.inversion_media_cultura,
    s.satisfaccion_vivir_distrito
FROM inversion_cultura i
JOIN social s ON i.cod_distrito = s.cod_distrito
ORDER BY s.satisfaccion_vivir_distrito DESC;


-- Relación entre la renta media y la tasa de centros públicos de enseñanza obligatoria:
SELECT 
    e.cod_distrito,
    eco.renta_media,
    e.tasa_centros_publicos_obligatoria
FROM educacion e
JOIN economia eco ON e.cod_distrito = eco.cod_distrito
ORDER BY eco.renta_media DESC;


-- Correlación entre la inversión en deporte y la satisfacción con instalaciones deportivas
WITH inversion_deportes AS (
    SELECT 
        cod_distrito,
        AVG(total_invertido) AS inversion_media_deportes
    FROM presupuestos
    WHERE area_inversion = 'Deportes, juventud y esparcimiento'
    GROUP BY cod_distrito
)
SELECT 
    i.cod_distrito,
    i.inversion_media_deportes,
    e.satisfaccion_instalaciones_deportivas
FROM inversion_deportes i
JOIN educacion e ON i.cod_distrito = e.cod_distrito
ORDER BY i.inversion_media_deportes DESC;


-- Relación entre la inversión en medio ambiente y la satisfacción con los espacios verdes:
WITH inversion_medio_ambiente AS (
    SELECT 
        cod_distrito,
        AVG(total_invertido) AS inversion_media_medio_ambiente
    FROM presupuestos
    WHERE area_inversion = 'Medio ambiente'
    GROUP BY cod_distrito
)
SELECT 
    i.cod_distrito,
    i.inversion_media_medio_ambiente,
    e.satisfaccion_espacios_verdes
FROM inversion_medio_ambiente i
JOIN educacion e ON i.cod_distrito = e.cod_distrito
ORDER BY e.satisfaccion_espacios_verdes DESC;



------------------------------------------------------------------------------------
-- ANÁLISIS SALUD

-- Relación entre inversión en salud y la autopercepción de buena salud
WITH inversion_salud AS (
    SELECT 
        cod_distrito,
        AVG(total_invertido) AS inversion_media_salud
    FROM presupuestos
    WHERE area_inversion = 'Salud pública'
    GROUP BY cod_distrito
)
SELECT 
    i.cod_distrito,
    i.inversion_media_salud,
    s.autopercepcion_salud_buena,
    s.esperanza_vida
FROM inversion_salud i
JOIN salud s ON i.cod_distrito = s.cod_distrito
ORDER BY i.inversion_media_salud DESC;


-- Relación entre la tasa de centros de salud y la esperanza de vida
SELECT 
    s.cod_distrito,
    s.tasa_centros_sanitarios,
    s.esperanza_vida,
    s.autopercepcion_salud_buena
FROM salud s
ORDER BY s.tasa_centros_sanitarios DESC;


-- Relación entre la inversión en deportes y el sedentarismo
WITH inversion_deportes AS (
    SELECT 
        cod_distrito,
        AVG(total_invertido) AS inversion_media_deportes
    FROM presupuestos
    WHERE area_inversion = 'Deportes, juventud y esparcimiento'
    GROUP BY cod_distrito
)
SELECT 
    i.cod_distrito,
    i.inversion_media_deportes,
    s.sedentarismo
FROM inversion_deportes i
JOIN salud s ON i.cod_distrito = s.cod_distrito
ORDER BY i.inversion_media_deportes DESC;


-- Relación entre la renta media y el consumo de medicamentos
SELECT 
    e.cod_distrito,
    e.renta_media,
    s.consumo_de_medicamentos
FROM economia e
JOIN salud s ON e.cod_distrito = s.cod_distrito
ORDER BY e.renta_media ASC;


-- Relación entre la renta media y la autopercepción de salud buena
SELECT 
    e.cod_distrito,
    e.renta_media,
    s.autopercepcion_salud_buena
FROM economia e
JOIN salud s ON e.cod_distrito = s.cod_distrito
ORDER BY e.renta_media DESC;


-- Relación entre la renta media y la presencia de enfermedades crónicas
SELECT 
    e.cod_distrito,
    e.renta_media,
    s.presencia_enfermedad_cronica
FROM economia e
JOIN salud s ON e.cod_distrito = s.cod_distrito
ORDER BY e.renta_media ASC;


-- Relación entre sedentarismo y la proporción de población envejecida:
SELECT 
    p.cod_distrito,
    p.proporcion_envejecimiento,
    s.sedentarismo
FROM poblacion p
JOIN salud s ON p.cod_distrito = s.cod_distrito
ORDER BY p.proporcion_envejecimiento DESC;


-- Relación entre la inversión en deportes y la esperanza de vida
WITH inversion_deportes AS (
    SELECT 
        cod_distrito,
        AVG(total_invertido) AS inversion_media_deportes
    FROM presupuestos
    WHERE area_inversion = 'Deportes, juventud y esparcimiento'
    GROUP BY cod_distrito
)
SELECT 
    i.cod_distrito,
    i.inversion_media_deportes,
    s.esperanza_vida
FROM inversion_deportes i
JOIN salud s ON i.cod_distrito = s.cod_distrito
ORDER BY i.inversion_media_deportes DESC;


-- Relación entre la tasa de enfermedad mental y la percepción de seguridad y calidad de vida:
SELECT 
    s.cod_distrito,
    s.probabilidad_enfermedad_mental,
    social.percepcion_seguridad,
    social.calidad_vida
FROM salud s
JOIN social ON s.cod_distrito = social.cod_distrito
ORDER BY s.probabilidad_enfermedad_mental DESC;


-- Relación entre la inversión en deportes, la tasa de superficie deportiva y satisfacción con instalaciones deportivas con sedentarismo
WITH inversion_deportes AS (
    SELECT 
        cod_distrito,
        AVG(total_invertido) AS inversion_media_deportes
    FROM presupuestos
    WHERE area_inversion = 'Deportes, juventud y esparcimiento'
    GROUP BY cod_distrito
)
SELECT 
	i.cod_distrito,
    i.inversion_media_deportes,
    e.tasa_superficie_deportiva,
    e.satisfaccion_instalaciones_deportivas,
    s.sedentarismo
FROM inversion_deportes i
JOIN educacion e ON i.cod_distrito = e.cod_distrito
JOIN salud s ON e.cod_distrito = s.cod_distrito
ORDER BY s.sedentarismo DESC;


-- Relación entre sedentarismo y nivel de renta
SELECT 
    e.cod_distrito,
    e.renta_media,
    s.sedentarismo
FROM economia e
JOIN salud s ON e.cod_distrito = s.cod_distrito
ORDER BY e.renta_media ASC;


-- Relación entre la tasa de enfermedad mental y el nivel de renta
SELECT 
    e.cod_distrito,
    e.renta_media,
    s.probabilidad_enfermedad_mental
FROM economia e
JOIN salud s ON e.cod_distrito = s.cod_distrito
ORDER BY s.probabilidad_enfermedad_mental DESC;


-- Relación entre la tasa de discapacitados y nivel de renta
SELECT 
    e.cod_distrito,
    e.renta_media,
    s.tasa_discapacitados
FROM economia e
JOIN salud s ON e.cod_distrito = s.cod_distrito
ORDER BY e.renta_media ASC;


-- Relación entre la tasa de centros sanitarios y la autopercepción de buena salud:
SELECT 
    s.cod_distrito,
    s.tasa_centros_sanitarios,
    s.autopercepcion_salud_buena
FROM salud s
ORDER BY s.tasa_centros_sanitarios DESC;


-- Relación entre la proporción de personas mayores y la presencia de enfermedades crónicas
SELECT 
    p.cod_distrito,
    p.proporcion_envejecimiento,
    s.presencia_enfermedad_cronica
FROM poblacion p
JOIN salud s ON p.cod_distrito = s.cod_distrito
ORDER BY p.proporcion_envejecimiento DESC;


-- Relación entre la inversión en salud pública y el consumo de medicamentos:
WITH inversion_salud AS (
    SELECT 
        cod_distrito,
        AVG(total_invertido) AS inversion_media_salud
    FROM presupuestos
    WHERE area_inversion = 'Salud pública'
    GROUP BY cod_distrito
)
SELECT 
    i.cod_distrito,
    i.inversion_media_salud,
    s.tasa_centros_sanitarios,
    s.consumo_de_medicamentos
FROM inversion_salud i
JOIN salud s ON i.cod_distrito = s.cod_distrito
ORDER BY s.consumo_de_medicamentos DESC;


-- Relación entre la inversión en salud pública y la probabilidad de enfermedad mental
WITH inversion_salud AS (
    SELECT 
        cod_distrito,
        AVG(total_invertido) AS inversion_media_salud
    FROM presupuestos
    WHERE area_inversion = 'Salud pública'
    GROUP BY cod_distrito
)
SELECT 
    i.cod_distrito,
    i.inversion_media_salud,
    s.probabilidad_enfermedad_mental
FROM inversion_salud i
JOIN salud s ON i.cod_distrito = s.cod_distrito
ORDER BY s.probabilidad_enfermedad_mental DESC;


-- Relación entre la proporción de envejecimiento y el consumo de medicamentos:
SELECT 
    p.cod_distrito,
    p.proporcion_envejecimiento,
    s.consumo_de_medicamentos
FROM poblacion p
JOIN salud s ON p.cod_distrito = s.cod_distrito
ORDER BY p.proporcion_envejecimiento DESC;
