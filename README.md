# 🏙️ Análisis de desigualdad en los distritos de Madrid 🧮

Este proyecto tiene como objetivo analizar la **desigualdad** entre los distritos de Madrid utilizando una serie de indicadores clave en ámbitos como **bienestar social**, **educación**, **economía** y **salud**. La finalidad es identificar cómo varían las condiciones de vida y las oportunidades entre los distritos de Madrid, y cómo afectan estas diferencias a los ciudadanos.

---

## 📑 Contenido del repositorio

- **code/**: Contiene los notebooks principales para la preparación de datos y el análisis exploratorio.
  - `main.ipynb`: Notebook donde se realiza la **extracción**, **limpieza** y **preparación** de los datos, que luego son cargados en una base de datos SQL.
  - `exploratory.ipynb`: Notebook que lleva a cabo el **análisis exploratorio** y cruces de variables, trabajando directamente desde la base de datos SQL, generando correlaciones, visualizaciones y resultados clave.

- **data/**: Carpeta que contiene los datos utilizados en el proyecto.
  - `raw/`: Datos sin procesar descargados de las fuentes originales.
  - `clean/`: Datos procesados y listos para análisis tras la limpieza y transformación.
  - `presupuestos/`: Contiene los ventiún datasets con la inversión y presupuesto desglosados por año de cada distrito.
 
- **sql/**: Carpeta que contiene las queries para la base de datos.
  - `create_desigualdad_distritos`: Queries necesarias para crear la base de datos
  - `analisis_desigualdad`: Queries para cruzar datos y realizar el análisis de datos
 
- **utils/**: Directorio del archivo **functions.py**, que contiene las funciones de soporte, limpieza y visualización de los datos.

- **visualizations/**: Carpeta que contiene los dashboards con visualizaciones de los datos.
  - `desigualdad_distritos_madrid.pbix`: Archivo de Power Bi con los dashboard interactivos.
  - `desigualdad_distritos_madrid.pdf`: Archivo PDF con los dashboards capturados en estático.

- **requirements.txt**: Archivo que contiene las librerías y módulos necesarias para el proyecto.

- **README.md**: Este archivo de documentación.

![Estructura del proyecto](images/flujo_de_trabajo.png)
---

## 🔍 Introducción

Este análisis se centra en evaluar la desigualdad entre los distritos de la ciudad de Madrid, utilizando indicadores agrupados en cuatro ámbitos clave:

1. **Bienestar Social e Igualdad**
2. **Educación y Cultura**
3. **Economía y Empleo**
4. **Salud**

La selección de estos ámbitos permite una evaluación integral de la equidad en cuanto a calidad de vida, oportunidades y acceso a recursos. Se emplea una metodología rigurosa basada en el **Proceso Analítico Jerárquico (AHP)** para ponderar y calcular los índices de desigualdad en cada ámbito.

El proyecto expone cómo las **diferencias de inversión** y **acceso a servicios** impactan la vida de los ciudadanos, y utiliza estas diferencias para construir una serie de **dashboards interactivos** que permiten la comparación entre distritos.

## 🗂️ Fuentes de datos

Los datos utilizados provienen de diversas fuentes oficiales en su versión más actualizada:

- **Riesgo de pobreza infantil por distrito**: [Alto Comisionado Contra la Pobreza Infantil, Gobierno de España (2021)](https://www.comisionadopobrezainfantil.gob.es/es/datos-e-indicadores).
- **Centros de atención sanitaria por distrito**: [Portal de datos abiertos del Ayuntamiento de Madrid (2024)](https://datos.madrid.es/portal/site/egob).
- **Locales y comercios por distrito**: [Estadística del Ayuntamiento de Madrid - Distritos en Cifras (2024)](https://www.madrid.es/portales/munimadrid/es/Inicio/El-Ayuntamiento/Estadistica?vgnextchannel=8156e39873674210VgnVCM1000000b205a0aRCRD).
- **Centros educativos por distrito**: [Portal de datos abiertos del Ayuntamiento de Madrid (2023)](https://datos.madrid.es/portal/site/egob).
- **Residencias y centros para mayores por distrito**: [Ayuntamiento de Madrid (2023)](https://datos.madrid.es/portal/site/egob).
- **Presupuestos e inversiones por distrito**: [Presupuestos Abiertos del Ayuntamiento de Madrid (2012-2022)](https://presupuestosabiertos.madrid.es/es/).
- **Otros indicadores y datos**: [Portal de datos abiertos del Ayuntamiento de Madrid (2018-2023)](https://datos.madrid.es/portal/site/egob).

## 📈 Metodología

### Cálculo de los índices de desigualdad

Se utilizó el **Proceso Analítico Jerárquico (AHP)** para ponderar la importancia relativa de cada indicador en cada uno de los ámbitos clave (social, económico, educativo y de salud). El **AHP** garantiza que cada variable se valore según su relevancia comparativa, asegurando un análisis justo y riguroso.

1. **Selección de indicadores**: Se seleccionan los valores más representativos de cada ámbito.
2. **Normalización de los datos**: Ajuste de los datos a una escala común de 0 a 100 (con MinMaxScaler).
3. **Asignación de pesos**: Utilizando matrices comparativas para ponderar la importancia de cada indicador en la construcción del índice.
4. **Cálculo del índice**: Sumamos los valores normalizados multiplicados por los pesos asignados para obtener una **nota de desigualdad** para cada distrito.

El resultado final es un índice por cada ámbito y un **índice general** para cada distrito, reflejando su situación relativa en función de los indicadores seleccionados.

#### 📊 Ejemplo de Matriz de Comparación AHP (Desigualdad Económica)

| Variable                  | renta_media | tasa_paro | tasa_paro_larga_duracion | tasa_paro_joven | pension_media | tasa_comercios |
|---------------------------|-------------|-----------|--------------------------|-----------------|---------------|----------------|
| **renta_media**            | 1           | 3         | 5                        | 5               | 6             | 6              |
| **tasa_paro**              | 1/3         | 1         | 3                        | 3               | 5             | 6              |
| **tasa_paro_larga_duracion**| 1/5         | 1/3       | 1                        | 3               | 5             | 6              |
| **tasa_paro_joven**        | 1/5         | 1/3       | 1/3                      | 1               | 3             | 5              |

#### Pesos resultantes:
- **Renta Media**: 0.42
- **Tasa Paro**: 0.23
- **Tasa Paro Larga Duración**: 0.16
- **Tasa Paro Joven**: 0.10

### Justificación del año 2020 en el análisis

El año 2020, marcado por la pandemia de COVID-19, fue un año atípico, pero se ha incluido deliberadamente en el análisis para captar el **impacto diferencial** que la crisis tuvo en los distritos más vulnerables. Según estudios del CSIC, la desigualdad económica se incrementó durante los primeros meses de la pandemia, afectando especialmente a los hogares de **ingresos más bajos**.

## 📊 Ámbitos de Análisis

1. **Bienestar Social e Igualdad**:
   - **Indicadores**: Calidad de vida, percepción de seguridad, tasa de intervención de los servicios sociales, tasa de riesgo de pobreza infantil.
  
2. **Educación y Cultura**:
   - **Indicadores**: Tasa de absentismo escolar, tasa de centros educativos, proporción de población con estudios superiores, etc.
  
3. **Economía y Empleo**:
   - **Indicadores**: Renta media, tasa de paro, tasa de comercios, etc.
  
4. **Salud**:
   - **Indicadores**: Esperanza de vida, tasa de sedentarismo, tasa de enfermedades crónicas y mentales.

![Base de datos](images/base_datos_desigualdad_madrid.jpg)

## 📊 Herramientas y Tecnologías

- **Python** 🐍
  - pandas, numpy, matplotlib, seaborn, sqlalchemy, scipy, pymysql, dotenv.
- **SQL** 🗄️
- **Power BI** 📊

## 📈 Resultados Clave

- **Economía**: Los distritos con mayor renta media presentan menores tasas de desempleo y mejores indicadores de bienestar.
- **Salud**: Se observó una correlación entre los distritos con mayor inversión en salud y mejores indicadores de esperanza de vida y bienestar.
- **Educación**: Los distritos con mayor inversión educativa tienen una menor proporción de población sin estudios y una mayor proporción de personas con estudios superiores.

![Dashboard general](images/dashboard_vision_general.png)
![Dashboard economia](images/dashboard_economia.png)
![Dashboard social](images/dashboard_social.png)
![Dashboard salud](images/dashboard_salud.png)
![Dashboard educacion](images/dashboard_educacion.png)

---

## 🚀 Ejecución del Proyecto

1. **Instalación del Entorno**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate

2. **Instalar dependencias**:
   ```bash
   pip install -r requirements.txt
4. **Conexión a SQL**:
   ```python
   from sqlalchemy import create_engine
   engine = create_engine(f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@localhost/{DB_NAME}")

---
## 👤 Contacto

- **Autora**: [Almudena Ocaña López-Gasco](https://es.linkedin.com/in/almudena-ocaloga)


