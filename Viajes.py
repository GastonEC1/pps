import wx
import wx.grid as gridlib
import wx.adv
import mysql.connector
import datetime

# Configuración de la conexión a la base de datos
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="1234",
    database="tesina"
)
cursor = db.cursor()

class ViajesApp(wx.Frame):
    def __init__(self, *args, **kw):
        super(ViajesApp, self).__init__(*args, **kw)
        self.InitUI()

    def InitUI(self):
        panel = wx.Panel(self)
        self.notebook = wx.Notebook(panel)

        # Pestañas
        self.tab_agregar = wx.Panel(self.notebook)
        self.notebook.AddPage(self.tab_agregar, "Agregar/Modificar Viaje")

        self.tab_pendientes = wx.Panel(self.notebook)
        self.notebook.AddPage(self.tab_pendientes, "Pendientes")

        self.tab_historial = wx.Panel(self.notebook)
        self.notebook.AddPage(self.tab_historial, "Historial")

        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(self.notebook, 1, flag=wx.EXPAND | wx.ALL, border=5)
        panel.SetSizer(vbox)

        self.init_tab_agregar()
        self.init_tab_pendientes()
        self.init_tab_historial()

        self.load_pendientes()
        self.load_historial()

        self.SetSize((1000, 800))  # Tamaño de la ventana principal
        self.SetTitle("Formulario Clientes")
        self.Center()

    def init_tab_agregar(self):
     vbox = wx.BoxSizer(wx.VERTICAL)

    # Fecha
     hbox_fecha = wx.BoxSizer(wx.HORIZONTAL)
     lbl_fecha = wx.StaticText(self.tab_agregar, label="Fecha:")
     self.txt_fecha = wx.adv.DatePickerCtrl(self.tab_agregar, style=wx.adv.DP_DROPDOWN | wx.adv.DP_SHOWCENTURY)
     hbox_fecha.Add(lbl_fecha, flag=wx.RIGHT, border=8)
     hbox_fecha.Add(self.txt_fecha, proportion=1)
     vbox.Add(hbox_fecha, flag=wx.EXPAND | wx.ALL, border=10)

    # Destino
     hbox_destino = wx.BoxSizer(wx.HORIZONTAL)
     lbl_destino = wx.StaticText(self.tab_agregar, label="Destino:")
     self.txt_destino = wx.TextCtrl(self.tab_agregar)
     hbox_destino.Add(lbl_destino, flag=wx.RIGHT, border=8)
     hbox_destino.Add(self.txt_destino, proportion=1)
     vbox.Add(hbox_destino, flag=wx.EXPAND | wx.ALL, border=10)

    # Institución
     hbox_tipo = wx.BoxSizer(wx.HORIZONTAL)
     lbl_tipo = wx.StaticText(self.tab_agregar, label="Institución:")
     self.txt_tipo = wx.Choice(self.tab_agregar)
     hbox_tipo.Add(lbl_tipo, flag=wx.RIGHT, border=8)
     hbox_tipo.Add(self.txt_tipo, proportion=1)
     vbox.Add(hbox_tipo, flag=wx.EXPAND | wx.ALL, border=10)

    # Vendedor
     hbox_vendedor = wx.BoxSizer(wx.HORIZONTAL)
     lbl_vendedor = wx.StaticText(self.tab_agregar, label="Vendedor:")
     self.txt_vendedor = wx.Choice(self.tab_agregar)
     hbox_vendedor.Add(lbl_vendedor, flag=wx.RIGHT, border=8)
     hbox_vendedor.Add(self.txt_vendedor, proportion=1)
     vbox.Add(hbox_vendedor, flag=wx.EXPAND | wx.ALL, border=10)

    # Precio
     hbox_precio = wx.BoxSizer(wx.HORIZONTAL)
     lbl_precio = wx.StaticText(self.tab_agregar, label="Precio:")
     self.txt_precio = wx.TextCtrl(self.tab_agregar)
     hbox_precio.Add(lbl_precio, flag=wx.RIGHT, border=8)
     hbox_precio.Add(self.txt_precio, proportion=1)
     vbox.Add(hbox_precio, flag=wx.EXPAND | wx.ALL, border=10)

    # Características
     hbox_caracteristicas = wx.BoxSizer(wx.HORIZONTAL)
     lbl_caracteristicas = wx.StaticText(self.tab_agregar, label="Características:")
     self.txt_caracteristicas = wx.TextCtrl(self.tab_agregar, style=wx.TE_MULTILINE)
     hbox_caracteristicas.Add(lbl_caracteristicas, flag=wx.RIGHT, border=8)
     hbox_caracteristicas.Add(self.txt_caracteristicas, proportion=1, flag=wx.EXPAND)
     vbox.Add(hbox_caracteristicas, flag=wx.EXPAND | wx.ALL, border=10)

    # Hospedaje
     hbox_hospedaje = wx.BoxSizer(wx.HORIZONTAL)
     lbl_hospedaje = wx.StaticText(self.tab_agregar, label="Hospedaje:")
     self.txt_hospedaje = wx.TextCtrl(self.tab_agregar)
     hbox_hospedaje.Add(lbl_hospedaje, flag=wx.RIGHT, border=8)
     hbox_hospedaje.Add(self.txt_hospedaje, proportion=1)
     vbox.Add(hbox_hospedaje, flag=wx.EXPAND | wx.ALL, border=10)

    # Botón Guardar
     self.btn_guardar = wx.Button(self.tab_agregar, label="Guardar")
     vbox.Add(self.btn_guardar, flag=wx.ALL | wx.CENTER, border=10)

     self.tab_agregar.SetSizer(vbox)

    # Bind evento de botón
     self.btn_guardar.Bind(wx.EVT_BUTTON, self.guardar_viaje)

    # Cargar instituciones y vendedores
     self.load_instituciones()
     self.load_vendedores()

    def init_tab_pendientes(self):
        vbox = wx.BoxSizer(wx.VERTICAL)
        self.grid_pendientes = gridlib.Grid(self.tab_pendientes)
        self.grid_pendientes.CreateGrid(0, 8)
        self.grid_pendientes.SetColLabelValue(0, "ID")
        self.grid_pendientes.SetColLabelValue(1, "Fecha")
        self.grid_pendientes.SetColLabelValue(2, "Destino")
        self.grid_pendientes.SetColLabelValue(3, "Institución")
        self.grid_pendientes.SetColLabelValue(4, "Vendedor")
        self.grid_pendientes.SetColLabelValue(5, "Precio")
        self.grid_pendientes.SetColLabelValue(6, "Características")
        self.grid_pendientes.SetColLabelValue(7, "Hospedaje")

        hbox = wx.BoxSizer(wx.HORIZONTAL)
        self.btn_marcar_realizado = wx.Button(self.tab_pendientes, label="Marcar Realizado")
        self.btn_eliminar = wx.Button(self.tab_pendientes, label="Eliminar Viaje")
        self.btn_modificar = wx.Button(self.tab_pendientes, label="Modificar Viaje")

        hbox.Add(self.btn_marcar_realizado, flag=wx.ALL, border=10)
        hbox.Add(self.btn_eliminar, flag=wx.ALL, border=10)
        hbox.Add(self.btn_modificar, flag=wx.ALL, border=10)

        vbox.Add(self.grid_pendientes, 1, flag=wx.EXPAND | wx.ALL, border=5)
        vbox.Add(hbox, flag=wx.ALIGN_CENTER | wx.ALL, border=10)

        self.tab_pendientes.SetSizer(vbox)

        self.btn_marcar_realizado.Bind(wx.EVT_BUTTON, self.marcar_realizado)
        self.btn_eliminar.Bind(wx.EVT_BUTTON, self.eliminar_pendiente)
        self.btn_modificar.Bind(wx.EVT_BUTTON, self.modificar_viaje)

    def init_tab_historial(self):
     vbox = wx.BoxSizer(wx.VERTICAL)
     self.grid_historial = gridlib.Grid(self.tab_historial)
     self.grid_historial.CreateGrid(0, 8)
     self.grid_historial.SetColLabelValue(0, "ID")
     self.grid_historial.SetColLabelValue(1, "Fecha")
     self.grid_historial.SetColLabelValue(2, "Destino")
     self.grid_historial.SetColLabelValue(3, "Institución")
     self.grid_historial.SetColLabelValue(4, "Vendedor")
     self.grid_historial.SetColLabelValue(5, "Precio")
     self.grid_historial.SetColLabelValue(6, "Características")
     self.grid_historial.SetColLabelValue(7, "Hospedaje")

     hbox = wx.BoxSizer(wx.HORIZONTAL)
     self.btn_eliminar_historial = wx.Button(self.tab_historial, label="Eliminar Viaje")

     hbox.Add(self.btn_eliminar_historial, flag=wx.ALL, border=10)

     vbox.Add(self.grid_historial, 1, flag=wx.EXPAND | wx.ALL, border=5)
     vbox.Add(hbox, flag=wx.ALIGN_CENTER | wx.ALL, border=10)

     self.tab_historial.SetSizer(vbox)

    
     self.btn_eliminar_historial.Bind(wx.EVT_BUTTON, self.eliminar_historial)

    def eliminar_historial(self, event):
    
     fila_seleccionada = self.grid_historial.GetSelectedRows()
    
     if not fila_seleccionada:
        wx.MessageBox('Por favor, seleccione una fila para eliminar.', 'Error', wx.OK | wx.ICON_ERROR)
        return
    
    # Confirmar la eliminación
     dialogo_confirmacion = wx.MessageDialog(self, 
                                            '¿Está seguro de que desea eliminar el viaje seleccionado?', 
                                            'Confirmar eliminación', 
                                            wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION)
     if dialogo_confirmacion.ShowModal() == wx.ID_YES:
        for fila in fila_seleccionada:
            self.grid_historial.DeleteRows(fila)
        
        wx.MessageBox('Viaje(s) eliminado(s) correctamente.', 'Éxito', wx.OK | wx.ICON_INFORMATION)



    def load_instituciones(self):
        self.txt_tipo.Clear()
        self.txt_tipo.Append("Particular")  # Primera opción
        cursor.execute("SELECT Nombre FROM Institucional")
        for row in cursor.fetchall():
            self.txt_tipo.Append(row[0])  # Añadir instituciones al menú desplegable

    def load_vendedores(self):
     self.txt_vendedor.Clear()
     try:
        cursor.execute("SELECT Nom_ape FROM Coordinadores")  # Actualiza según el nombre correcto de la columna
        for row in cursor.fetchall():
            self.txt_vendedor.Append(row[0])  # Añadir coordinadores como vendedores
     except Exception as e:
        wx.LogError(f"Error al cargar vendedores: {e}")

    def load_pendientes(self):
        try:
            cursor.execute("SELECT * FROM viajes WHERE estado = 'Pendiente'")
            rows = cursor.fetchall()

            # Verifica el número de columnas en la grid
            num_cols = 8  # Asegúrate de que coincida con el número de columnas definidas

            # Verifica si hay filas para eliminar
            if self.grid_pendientes.GetNumberRows() > 0:
                self.grid_pendientes.DeleteRows(numRows=self.grid_pendientes.GetNumberRows())

            for row_idx, row in enumerate(rows):
                self.grid_pendientes.AppendRows(1)
                for col_idx in range(num_cols):
                    self.grid_pendientes.SetCellValue(row_idx, col_idx, str(row[col_idx]))
        except Exception as e:
            wx.LogError(f"Error al cargar pendientes: {e}")

   

    def load_historial(self):
        # Similar al método load_pendientes, pero para la cuadrícula de historial
        if self.grid_historial.GetNumberRows() > 0:
            self.grid_historial.DeleteRows(numRows=self.grid_historial.GetNumberRows(), updateLabels=True)

        cursor.execute("SELECT * FROM viajes WHERE estado = 'Realizado'")
        for row in cursor.fetchall():
            self.grid_historial.AppendRows(1)
            for col in range(8):
                value = row[col]
                if isinstance(value, float):
                    value = str(value)  # Convertir float a str
                self.grid_historial.SetCellValue(self.grid_historial.GetNumberRows() - 1, col, str(value))




    def guardar_viaje(self, event):
        fecha = self.txt_fecha.GetValue().FormatISODate()
        destino = self.txt_destino.GetValue()
        tipo = self.txt_tipo.GetStringSelection()
        vendedor = self.txt_vendedor.GetStringSelection()
        precio = self.txt_precio.GetValue()
        caracteristicas = self.txt_caracteristicas.GetValue()
        hospedaje = self.txt_hospedaje.GetValue()

        try:
            cursor.execute(
                "INSERT INTO viajes (fecha, destino, tipo, vendedor, precio, caracteristicas, hospedaje, estado) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                (fecha, destino, tipo, vendedor, precio, caracteristicas, hospedaje, 'Pendiente')
            )
            db.commit()
            wx.MessageBox('Viaje guardado exitosamente', 'Éxito', wx.OK | wx.ICON_INFORMATION)
            self.load_pendientes()
        except Exception as e:
            wx.LogError(f"Error al guardar el viaje: {e}")

    def marcar_realizado(self, event):
        selected_row = self.grid_pendientes.GetGridCursorRow()
        if selected_row != -1:
            viaje_id = self.grid_pendientes.GetCellValue(selected_row, 0)
            cursor.execute("UPDATE viajes SET estado = 'Realizado' WHERE Id = %s", (viaje_id,))
            db.commit()
            self.load_pendientes()
            self.load_historial()
        else:
            wx.MessageBox("Seleccione un viaje para marcar como realizado.", "Error", wx.OK | wx.ICON_ERROR)




    def eliminar_pendiente(self, event):
        selected_row = self.grid_pendientes.GetGridCursorRow()
        if selected_row >= 0:
            viaje_id = self.grid_pendientes.GetCellValue(selected_row, 0)
            try:
                cursor.execute("DELETE FROM viajes WHERE id = %s", (viaje_id,))
                db.commit()
                wx.MessageBox('Viaje eliminado exitosamente', 'Éxito', wx.OK | wx.ICON_INFORMATION)
                self.load_pendientes()
            except Exception as e:
                wx.LogError(f"Error al eliminar el viaje: {e}")



    def modificar_viaje(self, event):
     selected_rows = self.grid_pendientes.GetSelectedRows()
     if len(selected_rows) == 1:
        row = selected_rows[0]
        viaje_id = self.grid_pendientes.GetCellValue(row, 0)  # Obtener el ID del viaje

        # Obtener los valores actuales del viaje
        fecha = self.grid_pendientes.GetCellValue(row, 1)
        destino = self.grid_pendientes.GetCellValue(row, 2)
        institucion = self.grid_pendientes.GetCellValue(row, 3)
        vendedor = self.grid_pendientes.GetCellValue(row, 4)
        precio = self.grid_pendientes.GetCellValue(row, 5)
        caracteristicas = self.grid_pendientes.GetCellValue(row, 6)
        hospedaje = self.grid_pendientes.GetCellValue(row, 7)

        # Crear el diálogo de modificación
        dlg = wx.Dialog(self, title="Modificar Viaje", size=(500, 600))

        panel = wx.Panel(dlg)
        vbox = wx.BoxSizer(wx.VERTICAL)

        # Campos de texto
        self.txt_fecha_mod = wx.adv.DatePickerCtrl(panel)
        self.txt_destino_mod = wx.TextCtrl(panel, value=destino)
        self.txt_precio_mod = wx.TextCtrl(panel, value=precio)
        self.txt_caracteristicas_mod = wx.TextCtrl(panel, value=caracteristicas)
        self.txt_hospedaje_mod = wx.TextCtrl(panel, value=hospedaje)

        # Menús desplegables para vendedores e instituciones
        self.combo_vendedor_mod = wx.ComboBox(panel, choices=[], style=wx.CB_READONLY)
        self.combo_institucion_mod = wx.ComboBox(panel, choices=[], style=wx.CB_READONLY)

        # Cargar opciones para los menús desplegables
        self.load_vendedores_mod(vendedor)  # Cargar y seleccionar el vendedor actual
        self.load_instituciones_mod(institucion)  # Cargar y seleccionar la institución actual

        # Organizar los campos en el formulario usando un sizer vertical
        vbox.Add(wx.StaticText(panel, label="Fecha:"), flag=wx.LEFT | wx.TOP, border=5)
        vbox.Add(self.txt_fecha_mod, flag=wx.EXPAND | wx.LEFT | wx.RIGHT, border=5)

        vbox.Add(wx.StaticText(panel, label="Destino:"), flag=wx.LEFT | wx.TOP, border=5)
        vbox.Add(self.txt_destino_mod, flag=wx.EXPAND | wx.LEFT | wx.RIGHT, border=5)

        vbox.Add(wx.StaticText(panel, label="Institución:"), flag=wx.LEFT | wx.TOP, border=5)
        vbox.Add(self.combo_institucion_mod, flag=wx.EXPAND | wx.LEFT | wx.RIGHT, border=5)

        vbox.Add(wx.StaticText(panel, label="Vendedor:"), flag=wx.LEFT | wx.TOP, border=5)
        vbox.Add(self.combo_vendedor_mod, flag=wx.EXPAND | wx.LEFT | wx.RIGHT, border=5)

        vbox.Add(wx.StaticText(panel, label="Precio:"), flag=wx.LEFT | wx.TOP, border=5)
        vbox.Add(self.txt_precio_mod, flag=wx.EXPAND | wx.LEFT | wx.RIGHT, border=5)

        vbox.Add(wx.StaticText(panel, label="Características:"), flag=wx.LEFT | wx.TOP, border=5)
        vbox.Add(self.txt_caracteristicas_mod, flag=wx.EXPAND | wx.LEFT | wx.RIGHT, border=5)

        vbox.Add(wx.StaticText(panel, label="Hospedaje:"), flag=wx.LEFT | wx.TOP, border=5)
        vbox.Add(self.txt_hospedaje_mod, flag=wx.EXPAND | wx.LEFT | wx.RIGHT, border=5)

        # Botón para guardar cambios
        btn_guardar_mod = wx.Button(panel, label="Guardar Cambios")
        vbox.Add(btn_guardar_mod, flag=wx.ALIGN_CENTER | wx.ALL, border=10)

        # Configurar el sizer del panel
        panel.SetSizer(vbox)
        vbox.Fit(dlg)

        # Ajustar el tamaño del diálogo al contenido
        dlg.SetSizeHints(500, 600)  # Tamaño mínimo y máximo del diálogo
        dlg.SetSize((500, 600))     # Tamaño inicial del diálogo

        # Bind evento del botón para guardar cambios
        btn_guardar_mod.Bind(wx.EVT_BUTTON, lambda event: self.guardar_cambios_viaje(event, viaje_id, dlg))

        dlg.ShowModal()  # Mostrar el diálogo
        dlg.Destroy()  # Destruir el diálogo cuando se cierre


    def actualizar_viaje(self, event, viaje_id):
    # Obtener los valores de los campos del diálogo de modificación
     fecha = self.txt_fecha_mod.GetValue().FormatISODate()
     destino = self.txt_destino_mod.GetValue()
     institucion = self.combo_institucion_mod.GetValue()  # Usar el valor seleccionado del combo box
     vendedor = self.combo_vendedor_mod.GetValue()  # Usar el valor seleccionado del combo box
     precio = self.txt_precio_mod.GetValue()
     caracteristicas = self.txt_caracteristicas_mod.GetValue()
     hospedaje = self.txt_hospedaje_mod.GetValue()

     try:
        # Consulta de actualización
        query = """
        UPDATE viajes 
        SET fecha = %s, destino = %s, tipo = %s, vendedor = %s, precio = %s, caracteristicas = %s, hospedaje = %s
        WHERE id = %s
        """
        cursor.execute(query, (fecha, destino, institucion, vendedor, precio, caracteristicas, hospedaje, viaje_id))
        db.commit()
        wx.MessageBox('Viaje actualizado exitosamente', 'Éxito', wx.OK | wx.ICON_INFORMATION)
        self.load_pendientes()
        self.load_historial()
     except Exception as e:
        wx.LogError(f"Error al actualizar el viaje: {e}")


    def guardar_cambios_viaje(self, event, viaje_id, dlg):
        # Obtener los nuevos valores del formulario de modificación
        nueva_fecha = self.txt_fecha_mod.GetValue().FormatISODate()
        nuevo_destino = self.txt_destino_mod.GetValue()
        nueva_institucion = self.combo_institucion_mod.GetValue()
        nuevo_vendedor = self.combo_vendedor_mod.GetValue()
        nuevo_precio = self.txt_precio_mod.GetValue()
        nuevas_caracteristicas = self.txt_caracteristicas_mod.GetValue()
        nuevo_hospedaje = self.txt_hospedaje_mod.GetValue()

        try:
            # Actualizar el viaje en la base de datos
            cursor.execute("""
                UPDATE viajes 
                SET fecha = %s, destino = %s, tipo = %s, vendedor = %s, precio = %s, caracteristicas = %s, hospedaje = %s 
                WHERE id = %s
            """, (nueva_fecha, nuevo_destino, nueva_institucion, nuevo_vendedor, nuevo_precio, nuevas_caracteristicas, nuevo_hospedaje, viaje_id))
            
            db.commit()

            wx.MessageBox('Viaje modificado exitosamente', 'Éxito', wx.OK | wx.ICON_INFORMATION)
            dlg.Close()  # Cerrar el diálogo tras guardar
            self.load_pendientes()  # Recargar los datos en la pestaña de viajes pendientes
        except Exception as e:
            wx.LogError(f"Error al modificar el viaje: {e}")

    def load_instituciones_mod(self, institucion_actual):
        self.combo_institucion_mod.Clear()
        self.combo_institucion_mod.Append("Particular")
        cursor.execute("SELECT Nombre FROM Institucional")
        for row in cursor.fetchall():
            self.combo_institucion_mod.Append(row[0])
        
        # Seleccionar la institución actual
        self.combo_institucion_mod.SetStringSelection(institucion_actual)

    def load_vendedores_mod(self, vendedor_actual):
        self.combo_vendedor_mod.Clear()
        cursor.execute("SELECT Nom_ape FROM Coordinadores")
        for row in cursor.fetchall():
            self.combo_vendedor_mod.Append(row[0])
        
        # Seleccionar el vendedor actual
        self.combo_vendedor_mod.SetStringSelection(vendedor_actual)



    def OnClose(self, event):
        self.Destroy()

if __name__ == '__main__':
    app = wx.App()
    frame = ViajesApp(None)
    frame.Show()
    app.MainLoop()
