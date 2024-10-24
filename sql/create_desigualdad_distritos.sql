CREATE DATABASE desigualdad_distritos;
USE desigualdad_distritos;

CREATE TABLE indices (
    cod_distrito FLOAT,
    distrito VARCHAR(100),
    indice_desigualdad_salud FLOAT,
    indice_desigualdad_social FLOAT,
    indice_desigualdad_economia FLOAT,
    indice_desigualdad_educacion FLOAT,
    indice_desigualdad_general FLOAT,
    PRIMARY KEY (cod_distrito)
);

CREATE TABLE poblacion (
    cod_distrito FLOAT,
    distrito VARCHAR(100),
    edad_media FLOAT,
    numero_habitantes FLOAT,
    densidad_poblacion FLOAT,
    proporcion_envejecimiento FLOAT,
    proporcion_migrantes FLOAT,
    indice_dependencia FLOAT,
    PRIMARY KEY (cod_distrito)
);

CREATE TABLE economia (
    cod_distrito FLOAT,
    distrito VARCHAR(100),
    renta_media FLOAT,
    tasa_paro FLOAT,
    tasa_paro_larga_duracion FLOAT,
    tasa_paro_joven FLOAT,
    pension_media FLOAT,
    tasa_comercios FLOAT,
    PRIMARY KEY (cod_distrito)
);

CREATE TABLE educacion (
    cod_distrito FLOAT,
    distrito VARCHAR(100),
    tasa_centros_enseñanza FLOAT,
    tasa_centros_publicos_obligatoria FLOAT,
    tasa_absentismo FLOAT,
    tasa_sin_estudios FLOAT,
    tasa_poblacion_educacion_obligatoria FLOAT,
    tasa_poblacion_educacion_superior FLOAT,
    tasa_bibliotecas FLOAT,
    tasa_superficie_deportiva FLOAT,
    tasa_zonas_verdes FLOAT,
    tasa_centros_culturales FLOAT,
    satisfaccion_instalaciones_deportivas FLOAT,
    satisfaccion_centros_culturales FLOAT,
    satisfaccion_espacios_verdes FLOAT,
    PRIMARY KEY (cod_distrito)
);

CREATE TABLE social (
    cod_distrito FLOAT,
    distrito VARCHAR(100),
    calidad_vida FLOAT,
    percepcion_seguridad FLOAT,
    satisfaccion_vivir_distrito FLOAT,
    tasa_intervenciones_policia FLOAT,
    amigable_lgbt FLOAT,
    tasa_demandas_cai FLOAT,
    tasa_personas_atendidas_ss FLOAT,
    tasa_ayuda_domicilio FLOAT,
    tasa_residencias FLOAT,
    tasa_centros_ss FLOAT,
    tasa_riesgo_pobreza_infantil FLOAT,
    PRIMARY KEY (cod_distrito)
);

CREATE TABLE salud (
    cod_distrito FLOAT,
    distrito VARCHAR(100),
    autopercepcion_salud_buena FLOAT,
    consumo_de_medicamentos FLOAT,
    presencia_enfermedad_cronica FLOAT,
    probabilidad_enfermedad_mental FLOAT,
    sedentarismo FLOAT,
    esperanza_vida FLOAT,
    tasa_discapacitados FLOAT,
    tasa_centros_sanitarios FLOAT,
    PRIMARY KEY (cod_distrito)
);

CREATE TABLE presupuestos (
    cod_distrito FLOAT,
    año INT,
    area_inversion VARCHAR(255),
    total_invertido FLOAT,
    PRIMARY KEY (cod_distrito, año, area_inversion)
);

-- Ejecutar hasta aquí para insertar los datos en las tablas

-- Ejecutar a partir de aquí una vez tengas la información en la base de datos
CREATE INDEX idx_cod_distrito ON indices(cod_distrito);

ALTER TABLE poblacion
ADD CONSTRAINT fk_poblacion_indices FOREIGN KEY (cod_distrito) REFERENCES indices(cod_distrito);

ALTER TABLE economia
ADD CONSTRAINT fk_economia_indices FOREIGN KEY (cod_distrito) REFERENCES indices(cod_distrito);

ALTER TABLE educacion
ADD CONSTRAINT fk_educacion_indices FOREIGN KEY (cod_distrito) REFERENCES indices(cod_distrito);

ALTER TABLE social
ADD CONSTRAINT fk_bienestar_indices FOREIGN KEY (cod_distrito) REFERENCES indices(cod_distrito);

ALTER TABLE salud
ADD CONSTRAINT fk_salud_indices FOREIGN KEY (cod_distrito) REFERENCES indices(cod_distrito);

ALTER TABLE presupuestos
ADD CONSTRAINT fk_presupuestos_indices FOREIGN KEY (cod_distrito) REFERENCES indices(cod_distrito);