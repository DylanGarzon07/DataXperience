import pandas as pd
import numpy as np

# 1. Cargar el conjunto de datos desde el CSV
df = pd.read_csv('Data CallCenter.csv')

# 2. Eliminar filas que sean iguales (duplicados)
df = df.drop_duplicates()

# 3. Limpiar y estandarizar columnas de texto
columnas_texto = ['Agente', 'Departamento']
for col in columnas_texto:
    # Convertir a texto, quitar espacios al inicio/final y poner mayúscula inicial
    df[col] = df[col].astype(str).str.strip().str.title()
    # Reemplazar la palabra 'Nan' por un valor nulo real de numpy
    df[col] = df[col].replace('Nan', np.nan)

# 4. Limpiar variable numérica de la duración de llamadas
# Quitar la palabra " seg" para dejar solo el número
df['Duracion_Segundos'] = df['Duracion_Segundos'].astype(str).str.replace(' seg', '', regex=False)
# Convertir la columna a formato numérico (forzando errores a nulos)
df['Duracion_Segundos'] = pd.to_numeric(df['Duracion_Segundos'], errors='coerce')
# Reemplazar duraciones negativas por valores nulos temporalmente
df['Duracion_Segundos'] = df['Duracion_Segundos'].apply(lambda x: x if x >= 0 else np.nan)

# 5. Estandarizar Fechas
# format='mixed' y dayfirst=True le permiten a Pandas leer múltiples formatos sin borrar los datos
df['Fecha_Hora'] = pd.to_datetime(df['Fecha_Hora'], format='mixed', dayfirst=True, errors='coerce')

# Eliminar la zona horaria (si existe) para que Excel no genere errores al guardar
df['Fecha_Hora'] = df['Fecha_Hora'].dt.tz_localize(None)

# 6. Limpiar valores atípicos (La satisfacción en encuestas debe ser del 1 al 5)
df['Nivel_Satisfaccion'] = df['Nivel_Satisfaccion'].apply(
    lambda x: x if pd.notna(x) and 1 <= x <= 5 else np.nan
)

# 7. Manejo de valores nulos (Rellenar espacios vacíos)
df['Agente'] = df['Agente'].fillna('Sin Asignar')
df['Departamento'] = df['Departamento'].fillna('Desconocido')
# Usar la mediana para no afectar el promedio con los nulos de duración y satisfacción
df['Duracion_Segundos'] = df['Duracion_Segundos'].fillna(df['Duracion_Segundos'].median())
df['Nivel_Satisfaccion'] = df['Nivel_Satisfaccion'].fillna(df['Nivel_Satisfaccion'].median())

# 8. Corregir columna de control para el conteo de llamadas
df['Llamadas_Totales'] = 1

# 9. Exportar tabla depurada a Excel (.xlsx) sin la columna de índice
df.to_excel('Data CallCenter Limpia.xlsx', index=False)

# Imprimir confirmación y resumen de los datos para la evidencia del proyecto
print("Archivo exportado exitosamente como 'Data CallCenter Limpia.xlsx'")
print(df.info())