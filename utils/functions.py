import pandas as pd
import os
import sys
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import chi2_contingency
from scipy import stats
import numpy as np
from sklearn.preprocessing import MinMaxScaler



###### FUNCIONES DE LIMPIEZA DE DATOS ######

def eliminar_espacios(df, column):
    '''
    Elimina los espacios en blancos al comienzo y final de los valores de la columna.

    Args:        
        df (pandas.DataFrame): DataFrame que contiene la columna.
        column (str): Columna del DataFrame que contendrán los valores a los que quitar espacios.
    '''
    df[column] = df[column].str.strip()

def estandarizar_columnas(df):
    """
    Estandariza los nombres de las columnas de un DataFrame, quitando tildes,
    dejándolos en minúsculas, reemplazando espacios y guiones por guiones bajos.

    Args:
        df (pandas.DataFrame): DataFrame que contiene las columnas a estandarizar.

    """
    # Código para quitar tildes
    df.columns = df.columns.str.normalize('NFKD')\
                            .str.encode('ascii', errors='ignore')\
                            .str.decode('utf-8')
    
    # Convertir a minúsculas, reemplazar espacios y guiones por guiones bajos
    df.columns = df.columns.str.lower().str.replace(' ', '_').str.replace('-', '_')

def estandarizar_numeros(df, column):
    """
    Estandariza los valores numéricos en la columna de un DataFrame.
    Reemplaza los puntos por nada (elimina los separadores de miles) 
    y las comas por puntos (convierte decimales al formato estándar).
    
    Args:
        df (pandas.DataFrame): DataFrame que contiene la columna con el valor.
    """
    df[column] = df[column].str.replace('.', '', regex=False)
    df[column] = df[column].str.replace(',', '.', regex=False)

def convertir_a_numerico(df, column):
    df[column] = pd.to_numeric(df[column], errors='coerce')



###### FUNCIONES DE TRANSFORMACION DE DATOS ######

def convertir_cp_distrito(df, cp_column):
    """
    Convierte los códigos postales en códigos de distritos en un DataFrame.

    Args:
        df (pandas.DataFrame): DataFrame que contiene la columna con los códigos postales.
        cp_column (str): Nombre de la columna que contiene los códigos postales.
        distrito_column (str): Nombre de la columna que contendrán los códigos de distritos.

    Returns:
        pandas.DataFrame: DataFrame con la nueva columna de distritos.
    """
    # Diccionario que convierte códigos postales en códigos de distritos
    codigos_distritos = {
        '28001': 4, '28002': 5, '28003': 7, '28004': 1, '28005': 1, '28006': 4,
        '28007': 3, '28008': 9, '28009': 3, '28010': 7, '28011': 11, '28012': 1,
        '28013': 1, '28014': 3, '28015': 7, '28016': 5, '28017': 15, '28018': 13,
        '28019': 10, '28020': 6, '28021': 17, '28022': 20, '28023': 9, '28024': 11,
        '28025': 10, '28026': 12, '28027': 15, '28028': 4, '28029': 6, '28030': 14,
        '28031': 19, '28032': 19, '28033': 16, '28034': 8, '28035': 8, '28036': 5,
        '28037': 20, '28038': 13, '28039': 6, '28040': 9, '28041': 12, '28042': 21,
        '28043': 16, '28044': 11, '28045': 2, '28046': 5, '28047': 11, '28048': 8,
        '28049': 8, '28050': 16, '28051': 18, '28052': 18, '28053': 13, '28054': 17,
        '28055': 18, '28070': 1}
    
    # Convertir la columna de códigos postales a enteros, luego a cadenas
    df[cp_column] = df[cp_column].fillna(0).astype(int).astype(str)

    # Crear una nueva columna en el DataFrame con los códigos de distritos
    df['cod_distrito'] = df[cp_column].map(codigos_distritos)
    
    return df

def convertir_distrito_a_codigo(df, columna_distrito):
    """
    Convierte los nombres de distritos en códigos de distritos en un DataFrame.

    Args:
        df (pandas.DataFrame): DataFrame que contiene la columna con los nombres de distritos.
        columna_distrito (str): Nombre de la columna que contiene los nombres de distritos.

    Returns:
        pandas.DataFrame: DataFrame con la nueva columna de códigos de distritos.
    
    """
    #Diccionario con los nombres de distrito y sus correspondientes códigos
    distrito_a_codigo = {'Centro': 1, 'Arganzuela': 2, 'Retiro': 3,
                         'Salamanca': 4, 'Chamartín': 5, 'Tetuán': 6,
                         'Chamberí': 7, 'Fuencarral-El Pardo': 8,
                         'Moncloa-Aravaca': 9, 'Latina': 10, 'Carabanchel': 11,
                         'Usera': 12, 'Puente de Vallecas': 13, 'Moratalaz': 14,
                         'Ciudad Lineal': 15, 'Hortaleza': 16, 'Villaverde': 17,
                         'Villa de Vallecas': 18, 'Vicálvaro': 19,
                         'San Blas-Canillejas': 20, 'Barajas': 21,}
    
    # Mapeamos la columna usando el diccionario anterior
    df['cod_distrito'] = df[columna_distrito].map(distrito_a_codigo)
    return df



###### FUNCIONES DE PREPARACIÓN DE DATOS ######

