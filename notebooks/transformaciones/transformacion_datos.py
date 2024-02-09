import os
import csv
import pandas as pd
from datetime import datetime

import os
import csv
import pandas as pd
from datetime import datetime


def convertir_a_tiempo(hora_entera):
    # Obtener la hora del Timestamp si es necesario
    if isinstance(hora_entera, pd.Timestamp):
        hora_entera = hora_entera.hour

    # Crear un objeto de tiempo con la hora
    tiempo = datetime.strptime(str(hora_entera % 24), '%H').time()
    return tiempo

def procesar_dataframe(df_procesado, names_columns):
    """
    Procesa un DataFrame.

    Args:
    - df_procesado: DataFrame a procesar.
    - names_columns: Lista de nombres de columnas.

    Returns:
    - df_procesado: DataFrame procesado.
    """
    # Convierte los nombres de columnas en una lista de listas
    names_columns1 = [column_name.split(';') for column_name in names_columns]

    # Renombra las columnas del DataFrame
    df_procesado.rename(columns=dict(zip(df_procesado.columns, names_columns1[0])), inplace=True)

    # Combina las columnas 'DESDE' y 'HASTA' para crear la columna 'RANGO'
    df_procesado['RANGO'] = df_procesado['DESDE'] + '-' + df_procesado['HASTA']

    # Convierte la columna 'DESDE' a formato datetime y extrae la hora
    df_procesado['HORA'] = pd.to_datetime(df_procesado['DESDE'], format='%H:%M:%S')


    # Aplica la función 'convertir_a_tiempo' para obtener la hora del rango
    df_procesado['HORA_RANGO'] = df_procesado['HORA'].apply(convertir_a_tiempo)

    return df_procesado




def transformar_csv_a_dataframe(indice, archivo_csv):
    """
    Transforma todos los archivos CSV.
    
    Args:
    - indice: Índice del archivo CSV que se está procesando.
    - archivo_csv: Ruta al archivo CSV.
    
    Returns:
    - df_salida_comas_y_comillas: DataFrame que contiene los datos modificados.
    - columns_df: Lista de nombres de columnas.
    """
    print(indice)  # Imprime el índice para seguir el progreso
    
    # Lista para almacenar las líneas modificadas
    lineas_modificadas = []
    
    # Abre el archivo CSV
    with open(archivo_csv, 'r', newline='', encoding='utf-8-sig') as file:
        # Crea un objeto lector de CSV
        csv_reader = csv.reader(file, delimiter=';')
        
        # Obtiene los nombres de las columnas
        columns_df = next(csv_reader)
        
        # Itera a través de cada línea en el archivo
        for linea in csv_reader:
            # Modifica la línea eliminando el primer y último carácter
            linea_modificada = [campo[1:-1] if campo.startswith('"') else campo for campo in linea]
            
            # Agrega la línea modificada a la lista
            lineas_modificadas.append(linea_modificada)
    
    # Crea un DataFrame a partir de las líneas modificadas
    df_salida_comas_y_comillas = pd.DataFrame([linea[0].split(';') for linea in lineas_modificadas])
    
    return df_salida_comas_y_comillas, columns_df

"""
def transformar_todos_csvs(indice,archivo_csv):
    print(indice)
    # Lista para almacenar las líneas modificadas
    lineas_modificadas = []

 
    with open(archivo_csv, 'r', newline='', encoding='utf-8-sig') as file:
        # Crear un objeto CSV Reader
        csv_reader = csv.reader(file, delimiter=';')
        next(csv_reader)
        # Recorrer cada línea en el archivo
        for linea in csv_reader:
            # Modificar la línea eliminando el primer y último caracter
            linea_modificada = [campo[1:-1] if campo.startswith('"') else campo for campo in linea]
            
            # Agregar la línea modificada a la lista
            lineas_modificadas.append(linea_modificada)


    df_salida_comas_y_comillas = pd.DataFrame([linea[0].split(';') for linea in lineas_modificadas])
    return df_salida_comas_y_comillas
"""


def ejecutar_transformacion_y_unificacion_de_dataframes(carpeta):
    """
    Carga archivos CSV desde una carpeta, los convierte en DataFrames y los combina en uno solo con carga incremental.

    Args:
    - carpeta: Ruta de la carpeta que contiene los archivos CSV.

    Returns:
    - df_final: DataFrame combinado.
    """
  
    df_final = pd.DataFrame()
    df_procesado_final= pd.DataFrame()
    # Itera sobre cada archivo en la carpeta
    for i, archivo in enumerate(os.listdir(carpeta)):
        # Verifica si el archivo es un CSV
        if archivo.endswith('.csv'):
            # Construye la ruta completa al archivo CSV
            archivo_csv = os.path.join(carpeta, archivo)

            # Imprime la ruta del archivo para seguimiento
            print(archivo_csv)

            # Transforma el archivo CSV en un DataFrame y lo procesa
            df_procesado, nombres_columnas = transformar_csv_a_dataframe(i, archivo_csv)
            df_procesado_final = procesar_dataframe(df_procesado, nombres_columnas)
            if(i!=0):
                # Lee el DataFrame final desde el archivo CSV (actualización por cada iteración)
                df_final = pd.read_csv('df_final_name.csv', low_memory=False)

                # Concatena el DataFrame procesado al DataFrame final
                df_final = pd.concat([df_final, df_procesado_final], ignore_index=True, axis=0)
                
            # Guarda el DataFrame final en un archivo CSV (excepto para la primera iteración)
            
                df_final.to_csv('df_final_name.csv', index=False)
                print("!=0",df_final.shape)
            else:
                df_procesado_final.to_csv('df_final_name.csv', index=False)
                print("primer",df_procesado_final.shape)

              # Inicializa un DataFrame vacío para almacenar los datos
            df_final = pd.DataFrame()
            df_procesado_final= pd.DataFrame()
            # Libera memoria
            del df_final
            del df_procesado_final
            df_final = pd.DataFrame()
            df_procesado_final= pd.DataFrame()

    # Imprime la forma del DataFrame final para seguimiento
    print("Forma del DataFrame final:", df_final.shape)
    
    return df_final
