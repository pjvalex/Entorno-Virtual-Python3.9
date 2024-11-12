import os
from PyQt6 import uic
from conexion import Conexion
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import matplotlib.pyplot as plt
from PyQt6.QtWidgets import QMessageBox

class ReportesWindow():
    def __init__(self):
        # Cargar la interfaz del inventario
        self.reportesWindow = uic.loadUi("GUI/reportes.ui")
        self.reportesWindow.show()

        # Conectar botones a sus funciones correspondientes
        self.reportesWindow.generarPDF_boton.clicked.connect(self.generar_reporte)
        self.reportesWindow.generarGrafico_boton.clicked.connect(self.generar_grafico)
        self.reportesWindow.menu_principal_boton.clicked.connect(self.ir_al_menu_principal)

    def ir_al_menu_principal(self):
        self.reportesWindow.hide()
    
    def generar_reporte(self):
        self.conn = Conexion().conectar()
        self.cur = self.conn.cursor()
        # Crear la carpeta de reportes si no existe
        ruta_carpeta = "reportes y graficos"
        os.makedirs(ruta_carpeta, exist_ok=True)
        
        # Ruta del archivo PDF dentro de la carpeta
        archivo_pdf = os.path.join(ruta_carpeta, "reporte_ordenes_trabajo.pdf")
        
        # Generar el PDF
        c = canvas.Canvas(archivo_pdf, pagesize=letter)
        c.setFont("Helvetica", 10)

        # Título
        c.drawString(100, 750, "Reporte de Órdenes de Trabajo")
        
        # Consultar las órdenes de trabajo
        self.cur.execute("SELECT * FROM orden_trabajo")
        ordenes = self.cur.fetchall()

        # Posición inicial para el contenido
        y = 730

        # Añadir encabezados de columna
        c.drawString(100, y, "ID")
        c.drawString(150, y, "Nombre")
        c.drawString(250, y, "Teléfono")
        c.drawString(350, y, "Tipo de Servicio")
        c.drawString(450, y, "Monto")
        y -= 15

        # Agregar las órdenes al PDF
        for orden in ordenes:
            c.drawString(100, y, str(orden[0]))  # ID
            c.drawString(150, y, orden[1])       # Nombre
            c.drawString(250, y, orden[2])       # Teléfono
            c.drawString(350, y, orden[4])       # Tipo de servicio
            c.drawString(450, y, str(orden[9]))  # Monto
            y -= 15

            # Si llegamos al final de la página, creamos una nueva
            if y < 100:
                c.showPage()
                c.setFont("Helvetica", 10)
                y = 750

        # Guardar el PDF
        c.save()
        print(f"Reporte guardado con exito")
        self.conn.close()
        QMessageBox.information(None, "Éxito", "Reporte guardado con exito")


    def generar_grafico(self):
        self.conn = Conexion().conectar()
        self.cur = self.conn.cursor()

        # Consultar las órdenes de trabajo
        self.cur.execute("SELECT tipo_servicio, SUM(monto) FROM orden_trabajo GROUP BY tipo_servicio")
        data = self.cur.fetchall()

        # Dividir los datos en tipos de servicio y montos
        tipos_servicio = [item[0] for item in data]
        montos = [item[1] for item in data]

        # Crear gráfico de barras
        plt.bar(tipos_servicio, montos)
        plt.xlabel("Tipo de Servicio")
        plt.ylabel("Monto Total")
        plt.title("Monto Total por Tipo de Servicio")
        plt.xticks(rotation=45)
        plt.tight_layout()

        # Mostrar gráfico
        plt.show()
        self.conn.close()
        