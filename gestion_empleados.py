import datetime
from vacaciones import calcular_antiguedad, calcular_vacaciones_correspondientes
from fechas import validar_fecha, calcular_dias_entre_fechas
from db import cargar_empleados, guardar_empleados

# --- Alta de empleado ---
def agregar_empleado(empleados):
    print("\n--- Agregar Nuevo Empleado ---")
    numero_legajo = input("Número de Legajo: ").strip()

    if any(emp.get("numero_legajo") == numero_legajo for emp in empleados):
        print("⚠️ Ya existe un empleado con ese legajo.")
        return

    nombre = input("Nombre: ").strip().title()
    apellido = input("Apellido: ").strip().title()
    sector = input("Sector: ").strip().title()

    fecha_ingreso_str = ""
    while not validar_fecha(fecha_ingreso_str):
        fecha_ingreso_str = input("Fecha de ingreso (AAAA-MM-DD): ").strip()
        if not validar_fecha(fecha_ingreso_str):
            print("Formato inválido.")

    vacaciones_previas = -1
    while vacaciones_previas < 0:
        try:
            vacaciones_previas = int(input("Vacaciones período anterior: ").strip())
        except ValueError:
            print("⚠️ Número inválido.")

    antiguedad = calcular_antiguedad(fecha_ingreso_str)
    vacaciones_actuales = calcular_vacaciones_correspondientes(antiguedad)

    empleado = {
        "numero_legajo": numero_legajo,
        "nombre": nombre,
        "apellido": apellido,
        "sector": sector,
        "fecha_ingreso": fecha_ingreso_str,
        "vacaciones_periodo_anterior": vacaciones_previas,
        "vacaciones_tomadas": [],
        "saldo_vacaciones_pendiente": vacaciones_actuales + vacaciones_previas,
        "last_vacation_update_year": datetime.date.today().year
    }

    empleados.append(empleado)
    guardar_empleados(empleados)
    print(f"✅ Empleado {nombre} {apellido} agregado correctamente.")

# --- Modificación ---
def modificar_empleado(legajo, empleados):
    emp = next((e for e in empleados if str(e["numero_legajo"]) == str(legajo)), None)
    if not emp:
        print("❌ Legajo no encontrado.")
        return

    print(f"\n✏️ Modificando: {emp['nombre']} {emp['apellido']}")
    emp["nombre"] = input(f"Nuevo nombre [{emp['nombre']}]: ") or emp["nombre"]
    emp["apellido"] = input(f"Nuevo apellido [{emp['apellido']}]: ") or emp["apellido"]
    emp["sector"] = input(f"Nuevo sector [{emp['sector']}]: ") or emp["sector"]

    guardar_empleados(empleados)
    print("✅ Modificación realizada.")

# --- Baja ---
def eliminar_empleado(legajo, empleados):
    emp = next((e for e in empleados if str(e["numero_legajo"]) == str(legajo)), None)
    if not emp:
        print("❌ Legajo no encontrado.")
        return

    confirmar = input(f"¿Estás seguro de eliminar a {emp['nombre']} {emp['apellido']}? (s/n): ").lower()
    if confirmar != "s":
        print("🚫 Acción cancelada.")
        return

    empleados.remove(emp)
    guardar_empleados(empleados)
    print("🗑️ Empleado eliminado.")

# --- Visualización ---
def mostrar_empleados(empleados):
    if not empleados:
        print("⚠️ No hay empleados registrados.")
        return

    print("\n--- Lista de Empleados ---")
    for i, emp in enumerate(empleados, 1):
        antiguedad = calcular_antiguedad(emp["fecha_ingreso"])
        print(f"\n[{i}] Legajo: {emp['numero_legajo']} - {emp['nombre']} {emp['apellido']} ({emp['sector']})")
        print(f"   Ingreso: {emp['fecha_ingreso']} | Antigüedad: {antiguedad} años")
        print(f"   Vac. anteriores: {emp['vacaciones_periodo_anterior']} | Saldo actual: {emp['saldo_vacaciones_pendiente']} días")
        if emp["vacaciones_tomadas"]:
            print("   Tomadas:")
            for v in emp["vacaciones_tomadas"]:
                print(f"      {v['inicio']} a {v['fin']} ({v['dias']} días)")
        else:
            print("   Tomadas: Ninguna")

# --- Registro de vacaciones ---
def registrar_vacaciones(empleados):
    if not empleados:
        print("⚠️ No hay empleados disponibles.")
        return

    mostrar_empleados(empleados)
    try:
        idx = int(input("\nNúmero del empleado: ").strip()) - 1
        empleado = empleados[idx]
    except:
        print("❌ Índice inválido.")
        return

    print(f"\n📅 Registro de vacaciones para {empleado['nombre']}")
    fecha_inicio_str = ""
    while not validar_fecha(fecha_inicio_str):
        fecha_inicio_str = input("Inicio (AAAA-MM-DD): ").strip()

    fecha_fin_str = ""
    while not validar_fecha(fecha_fin_str):
        fecha_fin_str = input("Fin (AAAA-MM-DD): ").strip()

    dias = calcular_dias_entre_fechas(fecha_inicio_str, fecha_fin_str)
    if dias > 0 and empleado["saldo_vacaciones_pendiente"] >= dias:
        empleado["vacaciones_tomadas"].append({
            "inicio": fecha_inicio_str,
            "fin": fecha_fin_str,
            "dias": dias
        })
        empleado["saldo_vacaciones_pendiente"] -= dias
        guardar_empleados(empleados)
        print(f"✅ {dias} días registrados. Saldo actual: {empleado['saldo_vacaciones_pendiente']} días.")
    else:
        print("⚠️ Saldo insuficiente o fechas inválidas.")

# --- Actualización anual de vacaciones ---
def actualizar_vacaciones_anuales(empleados):
    current_year = datetime.date.today().year
    actualizados = 0
    for emp in empleados:
        antiguedad = calcular_antiguedad(emp["fecha_ingreso"])
        if emp.get("last_vacation_update_year", 0) < current_year:
            dias = calcular_vacaciones_correspondientes(antiguedad)
            emp["saldo_vacaciones_pendiente"] += dias
            emp["last_vacation_update_year"] = current_year
            print(f"🔄 {emp['nombre']} actualizado con +{dias} días.")
            actualizados += 1
    if actualizados:
        guardar_empleados(empleados)
    else:
        print("ℹ️ Todos los empleados ya fueron actualizados.")

# --- Submenú de gestión ---
def menu_empleados(empleados):
    while True:        
        print("\n👥 ABM Empleados - Clínica Santa Lucía")
        print("────────────────────────────────────────")
        print("1. Alta Empleado")
        print("2. Modificar Empleado")
        print("3. Eliminar Empleado")
        print("4. Ver Empleados")
        print("5. Registrar Vacaciones")
        print("6. Actualizar Vacaciones Anuales")
        print("0. Volver al menú principal")

        opcion = input("\nElige una opción: ").strip()
        if opcion == "1":
            agregar_empleado(empleados)
        elif opcion == "2":
            legajo = input("Número de legajo a modificar: ").strip()
            modificar_empleado(legajo, empleados)
        elif opcion == "3":
            legajo = input("Número de legajo a eliminar: ").strip()
            eliminar_empleado(legajo, empleados)
        elif opcion == "4":
            mostrar_empleados(empleados)
        elif opcion == "5":
            registrar_vacaciones(empleados)
        elif opcion == "6":
            actualizar_vacaciones_anuales(empleados)
        elif opcion == "0":
            break
        else:
            print("⚠️ Opción no válida.")