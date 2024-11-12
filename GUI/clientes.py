from PyQt6 import uic
from PyQt6.QtWidgets import QMessageBox, QTableWidgetItem, QInputDialog, QTableWidget
from conexion import Conexion

class ClientesWindow():
    def __init__(self):
        # Cargar la interfaz del inventario
        self.clientesWindow = uic.loadUi("GUI/clientes.ui")
        self.clientesWindow.show()

        self.clientesWindow.irAlMenu.clicked.connect(self.ir_al_menu_principal)
        self.cargar_clientes()


    def ir_al_menu_principal(self):
        self.clientesWindow.hide()

    def cargar_clientes(self):
        conexion = Conexion()
        try:
            # Consultar las ordenes de trabajo
            cur = conexion.con.cursor()
            cur.execute("SELECT * FROM orden_trabajo")
            items = cur.fetchall()

            # Limpiar y llenar la tabla
            self.clientesWindow.tableWidgetClientes.setRowCount(0)
            self.clientesWindow.tableWidgetClientes.verticalHeader().setVisible(False)
            
          # Configurar para seleccionar toda la fila
            self.clientesWindow.tableWidgetClientes.setSelectionBehavior(
                QTableWidget.SelectionBehavior.SelectRows
            )

            
            for item in items:
                row_position = self.clientesWindow.tableWidgetClientes.rowCount()
                self.clientesWindow.tableWidgetClientes.insertRow(row_position)

                # Llenar cada columna de la tabla
                for col, data in enumerate(item):
                    self.clientesWindow.tableWidgetClientes.setItem(row_position, col, QTableWidgetItem(str(data)))
            
            # Ajustar tamaño de las columnas automáticamente al contenido
            self.clientesWindow.tableWidgetClientes.resizeColumnsToContents()

            # Ajustar tamaño de las filas automáticamente al contenido
            self.clientesWindow.tableWidgetClientes.resizeRowsToContents()
            
                    
        except Exception as ex:
            QMessageBox.critical(self.clientesWindow, "Error", f"No se pudo cargar el inventario: {ex}")
        finally:
            conexion.cerrar_conexion()