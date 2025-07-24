import os
import datetime 
from reportes import exportar_empleados_a_excel, exportar_empleados_a_pdf
from db import cargar_empleados


def generar_reporte_interactivo():
    print("\n📋 Generador de Reportes de Empleados\n")
    while True:
        empleados = cargar_empleados()
        if not empleados:
            print("⚠️ No hay empleados disponibles.")
            return

        print("¿Qué tipo de reporte deseas generar?")
        print("1. Excel (.xlsx)")
        print("2. PDF (.pdf)")
        print("0. Volver al Menú Principal")
        tipo = input("Elegí una opción: ").strip()
        if tipo == "0":
            print("↩️ Regresando al menú principal.")
            break

        print("\n¿Qué deseas exportar?")
        print("1. Todos los empleados")
        print("2. Un empleado en particular")
        print("0. Cancelar")
        modo = input("Elegí una opción: ").strip()
        if modo == "0":
            print("↩️ Regresando al menú principal.")
            break

        if modo == "2":
            legajos = [str(emp["numero_legajo"]) for emp in empleados]
            legajo = input(f"Ingresá el número de legajo ({', '.join(legajos)}): ").strip()
            emp_filtrado = [e for e in empleados if str(e["numero_legajo"]) == legajo]
            if not emp_filtrado:
                print("❌ Legajo no encontrado.")
                continue
            empleados = emp_filtrado  # Exporta solo uno

        nombre_archivo = input("📝 Nombre del archivo (sin extensión): ").strip()
        hoy = datetime.date.today().isoformat()
        ruta_destino = os.path.join(os.getcwd(), "reportes", hoy)
        os.makedirs(ruta_destino, exist_ok=True)

        extension = ".xlsx" if tipo == "1" else ".pdf" if tipo == "2" else None
        if not extension:
            print("⚠️ Opción inválida.")
            continue

        archivo_completo = os.path.join(ruta_destino, f"{nombre_archivo}{extension}")
        try:
            if tipo == "1":
                exportar_empleados_a_excel(nombre_archivo=archivo_completo, empleados=empleados)
            else:
                exportar_empleados_a_pdf(nombre_pdf=archivo_completo, empleados=empleados)
            print(f"\n✅ Reporte generado en: {archivo_completo}")
            abrir = input("¿Deseás abrir el archivo ahora? (s/n): ").strip().lower()
            if abrir == "s":
                os.startfile(archivo_completo)
        except Exception as e:
            print(f"❌ Error al generar el reporte: {e}")