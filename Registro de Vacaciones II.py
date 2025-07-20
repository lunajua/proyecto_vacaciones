import datetime
import json
import os

# --- Configuración ---
# Nombre del archivo donde se guardarán los datos de los empleados
DATA_FILE = "empleados.json"

# Reglas de vacaciones: Días de vacaciones según la antigüedad en años
# Puedes ajustar estas reglas según las políticas de tu empresa o leyes locales
REGLAS_VACACIONES = {
    0: 14,  # Menos de 5 años (por ejemplo, 14 días)
    5: 21,  # De 5 a menos de 10 años, 21 días
    10: 28, # De 10 a menos de 20 años, 28 días
    20: 35  # 20 años o más, 35 días
}

# --- Funciones de Utilidad ---

def cargar_empleados():
    """Carga los datos de los empleados desde un archivo JSON."""
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError:
            print(f"Advertencia: El archivo '{DATA_FILE}' está corrupto o vacío. Se iniciará con una lista de empleados vacía.")
            return []
    return [] # Retorna una lista vacía si el archivo no existe

def guardar_empleados(empleados):
    """Guarda los datos de los empleados en un archivo JSON."""
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(empleados, f, indent=4, ensure_ascii=False)
    print(f"Datos guardados en '{DATA_FILE}'.")

def validar_fecha(fecha_str):
    """Valida que una cadena sea una fecha válida en formato AAAA-MM-DD."""
    try:
        return datetime.datetime.strptime(fecha_str, "%Y-%m-%d").date()
    except ValueError:
        return None

def calcular_antiguedad(fecha_ingreso_str):
    """
    Calcula la antigüedad en años de un empleado.
    Args:
        fecha_ingreso_str (str): Fecha de ingreso en formato 'AAAA-MM-DD'.
    Returns:
        int: Antigüedad en años.
    """
    fecha_ingreso = validar_fecha(fecha_ingreso_str)
    if not fecha_ingreso:
        return 0 # Retorna 0 si la fecha de ingreso no es válida

    hoy = datetime.date.today()
    # Calcula la diferencia en años. Ajusta si el cumpleaños no ha pasado aún.
    antiguedad = hoy.year - fecha_ingreso.year - ((hoy.month, hoy.day) < (fecha_ingreso.month, fecha_ingreso.day))
    return max(0, antiguedad) # Asegura que la antigüedad no sea negativa

def calcular_vacaciones_correspondientes(antiguedad):
    """
    Calcula los días de vacaciones que le corresponden a un empleado
    basado en su antigüedad y las reglas definidas.
    Args:
        antiguedad (int): Antigüedad del empleado en años.
    Returns:
        int: Días de vacaciones correspondientes.
    """
    dias = 0
    # Itera sobre las reglas de vacaciones en orden descendente de antigüedad
    # para encontrar la regla aplicable.
    for antiguedad_minima in sorted(REGLAS_VACACIONES.keys(), reverse=True):
        if antiguedad >= antiguedad_minima:
            dias = REGLAS_VACACIONES[antiguedad_minima]
            break
    return dias

def calcular_dias_entre_fechas(fecha_inicio_str, fecha_fin_str):
    """
    Calcula la cantidad de días entre dos fechas (inclusive).
    Args:
        fecha_inicio_str (str): Fecha de inicio en formato 'AAAA-MM-DD'.
        fecha_fin_str (str): Fecha de fin en formato 'AAAA-MM-DD'.
    Returns:
        int: Número de días, o -1 si las fechas no son válidas o el inicio es posterior al fin.
    """
    fecha_inicio = validar_fecha(fecha_inicio_str)
    fecha_fin = validar_fecha(fecha_fin_str)

    if not fecha_inicio or not fecha_fin:
        print("Error: Formato de fecha inválido. Use AAAA-MM-DD.")
        return -1
    if fecha_inicio > fecha_fin:
        print("Error: La fecha de inicio no puede ser posterior a la fecha de fin.")
        return -1

    delta = fecha_fin - fecha_inicio
    return delta.days + 1 # +1 para incluir el día de fin

# --- Funciones de Gestión de Empleados ---

