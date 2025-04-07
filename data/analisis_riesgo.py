import pandas as pd

# Cargar el CSV
df = pd.read_csv("riesgo_oropouche.csv")

# Mostrar las zonas de alto riesgo
print("-------- ZONAS DE ALTO RIESGO --------")
alto_riesgo = df[df["Riesgo"] == "Alto"]
print(alto_riesgo[["Municipio", "Zona", "Latitud", "Longitud", "Notas"]])