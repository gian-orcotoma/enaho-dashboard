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

datos1 = filtered2
# Convertir el DataFrame a JSON con formato 'records'
datos_json = datos1.to_json(orient='records' )
print(datos_json)
# Guardar en un archivo JSON para usar en Observable
#with open('datos_observable.json', 'w', encoding='utf-8') as file:
 #   file.write(datos_json)
