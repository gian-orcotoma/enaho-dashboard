import pandas as pd
import json
import os

path = 'datasets/Datacrim_Utilidad_Democracia'

# Leer datos
data = pd.read_csv(os.path.join(path, 'UtilidadDemocracia Nov2015-Dic2023.csv'))
data.columns = ['Periodo','Departamento','Utilidad','Porcentaje']

# Filtrar necesarios
democracia_elecciones = data.loc[data["Utilidad"] == "PARA ELEGIR AUTORIDADES"]
democracia_elecciones = democracia_elecciones[~data.Periodo.str.contains("CV")]
#democracia_elecciones.sort_values(by=['Departamento'], inplace=True)

# Resultado
print(json.dumps(democracia_elecciones.to_dict(orient='records')))