def crear_df_presupuestos(carpeta):
    # Lista de los archivos CSV en la carpeta
    archivos_csv = [f for f in os.listdir(carpeta) if f.endswith('.csv')] 

    # Dataframe vacío para alamacenar los resultados
    df_presupuestos = pd.DataFrame()
    
    for archivo in archivos_csv:
        # Leer cada archivo csv en la carpeta
        df = pd.read_csv(os.path.join(carpeta, archivo))
        
        # Obtener el código del distrito a partir del nombre del archivo
        cod_distrito = archivo.split('-')[-1].split('.')[0][-2:]
        
        # Extraer el año de cada fila
        if 'Año' in df.columns:
            df['año'] = df['Año']
        else:
            continue 

        # Filtrar solo los años entre 2012 y 2022
        df = df[(df['año'] >= 2012) & (df['año'] <= 2022)]
        
        # Añadir la columna del código de distrito
        df['cod_distrito'] = cod_distrito
        
        # Renombrar las columnas para asegurar consistencia
        df = df.rename(columns={
            'Nombre Línea': 'area_inversion',
            'Presupuesto Gasto': 'presupuesto',
            'Gasto Real': 'total_invertido'})
        
        # Combinar los datos en un solo DataFrame
        df_presupuestos = pd.concat([df_presupuestos, df], ignore_index=True)
    
        # Agrupar por distrito, año y área de inversión, y sumar los totales
        df_presupuestos = df_presupuestos.groupby(['cod_distrito', 'año', 'area_inversion']).agg({'total_invertido': 'sum'}).reset_index()
        
    return df_presupuestos 

def crear_df_educacion(df):
    # Definir los indicadores educativos
    educacion_indicadores = [ 
        'Número Habitantes', 'Escuelas Infantiles Públicas CAM',
        'Colegios Públicos Infantil y Primaria', 'Escuelas Infantiles Municipales',
        'Institutos Públicos de Educación Secundaria',
        'Casos trabajados por el programa de absentismo municipal', 
        'Población mayor/igual  de 25 años  que no sabe leer ni escribir o sin estudios', 
        'Población mayor/igual  de 25 años con enseñanza primaria incompleta', 
        'Población mayor/igual  de 25 años con Bachiller Elemental, Graduado Escolar, ESO, Formación profesional 1º grado',  
        'Población mayor/igual  de 25 años  con estudios superiores, licenciatura, arquitectura, ingeniería sup., estudios sup. no universitarios, doctorado,  postgraduado']

    # Filtrar el dataframe por los indicadores de educación
    df_educacion = df[df['indicador_completo'].isin(educacion_indicadores)].pivot_table(
        index=['cod_distrito', 'distrito'], 
        columns='indicador_completo', 
        values='valor_indicador', 
        aggfunc='first').reset_index()

    return df_educacion

def crear_df_cultura(df):
    # Definir los indicadores culturales
    cultura_indicadores = [
    'Número Habitantes',
    'Bibliotecas públicas Municipales', 
    'Bibliotecas públicas Comunidad Madrid', 
    'Centros y Espacios Culturales', 
    'Centros deportivos Municipales', 
    'Superficie deportiva m2', 
    'Relación de Superficie de zonas verdes y Parques de distrito (ha) entre número de Habitantes *10.000', 
    'Grado de satisfacción con los espacios verdes',
    'Grado de satisfacción con los centros culturales', 
    'Grado de satisfacción con las instalaciones deportivas']

    # Crear dataframe de Cultura, Deporte y Ocio por distritos
    df_cultura = df[df['indicador_completo'].isin(cultura_indicadores)].pivot_table(
        index=['cod_distrito', 'distrito'], 
        columns='indicador_completo', 
        values='valor_indicador', 
        aggfunc='first').reset_index()
    
    return df_cultura

def crear_df_economia(df):
    # Definir los indicadores de Economía y Empleo
    economia_indicadores = [
        'Número Habitantes',
        'Renta disponible media por persona', 
        'Pensión media mensual Hombres', 
        'Pensión media mensual  Mujeres', 
        'Tasa absoluta de paro registrado (febrero)', 
        'Tasa de desempleo en mujeres de 16 a 24 años', 
        'Tasa de desempleo en hombres de 16 a 24 años', 
        'Personas paradas de larga duración (febrero)'
    ]
    
    # Filtrar el DataFrame original con los indicadores de economía y empleo
    df_economia = df[df['indicador_completo'].isin(economia_indicadores)].pivot_table(
        index=['cod_distrito', 'distrito'], 
        columns='indicador_completo', 
        values='valor_indicador', 
        aggfunc='first'
    ).reset_index()
    
    return df_economia


def crear_df_bienestar(df):
    # Indicadores de Bienestar Social
    bienestar_indicadores = [
    'Número Habitantes', 
    'Satisfacción de vivir en su barrio',
    'Madrid ciudad amigable con las personas lesbianas, gays, transexuales y bisexuales', 
    'Calidad de vida actual en su barrio',
    'Percepción de seguridad en Madrid', 
    'Intervenciones de la Policía Municipal en materia de seguridad: delitos relacionados con las personas',
    'Intervenciones de la Policía Municipal en materia de seguridad: relacionadas con la tenencia de armas',
    'Intervenciones de la Policía Municipal en materia de seguridad: relacionadas con el patrimonio',
    'Intervenciones de la Policía Municipal en materia de seguridad: relacionadas con la tenencia y consumo de drogas']

    # Crear dataframe de Bienestar Social por distritos
    df_bienestar = df[df['indicador_completo'].isin(bienestar_indicadores)].pivot_table(
        index=['cod_distrito', 'distrito'], 
        columns='indicador_completo', 
        values='valor_indicador', 
        aggfunc='first').reset_index()
    
    return df_bienestar

