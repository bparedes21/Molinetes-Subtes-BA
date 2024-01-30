import os
import csv
import pandas as pd
from datetime import datetime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import func
# Función para convertir el número entero a formato de tiempo
def convertir_a_tiempo(hora_entera):

    # Crear un objeto de tiempo con la hora
    tiempo = pd.to_datetime(str(hora_entera % 24), format='%H').time()
    return tiempo

def Procesar_DF(df_procesado,names_columns):
    #names_columns=['FECHA;DESDE;HASTA;LINEA;MOLINETE;ESTACION;pax_pagos;pax_pases_pagos;pax_franq;pax_TOTAL']
    names_columns1=[column_name.split(';') for column_name in names_columns]
   
    # Assuming df_procesado is your DataFrame and new_column_names is a list of new column names
    df_procesado.rename(columns=dict(zip(df_procesado.columns,names_columns1[0] )), inplace=True)
    # Unir las columnas 'DESDE' y 'HASTA' con un guion medio y crear una nueva columna 'RANGO'
   
    df_procesado['RANGO'] = df_procesado['DESDE'] + '-' + df_procesado['HASTA']
    
    df_procesado['DESDE1'] = pd.to_datetime(df_procesado['DESDE'], format='%H:%M:%S')
    df_procesado['HORA']=df_procesado['DESDE1'].dt.hour
    df_procesado['HORA_RANGO'] = df_procesado['HORA'].apply(convertir_a_tiempo)

    df_procesado.drop(columns=['DESDE1','HORA'], inplace=True)

    return df_procesado

def transformar_primer_csv(indice,archivo_csv):
    print(indice)
    # Lista para almacenar las líneas modificadas
    lineas_modificadas = []

 
    with open(archivo_csv, 'r', newline='', encoding='utf-8-sig') as file:
        # Crear un objeto CSV Reader
        csv_reader = csv.reader(file, delimiter=';')
        # Inicializar columns_df fuera del bloque with
        columns_df=next(csv_reader)

        # Recorrer cada línea en el archivo
        for linea in csv_reader:
            # Modificar la línea eliminando el primer y último caracter
            linea_modificada = [campo[1:-1] if campo.startswith('"') else campo for campo in linea]
            
            # Agregar la línea modificada a la lista
            lineas_modificadas.append(linea_modificada)


    df_salida_comas_y_comillas = pd.DataFrame([linea[0].split(';') for linea in lineas_modificadas])
   
    return df_salida_comas_y_comillas,columns_df

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

def crear_dataframe_y_cargar(carpeta, session,tabla_destino,clase):


    # Ruta de la carpeta que contiene los archivos CSV
    df_procesado=pd.DataFrame()
    for i, archivo in enumerate(os.listdir(carpeta)):
        if archivo.endswith('.csv'):  # Asegúrate de que solo estás leyendo archivos CSV
            archivo_csv = os.path.join(carpeta, archivo)
            

            print(archivo_csv)
            
            df_procesado,names_columns=transformar_primer_csv(i,archivo_csv)
            df_procesado_final=Procesar_DF(df_procesado,names_columns)
            print(df_procesado_final.shape)
            break

                
    # Iterar sobre las filas y agregar cada una a la base de datos
    for index, row in df_procesado.iterrows():

        session.add(clase(**row.to_dict()))


    # Commit para guardar los cambios en la base de datos
    session.commit()
