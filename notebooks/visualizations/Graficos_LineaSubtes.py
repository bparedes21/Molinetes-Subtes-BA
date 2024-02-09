import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.ticker as ticker

# Asumiendo que 'dataframes_lineas' es tu DataFrame con la información
# de líneas, estaciones y cantidad de pasajeros

def generar_tabla_estaciones_top(dataframes_lineas): 
    # Agrupar por línea y estación, obtener la suma total de pasajeros por grupo
    por_linea_estacion = dataframes_lineas.groupby(['LINEA', 'ESTACION'])['pax_TOTAL'].sum().reset_index()

    # Encontrar la estación con más pasajeros por cada línea (top 1)
    top1_por_linea = por_linea_estacion.loc[por_linea_estacion.groupby('LINEA')['pax_TOTAL'].idxmax()]

    # Ordenar el DataFrame por el ID de la línea
    top1_por_linea = top1_por_linea.sort_values(by='LINEA')

    # Ordenar el DataFrame por la columna 'pax_TOTAL' en orden descendente
    top1_por_linea_estacion = top1_por_linea.sort_values(by='pax_TOTAL', ascending=False)

    # Crear un DataFrame con las columnas necesarias
    table_data = pd.DataFrame({
        'LINEA': top1_por_linea_estacion['LINEA'],
        'ESTACION': top1_por_linea_estacion['ESTACION'],
        'Pasajeros': top1_por_linea_estacion['pax_TOTAL']
    })

    # Mostrar la tabla
    #display(table_data)

    # Crear una tabla usando pandas y matplotlib
    fig, ax = plt.subplots(figsize=(10, 6)) 
    ax.axis('tight')
    ax.axis('off')

    # Agregar una fila con celdas vacías para el espacio del título sombreado
    ax.table(cellText=[[''] * len(table_data.columns)],
            colLabels=table_data.columns,
            cellLoc='center', 
            loc='bottom',
            bbox=[0, 1, 1, 0.1],
            cellColours=[['lightgray'] * len(table_data.columns)])

    # Agregar la tabla de datos
    table = ax.table(cellText=table_data.values,
                    colLabels=table_data.columns,
                    cellLoc='center', 
                    loc='center')

    # Rellenar el título de las columnas con color gris
    for key, cell in table.get_celld().items():
        if key[0] == 0:
            cell.set_facecolor('lightgray')

    # Guardar la tabla como una imagen (por ejemplo, en formato PNG)
    plt.savefig('tabla.png', format='png', bbox_inches='tight')


def generar_tabla_promedio_pasajeros(dataframes_lineas):
    # Calcular la suma total de pasajeros por línea
    suma_pasajeros_por_linea = dataframes_lineas.groupby('LINEA')['pax_TOTAL'].sum().reset_index()

    # Contar la cantidad de estaciones por línea
    estaciones_por_linea = dataframes_lineas.groupby('LINEA')['ESTACION'].nunique().reset_index()

    # Calcular el promedio de pasajeros por estación para cada línea
    promedio_por_linea = suma_pasajeros_por_linea.merge(estaciones_por_linea, on='LINEA')
    promedio_por_linea['Promedio_Pasajeros'] = promedio_por_linea['pax_TOTAL'] / promedio_por_linea['ESTACION']

    # Redondear el promedio de pasajeros por línea
    promedio_por_linea['Promedio_Pasajeros'] = promedio_por_linea['Promedio_Pasajeros'].round()

    # Ordenar el DataFrame por el promedio de pasajeros en orden descendente
    promedio_por_linea = promedio_por_linea.sort_values(by='Promedio_Pasajeros', ascending=False)

    # Crear un DataFrame con las columnas necesarias
    table_data = pd.DataFrame({
        'ID_Línea': promedio_por_linea['LINEA'],
        'Promedio_Pasajeros': promedio_por_linea['Promedio_Pasajeros']
    })

    # Mostrar la tabla
    #display(table_data)

    # Crear una tabla usando pandas y matplotlib
    fig, ax = plt.subplots(figsize=(6, 8)) 
    ax.axis('tight')
    ax.axis('off')

    # Agregar una fila con celdas vacías para el espacio del título sombreado
    ax.table(cellText=[[''] * len(table_data.columns)],
             colLabels=table_data.columns,
             cellLoc='center', 
             loc='bottom',
             bbox=[0, 1, 1, 0.1],
             cellColours=[['lightgray'] * len(table_data.columns)])

    # Asegúrate de que highlight tenga la longitud correcta
    max_promedio = promedio_por_linea['Promedio_Pasajeros'].max()
    highlight = ['yellow' if promedio == max_promedio else 'white' for promedio in promedio_por_linea['Promedio_Pasajeros']]

    # Crear una lista de listas de colores para cada fila en la tabla
    cellColours = [['yellow' if promedio == max_promedio else 'white'] * len(table_data.columns) for promedio in promedio_por_linea['Promedio_Pasajeros']]

    # Agregar la tabla de datos
    table = ax.table(cellText=table_data.values,
                     colLabels=table_data.columns,
                     cellLoc='center', 
                     loc='center',
                     cellColours=cellColours)

    # Rellenar el título de las columnas con color gris
    for key, cell in table.get_celld().items():
        if key[0] == 0:
            cell.set_facecolor('lightgray')

    # Guardar la tabla como una imagen (por ejemplo, en formato PNG)
    plt.savefig('tabla_promedio.png', format='png', bbox_inches='tight')