def crear_df_social(df):
    servicios_sociales_indicadores = [
    'Tasa de riesgo de pobreza o exclusión social', 
    'Número Habitantes',
    'Personas atendidas en la Unidad de Primera Atención en Centros de Servicios Sociales', 
    'Personas con Servicio de Ayuda a Domicilio (modalidad auxiliar de hogar)',  
    'Personas socias de los Centros Municipales de Mayores', 
    'Demandas de intervención en los Centros de Atención a la Infancia (CAI)', 
    'Centros de Servicios Sociales', 
    'Centros Municipales de Mayores']

    # Crear dataframe de Servicios Sociales por distritos
    df_social = df[df['indicador_completo'].isin(servicios_sociales_indicadores)].pivot_table(
        index=['cod_distrito', 'distrito'], 
        columns='indicador_completo', 
        values='valor_indicador', 
        aggfunc='first').reset_index()
    
    return df_social

def crear_df_salud(df):
    # Indicadores de la categoría Salud
    salud_indicadores = [
        'Número Habitantes',
        'Esperanza de vida al nacer Mujeres', 
        'Esperanza de vida al nacer Hombres',
        'Número de personas con grado de discapacidad reconocido',
        'Autopercepción de buen estado de salud  (porcentaje respuesta muy buena + buena)',
        'Sedentarismo', 
        'Índice de obesidad',
        'Consumo de medicamentos',  
        'Presencia de enfermedad crónica', 
        'Probabilidad de padecer enfermedad mental (GHQ-12)          (2018. EMS)']

    # Crear dataframe de Salud por distritos
    df_salud = df[df['indicador_completo'].isin(salud_indicadores)].pivot_table(
        index=['cod_distrito', 'distrito'], 
        columns='indicador_completo', 
        values='valor_indicador', 
        aggfunc='first').reset_index()
    
    return df_salud

def crear_df_poblacion(df):
    # Crear un dataframe con los indicadores de población por distrito
    poblacion_indicadores = [
        'Población densidad (hab./Ha.)', 
        'Número Habitantes', 
        'Edad media de la población', 
        'Proporción de envejecimiento (Población mayor de 65 años/Población total)', 
        'Índice de dependencia (Población de 0-15 + población 65 años y más / Pob. 16-64)',
        'Proporción de personas migrantes (Población extranjera menos UE y resto países de OCDE / Población total)']

    # Filtramos el dataframe original solo con los indicadores relevantes y agrupamos por distrito
    df_poblacion = df[df['indicador_completo'].isin(poblacion_indicadores)].pivot_table(
        index=['cod_distrito', 'distrito'], 
        columns='indicador_completo', 
        values='valor_indicador', 
        aggfunc='first').reset_index()
    
    return df_poblacion



###### FUNCIONES DE ANÁLISIS DE DATOS ######

def eda_bi_distritos(df, num_var, distrito_var):
    """
    Realiza un análisis bivariable entre una variable numérica y los distritos.
    
    Parámetros:
    df (DataFrame): El DataFrame con las columnas a analizar.
    num_var (str): El nombre de la columna de la variable numérica.
    distrito_var (str): El nombre de la columna del distrito (categórica).
    
    Retorna:
    - Gráfico de barras (barplot) que muestra la variable numérica por distrito.
    """
    # Ordenar los distritos por la variable numérica de mayor a menor
    df_sorted = df.sort_values(by=num_var, ascending=False)
    
    # Crear una paleta de colores únicos para cada distrito
    num_distritos = df[distrito_var].nunique()  # Número de distritos
    palette = sns.color_palette("husl", num_distritos)  # Usamos 'husl' para colores distintivos
    
    # Crear el gráfico de barras ordenado y coloreado
    plt.figure(figsize=(12, 7))
    sns.barplot(x=distrito_var, y=num_var, data=df_sorted, 
                order=df_sorted[distrito_var], hue=distrito_var, palette=palette, dodge=False)
    plt.xticks(rotation=90)
    plt.title(f"Barplot de {num_var} por {distrito_var} (ordenado de mayor a menor)")
    plt.show()



###### FUNCIONES DE CÁLCULO DE PESOS INDICADORES (AHP) ######

def calcular_pesos_ahp(variables, matriz_comparacion):
    """
    Esta función calcula los pesos AHP para las variables basadas en una matriz de comparación por pares.
    
    Args:
    - variables (list): Lista de nombres de las variables.
    - matriz_comparacion (ndarray): Matriz de comparación por pares de las variables.
    
    Returns:
    - DataFrame: Un DataFrame con las variables y sus respectivos pesos AHP.
    """
    # Normalizar la matriz: sumamos cada columna y dividimos cada elemento por la suma de su columna
    suma_columnas = matriz_comparacion.sum(axis=0)
    matriz_normalizada = matriz_comparacion / suma_columnas

    # Calcular el promedio de cada fila (esto nos da los pesos para cada criterio)
    pesos = matriz_normalizada.mean(axis=1)

    # Asignar los nombres de las variables a los pesos calculados
    pesos_ahp = pd.DataFrame({'Variable': variables, 'Peso AHP': pesos})

    return pesos_ahp



