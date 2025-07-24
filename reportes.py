import pandas as pd
from db import cargar_empleados
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

def exportar_empleados_a_excel(nombre_archivo="reporte_empleados.xlsx", empleados = None):
    if empleados is None:
        from db import cargar_empleados
        empleados = cargar_empleados()
        return
        
    for emp in empleados:
        emp["vacaciones_tomadas"] = "; ".join([f"{v['inicio']} a {v['fin']} ({v['dias']} dias)" for v in emp.get("vacaciones_tomadas", [])]) if emp.get("vacaciones_tomadas") else "Ninguna"

    df = pd.DataFrame(empleados)
    
    # Aplanar vacaciones tomadas (podés ajustarlo)
    df["vacaciones_tomadas"] = df["vacaciones_tomadas"].apply(
        lambda vac: "; ".join([f"{v['inicio']} a {v['fin']} ({v['dias']} días)" for v in vac]) if vac else "Ninguna")#

    df.to_excel(nombre_archivo, index=False)
    print(f"Reporte exportado exitosamente a {nombre_archivo}.")


def exportar_empleados_a_pdf(nombre_pdf="reporte_empleados.pdf", empleados = None):
    if empleados is None:
        from db import cargar_empleados
        empleados = cargar_empleados()
        return

    c = canvas.Canvas(nombre_pdf, pagesize=A4)
    width, height = A4
    y = height - 50

    c.setFont("Helvetica", 12)
    c.drawString(50, y, "Reporte de Empleados")
    y -= 30

    for emp in empleados:
        texto = f"{emp['numero_legajo']} - {emp['nombre']} {emp['apellido']} | {emp['sector']} | Vacaciones Pendientes: {emp['saldo_vacaciones_pendiente']} días"
        c.drawString(50, y, texto)
        y -= 20
        if y < 100:
            c.showPage()
            y = height - 50

    c.save()
    print(f"Reporte PDF generado en {nombre_pdf}")