def grafico_pasajeros_por_hora(dataframes_lineas):
    # Seleccionar solo las columnas relevantes para el gráfico de barras
    columns_for_plot = ['HORA_RANGO', 'pax_TOTAL']

    # Filtrar el DataFrame para incluir solo las columnas seleccionadas
    df_for_plot = dataframes_lineas[columns_for_plot]

    # Agrupar por 'Hora' y sumar la cantidad total de pasajeros por hora
    total_pasajeros_por_hora = df_for_plot.groupby('HORA_RANGO')['pax_TOTAL'].sum().reset_index()

    # Convertir la cantidad de pasajeros a miles
    total_pasajeros_por_hora['pax_TOTAL'] /= 1000

    # Establecer un estilo de fondo blanco
    sns.set(style="whitegrid")

    # Tamaño del gráfico
    plt.figure(figsize=(12, 6))

    # Gráfico de barras utilizando barplot
    ax = sns.barplot(
        data=total_pasajeros_por_hora,
        x='HORA_RANGO',
        y='pax_TOTAL',
        color='skyblue',  # Color de las barras
        edgecolor='black',  # Agregar bordes a las barras para mayor claridad
    )

    # Añadir título y etiquetas de los ejes
    plt.title('Total de pasajeros por hora (en miles)', fontsize=18)
    plt.xlabel('Hora del día', fontsize=14)
    plt.ylabel('Cantidad de Pasajeros (Miles)', fontsize=14)

    # Rotación de las etiquetas del eje x para mejorar la legibilidad
    plt.xticks(rotation=45)

    # Formatear el eje y para mostrar los valores en miles
    ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, pos: '{:,.0f}'.format(x)))

    # Ajustar diseño y espacio entre las barras
    sns.despine()
    plt.tight_layout()

    # Guardar el gráfico como una imagen
    plt.savefig('grafico_pasajeros_por_hora.png')

    # Mostrar el gráfico
    plt.show()


def grafico_pasajeros_por_linea(dataframes_lineas):
    # Seleccionar solo las columnas relevantes para el gráfico de barras
    columns_for_plot = ['LINEA', 'pax_TOTAL']

    # Filtrar el DataFrame para incluir solo las columnas seleccionadas
    df_for_plot = dataframes_lineas[columns_for_plot]

    # Agrupar por 'Línea', obtener la suma total de pasajeros por línea
    total_pasajeros_por_linea = df_for_plot.groupby('LINEA')['pax_TOTAL'].sum().reset_index()

    # Ordenar el DataFrame por la columna 'pax_TOTAL' en orden descendente
    total_pasajeros_por_linea = total_pasajeros_por_linea.sort_values(by='pax_TOTAL', ascending=False)

    # Establecer un estilo de fondo blanco
    sns.set(style="whitegrid")

    # Definir colores para cada línea
    colores_lineas = {'LineaA': 'lightblue', 'LineaB': 'red', 'LineaC': 'violet', 'LineaD': 'limegreen', 'LineaE': 'blue', 'LineaH': 'yellow'}

    # Tamaño del gráfico
    plt.figure(figsize=(12, 6))

    # Gráfico de barras
    sns.barplot(
        data=total_pasajeros_por_linea,
        x='LINEA',
        y='pax_TOTAL',
        palette=colores_lineas,  # Definir colores para cada línea
    )

    # Añadir título y etiquetas de los ejes
    plt.title('Cantidad total de pasajeros por línea de subte', fontsize=16)
    plt.xlabel('Línea de Subte', fontsize=14)
    plt.ylabel('Cantidad de Pasajeros', fontsize=14)

    # Rotación de las etiquetas del eje x para mejorar la legibilidad
    plt.xticks(rotation=45)

    # Ajustar diseño y espacio entre las barras
    sns.despine()
    plt.tight_layout()

    # Guardar el gráfico como una imagen
    plt.savefig('grafico_pasajeros_lineas.png')

    # Mostrar el gráfico
    plt.show()

