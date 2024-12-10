import pandas as pd
from cargar_enaho import cargar_enaho

#datos = pd.read_csv('D:/Estudio/ENEI/Proyecto integrador/Software/enaho-dashboard/datasets/ENAHO/784-Modulo85/Enaho01B-2022-2.csv',encoding='latin-1')
datos = cargar_enaho()
data = datos[["AÑO","MES","UBIGEO","ESTRATO","P23","FACTOR07"]]

filtered_df = data[data['P23'].notna() & (data['P23'] != None) & (data["P23"] != '' )]

clasif2 = {
    1.0: "Si",2.0: "No",3.0: "No",9.0: "No", "2":"No",2:"No",3:"No",1:"Si",9:"No","1":"Si","3":"No","9":"No"
}
clasificacion = {
    1: "Urbano",2: "Urbano",3: "Urbano",4: "Urbano", 5: "Rural",6: "Rural",7: "Rural",8: "Rural"
}

filtered_df.loc[:,"PAGO_EXTRA"] = filtered_df["P23"].map(clasif2)
filtered2 = filtered_df.dropna(subset=['PAGO_EXTRA'])
filtered2.loc[:,"ZONA"] = filtered2["ESTRATO"].map(clasificacion)
filtered2.drop(columns=["ESTRATO","UBIGEO","P23"], inplace=True)

df2 = filtered2

def calcular_periodo(fechas):
    periodos = []
    for i in range(len(fechas)):
        if i >= 5:  # Asegurar al menos 6 meses
            start_date = fechas.iloc[i-5]
            end_date = fechas.iloc[i]
            periodos.append(f"{start_date:%Y-%m} a {end_date:%Y-%m}")
        else:
            periodos.append(None)
    return periodos

### ZONA URBANA (SI)
df_si = df2[df2['PAGO_EXTRA'] == 'Si']
df_si = df_si[df_si['ZONA'] == 'Urbano']
resultado = df_si.groupby(["AÑO","MES","ZONA"])["FACTOR07"].sum().reset_index()
resultado['FECHA'] = pd.to_datetime({'year': resultado['AÑO'],'month': resultado['MES'],'day': 1})
df_si_a = resultado.sort_values(by=['ZONA', 'FECHA'])
df_si_a['FACTOR07'] = df_si_a['FACTOR07'].round(2)
df_si_a['SUMA_SEMESTRE_MOVIL'] = (
    df_si_a.groupby('ZONA')['FACTOR07']
    .rolling(window=6, min_periods=6)  # Ventana de 6 meses
    .sum()
    .reset_index(level=0, drop=True)
)
df_si_a['PERIODO_SEMESTRE_MOVIL'] = (
    df_si_a.groupby('ZONA')['FECHA']
    .transform(calcular_periodo)
)
df_final_urbano = df_si_a[["AÑO","ZONA","MES","PERIODO_SEMESTRE_MOVIL","SUMA_SEMESTRE_MOVIL"]]
df_final_urbano = df_final_urbano.drop(index=[0,1,2,3,4])
df_final_urbano = df_final_urbano[['PERIODO_SEMESTRE_MOVIL','ZONA','SUMA_SEMESTRE_MOVIL']]

#### ZONA URBANO (TOTAL) 
df_total_urbano = df2[df2['ZONA'] == 'Urbano']
df_total_urbano['FECHA'] = pd.to_datetime({'year': df_total_urbano['AÑO'],'month': df_total_urbano['MES'],'day': 1})
df_total_urbano = df_total_urbano.sort_values(by='FECHA')
df_total_urbano['FACTOR07'] = df_total_urbano['FACTOR07'].round(2)
df_total_urbano1 = df_total_urbano.groupby(["AÑO", "MES","ZONA"])["FACTOR07"].sum().reset_index()
df_total_urbano1['FECHA'] = pd.to_datetime({'year': df_total_urbano1['AÑO'],'month': df_total_urbano1['MES'],'day': 1})
df_total_urbano1 = df_total_urbano1.sort_values(by=['ZONA', 'FECHA'])
df_total_urbano1['SUMA_TOTAL_SEMESTRE_MOVIL'] = (
    df_total_urbano1.groupby('ZONA')['FACTOR07']
    .rolling(window=6, min_periods=6)  # Ventana de 6 meses
    .sum()
    .reset_index(level=0, drop=True)
)
df_total_urbano1['PERIODO_SEMESTRE_MOVIL'] = (
    df_total_urbano1.groupby('ZONA')['FECHA']
    .transform(calcular_periodo)
)
df_total_urbano1 = df_total_urbano1.drop(index=[0,1,2,3,4])
df_total_urbano1 = df_total_urbano1[['PERIODO_SEMESTRE_MOVIL','ZONA','SUMA_TOTAL_SEMESTRE_MOVIL']]
df_urbano_semestre_movil = pd.merge(df_final_urbano, df_total_urbano1, on=['ZONA', 'PERIODO_SEMESTRE_MOVIL'], how='inner')
# Dataframe unido
df_urbano_semestre_movil['Porcentaje'] = df_urbano_semestre_movil['SUMA_SEMESTRE_MOVIL'] / df_urbano_semestre_movil['SUMA_TOTAL_SEMESTRE_MOVIL']
df_urbano_semestre_movil['Porcentaje_100'] = df_urbano_semestre_movil['Porcentaje']*100
df_urbano_semestre_movil[['PERIODO_INICIO', 'PERIODO_FIN']] = df_urbano_semestre_movil['PERIODO_SEMESTRE_MOVIL'].str.split('a', expand=True)


