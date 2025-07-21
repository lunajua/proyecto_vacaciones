import os
import json
from config import DATA_FILE

def cargar_empleados():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError:
            print(f"Advertencia: El archivo '{DATA_FILE}' está corrupto. Se iniciará vacío.")
            return []
    return []

def guardar_empleados(empleados):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(empleados, f, indent=4, ensure_ascii=False)
    print(f"Datos guardados en '{DATA_FILE}'.")