def guardar_grafico_pasajeros_por_estacion_linea_B(dataframes_lineas):
    # Seleccionar solo las columnas relevantes para el gráfico de barras
    columns_for_plot = ['ESTACION', 'pax_TOTAL']

    # Filtrar el DataFrame para incluir solo las columnas seleccionadas y las estaciones de la línea B
    df_linea_b = dataframes_lineas[dataframes_lineas['LINEA'] == 'LineaB'][columns_for_plot]

    # Agrupar por 'Estación', obtener la suma total de pasajeros por estación
    total_pasajeros_por_estacion = df_linea_b.groupby('ESTACION')['pax_TOTAL'].sum().reset_index()

    # Ordenar el DataFrame por la columna 'pax_TOTAL' en orden ascendente
    total_pasajeros_por_estacion = total_pasajeros_por_estacion.sort_values(by='pax_TOTAL', ascending=True)

    # Establecer una paleta de colores rojos degradados
    colores_rojos = sns.color_palette("Reds", n_colors=len(total_pasajeros_por_estacion))

    # Establecer un estilo de fondo blanco
    sns.set(style="whitegrid")

    # Tamaño del gráfico
    plt.figure(figsize=(14, 8))

    # Gráfico de barras
    sns.barplot(
        data=total_pasajeros_por_estacion,
        x='ESTACION',
        y='pax_TOTAL',
        palette=colores_rojos,  # Paleta de colores rojos degradados
    )

    # Añadir título y etiquetas de los ejes
    plt.title('Cantidad total de pasajeros por estación de la Línea B', fontsize=18)
    plt.xlabel('Estación de Subte (Línea B)', fontsize=14)
    plt.ylabel('Cantidad de Pasajeros', fontsize=14)

    # Rotación de las etiquetas del eje x para mejorar la legibilidad
    plt.xticks(rotation=45, ha='right')

    # Ajustar diseño y espacio entre las barras
    sns.despine()
    plt.tight_layout()

    # Guardar el gráfico como una imagen
    plt.savefig('grafico_pasajeros_lineaB_estaciones.png')

    # Mostrar el gráfico
    plt.show()


def guardar_grafico_estacion_mayor_pasajeros(dataframes_lineas):
    # Agrupar por línea y estación, obtener la suma total de pasajeros por grupo
    por_linea_estacion = dataframes_lineas.groupby(['LINEA', 'ESTACION'])['pax_TOTAL'].sum().reset_index()

    # Encontrar la estación con más pasajeros por cada línea (top 1)
    top1_por_linea = por_linea_estacion.loc[por_linea_estacion.groupby('LINEA')['pax_TOTAL'].idxmax()]

    # Ordenar el DataFrame por la columna 'LINEA'
    top1_por_linea = top1_por_linea.sort_values(by='LINEA')

    # Ordenar el DataFrame por la columna 'pax_TOTAL' en orden descendente
    top1_por_linea_estacion = top1_por_linea.sort_values(by='pax_TOTAL', ascending=False)

    # Definir colores para cada línea
    colores_lineas = {'LineaA': 'lightblue', 'LineaB': 'red', 'LineaC': 'violet', 'LineaD': 'limegreen', 'LineaE': 'blue', 'LineaH': 'yellow'}

    # Crear un gráfico de barras con colores específicos para cada línea
    plt.figure(figsize=(12, 6))
    plt.bar(top1_por_linea_estacion['ESTACION'], top1_por_linea_estacion['pax_TOTAL'], color=top1_por_linea_estacion['LINEA'].map(colores_lineas))
    plt.title('Estación con más pasajeros por línea')
    plt.xlabel('Estación de Subte')
    plt.ylabel('Cantidad de Pasajeros')
    plt.xticks(rotation=45, ha='right')  # Rotar las etiquetas del eje x para mejorar la legibilidad

    # Guardar la imagen con el nombre "estacion_con_mayor_cantidad_de_pasajeros.png"
    plt.savefig('estacion_con_mayor_cantidad_de_pasajeros.png', format='png', bbox_inches='tight')
    plt.show()


