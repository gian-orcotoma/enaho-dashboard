import pandas as pd
import unicodedata
import sys

archivo = "datasets/Datacrim_Opinion_Gestion_Gobierno/Opinion_Gestion_Gob_Central.xls"
archivo2 = "datasets/Datacrim_Opinion_Gestion_Gobierno/Opinion_Gestion_Gob_Regional.xls"
archivo3 = "datasets/Datacrim_Opinion_Gestion_Gobierno/Opinion_Gestion_Gob_Local.xls"


def procesar_file(archivo):
  try:
      with open(archivo, 'r', encoding='latin-1') as f:
          html_content = f.read()
      tablas = pd.read_html(html_content, decimal=',',thousands='.')
      df = tablas[0]
      resultado = df
      return resultado
  except Exception as e:
      sys.stderr.write(e)
      sys.stderr.write(archivo)
      resultado = str(e)
      return resultado
  

def remove_tildes(text):
    return ''.join(c for c in unicodedata.normalize('NFKD', text) if not unicodedata.combining(c))


df1 = procesar_file(archivo)
df11 = df1.head(90)
df11 = df11.drop(df11.columns[2], axis=1)
df11.columns = df11.columns.droplevel(0)  # Quitar el primer nivel del MultiIndex
df_melted = df11.melt(id_vars=['ÁMBITO GEOGRÁFICO', 'OPINIÓN DE LA POBLACIÓN'],var_name='Periodo',value_name='Valor')
df_melted = df_melted.sort_values(by=['Periodo','ÁMBITO GEOGRÁFICO'])
df_melted = df_melted.rename(columns={
    'ÁMBITO GEOGRÁFICO': 'ZONA',
    'OPINIÓN DE LA POBLACIÓN': 'OPINION DE LA POBLACION',
    'Periodo': 'Periodo'
})
# Aplicar la función a la columna 'Respuesta'
df_melted['OPINION DE LA POBLACION'] = df_melted['OPINION DE LA POBLACION'].apply(remove_tildes)
df_21 = df_melted.copy()
df_21["PREGUNTA"] = "GOBIERNO CENTRAL"


df12 = procesar_file(archivo3)
df122 = df12.head(90)
df122 = df122.drop(df122.columns[2], axis=1)
df122.columns = df122.columns.droplevel(0)  # Quitar el primer nivel del MultiIndex
df_melted = df122.melt(id_vars=['ÁMBITO GEOGRÁFICO', 'OPINIÓN DE LA POBLACIÓN'],var_name='Periodo',value_name='Valor')
df_melted = df_melted.sort_values(by=['Periodo','ÁMBITO GEOGRÁFICO'])
df_melted = df_melted.rename(columns={
    'ÁMBITO GEOGRÁFICO': 'ZONA',
    'OPINIÓN DE LA POBLACIÓN': 'OPINION DE LA POBLACION',
    'Periodo': 'Periodo'
})
# Aplicar la función a la columna 'Respuesta'
df_melted['OPINION DE LA POBLACION'] = df_melted['OPINION DE LA POBLACION'].apply(remove_tildes)
df_22 = df_melted.copy()
df_22["PREGUNTA"] = "GOBIERNO LOCAL"


df13 = procesar_file(archivo2)
df123 = df13.head(90)
df123 = df123.drop(df123.columns[2], axis=1)
df123.columns = df123.columns.droplevel(0)  # Quitar el primer nivel del MultiIndex
df_melted = df123.melt(id_vars=['ÁMBITO GEOGRÁFICO', 'OPINIÓN DE LA POBLACIÓN'],var_name='Periodo',value_name='Valor')
df_melted = df_melted.sort_values(by=['Periodo','ÁMBITO GEOGRÁFICO'])
df_melted = df_melted.rename(columns={
    'ÁMBITO GEOGRÁFICO': 'ZONA',
    'OPINIÓN DE LA POBLACIÓN': 'OPINION DE LA POBLACION',
    'Periodo': 'Periodo'
})
# Aplicar la función a la columna 'Respuesta'
df_melted['OPINION DE LA POBLACION'] = df_melted['OPINION DE LA POBLACION'].apply(remove_tildes)
df_23 = df_melted.copy()
df_23["PREGUNTA"] = "GOBIERNO REGIONAL"

# Unir todos lod df
result = pd.concat([df_21, df_22,df_23], ignore_index=True)
result = result.loc[result["OPINION DE LA POBLACION"] != "NO SABE / NO RESPONDE"]
json_result = result.to_json(orient='records')
print(json_result)


