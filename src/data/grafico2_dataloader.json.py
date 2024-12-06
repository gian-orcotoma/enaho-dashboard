import pandas as pd
import cargar_enaho

#datos = pd.read_csv('/Users/cynthiacevallos/Downloads/enaho-dashboard-main/datasets/ENAHO/data/Enaho01B-2023-2.csv',encoding='latin-1')
datos = cargar_enaho()


#datos = datos
meses = {
    1: 'Enero',
    2: 'Febrero',
    3: 'Marzo',
    4: 'Abril',  # O ajustar a 'Semiurbano' si es necesario
    5: 'Mayo',
    6: 'Junio',
    7: 'Julio',
    8: 'Agosto',
    9: 'Setiembre',
    10: 'Octubre',
    11: 'Noviembre',
    12: 'Diciembre'
}


clasificacion = {
    1: 'Urbano',
    2: 'Urbano',
    3: 'Urbano',
    4: 'Urbano',  # O ajustar a 'Semiurbano' si es necesario
    5: 'Rural',
    6: 'Rural',
    7: 'Rural',
    8: 'Rural'
}

clasif2 = {
    1: 'Si',
    2: 'No',
    3: 'No',
}

# Crear un DataFrame como ejemplo
datos1 = datos[["AÑO","MES","UBIGEO","ESTRATO","P23","FACTOR07"]]
#print([col for col in datos.columns if "P2C" in col])  # Filtra nombres relacionados
datos1.loc[:, 'ZONA'] = datos['ESTRATO'].map(clasificacion)
datos1.loc[:, 'MES_NOMBRE'] = datos['MES'].map(meses)
#datos1.loc[:, 'PAGO_EXTRA'] = datos['P2C$06'].map(clasif2)
datos1.loc[:, 'PAGO_EXTRA'] = datos['P23'].map(clasif2)

# Ordenar por la clave 'mes' usando el índice en el orden de meses

# Convertir el DataFrame a JSON con formato 'records'
datos_json = datos1.to_json(orient='records', indent=4)

# Guardar en un archivo JSON para usar en Observable
with open('datos_observable.json', 'w', encoding='utf-8') as file:
    file.write(datos_json)