def guardar_grafico_pasajeros_por_mes(dataframes_lineas):
    # Asumiendo que 'FECHA' es una cadena (string) en formato 'YYYY-MM-DD'
    dataframes_lineas['FECHA'] = pd.to_datetime(dataframes_lineas['FECHA'], format='%d/%m/%Y')

    # Extraer el mes de la fecha
    dataframes_lineas['MES'] = dataframes_lineas['FECHA'].dt.month_name()

    # Agrupar por mes y línea, obtener la suma total de pasajeros por grupo
    total_pasajeros_por_mes_linea = dataframes_lineas.groupby(['MES'])['pax_TOTAL'].sum().reset_index()
    # Ordenar los meses por la cantidad total de pasajeros en orden ascendente
    total_pasajeros_por_mes_linea = total_pasajeros_por_mes_linea.sort_values(by='pax_TOTAL')

    # Establecer un estilo de fondo blanco
    sns.set(style="whitegrid")

    # Tamaño del gráfico
    plt.figure(figsize=(14, 8))

    # Gráfico de barras
    sns.barplot(
        data=total_pasajeros_por_mes_linea,
        x='MES',
        y='pax_TOTAL',
        palette='viridis',  # Puedes ajustar la paleta de colores según tus preferencias
    )

    # Añadir título y etiquetas de los ejes
    plt.title('Total de pasajeros por línea y mes', fontsize=18)
    plt.xlabel('Mes', fontsize=14)
    plt.ylabel('Total de Pasajeros', fontsize=14)

    # Rotación de las etiquetas del eje x para mejorar la legibilidad
    plt.xticks(rotation=45)

    # Ajustar diseño y espacio entre las barras
    sns.despine()
    plt.tight_layout()
    
    # Guardar el gráfico como una imagen (puedes ajustar el formato según tus necesidades)
    plt.savefig('gráfico_meses.png')
    
    # Mostrar el gráfico
    plt.show()


def guardar_tabla_suma_pasajeros(dataframes_lineas):
    # Calcular el promedio de pasajeros por línea
    promedio_por_linea = dataframes_lineas.groupby('LINEA')['pax_TOTAL'].sum().reset_index()

    # Ordenar el DataFrame por el promedio de pasajeros en orden descendente
    promedio_por_linea = promedio_por_linea.sort_values(by='pax_TOTAL', ascending=False)

    # Crear una tabla usando pandas y matplotlib
    fig, ax = plt.subplots(figsize=(10, 6)) 
    ax.axis('tight')
    ax.axis('off')

    # Crear un DataFrame con las columnas necesarias
    table_data = pd.DataFrame({
        'Línea': promedio_por_linea['LINEA'],
        'Promedio Pasajeros': promedio_por_linea['pax_TOTAL']
    })

    # Colores para el fondo de las celdas
    colors = [['lightgrey', 'lightgrey']] * len(table_data)

    # Resaltar la fila con el máximo promedio en amarillo
    max_promedio_index = table_data['Promedio Pasajeros'].idxmax()
    colors[max_promedio_index] = ['yellow', 'yellow']

    # Agregar la tabla al gráfico
    table = ax.table(cellText=table_data.values,
                     colLabels=table_data.columns,
                     cellLoc='center',
                     loc='center',
                     cellColours=colors)

    # Establecer el formato de la tabla
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.auto_set_column_width(col=list(range(len(table_data.columns))))

    # Agregar título a la tabla
    table.auto_set_column_width(col=list(range(len(table_data.columns))))
    table.scale(1, 1.5)  # Ajustar la altura de las filas para el título

    # Guardar la tabla como una imagen (por ejemplo, en formato PNG)
    plt.savefig('tabla_suma_pasajeros.png', format='png', bbox_inches='tight')
