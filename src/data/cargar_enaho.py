import os
import pandas as pd
import sys

# Ruta principal donde buscar las carpetas y archivos CSV
path = "datasets/ENAHO"

# Columnas para realizar el join
join_columns = ["AÑO", "MES", "CONGLOME", "VIVIENDA", "HOGAR", "CODPERSO", "CODINFOR", "UBIGEO", "DOMINIO", "ESTRATO"]

def cargar_enaho():
    # Lista para almacenar los DataFrames resultantes de cada carpeta
    folder_dataframes = []

    # Iterar sobre las carpetas en el directorio principal
    for folder_name in os.listdir(path):
        folder_path = os.path.join(path, folder_name)
        
        # Verificar si es una carpeta
        if os.path.isdir(folder_path):
            # Lista para almacenar DataFrames temporales de la carpeta actual
            folder_csvs = []
            
            # Iterar sobre los archivos dentro de la carpeta
            for file_name in os.listdir(folder_path):
                if file_name.endswith(".csv"):
                    sys.stderr.write(f"[cargar_enaho.py] 📊 Leyendo archivo {os.path.join(folder_path, file_name)}")
                    file_path = os.path.join(folder_path, file_name)
                    try:
                        # Leer el archivo CSV
                        df = pd.read_csv(file_path, encoding='latin-1')
                        
                        # Verificar que las columnas necesarias existan
                        if all(col in df.columns for col in join_columns):
                            folder_csvs.append(df)
                        else:
                            pass
                            # print(f"El archivo {file_path} no contiene las columnas requeridas y será ignorado.")
                    except Exception as e:
                        sys.stderr.write(f"[cargar_enaho.py] ❌ Error leyendo: {os.path.join(folder_path, file_name)}")
            
            # Si hay DataFrames en la carpeta, combinarlos
            if folder_csvs:
                folder_df = folder_csvs[0]
                for df in folder_csvs[1:]:
                    folder_df = folder_df.merge(df, on=join_columns, how='outer')
                
                # Agregar el DataFrame combinado de esta carpeta a la lista principal
                folder_dataframes.append(folder_df)
    
    # Combinar todos los DataFrames de las carpetas
    if folder_dataframes:
        final_combined_df = pd.concat(folder_dataframes, ignore_index=True)
        return final_combined_df
    else:
        raise Exception("No se encontraron archivos válidos para combinar en ninguna carpeta.")