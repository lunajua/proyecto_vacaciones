from reportes import *
from db import cargar_empleados
from empleados import (
    agregar_empleado,
    mostrar_empleados,
    registrar_vacaciones,
    actualizar_vacaciones_anuales
)

def main_menu():
    empleados = cargar_empleados()
    while True:
        print("\n--- Bienvenido al Registro de Vacaciones de Clinica Santa Lucia---")
        print("\n--- Menú Principal ---")
        print("1. Agregar Empleado")
        print("2. Ver Empleados")
        print("3. Registrar Vacaciones")
        print("4. Actualizar Saldo Anual")
        print("5. Exportar Reportes")
        print("6. Salir")
        opcion = input("Opción: ").strip()

        if opcion == "1":
            agregar_empleado(empleados)
        elif opcion == "2":
            mostrar_empleados(empleados)
        elif opcion == "3":
            registrar_vacaciones(empleados)
        elif opcion == "4":
            actualizar_vacaciones_anuales(empleados)
        elif opcion == "5":
            from reportes import exportar_empleados_a_excel, exportar_empleados_a_pdf
            exportar_empleados_a_excel()
            exportar_empleados_a_pdf()
        elif opcion == "6":
            print("¡Gracias por utilizar sistemas TatoLab!")
            break
        else:
            print("Opción inválida.")

if __name__ == "__main__":
    main_menu()
    exportar_empleados_a_excel()
    exportar_empleados_a_pdf()