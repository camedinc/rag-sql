#------------------------------------------------------------------------------
# Script que unifica los .csv en un consolidado
#------------------------------------------------------------------------------
import pandas as pd
#import pandas as pd
import glob
import os

# Ruta base
base_path = "archive/Data"
print(base_path)

# Lista de prefijos de los archivos
prefixes = ["merged_movies_data"]
print(prefixes)

for prefix in prefixes:
    all_files = []  # Lista para almacenar los DataFrames
    
    # Buscar archivos en cada carpeta
    for folder in os.listdir(base_path):
        folder_path = os.path.join(base_path, folder)
        
        if os.path.isdir(folder_path):  # Solo procesar carpetas
            file_pattern = os.path.join(folder_path, f"{prefix}_*.csv")
            files = glob.glob(file_pattern)  # Buscar archivos que coincidan
            
            for file in files:
                df = pd.read_csv(file)  # Leer archivo
                all_files.append(df)  # Agregarlo a la lista
    
    # Si encontramos archivos, los concatenamos
    if all_files:
        final_df = pd.concat(all_files, ignore_index=True)  # Unimos los DataFrames
        #final_df.to_csv(f"{prefix}.csv", index=False)  # Guardamos el archivo final
        final_df.to_csv(f"data_clean/{prefix}.csv", index=False)  # Guardamos el archivo final en la carpeta 'data_clean'


print("Archivos consolidados generados!")