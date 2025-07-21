import datetime

def validar_fecha(fecha_str):
    try:
        return datetime.datetime.strptime(fecha_str, "%Y-%m-%d").date()
    except ValueError:
        return None

def calcular_dias_entre_fechas(fecha_inicio_str, fecha_fin_str):
    fecha_inicio = validar_fecha(fecha_inicio_str)
    fecha_fin = validar_fecha(fecha_fin_str)
    if not fecha_inicio or not fecha_fin or fecha_inicio > fecha_fin:
        return -1
    return (fecha_fin - fecha_inicio).days + 1