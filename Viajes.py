import wx
import wx.grid as gridlib
import wx.adv
import mysql.connector
from datetime import datetime

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

        self.SetSize((1000, 800))  # Aumentar el tamaño de la ventana principal
        self.SetTitle("Formulario Clientes")
        self.Center()

    def init_tab_agregar(self):
        vbox = wx.BoxSizer(wx.VERTICAL)
        lbl_fecha = wx.StaticText(self.tab_agregar, label="Fecha:")
        self.txt_fecha = wx.adv.DatePickerCtrl(self.tab_agregar, style=wx.adv.DP_DROPDOWN | wx.adv.DP_SHOWCENTURY)
        lbl_destino = wx.StaticText(self.tab_agregar, label="Destino:")
        self.txt_destino = wx.TextCtrl(self.tab_agregar)
        lbl_tipo = wx.StaticText(self.tab_agregar, label="Tipo de Viaje:")
        self.txt_tipo = wx.TextCtrl(self.tab_agregar)
        lbl_vendedor = wx.StaticText(self.tab_agregar, label="Vendedor:")
        self.txt_vendedor = wx.TextCtrl(self.tab_agregar)
        lbl_precio = wx.StaticText(self.tab_agregar, label="Precio:")
        self.txt_precio = wx.TextCtrl(self.tab_agregar)
        lbl_caracteristicas = wx.StaticText(self.tab_agregar, label="Características:")
        self.txt_caracteristicas = wx.TextCtrl(self.tab_agregar, style=wx.TE_MULTILINE)
        lbl_hospedaje = wx.StaticText(self.tab_agregar, label="Hospedaje:")
        self.txt_hospedaje = wx.TextCtrl(self.tab_agregar)
        btn_guardar = wx.Button(self.tab_agregar, label="Guardar Viaje")

        vbox.Add(lbl_fecha, flag=wx.LEFT | wx.TOP, border=10)
        vbox.Add(self.txt_fecha, flag=wx.LEFT | wx.EXPAND | wx.ALL, border=5)
        vbox.Add(lbl_destino, flag=wx.LEFT | wx.TOP, border=10)
        vbox.Add(self.txt_destino, flag=wx.LEFT | wx.EXPAND | wx.ALL, border=5)
        vbox.Add(lbl_tipo, flag=wx.LEFT | wx.TOP, border=10)
        vbox.Add(self.txt_tipo, flag=wx.LEFT | wx.EXPAND | wx.ALL, border=5)
        vbox.Add(lbl_vendedor, flag=wx.LEFT | wx.TOP, border=10)
        vbox.Add(self.txt_vendedor, flag=wx.LEFT | wx.EXPAND | wx.ALL, border=5)
        vbox.Add(lbl_precio, flag=wx.LEFT | wx.TOP, border=10)
        vbox.Add(self.txt_precio, flag=wx.LEFT | wx.EXPAND | wx.ALL, border=5)
        vbox.Add(lbl_caracteristicas, flag=wx.LEFT | wx.TOP, border=10)
        vbox.Add(self.txt_caracteristicas, flag=wx.LEFT | wx.EXPAND | wx.ALL, border=5)
        vbox.Add(lbl_hospedaje, flag=wx.LEFT | wx.TOP, border=10)
        vbox.Add(self.txt_hospedaje, flag=wx.LEFT | wx.EXPAND | wx.ALL, border=5)
        vbox.Add(btn_guardar, flag=wx.ALL | wx.CENTER, border=10)
        self.tab_agregar.SetSizer(vbox)

        btn_guardar.Bind(wx.EVT_BUTTON, self.guardar_viaje)

    def init_tab_pendientes(self):
     vbox = wx.BoxSizer(wx.VERTICAL)
     self.grid_pendientes = gridlib.Grid(self.tab_pendientes)
     self.grid_pendientes.CreateGrid(0, 8)
     self.grid_pendientes.SetColLabelValue(0, "ID")
     self.grid_pendientes.SetColLabelValue(1, "Fecha")
     self.grid_pendientes.SetColLabelValue(2, "Destino")
     self.grid_pendientes.SetColLabelValue(3, "Tipo")
     self.grid_pendientes.SetColLabelValue(4, "Vendedor")
     self.grid_pendientes.SetColLabelValue(5, "Precio")
     self.grid_pendientes.SetColLabelValue(6, "Características")
     self.grid_pendientes.SetColLabelValue(7, "Hospedaje")

    # Crear un sizer horizontal para los botones
     hbox = wx.BoxSizer(wx.HORIZONTAL)
     self.btn_marcar_realizado = wx.Button(self.tab_pendientes, label="Marcar Realizado")
     self.btn_eliminar = wx.Button(self.tab_pendientes, label="Eliminar Viaje")
     self.btn_modificar = wx.Button(self.tab_pendientes, label="Modificar Viaje")

     hbox.Add(self.btn_marcar_realizado, flag=wx.ALL, border=10)
     hbox.Add(self.btn_eliminar, flag=wx.ALL, border=10)
     hbox.Add(self.btn_modificar, flag=wx.ALL, border=10)

     vbox.Add(self.grid_pendientes, 1, flag=wx.EXPAND | wx.ALL, border=5)
     vbox.Add(hbox, flag=wx.ALIGN_CENTER | wx.ALL, border=10)  # Agregar los botones a la parte inferior

     self.tab_pendientes.SetSizer(vbox)

     self.btn_marcar_realizado.Bind(wx.EVT_BUTTON, self.marcar_realizado)
     self.btn_eliminar.Bind(wx.EVT_BUTTON, self.eliminar_pendiente)
     self.btn_modificar.Bind(wx.EVT_BUTTON, self.modificar_pendiente)

    def init_tab_historial(self):
        vbox = wx.BoxSizer(wx.VERTICAL)
        self.grid_historial = gridlib.Grid(self.tab_historial)
        self.grid_historial.CreateGrid(0, 8)
        self.grid_historial.SetColLabelValue(0, "ID")
        self.grid_historial.SetColLabelValue(1, "Fecha")
        self.grid_historial.SetColLabelValue(2, "Destino")
        self.grid_historial.SetColLabelValue(3, "Tipo")
        self.grid_historial.SetColLabelValue(4, "Vendedor")
        self.grid_historial.SetColLabelValue(5, "Precio")
        self.grid_historial.SetColLabelValue(6, "Características")
        self.grid_historial.SetColLabelValue(7, "Hospedaje")

        vbox.Add(self.grid_historial, 1, flag=wx.EXPAND | wx.ALL, border=5)
        self.tab_historial.SetSizer(vbox)

    def load_pendientes(self):
        # Verificar si hay filas en la cuadrícula y eliminarlas si es necesario
        if self.grid_pendientes.GetNumberRows() > 0:
            self.grid_pendientes.DeleteRows(numRows=self.grid_pendientes.GetNumberRows(), updateLabels=True)

        # Cargar datos de la base de datos
        cursor.execute("SELECT * FROM viajes WHERE estado = 'Pendiente'")
        for row in cursor.fetchall():
            self.grid_pendientes.AppendRows(1)
            for col in range(8):
                value = row[col]
                if isinstance(value, float):
                    value = str(value)  # Convertir float a str
                self.grid_pendientes.SetCellValue(self.grid_pendientes.GetNumberRows() - 1, col, str(value))

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
        tipo = self.txt_tipo.GetValue()
        vendedor = self.txt_vendedor.GetValue()
        precio = self.txt_precio.GetValue()
        caracteristicas = self.txt_caracteristicas.GetValue()
        hospedaje = self.txt_hospedaje.GetValue()

        cursor.execute("""
            INSERT INTO viajes (Fecha, Destino, Tipo, Vendedor, Precio, Caracteristicas, Hospedaje, estado)
            VALUES (%s, %s, %s, %s, %s, %s, %s, 'Pendiente')
        """, (fecha, destino, tipo, vendedor, precio, caracteristicas, hospedaje))
        db.commit()
        wx.MessageBox("Viaje guardado correctamente.", "Info", wx.OK | wx.ICON_INFORMATION)
        self.clear_fields()
        self.load_pendientes()

    def clear_fields(self):
        self.txt_fecha.SetValue(wx.DateTime.Now())
        self.txt_destino.Clear()
        self.txt_tipo.Clear()
        self.txt_vendedor.Clear()
        self.txt_precio.Clear()
        self.txt_caracteristicas.Clear()
        self.txt_hospedaje.Clear()

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
        if selected_row != -1:
            viaje_id = self.grid_pendientes.GetCellValue(selected_row, 0)
            try:
                cursor.execute("DELETE FROM viajes WHERE Id = %s", (viaje_id,))
                db.commit()
                self.load_pendientes()
                self.load_historial()
            except mysql.connector.Error as e:
                wx.MessageBox(f"No se pudo eliminar el viaje: {e}", "Error", wx.OK | wx.ICON_ERROR)
        else:
            wx.MessageBox("Seleccione un viaje para eliminar.", "Error", wx.OK | wx.ICON_ERROR)

    def modificar_pendiente(self, event):
        selected_row = self.grid_pendientes.GetGridCursorRow()
        if selected_row != -1:
            viaje_id = self.grid_pendientes.GetCellValue(selected_row, 0)
            dialog = ModificarViajeDialog(self, viaje_id)
            if dialog.ShowModal() == wx.ID_OK:
                self.load_pendientes()  # Actualizar la cuadrícula después de la modificación
                self.load_historial()
            dialog.Destroy()
        else:
            wx.MessageBox("Seleccione un viaje para modificar.", "Error", wx.OK | wx.ICON_ERROR)

