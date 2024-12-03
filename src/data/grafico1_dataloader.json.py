import pandas as pd
import sys
from cargar_enaho import cargar_enaho
import json

# Cargar la BD

data = cargar_enaho()
data.sort_values(by=['AÑO','MES','CONGLOME', 'VIVIENDA', 'HOGAR', 'CODPERSO'], inplace=True)

# Seleccionar datos relevantes
preguntas = [f'P2_1${str(n).zfill(2)}' for n in range(1,17-1)]
problemas = data[
    ['AÑO','MES','CONGLOME', 'VIVIENDA', 'HOGAR', 'CODPERSO'] + preguntas
]

# Si se respondió
problemas.loc[:, preguntas] = problemas[preguntas].replace("0", pd.NA).isna()

# Factor de expansion
problemas.loc[:, preguntas] = problemas[preguntas].multiply(data.FACTOR07, axis=0)

# Agrupar sumando
problemas_por_mes = problemas[['AÑO','MES'] + preguntas].groupby(['AÑO','MES']).sum()

problemas_json = {
    'data': []
}

for col in problemas_por_mes:
  col = pd.DataFrame(problemas_por_mes[col])
  
  # Fechas
  col['AÑO'] = col.index.get_level_values(0)
  col['MES'] = col.index.get_level_values(1)
  
  # Nombre
  nombre = list(col.columns)[0]
  col['PREGUNTA'] = nombre
  col.rename(columns={nombre: 'VALOR'}, inplace=True)
  dic = col.to_dict(orient='records')
  problemas_json['data'] += dic
  break

print(json.dumps(problemas_json))