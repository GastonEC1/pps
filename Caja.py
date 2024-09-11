import wx
import wx.adv as adv
import mysql.connector
from mysql.connector import Error
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os

class FormularioCaja(wx.Frame):
    def __init__(self, *args, **kw):
        super(FormularioCaja, self).__init__(*args, **kw)

        panel = wx.Panel(self)
        sizer = wx.BoxSizer(wx.VERTICAL)

        # Create a static box for Caja form
        formGroupBox = wx.StaticBox(panel, label="Datos de Caja")
        formGroupBoxSizer = wx.StaticBoxSizer(formGroupBox, wx.VERTICAL)

        # Create form controls
        self.tipo_label = wx.StaticText(panel, label="Tipo (ingreso/egreso):")
        self.tipo_combo = wx.ComboBox(panel, choices=['ingreso', 'egreso'], style=wx.CB_READONLY)

        self.monto_label = wx.StaticText(panel, label="Monto:")
        self.monto_text = wx.TextCtrl(panel)

        self.fecha_label = wx.StaticText(panel, label="Fecha:")
        self.fecha_picker = adv.DatePickerCtrl(panel, style=adv.DP_DROPDOWN | adv.DP_SHOWCENTURY)

        self.descripcion_label = wx.StaticText(panel, label="Descripción:")
        self.descripcion_text = wx.TextCtrl(panel, style=wx.TE_MULTILINE)

        self.viaje_label = wx.StaticText(panel, label="ID de Viaje:")
        self.viaje_text = wx.TextCtrl(panel)

        # Create buttons
        self.guardar_button = wx.Button(panel, label="Guardar")
        self.modificar_button = wx.Button(panel, label="Modificar")
        self.eliminar_button = wx.Button(panel, label="Eliminar")
        self.buscar_button = wx.Button(panel, label="Buscar")
        self.limpiar_button = wx.Button(panel, label="Limpiar")
        self.finalizar_dia_button = wx.Button(panel, label="Finalizar Día")
        self.historial_button = wx.Button(panel, label="Historial")

        # Create ListCtrl to show existing Caja entries
        self.caja_list = wx.ListCtrl(panel, style=wx.LC_REPORT | wx.LC_SORT_ASCENDING)
        self.caja_list.InsertColumn(0, "ID", width=50)
        self.caja_list.InsertColumn(1, "Tipo", width=100)
        self.caja_list.InsertColumn(2, "Monto", width=100)
        self.caja_list.InsertColumn(3, "Fecha", width=120)
        self.caja_list.InsertColumn(4, "Descripción", width=200)
        self.caja_list.InsertColumn(5, "ID Viaje", width=100)

        # Arrange controls in sizers
        formGridSizer = wx.GridBagSizer(5, 5)
        formGridSizer.Add(self.tipo_label, pos=(0, 0), flag=wx.ALIGN_RIGHT)
        formGridSizer.Add(self.tipo_combo, pos=(0, 1), flag=wx.EXPAND)
        formGridSizer.Add(self.monto_label, pos=(1, 0), flag=wx.ALIGN_RIGHT)
        formGridSizer.Add(self.monto_text, pos=(1, 1), flag=wx.EXPAND)
        formGridSizer.Add(self.fecha_label, pos=(2, 0), flag=wx.ALIGN_RIGHT)
        formGridSizer.Add(self.fecha_picker, pos=(2, 1), flag=wx.EXPAND)
        formGridSizer.Add(self.descripcion_label, pos=(3, 0), flag=wx.ALIGN_RIGHT)
        formGridSizer.Add(self.descripcion_text, pos=(3, 1), flag=wx.EXPAND)
        formGridSizer.Add(self.viaje_label, pos=(4, 0), flag=wx.ALIGN_RIGHT)
        formGridSizer.Add(self.viaje_text, pos=(4, 1), flag=wx.EXPAND)
        formGridSizer.Add(self.guardar_button, pos=(5, 0))
        formGridSizer.Add(self.modificar_button, pos=(5, 1))
        formGridSizer.Add(self.eliminar_button, pos=(5, 2))
        formGridSizer.Add(self.buscar_button, pos=(5, 3))
        formGridSizer.Add(self.limpiar_button, pos=(5, 4))
        formGridSizer.Add(self.finalizar_dia_button, pos=(6, 0), span=(1, 5))

        formGroupBoxSizer.Add(formGridSizer, proportion=1, flag=wx.EXPAND | wx.ALL, border=10)
        sizer.Add(formGroupBoxSizer, proportion=1, flag=wx.EXPAND | wx.ALL, border=10)
        sizer.Add(self.caja_list, proportion=2, flag=wx.EXPAND | wx.ALL, border=10)
        sizer.Add(self.historial_button, flag=wx.EXPAND | wx.ALL, border=10)

        panel.SetSizer(sizer)

        self.SetSize((900, 600))
        self.SetTitle("Formulario Caja")

        # Bind events
        self.guardar_button.Bind(wx.EVT_BUTTON, self.on_guardar)
        self.modificar_button.Bind(wx.EVT_BUTTON, self.on_modificar)
        self.eliminar_button.Bind(wx.EVT_BUTTON, self.on_eliminar)
        self.buscar_button.Bind(wx.EVT_BUTTON, self.on_buscar)
        self.limpiar_button.Bind(wx.EVT_BUTTON, self.on_limpiar)
        self.finalizar_dia_button.Bind(wx.EVT_BUTTON, self.on_finalizar_dia)
        self.historial_button.Bind(wx.EVT_BUTTON, self.on_historial)
        self.caja_list.Bind(wx.EVT_LIST_ITEM_SELECTED, self.on_item_selected)

        # Set up database connection
        self.conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="1234",
            database="tesina"
        )
        self.cursor = self.conn.cursor()

        # Ensure Historial table exists
        self.create_historial_table()

        # Load existing Caja data
        self.load_caja()

    def create_historial_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS Historial (
            Id INT AUTO_INCREMENT PRIMARY KEY,
            tipo VARCHAR(50),
            monto DECIMAL(10, 2),
            fecha DATE,
            descripcion TEXT,
            viaje_id INT
        )
        """
        try:
            self.cursor.execute(query)
            self.conn.commit()
        except Error as err:
            wx.MessageBox(f'Error al crear la tabla Historial: {err}', 'Error', wx.OK | wx.ICON_ERROR)

    def load_caja(self):
        self.caja_list.DeleteAllItems()
        query = "SELECT Id, tipo, monto, fecha, descripcion, viaje_id FROM Caja"
        try:
            self.cursor.execute(query)
            for row in self.cursor.fetchall():
                self.caja_list.Append(row)
        except Error as err:
            wx.MessageBox(f'Error al cargar datos: {err}', 'Error', wx.OK | wx.ICON_ERROR)

    def on_guardar(self, event):
        tipo = self.tipo_combo.GetValue().strip()
        monto = self.monto_text.GetValue().strip()
        fecha = self.fecha_picker.GetValue().FormatISODate()
        descripcion = self.descripcion_text.GetValue().strip()
        viaje_id = self.viaje_text.GetValue().strip()

        # Validate that all fields are filled
        if not all([tipo, monto, descripcion, viaje_id]):
            wx.MessageBox('Todos los campos deben estar completos.', 'Información', wx.OK | wx.ICON_WARNING)
            return

        query = "INSERT INTO Caja (tipo, monto, fecha, descripcion, viaje_id) VALUES (%s, %s, %s, %s, %s)"
        try:
            self.cursor.execute(query, (tipo, monto, fecha, descripcion, viaje_id))
            self.conn.commit()
            wx.MessageBox('Datos guardados correctamente', 'Info', wx.OK | wx.ICON_INFORMATION)
            self.load_caja()
        except Error as err:
            wx.MessageBox(f'Error al guardar datos: {err}', 'Error', wx.OK | wx.ICON_ERROR)

    def on_modificar(self, event):
        selected_index = self.caja_list.GetFirstSelected()
        if selected_index == -1:
            wx.MessageBox('Seleccione una entrada de caja para modificar.', 'Información', wx.OK | wx.ICON_WARNING)
            return

        id_caja = self.caja_list.GetItemText(selected_index, 0)
        tipo = self.tipo_combo.GetValue().strip()
        monto = self.monto_text.GetValue().strip()
        fecha = self.fecha_picker.GetValue().FormatISODate()
        descripcion = self.descripcion_text.GetValue().strip()
        viaje_id = self.viaje_text.GetValue().strip()

        # Validate that all fields are filled
        if not all([tipo, monto, descripcion, viaje_id]):
            wx.MessageBox('Todos los campos deben estar completos.', 'Información', wx.OK | wx.ICON_WARNING)
            return

        query = "UPDATE Caja SET tipo=%s, monto=%s, fecha=%s, descripcion=%s, viaje_id=%s WHERE Id=%s"
        try:
            self.cursor.execute(query, (tipo, monto, fecha, descripcion, viaje_id, id_caja))
            self.conn.commit()
            wx.MessageBox('Datos modificados correctamente', 'Info', wx.OK | wx.ICON_INFORMATION)
            self.load_caja()
        except Error as err:
            wx.MessageBox(f'Error al modificar datos: {err}', 'Error', wx.OK | wx.ICON_ERROR)

    def on_eliminar(self, event):
        selected_index = self.caja_list.GetFirstSelected()
        if selected_index == -1:
            wx.MessageBox('Seleccione una entrada de caja para eliminar.', 'Información', wx.OK | wx.ICON_WARNING)
            return

        id_caja = self.caja_list.GetItemText(selected_index, 0)
        query = "DELETE FROM Caja WHERE Id = %s"
        try:
            self.cursor.execute(query, (id_caja,))
            self.conn.commit()
            wx.MessageBox('Datos eliminados correctamente', 'Info', wx.OK | wx.ICON_INFORMATION)
            self.load_caja()
        except Error as err:
            wx.MessageBox(f'Error al eliminar datos: {err}', 'Error', wx.OK | wx.ICON_ERROR)

    def on_buscar(self, event):
        fecha = wx.GetTextFromUser("Ingrese la fecha a buscar (YYYY-MM-DD):", "Buscar Fecha")
        if fecha:
            self.caja_list.DeleteAllItems()
            query = "SELECT Id, tipo, monto, fecha, descripcion, viaje_id FROM Caja WHERE fecha = %s"
            try:
                self.cursor.execute(query, (fecha,))
                for row in self.cursor.fetchall():
                    self.caja_list.Append(row)
            except Error as err:
                wx.MessageBox(f'Error al buscar datos: {err}', 'Error', wx.OK | wx.ICON_ERROR)

    def on_limpiar(self, event):
        self.tipo_combo.SetValue('')
        self.monto_text.SetValue('')
        self.fecha_picker.SetValue(wx.DateTime.Now())
        self.descripcion_text.SetValue('')
        self.viaje_text.SetValue('')

    def on_finalizar_dia(self, event):
        fecha = wx.DateTime.Now().FormatISODate()
        self.mover_datos_a_historial(fecha)
        self.caja_list.DeleteAllItems()

    def mover_datos_a_historial(self, fecha):
        query = """
        INSERT INTO Historial (tipo, monto, fecha, descripcion, viaje_id)
        SELECT tipo, monto, fecha, descripcion, viaje_id
        FROM Caja
        WHERE fecha = %s
        """
        try:
            self.cursor.execute(query, (fecha,))
            self.conn.commit()
            wx.MessageBox('Datos movidos al historial correctamente', 'Info', wx.OK | wx.ICON_INFORMATION)
        except Error as err:
            wx.MessageBox(f'Error al mover datos al historial: {err}', 'Error', wx.OK | wx.ICON_ERROR)

    def on_historial(self, event):
        self.historial_frame = wx.Frame(self, title="Historial de Caja", size=(800, 600))
        panel = wx.Panel(self.historial_frame)
        sizer = wx.BoxSizer(wx.VERTICAL)

        # Create ListCtrl to show historial entries
        self.historial_list = wx.ListCtrl(panel, style=wx.LC_REPORT | wx.LC_SORT_ASCENDING)
        self.historial_list.InsertColumn(0, "ID", width=50)
        self.historial_list.InsertColumn(1, "Tipo", width=100)
        self.historial_list.InsertColumn(2, "Monto", width=100)
        self.historial_list.InsertColumn(3, "Fecha", width=120)
        self.historial_list.InsertColumn(4, "Descripción", width=200)
        self.historial_list.InsertColumn(5, "ID Viaje", width=100)

        # Create DatePicker for filtering
        self.fecha_historial_picker = adv.DatePickerCtrl(panel, style=adv.DP_DROPDOWN | adv.DP_SHOWCENTURY)
        self.buscar_historial_button = wx.Button(panel, label="Buscar Historial")

        # Arrange controls in sizers
        sizer.Add(wx.StaticText(panel, label="Selecciona una fecha para filtrar:"), flag=wx.ALL, border=5)
        sizer.Add(self.fecha_historial_picker, flag=wx.EXPAND | wx.ALL, border=5)
        sizer.Add(self.buscar_historial_button, flag=wx.EXPAND | wx.ALL, border=5)
        sizer.Add(self.historial_list, proportion=1, flag=wx.EXPAND | wx.ALL, border=5)

        panel.SetSizer(sizer)
        self.historial_frame.Bind(wx.EVT_BUTTON, self.on_buscar_historial, self.buscar_historial_button)
        self.historial_frame.Bind(wx.EVT_LIST_ITEM_SELECTED, self.on_historial_item_selected, self.historial_list)

        self.load_historial()
        self.historial_frame.Show()

    def load_historial(self):
        self.historial_list.DeleteAllItems()
        query = "SELECT Id, tipo, monto, fecha, descripcion, viaje_id FROM Historial"
        try:
            self.cursor.execute(query)
            for row in self.cursor.fetchall():
                self.historial_list.Append(row)
        except Error as err:
            wx.MessageBox(f'Error al cargar datos del historial: {err}', 'Error', wx.OK | wx.ICON_ERROR)

    def on_buscar_historial(self, event):
        fecha = self.fecha_historial_picker.GetValue().FormatISODate()
        self.historial_list.DeleteAllItems()
        query = "SELECT Id, tipo, monto, fecha, descripcion, viaje_id FROM Historial WHERE fecha = %s"
        try:
            self.cursor.execute(query, (fecha,))
            for row in self.cursor.fetchall():
                self.historial_list.Append(row)
        except Error as err:
            wx.MessageBox(f'Error al buscar historial: {err}', 'Error', wx.OK | wx.ICON_ERROR)

    def on_historial_item_selected(self, event):
        selected_index = self.historial_list.GetFirstSelected()
        if selected_index != -1:
            id_historial = self.historial_list.GetItemText(selected_index, 0)
            tipo = self.historial_list.GetItemText(selected_index, 1)
            monto = self.historial_list.GetItemText(selected_index, 2)
            fecha = self.historial_list.GetItemText(selected_index, 3)
            descripcion = self.historial_list.GetItemText(selected_index, 4)
            viaje_id = self.historial_list.GetItemText(selected_index, 5)
            
            # Generate PDF for the selected item
            filename = os.path.expanduser("~/Downloads/comprobante.pdf")
            self.generar_pdf(tipo, monto, fecha, descripcion, viaje_id, filename)

    def generar_pdf(self, tipo, monto, fecha, descripcion, viaje_id, filename):
        c = canvas.Canvas(filename, pagesize=letter)
        c.drawString(100, 750, f"Comprobante de {tipo.capitalize()}")
        c.drawString(100, 730, f"Tipo: {tipo.capitalize()}")
        c.drawString(100, 710, f"Monto: {monto}")
        c.drawString(100, 690, f"Fecha: {fecha}")
        c.drawString(100, 670, f"Descripción: {descripcion}")
        c.drawString(100, 650, f"ID Viaje: {viaje_id}")
        c.save()
        wx.MessageBox(f'Comprobante guardado en: {filename}', 'Info', wx.OK | wx.ICON_INFORMATION)

    def on_item_selected(self, event):
        # Handle item selection in caja_list
        selected_index = self.caja_list.GetFirstSelected()
        if selected_index != -1:
            id_caja = self.caja_list.GetItemText(selected_index, 0)
            tipo = self.caja_list.GetItemText(selected_index, 1)
            monto = self.caja_list.GetItemText(selected_index, 2)
            fecha = self.caja_list.GetItemText(selected_index, 3)
            descripcion = self.caja_list.GetItemText(selected_index, 4)
            viaje_id = self.caja_list.GetItemText(selected_index, 5)
            
            # Optionally do something with the selected item, like showing details or editing
            wx.MessageBox(f'Se ha seleccionado el ID {id_caja}\nTipo: {tipo}\nMonto: {monto}\nFecha: {fecha}\nDescripción: {descripcion}\nID Viaje: {viaje_id}', 'Selección', wx.OK | wx.ICON_INFORMATION)

if __name__ == "__main__":
    app = wx.App(False)
    frame = FormularioCaja(None)
    frame.Show()
    app.MainLoop()