class ModificarViajeDialog(wx.Dialog):
    def __init__(self, parent, viaje_id):
        super(ModificarViajeDialog, self).__init__(parent, title="Modificar Viaje", size=(600, 500))  # Ventana más grande
        self.viaje_id = viaje_id
        self.InitUI()
        self.load_viaje()

    def InitUI(self):
        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)
        lbl_fecha = wx.StaticText(panel, label="Fecha:")
        self.txt_fecha = wx.adv.DatePickerCtrl(panel, style=wx.adv.DP_DROPDOWN | wx.adv.DP_SHOWCENTURY)
        lbl_destino = wx.StaticText(panel, label="Destino:")
        self.txt_destino = wx.TextCtrl(panel)
        lbl_tipo = wx.StaticText(panel, label="Tipo de Viaje:")
        self.txt_tipo = wx.TextCtrl(panel)
        lbl_vendedor = wx.StaticText(panel, label="Vendedor:")
        self.txt_vendedor = wx.TextCtrl(panel)
        lbl_precio = wx.StaticText(panel, label="Precio:")
        self.txt_precio = wx.TextCtrl(panel)
        lbl_caracteristicas = wx.StaticText(panel, label="Características:")
        self.txt_caracteristicas = wx.TextCtrl(panel, style=wx.TE_MULTILINE)
        lbl_hospedaje = wx.StaticText(panel, label="Hospedaje:")
        self.txt_hospedaje = wx.TextCtrl(panel)
        btn_guardar = wx.Button(panel, label="Guardar Cambios")
        btn_cancelar = wx.Button(panel, label="Cancelar")

        vbox.Add(lbl_fecha, flag=wx.LEFT | wx.TOP, border=10)
        vbox.Add(self.txt_fecha, flag=wx.LEFT | wx.EXPAND | wx.ALL, border=5)
        vbox.Add(lbl_destino, flag=wx.LEFT | wx.TOP, border=10)
        vbox.Add(self.txt_destino, flag=wx.LEFT | wx.EXPAND | wx.ALL, border=5)
        vbox.Add(lbl_tipo, flag=wx.LEFT | wx.TOP, border=10)
        vbox.Add(self.txt_tipo, flag=wx.LEFT | wx.EXPAND | wx.ALL, border=5)
        vbox.Add(lbl_vendedor, flag=wx.LEFT | wx.TOP, border=10)
        vbox.Add(self.txt_vendedor, flag=wx.LEFT | wx.EXPAND | wx.ALL, border=5)
        vbox.Add(lbl_precio, flag=wx.LEFT | wx.TOP, border=10)
        vbox.Add(self.txt_precio, flag=wx.LEFT | wx.EXPAND | wx.ALL, border=5)
        vbox.Add(lbl_caracteristicas, flag=wx.LEFT | wx.TOP, border=10)
        vbox.Add(self.txt_caracteristicas, flag=wx.LEFT | wx.EXPAND | wx.ALL, border=5)
        vbox.Add(lbl_hospedaje, flag=wx.LEFT | wx.TOP, border=10)
        vbox.Add(self.txt_hospedaje, flag=wx.LEFT | wx.EXPAND | wx.ALL, border=5)
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox.Add(btn_guardar, flag=wx.RIGHT, border=5)
        hbox.Add(btn_cancelar)
        vbox.Add(hbox, flag=wx.ALIGN_CENTER | wx.TOP, border=10)
        panel.SetSizer(vbox)

        btn_guardar.Bind(wx.EVT_BUTTON, self.guardar_cambios)
        btn_cancelar.Bind(wx.EVT_BUTTON, self.OnCancel)

    def load_viaje(self):
        cursor.execute("SELECT * FROM viajes WHERE Id = %s", (self.viaje_id,))
        viaje = cursor.fetchone()
        if viaje:
            fecha = viaje[1]  # Suponiendo que la fecha está en la segunda columna
            if isinstance(fecha, str):  # Asegúrate de que la fecha sea una cadena
                fecha = datetime.strptime(fecha, '%Y-%m-%d').date()
            self.txt_fecha.SetValue(wx.DateTime.FromDMY(fecha.day, fecha.month - 1, fecha.year))
            self.txt_destino.SetValue(viaje[2])
            self.txt_tipo.SetValue(viaje[3])
            self.txt_vendedor.SetValue(viaje[4])
            self.txt_precio.SetValue(str(viaje[5]))  # Convertir float a str
            self.txt_caracteristicas.SetValue(viaje[6])
            self.txt_hospedaje.SetValue(viaje[7])

    def guardar_cambios(self, event):
        fecha = self.txt_fecha.GetValue().FormatISODate()
        destino = self.txt_destino.GetValue()
        tipo = self.txt_tipo.GetValue()
        vendedor = self.txt_vendedor.GetValue()
        precio = self.txt_precio.GetValue()
        caracteristicas = self.txt_caracteristicas.GetValue()
        hospedaje = self.txt_hospedaje.GetValue()

        cursor.execute("""
            UPDATE viajes
            SET Fecha = %s, Destino = %s, Tipo = %s, Vendedor = %s, Precio = %s, Caracteristicas = %s, Hospedaje = %s
            WHERE Id = %s
        """, (fecha, destino, tipo, vendedor, precio, caracteristicas, hospedaje, self.viaje_id))
        db.commit()
        wx.MessageBox("Viaje modificado correctamente.", "Info", wx.OK | wx.ICON_INFORMATION)
        self.EndModal(wx.ID_OK)

    def OnCancel(self, event):
        self.EndModal(wx.ID_CANCEL)

if __name__ == '__main__':
    app = wx.App()
    frame = ViajesApp(None)
    frame.Show()
    app.MainLoop()