###### FUNCIONES DE CÁLCULO DE ÍNDICES ######

def calcular_nota_economia(df):
    # Crear una copia del dataframe para no modificar el original
    df_economia = df.copy()

    # Seleccionar las columnas a normalizar
    indicadores = ['renta_media', 'tasa_paro', 'tasa_paro_larga_duracion', 'tasa_paro_joven', 'pension_media', 'tasa_comercios']

    # Normalizar las columnas (escala de 0 a 1)
    scaler = MinMaxScaler()
    df_economia[indicadores] = scaler.fit_transform(df_economia[indicadores])

    # Invertir el peso de las variables negativas
    df_economia['tasa_paro'] = 1 - df_economia['tasa_paro']
    df_economia['tasa_paro_larga_duracion'] = 1 - df_economia['tasa_paro_larga_duracion']
    df_economia['tasa_paro_joven'] = 1 - df_economia['tasa_paro_joven']

    # Asignar pesos basados en el AHP
    df_economia['nota_economia'] = (df_economia['renta_media'] * 0.427594 +
                                      df_economia['tasa_paro'] * 0.230195 +
                                      df_economia['tasa_paro_larga_duracion'] * 0.162574 +
                                      df_economia['tasa_paro_joven'] * 0.102090 +
                                      df_economia['pension_media'] * 0.046948 +
                                      df_economia['tasa_comercios'] * 0.030598)

    # Escalar la nota a 100
    df_economia['nota_economia'] = (df_economia['nota_economia'] * 100).round(2)

    # Seleccionar las columnas de interés
    df_nota_economia = df_economia[['cod_distrito', 'distrito', 'nota_economia']]

    return df_nota_economia

def calcular_nota_educacion(df):
    # Crear una copia del dataframe para no modificar el original
    df_educacion = df.copy()

    # Seleccionar las columnas a normalizar
    indicadores = [
        'tasa_sin_estudios', 
        'tasa_poblacion_educacion_superior', 
        'tasa_absentismo', 
        'tasa_centros_publicos_obligatoria', 
        'tasa_centros_enseñanza', 
        'tasa_bibliotecas', 
        'tasa_centros_culturales', 
        'satisfaccion_instalaciones_deportivas', 
        'satisfaccion_espacios_verdes']

    # Normalizar las columnas (escala de 0 a 1)
    scaler = MinMaxScaler()
    df_educacion[indicadores] = scaler.fit_transform(df_educacion[indicadores])

    # Invertir el peso de las variables negativas (si es relevante)
    df_educacion['tasa_sin_estudios'] = 1 - df_educacion['tasa_sin_estudios']
    df_educacion['tasa_absentismo'] = 1 - df_educacion['tasa_absentismo']

    # Asignar pesos basados en AHP
    df_educacion['nota_educacion'] = (
        df_educacion['tasa_sin_estudios'] * 0.312186 +
        df_educacion['tasa_poblacion_educacion_superior'] * 0.233266 +
        df_educacion['tasa_absentismo'] * 0.167700 +
        df_educacion['tasa_centros_publicos_obligatoria'] * 0.103495 +
        df_educacion['tasa_centros_enseñanza'] * 0.061458 +
        df_educacion['tasa_bibliotecas'] * 0.050164 +
        df_educacion['tasa_centros_culturales'] * 0.035483 +
        df_educacion['satisfaccion_instalaciones_deportivas'] * 0.021196 +
        df_educacion['satisfaccion_espacios_verdes'] * 0.015053)

    # Escalar la nota a 100
    df_educacion['nota_educacion'] = (df_educacion['nota_educacion'] * 100).round(2)

    # Seleccionar las columnas de interés
    df_nota_educacion = df_educacion[['cod_distrito', 'distrito', 'nota_educacion']]

    return df_nota_educacion

def calcular_nota_social(df):
    # Crear una copia del dataframe para no modificar el original
    df_social = df.copy()

    # Seleccionar las columnas a normalizar
    indicadores = ['tasa_riesgo_pobreza_infantil', 'tasa_intervenciones_policia', 'tasa_demandas_cai', 
                   'tasa_personas_atendidas_ss', 'tasa_ayuda_domicilio', 'calidad_vida', 
                   'percepcion_seguridad', 'tasa_residencias', 'satisfaccion_vivir_distrito',
                   'tasa_centros_ss', 'amigable_lgbt']

    # Normalizar las columnas (escala de 0 a 1)
    scaler = MinMaxScaler()
    df_social[indicadores] = scaler.fit_transform(df_social[indicadores])

    # Invertir el peso de las variables negativas (las que indican más desigualdad con valores más altos)
    df_social['tasa_riesgo_pobreza_infantil'] = 1 - df_social['tasa_riesgo_pobreza_infantil']
    df_social['tasa_intervenciones_policia'] = 1 - df_social['tasa_intervenciones_policia']
    df_social['tasa_demandas_cai'] = 1 - df_social['tasa_demandas_cai']
    df_social['tasa_personas_atendidas_ss'] = 1 - df_social['tasa_personas_atendidas_ss']

    # Asignar pesos según el AHP
    df_social['nota_social'] = (df_social['tasa_riesgo_pobreza_infantil'] * 0.301704 +
                                      df_social['tasa_intervenciones_policia'] * 0.191723 +
                                      df_social['tasa_demandas_cai'] * 0.141420 +
                                      df_social['tasa_personas_atendidas_ss'] * 0.103539 +
                                      df_social['tasa_ayuda_domicilio'] * 0.075159 +
                                      df_social['calidad_vida'] * 0.057293 +
                                      df_social['percepcion_seguridad'] * 0.040861 +
                                      df_social['tasa_residencias'] * 0.032163 +
                                      df_social['satisfaccion_vivir_distrito'] * 0.021747 +
                                      df_social['tasa_centros_ss'] * 0.020210 +
                                      df_social['amigable_lgbt'] * 0.014180)

    # Escalar la nota a 100
    df_social['nota_social'] = (df_social['nota_social'] * 100).round(2)

    # Seleccionar las columnas de interés
    df_nota_social = df_social[['cod_distrito', 'distrito', 'nota_social']]

    return df_nota_social