### ZONA RURAL (SI)
df_si_rural = df2[df2['PAGO_EXTRA'] == 'Si']
df_si_rural = df_si_rural[df_si_rural['ZONA'] == 'Rural']
resultado_rural = df_si_rural.groupby(["AÑO","MES","ZONA"])["FACTOR07"].sum().reset_index()
resultado_rural['FECHA'] = pd.to_datetime({'year': resultado_rural['AÑO'],'month': resultado_rural['MES'],'day': 1})
resultado_rural_si = resultado_rural.sort_values(by=['ZONA', 'FECHA'])
resultado_rural_si['FACTOR07'] = resultado_rural_si['FACTOR07'].round(2)
resultado_rural_si['SUMA_SEMESTRE_MOVIL'] = (
    resultado_rural_si.groupby('ZONA')['FACTOR07']
    .rolling(window=6, min_periods=6)  # Ventana de 6 meses
    .sum()
    .reset_index(level=0, drop=True)
)
resultado_rural_si['PERIODO_SEMESTRE_MOVIL'] = (
    resultado_rural_si.groupby('ZONA')['FECHA']
    .transform(calcular_periodo)
)
resultado_rural_si = resultado_rural_si.drop(index=[0,1,2,3,4])
resultado_rural_si = resultado_rural_si[['PERIODO_SEMESTRE_MOVIL','ZONA','SUMA_SEMESTRE_MOVIL']]

### ZONA RURAL (TOTAL)
df_total_rural = df2[df2['ZONA'] == 'Rural']
df_total_rural['FECHA'] = pd.to_datetime({'year': df_total_rural['AÑO'],'month': df_total_rural['MES'],'day': 1})
df_total_rural = df_total_rural.sort_values(by='FECHA')
df_total_rural['FACTOR07'] = df_total_rural['FACTOR07'].round(2)
df_total_rural = df_total_rural.groupby(["AÑO", "MES","ZONA"])["FACTOR07"].sum().reset_index()
df_total_rural['FECHA'] = pd.to_datetime({'year': df_total_rural['AÑO'],'month': df_total_rural['MES'],'day': 1})
df_total_rural = df_total_rural.sort_values(by=['ZONA', 'FECHA'])
df_total_rural['SUMA_TOTAL_SEMESTRE_MOVIL'] = (
    df_total_rural.groupby('ZONA')['FACTOR07']
    .rolling(window=6, min_periods=6)  # Ventana de 6 meses
    .sum()
    .reset_index(level=0, drop=True)
)
df_total_rural['PERIODO_SEMESTRE_MOVIL'] = (
    df_total_rural.groupby('ZONA')['FECHA']
    .transform(calcular_periodo)
)
df_total_rural = df_total_rural.drop(index=[0,1,2,3,4])
df_total_rural1 = df_total_rural[['PERIODO_SEMESTRE_MOVIL','ZONA','SUMA_TOTAL_SEMESTRE_MOVIL']]
df_rural_semestre_movil = pd.merge(resultado_rural_si, df_total_rural1, on=['ZONA', 'PERIODO_SEMESTRE_MOVIL'], how='inner')
df_rural_semestre_movil['Porcentaje'] = df_rural_semestre_movil['SUMA_SEMESTRE_MOVIL'] / df_rural_semestre_movil['SUMA_TOTAL_SEMESTRE_MOVIL']
df_rural_semestre_movil['Porcentaje_100'] = df_rural_semestre_movil['Porcentaje']*100
df_rural_semestre_movil[['PERIODO_INICIO', 'PERIODO_FIN']] = df_rural_semestre_movil['PERIODO_SEMESTRE_MOVIL'].str.split('a', expand=True)


