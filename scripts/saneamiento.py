import pandas as pd
import hashlib

def obtener_sha256(ruta_fichero):
    sha = hashlib.sha256()
    with open(ruta_fichero, "rb") as f:
        for bloque in iter(lambda: f.read(4096), b""):
            sha.update(bloque)
    return sha.hexdigest()

# 1. SHA-256 del Fichero Original
hash_original = obtener_sha256("datos/telemetria_envios.csv")
print(f"SHA-256 Original: {hash_original}")

# 2. Carga y Limpieza del Dataset
df = pd.read_csv("datos/telemetria_envios.csv")

# Eliminar filas duplicadas
df = df.drop_duplicates()
# Eliminar nulos en campos clave
df = df.dropna(subset=['temp_celsius', 'peso_kg', 'destino'])

# Filtrar inconsistencias y valores fuera de rango
df = df[df['peso_kg'] > 0]
df = df[df['temp_celsius'] < 50]
df = df[df['estado_envio'] != 'DESCONOCIDO_ERROR']

# 3. Guardar Fichero Depurado
df.to_csv("datos/telemetria_limpia.csv", index=False)

# 4. SHA-256 del Fichero Depurado
hash_limpio = obtener_sha256("datos/telemetria_limpia.csv")
print(f"SHA-256 Depurado: {hash_limpio}")