def calcular_nota_salud(df):
    # Crear una copia del dataframe para no modificar el original
    df_salud = df.copy()

    # Seleccionar las columnas a normalizar
    indicadores = ['esperanza_vida', 'autopercepcion_salud_buena', 'tasa_centros_sanitarios',
                   'presencia_enfermedad_cronica', 'probabilidad_enfermedad_mental',
                   'consumo_de_medicamentos', 'sedentarismo', 'tasa_discapacitados']

    # Normalizar las columnas (escala de 0 a 1)
    scaler = MinMaxScaler()
    df_salud[indicadores] = scaler.fit_transform(df_salud[indicadores])

    # Invertir el peso de las tasas negativas (indicadores negativos para la salud)
    df_salud['presencia_enfermedad_cronica'] = 1 - df_salud['presencia_enfermedad_cronica']
    df_salud['probabilidad_enfermedad_mental'] = 1 - df_salud['probabilidad_enfermedad_mental']
    df_salud['consumo_de_medicamentos'] = 1 - df_salud['consumo_de_medicamentos']
    df_salud['sedentarismo'] = 1 - df_salud['sedentarismo']
    df_salud['tasa_discapacitados'] = 1 - df_salud['tasa_discapacitados']

    # Asignar pesos basados en el AHP
    df_salud['nota_salud'] = (df_salud['esperanza_vida'] * 0.379511 +
                              df_salud['autopercepcion_salud_buena'] * 0.210312 +
                              df_salud['tasa_centros_sanitarios'] * 0.144085 +
                              df_salud['presencia_enfermedad_cronica'] * 0.103195 +
                              df_salud['probabilidad_enfermedad_mental'] * 0.072054 +
                              df_salud['consumo_de_medicamentos'] * 0.041516 +
                              df_salud['sedentarismo'] * 0.026998 +
                              df_salud['tasa_discapacitados'] * 0.022329)

    # Escalar la nota a 100
    df_salud['nota_salud'] = (df_salud['nota_salud'] * 100).round(2)

    # Seleccionar las columnas de interés
    df_nota_salud = df_salud[['cod_distrito', 'distrito', 'nota_salud']]

    return df_nota_salud



##### FUNCIONES PARA GRAFICAR DATOS #####

def graficar_variable_distrito(df, variable, titulo='Gráfico de distribución'):
    """
    Función para graficar una variable en relación a los distritos.
    
    Args:
        df (pd.DataFrame): DataFrame que contiene los datos (debe tener 'cod_distrito' y la variable seleccionada).
        variable (str): Nombre de la columna del DataFrame que quieres graficar.
        titulo (str): Título del gráfico (opcional).
    """
    # Diccionario que mapea códigos de distrito a nombres de distrito
    mapa_distritos = {
        1: "Centro", 2: "Arganzuela", 3: "Retiro", 4: "Salamanca", 5: "Chamartín",
        6: "Tetuán", 7: "Chamberí", 8: "Fuencarral-El Pardo", 9: "Moncloa-Aravaca", 10: "Latina",
        11: "Carabanchel", 12: "Usera", 13: "Puente de Vallecas", 14: "Moratalaz", 15: "Ciudad Lineal",
        16: "Hortaleza", 17: "Villaverde", 18: "Villa de Vallecas", 19: "Vicálvaro", 20: "San Blas-Canillejas",
        21: "Barajas"
    }
    
    # Traducir los códigos de distrito a nombres de distrito
    df['distrito'] = df['cod_distrito'].map(mapa_distritos)

    # Ordenar el DataFrame por la variable seleccionada
    df = df.sort_values(by=variable, ascending=False)

    # Graficar la variable seleccionada
    plt.figure(figsize=(10, 6))
    plt.bar(df['distrito'], df[variable], color='skyblue')

    # Títulos y etiquetas
    plt.title(f'{titulo} por distrito', fontsize=14)
    plt.xlabel('Distrito', fontsize=12)
    plt.ylabel(variable, fontsize=12)

    # Rotar las etiquetas de los distritos para que se vean mejor
    plt.xticks(rotation=90)

    # Mostrar el gráfico
    plt.tight_layout()
    plt.show()


