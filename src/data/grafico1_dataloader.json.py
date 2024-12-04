import pandas as pd
import sys
from cargar_enaho import cargar_enaho
import json

# Cargar la BD
data = cargar_enaho()
data.sort_values(by=['AÑO','MES','CONGLOME', 'VIVIENDA', 'HOGAR', 'CODPERSO'], inplace=True)

# Seleccionar datos relevantes
preguntas_nombres = [
  'Corrupción',
  'credibilidad y transparencia del gobierno',
  'La falta de empleo',
  'Falta de seguridad ciudadana',
  'Violencia en los hogares',
  'Falta de cobertura o mala atención en salud pública',
  'Falta de cobertura del sistema de seguridad social',
  'Mala calidad de la educación estatal',
  'Violación de derechos humanos',
  'Bajos sueldos o aumento de precios',
  'Pobreza',
  'Falta de vivienda',
  'Falta de apoyo a la agricultura',
  'Mal funcionamiento de la democracia',
  'Delincuencia',
  'Otro',
  'Ninguno',
]

preguntas_codigos = [f'P2_2${str(n).zfill(2)}' for n in range(1,17-1)]
problemas = data[
    ['AÑO','MES','CONGLOME', 'VIVIENDA', 'HOGAR', 'CODPERSO'] + preguntas_codigos
]

# Si se respondió
problemas.loc[:, preguntas_codigos] = problemas[preguntas_codigos].applymap(lambda x: 1 if x == "1" else 0)
#problemas.loc[:, preguntas_codigos] = problemas[preguntas_codigos].applymap(lambda x: 0 if x == " " else 1)

# Factor de expansion
problemas.loc[:, preguntas_codigos] = problemas[preguntas_codigos].multiply(data.FACTOR07, axis=0)

# Filtrar desde 2014 que es desde cuando se hace la pregunta
# problemas = problemas[problemas['AÑO'] >= 2014]

# Agrupar sumando
problemas_por_mes = problemas[['AÑO','MES'] + preguntas_codigos].groupby(['AÑO','MES']).sum()

# Salida de datos
problemas_json = {
    'data': []
}

for idx_pregunta in range(len(preguntas_codigos)):
  pregunta = preguntas_codigos[idx_pregunta]
  preg_nombre = preguntas_nombres[idx_pregunta]

  problema = pd.DataFrame(problemas_por_mes[pregunta])
  
  # Fechas
  problema['AÑO'] = problema.index.get_level_values(0)
  problema['MES'] = problema.index.get_level_values(1)
  problema['FECHA'] = problema['AÑO'].astype(str) + '-' + problema['MES'].astype(str).str.zfill(2)

  problema['TRIMESTRE'] = pd.to_datetime(problema['FECHA'], format='%Y-%m').dt.quarter
  problema['SEMESTRE'] = problema['MES'].apply(lambda x: 1 if x <= 6 else 2)
  problema.loc[:,'TRIMESTRE'] = problema['AÑO'].astype(str) + '-' + problema['TRIMESTRE'].astype(str).str.zfill(2)
  problema.loc[:,'SEMESTRE'] = problema['AÑO'].astype(str) + '-' + problema['SEMESTRE'].astype(str).str.zfill(2)

  # Nombre
  problema['PREGUNTA_NOM'] = preg_nombre
  
  cod = list(problema.columns)[0]
  problema['PREGUNTA_COD'] = pregunta
  problema.rename(columns={cod: 'VALOR'}, inplace=True)
  

  # Convertir
  dic = problema.to_dict(orient='records')
  problemas_json['data'] += dic

print(json.dumps(problemas_json['data']))