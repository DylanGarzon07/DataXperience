import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

# 1. Cargar el dataset limpio generado en la Etapa 1
df = pd.read_excel('Data CallCenter Limpia.xlsx')

# 2. Preparar la variable objetivo (Target)
# Convertimos el texto del estado a binario: 1 (Abandonada) y 0 (Atendida)
df['Es_Abandonada'] = (df['Estado'].str.lower().str.contains('abandonada')).astype(int)

# 3. Seleccionar las variables predictoras (Features)
# Usaremos la duración, el departamento y el tipo de llamada para encontrar patrones de abandono
X = df[['Duracion_Segundos', 'Departamento', 'Tipo_Llamada']]

# Convertir variables categóricas de texto a numéricas (One-Hot Encoding)
X = pd.get_dummies(X, columns=['Departamento', 'Tipo_Llamada'], drop_first=True)
y = df['Es_Abandonada']

# 4. Dividir los datos: 80% para entrenar el modelo y 20% para evaluarlo
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 5. Instanciar y entrenar el modelo de Regresión Logística
modelo = LogisticRegression(max_iter=1000)
modelo.fit(X_train, y_train)

# 6. Evaluar el rendimiento del modelo con los datos de prueba (test)
predicciones_test = modelo.predict(X_test)
precision = accuracy_score(y_test, predicciones_test)

# Imprimir la precisión para tener el dato en la presentación del video
print(f"Precisión del modelo de clasificación: {precision * 100:.2f}%")

# 7. Generar predicciones para toda la base de datos
df['Prediccion_Abandono'] = modelo.predict(X)
df['Probabilidad_Abandono_%'] = np.round(modelo.predict_proba(X)[:, 1] * 100, 2)

# Crear una etiqueta amigable para usar como filtro en Power BI
df['Riesgo_Llamada'] = df['Prediccion_Abandono'].apply(
    lambda x: 'Alto Riesgo de Abandono' if x == 1 else 'Atención Segura'
)

# 8. Exportar la tabla final para su consumo en la herramienta de BI
df.to_excel('Data CallCenter con Predicciones.xlsx', index=False)
print("Archivo 'Data CallCenter con Predicciones.xlsx' generado exitosamente.")