def graficar_inversion_area(df):
    """
    Función para graficar la inversión media anual por área y distrito en un gráfico de barras apiladas.
    
    Args:
        df (pd.DataFrame): DataFrame con columnas 'cod_distrito', 'area_inversion' e 'inversion_media_anual_area'.
    """
    # Diccionario que mapea códigos de distrito a nombres de distrito
    mapa_distritos = {
        1: "Centro", 2: "Arganzuela", 3: "Retiro", 4: "Salamanca", 5: "Chamartín",
        6: "Tetuán", 7: "Chamberí", 8: "Fuencarral-El Pardo", 9: "Moncloa-Aravaca", 10: "Latina",
        11: "Carabanchel", 12: "Usera", 13: "Puente de Vallecas", 14: "Moratalaz", 15: "Ciudad Lineal",
        16: "Hortaleza", 17: "Villaverde", 18: "Villa de Vallecas", 19: "Vicálvaro", 20: "San Blas-Canillejas",
        21: "Barajas"
    }

    # Mapear los nombres de los distritos
    df['distrito'] = df['cod_distrito'].map(mapa_distritos)

    # Pivotar la tabla para tener las áreas de inversión como columnas y los distritos como filas
    df_pivot = df.pivot(index='distrito', columns='area_inversion', values='inversion_media_anual_area')

    # Crear el gráfico de barras apiladas
    df_pivot.plot(kind='bar', stacked=True, figsize=(12, 8), cmap='tab20')

    # Títulos, leyenda y etiquetas
    plt.title('Inversión media anual por área y distrito', fontsize=14)
    plt.xlabel('Distrito', fontsize=12)
    plt.ylabel('Inversión media anual (€)', fontsize=12)
    plt.legend(title='Áreas de inversión', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.xticks(rotation=90)
    plt.show()


def graficar_inversion_por_año(df):
    """
    Función para graficar la inversión total anual por distrito a lo largo de los años en un gráfico de líneas.
    
    Args:
        df (pd.DataFrame): DataFrame con columnas 'cod_distrito', 'año' e 'inversion_total_anual'.
    """
    # Diccionario que mapea códigos de distrito a nombres de distrito
    mapa_distritos = {
        1: "Centro", 2: "Arganzuela", 3: "Retiro", 4: "Salamanca", 5: "Chamartín",
        6: "Tetuán", 7: "Chamberí", 8: "Fuencarral-El Pardo", 9: "Moncloa-Aravaca", 10: "Latina",
        11: "Carabanchel", 12: "Usera", 13: "Puente de Vallecas", 14: "Moratalaz", 15: "Ciudad Lineal",
        16: "Hortaleza", 17: "Villaverde", 18: "Villa de Vallecas", 19: "Vicálvaro", 20: "San Blas-Canillejas",
        21: "Barajas"
    }

    # Mapear los nombres de los distritos
    df['distrito'] = df['cod_distrito'].map(mapa_distritos)

    # Pivotar los datos para tener los distritos como columnas y los años como filas
    df_pivot = df.pivot(index='año', columns='distrito', values='inversion_total_anual')

    # Crear el gráfico de líneas
    ax = df_pivot.plot(kind='line', figsize=(12, 8), marker='o', linewidth=2)

    # Títulos, leyenda y etiquetas
    plt.title('Evolución de la inversión total anual por distrito (2012-2022)', fontsize=14)
    plt.xlabel('Año', fontsize=12)
    plt.ylabel('Inversión total anual (€)', fontsize=12)
    ax.legend(title='Distrito', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.grid(True)
    plt.tight_layout()
    plt.show()


def graficar_inversion_sp_tasa_paro(df):
    # Diccionario que mapea códigos de distrito a nombres de distrito
    mapa_distritos = {
        1: "Centro", 2: "Arganzuela", 3: "Retiro", 4: "Salamanca", 5: "Chamartín",
        6: "Tetuán", 7: "Chamberí", 8: "Fuencarral-El Pardo", 9: "Moncloa-Aravaca", 10: "Latina",
        11: "Carabanchel", 12: "Usera", 13: "Puente de Vallecas", 14: "Moratalaz", 15: "Ciudad Lineal",
        16: "Hortaleza", 17: "Villaverde", 18: "Villa de Vallecas", 19: "Vicálvaro", 20: "San Blas-Canillejas",
        21: "Barajas"
    }

    # Mapear los nombres de los distritos
    df['distrito'] = df['cod_distrito'].map(mapa_distritos)

    # Crear el gráfico de dispersión
    plt.figure(figsize=(10, 6))
    plt.scatter(df['inversion_media_sectores_productivos'], df['tasa_paro'], color='b', s=100)

    # Agregar etiquetas de los nombres de los distritos
    for i, distrito in enumerate(df['distrito']):
        plt.text(df['inversion_media_sectores_productivos'].iloc[i], df['tasa_paro'].iloc[i], distrito, fontsize=9)

    # Configurar etiquetas y título del gráfico
    plt.title('Inversión en Sectores Productivos vs tasa de paro por distrito', fontsize=14)
    plt.xlabel('Inversión media en Sectores Productivos (€)', fontsize=12)
    plt.ylabel('Tasa de Paro (%)', fontsize=12)

    # Mostrar la cuadrícula
    plt.grid(True)
    
    plt.show()

def graficar_educacion_superior_paro(df):

    #Diccionario de nombres de distritos
    mapa_distritos = {
        1: "Centro", 2: "Arganzuela", 3: "Retiro", 4: "Salamanca", 5: "Chamartín",
        6: "Tetuán", 7: "Chamberí", 8: "Fuencarral-El Pardo", 9: "Moncloa-Aravaca", 10: "Latina",
        11: "Carabanchel", 12: "Usera", 13: "Puente de Vallecas", 14: "Moratalaz", 15: "Ciudad Lineal",
        16: "Hortaleza", 17: "Villaverde", 18: "Villa de Vallecas", 19: "Vicálvaro", 20: "San Blas-Canillejas",
        21: "Barajas"}

    # Mapear los nombres de los distritos
    df['distrito'] = df['cod_distrito'].map(mapa_distritos)

    # Crear la figura y los ejes
    plt.figure(figsize=(10, 6))
    
    # Graficar los puntos de la tasa de población con educación superior vs tasa de paro
    plt.scatter(df['tasa_poblacion_educacion_superior'], df['tasa_paro'], color='green', s=100, alpha=0.7)
    
    # Añadir etiquetas de distrito a los puntos
    for i, row in df.iterrows():
        plt.text(row['tasa_poblacion_educacion_superior'], row['tasa_paro'], row['distrito'])
    
    # Añadir títulos y etiquetas
    plt.title('Comparación entre la tasa de población con educación superior y tasa de paro por distrito')
    plt.ylabel('Tasa de paro (%)')
    
    # Mostrar el gráfico con una cuadrícula
    plt.grid(True)
    plt.show()

def graficar_intervenciones_seguridad(df):

    #Diccionario de nombres de distritos
    mapa_distritos = {
        1: "Centro", 2: "Arganzuela", 3: "Retiro", 4: "Salamanca", 5: "Chamartín",
        6: "Tetuán", 7: "Chamberí", 8: "Fuencarral-El Pardo", 9: "Moncloa-Aravaca", 10: "Latina",
        11: "Carabanchel", 12: "Usera", 13: "Puente de Vallecas", 14: "Moratalaz", 15: "Ciudad Lineal",
        16: "Hortaleza", 17: "Villaverde", 18: "Villa de Vallecas", 19: "Vicálvaro", 20: "San Blas-Canillejas",
        21: "Barajas"}

    # Mapear los nombres de los distritos
    df['distrito'] = df['cod_distrito'].map(mapa_distritos)

    # Crear la figura y los ejes
    plt.figure(figsize=(10, 6))
    
    # Graficar los puntos de la tasa de intervenciones policiales vs percepción de seguridad
    plt.scatter(df['tasa_intervenciones_policia'], df['percepcion_seguridad'], color='green', s=100, alpha=0.7)
    
    # Añadir etiquetas de distrito a los puntos
    for i, row in df.iterrows():
        plt.text(row['tasa_intervenciones_policia'], row['percepcion_seguridad'], row['distrito'])
    
    # Añadir títulos y etiquetas
    plt.title('Comparación entre la tasa de intervenciones policiales y la percepción de seguridad por distrito')
    plt.xlabel('Tasa de intervenciones policiales')
    plt.ylabel('Percepción de seguridad')
    
    # Mostrar el gráfico con una cuadrícula
    plt.grid(True)
    plt.show()

def graficar_pobreza_infantil_ss(df):

    #Diccionario de nombres de distritos
    mapa_distritos = {
        1: "Centro", 2: "Arganzuela", 3: "Retiro", 4: "Salamanca", 5: "Chamartín",
        6: "Tetuán", 7: "Chamberí", 8: "Fuencarral-El Pardo", 9: "Moncloa-Aravaca", 10: "Latina",
        11: "Carabanchel", 12: "Usera", 13: "Puente de Vallecas", 14: "Moratalaz", 15: "Ciudad Lineal",
        16: "Hortaleza", 17: "Villaverde", 18: "Villa de Vallecas", 19: "Vicálvaro", 20: "San Blas-Canillejas",
        21: "Barajas"}

    # Mapear los nombres de los distritos
    df['distrito'] = df['cod_distrito'].map(mapa_distritos)

    # Crear la figura y los ejes
    plt.figure(figsize=(10, 6))
    
    # Graficar los puntos de la tasa de intervenciones policiales vs percepción de seguridad
    plt.scatter(df['tasa_riesgo_pobreza_infantil'], df['tasa_personas_atendidas_ss'], color='green', s=100, alpha=0.7)
    
    # Añadir etiquetas de distrito a los puntos
    for i, row in df.iterrows():
        plt.text(row['tasa_riesgo_pobreza_infantil'], row['tasa_personas_atendidas_ss'], row['distrito'])
    
    # Añadir títulos y etiquetas
    plt.title('Comparación entre la tasa de riesgo de pobreza infantil y las personas atendidas por Servicios Sociales')
    plt.xlabel('Tasa de riesgo de pobreza infantil')
    plt.ylabel('Personas atendidas por Servicios Sociales') 
    
    # Mostrar el gráfico con una cuadrícula
    plt.grid(True)
    plt.show()

def graficar_renta_educacion_superior(df):

    #Diccionario de nombres de distritos
    mapa_distritos = {
        1: "Centro", 2: "Arganzuela", 3: "Retiro", 4: "Salamanca", 5: "Chamartín",
        6: "Tetuán", 7: "Chamberí", 8: "Fuencarral-El Pardo", 9: "Moncloa-Aravaca", 10: "Latina",
        11: "Carabanchel", 12: "Usera", 13: "Puente de Vallecas", 14: "Moratalaz", 15: "Ciudad Lineal",
        16: "Hortaleza", 17: "Villaverde", 18: "Villa de Vallecas", 19: "Vicálvaro", 20: "San Blas-Canillejas",
        21: "Barajas"}

    # Mapear los nombres de los distritos
    df['distrito'] = df['cod_distrito'].map(mapa_distritos)

    # Crear la figura y los ejes
    plt.figure(figsize=(10, 6))
    
    # Graficar los puntos de la tasa de intervenciones policiales vs percepción de seguridad
    plt.scatter(df['renta_media'], df['tasa_poblacion_educacion_superior'], color='green', s=100, alpha=0.7)
    
    # Añadir etiquetas de distrito a los puntos
    for i, row in df.iterrows():
        plt.text(row['renta_media'], row['tasa_poblacion_educacion_superior'], row['distrito'])
    
    # Añadir títulos y etiquetas
    plt.title('Comparación entre la renta media y la tasa de población con educación superior')
    plt.xlabel('Renta media')
    plt.ylabel('Personas con educación superior') 
    
    # Mostrar el gráfico con una cuadrícula
    plt.grid(True)
    plt.show()

def graficar_absentismo_pobreza_infantil(df):

    #Diccionario de nombres de distritos
    mapa_distritos = {
        1: "Centro", 2: "Arganzuela", 3: "Retiro", 4: "Salamanca", 5: "Chamartín",
        6: "Tetuán", 7: "Chamberí", 8: "Fuencarral-El Pardo", 9: "Moncloa-Aravaca", 10: "Latina",
        11: "Carabanchel", 12: "Usera", 13: "Puente de Vallecas", 14: "Moratalaz", 15: "Ciudad Lineal",
        16: "Hortaleza", 17: "Villaverde", 18: "Villa de Vallecas", 19: "Vicálvaro", 20: "San Blas-Canillejas",
        21: "Barajas"}

    # Mapear los nombres de los distritos
    df['distrito'] = df['cod_distrito'].map(mapa_distritos)

    # Crear la figura y los ejes
    plt.figure(figsize=(10, 6))
    
    # Graficar los puntos de la tasa de intervenciones policiales vs percepción de seguridad
    plt.scatter(df['tasa_absentismo'], df['tasa_riesgo_pobreza_infantil'], color='green', s=100, alpha=0.7)
    
    # Añadir etiquetas de distrito a los puntos
    for i, row in df.iterrows():
        plt.text(row['tasa_absentismo'], row['tasa_riesgo_pobreza_infantil'], row['distrito'])
    
    # Añadir títulos y etiquetas
    plt.title('Comparación entre la tasa de absentismo y la tasa de riesgo de pobreza infantil')
    plt.xlabel('Tasa de absentismo')
    plt.ylabel('Tasa de riesgo de pobreza infantil') 
    
    # Mostrar el gráfico con una cuadrícula
    plt.grid(True)
    plt.show()


def graficar_centros_salud(df):

    #Diccionario de nombres de distritos
    mapa_distritos = {
        1: "Centro", 2: "Arganzuela", 3: "Retiro", 4: "Salamanca", 5: "Chamartín",
        6: "Tetuán", 7: "Chamberí", 8: "Fuencarral-El Pardo", 9: "Moncloa-Aravaca", 10: "Latina",
        11: "Carabanchel", 12: "Usera", 13: "Puente de Vallecas", 14: "Moratalaz", 15: "Ciudad Lineal",
        16: "Hortaleza", 17: "Villaverde", 18: "Villa de Vallecas", 19: "Vicálvaro", 20: "San Blas-Canillejas",
        21: "Barajas"}

    # Mapear los nombres de los distritos
    df['distrito'] = df['cod_distrito'].map(mapa_distritos)

    # Crear la figura y los ejes
    plt.figure(figsize=(10, 6))
    
    # Graficar los puntos de la tasa de intervenciones policiales vs percepción de seguridad
    plt.scatter(df['tasa_centros_sanitarios'], df['autopercepcion_salud_buena'], color='green', s=100, alpha=0.7)
    
    # Añadir etiquetas de distrito a los puntos
    for i, row in df.iterrows():
        plt.text(row['tasa_centros_sanitarios'], row['autopercepcion_salud_buena'], row['distrito'])
    
    # Añadir títulos y etiquetas
    plt.title('Comparación entre la tasa de centros sanitarios y la buena salud de los habitantes')
    plt.xlabel('Tasa de centros sanitarios')
    plt.ylabel('Autopercepción de buena salud') 
    
    # Mostrar el gráfico con una cuadrícula
    plt.grid(True)
    plt.show()


def graficar_renta_vs_salud(df, variables_salud):
    # Crear una figura con subplots
    fig, axs = plt.subplots(len(variables_salud), 1, figsize=(8, 5 * len(variables_salud)))  # Un gráfico por variable
    fig.tight_layout(pad=4.0)  # Ajustar el espacio entre gráficos

    # Iterar sobre las variables de salud y crear un gráfico para cada una
    for i, variable in enumerate(variables_salud):
        ax = axs[i]
        ax.scatter(df['renta_media'], df[variable], color='blue', s=100, alpha=0.7)
        ax.set_xlabel('Renta media (€)')
        ax.set_ylabel(variable.replace('_', ' '))  # Etiquetar el eje Y con el nombre de la variable
        ax.set_title(f'Relación entre renta media y {variable.replace("_", " ")}')
        ax.grid(True)

    plt.show()