from db import cargar_empleados
from gestion_empleados import menu_empleados
from interfaz_reportes import generar_reporte_interactivo

def main_menu():
    empleados = cargar_empleados()

    while True:
        print("\n╔════════════════════════════════════════════╗")
        print("║      SISTEMA RRHH - CLÍNICA SANTA LUCÍA    ║")
        print("╚════════════════════════════════════════════╝")
        print("1. Gestión de Empleados")
        print("2. Generar Reporte")
        print("0. Salir")

        opcion = input("\nSeleccioná una opción: ").strip()

        if opcion == "1":
            menu_empleados(empleados)
        elif opcion == "2":
            generar_reporte_interactivo()
        elif opcion == "0":
            print("👋 Hasta pronto, gracias por utilizar SistemasTato!")
            break
        else:
            print("⚠️ Opción no válida. Probá otra.")

if __name__ == "__main__":
    main_menu()