def agregar_empleado(empleados):
    """Permite al usuario agregar un nuevo empleado a la lista."""
    print("\n--- Agregar Nuevo Empleado ---")
    
    # Nuevo campo: Número de Legajo
    numero_legajo = input("Número de Legajo: ").strip()
    # Opcional: Podrías añadir una validación para asegurar que el legajo sea único
    # for emp in empleados:
    #     if emp.get("numero_legajo") == numero_legajo:
    #         print("Error: Ya existe un empleado con este número de legajo.")
    #         return

    nombre = input("Nombre: ").strip().title()
    apellido = input("Apellido: ").strip().title()
    sector = input("Sector: ").strip().title()

    fecha_ingreso_valida = False
    while not fecha_ingreso_valida:
        fecha_ingreso_str = input("Fecha de ingreso (AAAA-MM-DD): ").strip()
        if validar_fecha(fecha_ingreso_str):
            fecha_ingreso_valida = True
        else:
            print("Formato de fecha inválido. Por favor, use AAAA-MM-DD.")

    vacaciones_periodo_anterior_valida = False
    while not vacaciones_periodo_anterior_valida:
        try:
            vacaciones_periodo_anterior = int(input("Días de vacaciones del período anterior (0 si no aplica): ").strip())
            if vacaciones_periodo_anterior >= 0:
                vacaciones_periodo_anterior_valida = True
            else:
                print("Los días de vacaciones del período anterior no pueden ser negativos.")
        except ValueError:
            print("Entrada inválida. Por favor, ingrese un número entero.")


    antiguedad = calcular_antiguedad(fecha_ingreso_str)
    vacaciones_correspondientes = calcular_vacaciones_correspondientes(antiguedad)

    nuevo_empleado = {
        "numero_legajo": numero_legajo,
        "nombre": nombre,
        "apellido": apellido,
        "sector": sector,
        "fecha_ingreso": fecha_ingreso_str,
        "vacaciones_periodo_anterior": vacaciones_periodo_anterior, # Nuevo campo
        "vacaciones_tomadas": [], # Lista para almacenar los periodos de vacaciones tomados
        "saldo_vacaciones_pendiente": vacaciones_correspondientes + vacaciones_periodo_anterior, # Saldo inicial incluyendo período anterior
        "last_vacation_update_year": datetime.date.today().year # Año de la última actualización anual
    }
    empleados.append(nuevo_empleado)
    print(f"Empleado '{nombre} {apellido}' (Legajo: {numero_legajo}) agregado con éxito.")
    guardar_empleados(empleados)

def mostrar_empleados(empleados):
    """Muestra la lista de todos los empleados con sus detalles."""
    if not empleados:
        print("\nNo hay empleados registrados.")
        return

    print("\n--- Lista de Empleados ---")
    for i, emp in enumerate(empleados):
        antiguedad = calcular_antiguedad(emp["fecha_ingreso"])
        vacaciones_corresp = calcular_vacaciones_correspondientes(antiguedad)
        
        # Asegurarse de que los nuevos campos existan para compatibilidad con datos antiguos
        if "vacaciones_periodo_anterior" not in emp:
            emp["vacaciones_periodo_anterior"] = 0
        if "saldo_vacaciones_pendiente" not in emp: # Renombrado de dias_vacaciones_restantes
            emp["saldo_vacaciones_pendiente"] = vacaciones_corresp + emp["vacaciones_periodo_anterior"]
        if "last_vacation_update_year" not in emp:
            emp["last_vacation_update_year"] = 0 # Se actualizará en la opción 4

        print(f"\n[{i+1}] {emp.get('numero_legajo', 'N/A')} - {emp['nombre']} {emp['apellido']}")
        print(f"    Sector: {emp['sector']}")
        print(f"    Fecha de Ingreso: {emp['fecha_ingreso']}")
        print(f"    Antigüedad: {antiguedad} años")
        print(f"    Vacaciones Correspondientes (este período): {vacaciones_corresp} días")
        print(f"    Vacaciones del Período Anterior: {emp['vacaciones_periodo_anterior']} días") # Nuevo campo
        print(f"    Saldo de Vacaciones Pendiente: {emp['saldo_vacaciones_pendiente']} días") # Renombrado
        if emp["vacaciones_tomadas"]:
            print("    Vacaciones Tomadas:")
            for vac in emp["vacaciones_tomadas"]:
                print(f"        Desde: {vac['inicio']} Hasta: {vac['fin']} ({vac['dias']} días)")
        else:
            print("    Vacaciones Tomadas: Ninguna")

