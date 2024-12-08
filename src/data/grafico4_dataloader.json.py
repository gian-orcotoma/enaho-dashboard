import pandas as pd
import json
import os

entidades_nombres = {
  1:'Jurado Nacional de Elecciones',
  2:'ONPE',
  3:'RENIEC',
  4:'Municipalidad Provincial',
  5:'Municipalidad Distrital',
  6:'Policía Nacional del Perú',
  7:'Fuerzas Armadas',
  8:'Gobierno Regional',
  9:'Poder Judicial',
  10:'Ministerio de Educación',
  11:'Defensoría del Pueblo',
  12:'Congreso de la República',
  13:'Partidos Políticos',
  14:'Prensa Escrita',
  15:'Radio y Televisión',
  16:'Iglesia Católica',
  17:'Procuraduría Anticorrupción',
  18:'Ministerio Público - Fiscalía de la Nación',
  19:'Contraloría General de la República',
  20:'SUNAD o SUNAT',
  21:'Comisión de Alto Nivel Anticorrupción',
}

MESES = {
    "Ene":"01", "Feb":"02", "Mar":"03", "Abr":"04",
    "May":"05", "Jun":"06", "Jul":"07", "Ago":"08",
    "Set":"09", "Sep":"09", "Oct":"10", "Nov":"11", "Dic":"12",
}

def convertir_fecha(fecha):
  fecha = fecha.split(' ')
  return f'{fecha[1]}-{MESES.get(fecha[0])}'

def obtener_mes(periodo):
  mes_fin = periodo.split('-')[1]
  fecha = mes_fin.split()
  return f'{fecha[1]}-{MESES.get(fecha[0])}'



path = "datasets/Datacrim_Confianza_Entidades"

# Juntar datos
dataframes = []
for cod_entidad in range(1,21+1):
    # Leer el DF
    data = pd.read_csv(os.path.join(path, f"{cod_entidad}.csv"),  encoding='utf-8')
    data.drop_duplicates(inplace=True)
    data.columns = ['Periodo', 'Ambito', 'Confianza', 'Porcentaje']
    data = data[~data.Periodo.str.contains("CV")]
    data = data[data['Ambito'] == 'NACIONAL']
    data.columns = ['Periodo', 'Ambito', 'Confianza', 'Porcentaje']

    """
    # Formatear datos
    data.loc[:,'Confianza'] = data['Confianza'].replace({
    'NO SABE': 'NS',
    'NADA / POCO': 'NO',
    'SUFICIENTE / BASTANTE': 'SI'
    })
    """

    """
    data_pivot = pd.pivot_table(data, 
        index=['Periodo', 'Ambito'],  # Las filas
        columns='Confianza',            # Las columnas a pivotear
        values='Porcentaje',                  # Los valores a mostrar
        aggfunc='sum',                           # Función de agregación
        fill_value=0
    ).reset_index()
    data_pivot.rename(columns={
        'NO SABE': 'NS',
        'NADA / POCO': 'NO',
        'SUFICIENTE / BASTANTE': 'SI'
    }, inplace=True)
    """
    
    # Agregando columnas utiles
    data['Codigo'] = cod_entidad
    data['Entidad'] = entidades_nombres[cod_entidad]
    data['Mes'] = data['Periodo'].apply(obtener_mes)
    dataframes.append(data)

entidades = pd.concat(
    dataframes,
    axis=0
)
print(json.dumps(entidades.to_dict(orient='records')))