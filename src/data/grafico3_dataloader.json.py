import pandas as pd
import unicodedata

archivo = "/Users/cynthiacevallos/Downloads/enaho-dashboard-main/datasets/Datacrim_Corrupcion/P23.xls"
archivo1 = "/Users/cynthiacevallos/Downloads/enaho-dashboard-main/datasets/Datacrim_Corrupcion/P23-Sexo.xls"
archivo2 = "/Users/cynthiacevallos/Downloads/enaho-dashboard-main/datasets/Datacrim_Corrupcion/P23-Educacion.xls"

try:
    with open(archivo, 'r', encoding='latin-1') as f:
        html_content = f.read()
    tablas = pd.read_html(html_content, decimal=',',thousands='.')
    df = tablas[0]
    resultado = df
except Exception as e:
    resultado = str(e)

def remove_tildes(text):
    return ''.join(c for c in unicodedata.normalize('NFKD', text) if not unicodedata.combining(c))

resultado1 = resultado.head(9)
resultado1 = resultado1.drop(resultado1.columns[2], axis=1)
resultado1.columns = resultado1.columns.droplevel(0)  # Quitar el primer nivel del MultiIndex
df_melted = resultado1.melt(id_vars=['ÁMBITO GEOGRÁFICO', 'SE SINTIÓ OBLIGADO O DIO VOLUNTARIAMENTE REGALOS'],var_name='Periodo',value_name='Valor')
df_melted = df_melted.sort_values(by=['Periodo','ÁMBITO GEOGRÁFICO'])
df_melted = df_melted.rename(columns={
    'ÁMBITO GEOGRÁFICO': 'ZONA',
    'SE SINTIÓ OBLIGADO O DIO VOLUNTARIAMENTE REGALOS': 'P23',
    'Periodo': 'Periodo'
})
# Aplicar la función a la columna 'Respuesta'
df_melted['P23'] = df_melted['P23'].apply(remove_tildes)
df_3 = df_melted.copy()
df_3["VARIABLE"] = "ZONA"
df_3 = df_3.rename(columns={'ZONA': 'VARIABLE_2'})
df_3 = df_3.loc[df_3["VARIABLE_2"] != "NACIONAL"]
df_3["NIVEL"] = 1


try:
    with open(archivo1, 'r', encoding='latin-1') as f:
        html_content = f.read()
    tablas = pd.read_html(html_content, decimal=',',thousands='.')
    df = tablas[0]
    resultado = df
except Exception as e:
    resultado = str(e)

resultado1s = resultado.head(6)
resultado1s = resultado1s.drop(resultado1s.columns[2], axis=1)
resultado1s.columns = resultado1s.columns.droplevel(0)  # Quitar el primer nivel del MultiIndex
df_melted = resultado1s.melt(id_vars=['SEXO', 'SE SINTIÓ OBLIGADO O DIO VOLUNTARIAMENTE REGALOS'],var_name='Periodo',value_name='Valor')
df_melted = df_melted.sort_values(by=['Periodo','SEXO'])
df_melted = df_melted.rename(columns={
    'SE SINTIÓ OBLIGADO O DIO VOLUNTARIAMENTE REGALOS': 'P23',
    'Periodo': 'Periodo'
})
df_melted['P23'] = df_melted['P23'].apply(remove_tildes)
df_31 = df_melted.copy()
df_31["NIVEL"] = 2
df_31["VARIABLE"] = "SEXO"
df_31 = df_31.rename(columns={'SEXO': 'VARIABLE_2'})

try:
    with open(archivo2, 'r', encoding='latin-1') as f:
        html_content = f.read()
    tablas = pd.read_html(html_content, decimal=',',thousands='.')
    df = tablas[0]
    resultado = df
except Exception as e:
    resultado = str(e)

resultado1e = resultado.head(9)
resultado1e = resultado1e.drop(resultado1e.columns[2], axis=1)
resultado1e.columns = resultado1e.columns.droplevel(0) 
df_melted = resultado1e.melt(id_vars=['NIVEL EDUCATIVO', 'SE SINTIÓ OBLIGADO O DIO VOLUNTARIAMENTE REGALOS'],var_name='Periodo',value_name='Valor')
df_melted = df_melted.sort_values(by=['Periodo','NIVEL EDUCATIVO'])
df_melted = df_melted.rename(columns={
    'SE SINTIÓ OBLIGADO O DIO VOLUNTARIAMENTE REGALOS': 'P23',
    'Periodo': 'Periodo'
})

def remove_tildes(text):
    return ''.join(c for c in unicodedata.normalize('NFKD', text) if not unicodedata.combining(c))

# Aplicar la función a la columna 'Respuesta'
df_melted['P23'] = df_melted['P23'].apply(remove_tildes)
df_melted['NIVEL EDUCATIVO'] = df_melted['NIVEL EDUCATIVO'].str.replace('PRIMARIA 1/', 'PRIMARIA')


df_32 = df_melted.copy()
df_32["NIVEL"] = 3
df_32["VARIABLE"] = "NIVEL EDUCATIVO"
df_32 = df_32.rename(columns={'NIVEL EDUCATIVO': 'VARIABLE_2'})

result = pd.concat([df_3, df_31,df_32], ignore_index=True)

json_result = result.to_json(orient='records')

# Mostrar el JSON resultante
print(json_result)









