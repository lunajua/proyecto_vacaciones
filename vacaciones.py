import datetime
from config import REGLAS_VACACIONES
from fechas import validar_fecha

def calcular_antiguedad(fecha_ingreso_str):
    fecha_ingreso = validar_fecha(fecha_ingreso_str)
    if not fecha_ingreso:
        return 0

    hoy = datetime.date.today()
    antiguedad = hoy.year - fecha_ingreso.year - ((hoy.month, hoy.day) < (fecha_ingreso.month, fecha_ingreso.day))
    return max(0, antiguedad)

def calcular_vacaciones_correspondientes(antiguedad):
    dias = 0
    for antiguedad_minima in sorted(REGLAS_VACACIONES.keys(), reverse=True):
        if antiguedad >= antiguedad_minima:
            dias = REGLAS_VACACIONES[antiguedad_minima]
            break
    return dias