### ZONA TOTAL (SI)
df_si_total = df2[df2['PAGO_EXTRA'] == 'Si']
df_si_total["ZONA"] = 'TOTAL'
resultado_total_si = df_si_total.groupby(["AÑO","MES","ZONA"])["FACTOR07"].sum().reset_index()
resultado_total_si['FECHA'] = pd.to_datetime({'year': resultado_total_si['AÑO'],'month': resultado_total_si['MES'],'day': 1})
resultado_total_si = resultado_total_si.sort_values(by=['ZONA', 'FECHA'])
resultado_total_si['FACTOR07'] = resultado_total_si['FACTOR07'].round(2)
resultado_total_si['SUMA_SEMESTRE_MOVIL'] = (
    resultado_total_si.groupby('ZONA')['FACTOR07']
    .rolling(window=6, min_periods=6)  # Ventana de 6 meses
    .sum()
    .reset_index(level=0, drop=True)
)
resultado_total_si['PERIODO_SEMESTRE_MOVIL'] = (
    resultado_total_si.groupby('ZONA')['FECHA']
    .transform(calcular_periodo)
)
resultado_total_si = resultado_total_si.drop(index=[0,1,2,3,4])
resultado_total_si = resultado_total_si[['PERIODO_SEMESTRE_MOVIL','ZONA','SUMA_SEMESTRE_MOVIL']]

### ZONA TOTAL (TOTAL)
df_total_total = df2
df_total_total["ZONA"] = 'TOTAL'
df_total_total['FECHA'] = pd.to_datetime({'year': df_total_total['AÑO'],'month': df_total_total['MES'],'day': 1})
df_total_total = df_total_total.sort_values(by='FECHA')
df_total_total['FACTOR07'] = df_total_total['FACTOR07'].round(2)
df_total_total = df_total_total.groupby(["AÑO", "MES","ZONA"])["FACTOR07"].sum().reset_index()
df_total_total['FECHA'] = pd.to_datetime({'year': df_total_total['AÑO'],'month': df_total_total['MES'],'day': 1})
df_total_total = df_total_total.sort_values(by=['ZONA', 'FECHA'])
df_total_total['SUMA_TOTAL_SEMESTRE_MOVIL'] = (
    df_total_total.groupby('ZONA')['FACTOR07']
    .rolling(window=6, min_periods=6)  # Ventana de 6 meses
    .sum()
    .reset_index(level=0, drop=True)
)
df_total_total['PERIODO_SEMESTRE_MOVIL'] = (
    df_total_total.groupby('ZONA')['FECHA']
    .transform(calcular_periodo)
)
df_total_total1 = df_total_total.drop(index=[0,1,2,3,4])
df_total_total1 = df_total_total1[['PERIODO_SEMESTRE_MOVIL','ZONA','SUMA_TOTAL_SEMESTRE_MOVIL']]

df_total_semestre_movil = pd.merge(resultado_total_si, df_total_total1, on=['ZONA', 'PERIODO_SEMESTRE_MOVIL'], how='inner')
df_total_semestre_movil['Porcentaje'] = df_total_semestre_movil['SUMA_SEMESTRE_MOVIL'] / df_total_semestre_movil['SUMA_TOTAL_SEMESTRE_MOVIL']
df_total_semestre_movil['Porcentaje_100'] = df_total_semestre_movil['Porcentaje']*100
df_total_semestre_movil[['PERIODO_INICIO', 'PERIODO_FIN']] = df_total_semestre_movil['PERIODO_SEMESTRE_MOVIL'].str.split('a', expand=True)

#### DATAFRAME FINAL
df_concatenado = pd.concat([df_urbano_semestre_movil, df_rural_semestre_movil, df_total_semestre_movil], ignore_index=True)

# Convertir el DataFrame a JSON con formato 'records'
datos_json = df_concatenado.to_json(orient='records' )
print(datos_json)
# Guardar en un archivo JSON para usar en Observable
#with open('datos_observable.json', 'w', encoding='utf-8') as file:
 #   file.write(datos_json)