def registrar_vacaciones(empleados):
    """Permite registrar un período de vacaciones para un empleado."""
    if not empleados:
        print("\nNo hay empleados para registrar vacaciones.")
        return

    mostrar_empleados(empleados) # Muestra la lista para que el usuario elija
    try:
        indice = int(input("\nIngrese el número del empleado para registrar vacaciones: ")) - 1
        if not (0 <= indice < len(empleados)):
            print("Número de empleado inválido.")
            return
    except ValueError:
        print("Entrada inválida. Por favor, ingrese un número.")
        return

    empleado = empleados[indice]
    print(f"\n--- Registrar Vacaciones para {empleado['nombre']} {empleado['apellido']} (Legajo: {empleado.get('numero_legajo', 'N/A')}) ---")

    # Asegurarse de que el campo exista antes de usarlo
    if "saldo_vacaciones_pendiente" not in empleado:
        antiguedad = calcular_antiguedad(empleado["fecha_ingreso"])
        vacaciones_corresp = calcular_vacaciones_correspondientes(antiguedad)
        empleado["saldo_vacaciones_pendiente"] = vacaciones_corresp + empleado.get("vacaciones_periodo_anterior", 0)
        guardar_empleados(empleados) # Guarda para actualizar el archivo si el campo no existía

    fecha_inicio_valida = False
    while not fecha_inicio_valida:
        fecha_inicio_str = input("Fecha de inicio de vacaciones (AAAA-MM-DD): ").strip()
        if validar_fecha(fecha_inicio_str):
            fecha_inicio_valida = True
        else:
            print("Formato de fecha inválido. Por favor, use AAAA-MM-DD.")

    fecha_fin_valida = False
    while not fecha_fin_valida:
        fecha_fin_str = input("Fecha de fin de vacaciones (AAAA-MM-DD): ").strip()
        if validar_fecha(fecha_fin_str):
            fecha_fin_valida = True
        else:
            print("Formato de fecha inválido. Por favor, use AAAA-MM-DD.")

    dias_tomados = calcular_dias_entre_fechas(fecha_inicio_str, fecha_fin_str)

    if dias_tomados > 0:
        if empleado["saldo_vacaciones_pendiente"] >= dias_tomados: # Usando el nuevo campo
            empleado["vacaciones_tomadas"].append({
                "inicio": fecha_inicio_str,
                "fin": fecha_fin_str,
                "dias": dias_tomados
            })
            empleado["saldo_vacaciones_pendiente"] -= dias_tomados # Descontando del nuevo campo
            print(f"Vacaciones registradas. Se descontaron {dias_tomados} días.")
            print(f"Saldo restante para {empleado['nombre']}: {empleado['saldo_vacaciones_pendiente']} días.")
            guardar_empleados(empleados)
        else:
            print(f"Error: El empleado no tiene suficientes días de vacaciones pendientes ({empleado['saldo_vacaciones_pendiente']} días) para tomar {dias_tomados} días.")
    else:
        print("No se pudieron registrar las vacaciones debido a fechas inválidas.")

# --- Menú Principal ---

def main_menu():
    """Función principal que ejecuta el menú interactivo del programa."""
    empleados = cargar_empleados() # Carga los empleados al iniciar el programa

    while True:
        print("\n--- Sistema de Gestión de Empleados ---")
        print("1. Agregar Empleado")
        print("2. Ver Empleados")
        print("3. Registrar Vacaciones")
        print("4. Actualizar Vacaciones Anuales (Recomendado al inicio de cada año)")
        print("5. Salir")

        opcion = input("Seleccione una opción: ").strip()

        if opcion == '1':
            agregar_empleado(empleados)
        elif opcion == '2':
            mostrar_empleados(empleados)
        elif opcion == '3':
            registrar_vacaciones(empleados)
        elif opcion == '4':
            print("\n--- Actualizando Vacaciones Anuales ---")
            current_year = datetime.date.today().year
            updates_made = False
            for emp in empleados:
                # Asegurarse de que los campos existan para compatibilidad con datos antiguos
                if "vacaciones_periodo_anterior" not in emp:
                    emp["vacaciones_periodo_anterior"] = 0
                if "saldo_vacaciones_pendiente" not in emp:
                    antiguedad = calcular_antiguedad(emp["fecha_ingreso"])
                    vacaciones_corresp = calcular_vacaciones_correspondientes(antiguedad)
                    emp["saldo_vacaciones_pendiente"] = vacaciones_corresp + emp["vacaciones_periodo_anterior"]
                if "last_vacation_update_year" not in emp:
                    emp["last_vacation_update_year"] = 0 # Inicializar si no existe

                # Solo añadir vacaciones si el año actual es posterior al último año de actualización
                if emp["last_vacation_update_year"] < current_year:
                    antiguedad = calcular_antiguedad(emp["fecha_ingreso"])
                    vacaciones_corresp_este_anio = calcular_vacaciones_correspondientes(antiguedad)
                    
                    # Sumar las vacaciones correspondientes al saldo pendiente
                    emp["saldo_vacaciones_pendiente"] += vacaciones_corresp_este_anio
                    emp["last_vacation_update_year"] = current_year # Actualizar el año de la última actualización
                    print(f"Vacaciones de {vacaciones_corresp_este_anio} días añadidas a {emp['nombre']} {emp['apellido']} (Legajo: {emp.get('numero_legajo', 'N/A')}).")
                    updates_made = True
                else:
                    print(f"Vacaciones de {emp['nombre']} {emp['apellido']} (Legajo: {emp.get('numero_legajo', 'N/A')}) ya actualizadas para el año {current_year}.")
            
            if updates_made:
                guardar_empleados(empleados)
            else:
                print("No se realizaron actualizaciones de vacaciones para ningún empleado en este año.")
        elif opcion == '5':
            print("Saliendo del sistema. ¡Hasta luego!")
            break
        else:
            print("Opción no válida. Por favor, intente de nuevo.")

# Asegura que el menú principal se ejecute solo cuando el script se inicia directamente
if __name__ == "__main__":
    main_menu()