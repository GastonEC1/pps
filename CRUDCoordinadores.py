import wx
import wx.adv
import mysql.connector

class FormularioCoordinadores(wx.Frame):
    def __init__(self, *args, **kw):
        super(FormularioCoordinadores, self).__init__(*args, **kw)

        panel = wx.Panel(self)
        sizer = wx.BoxSizer(wx.VERTICAL)

        groupBox = wx.StaticBox(panel, label="Datos del Coordinador")
        groupBoxSizer = wx.StaticBoxSizer(groupBox, wx.VERTICAL)
        
        # Create form controls
        self.dni_label = wx.StaticText(panel, label="DNI:")
        self.dni_text = wx.TextCtrl(panel)

        self.nom_ape_label = wx.StaticText(panel, label="Nombre y Apellido:")
        self.nom_ape_text = wx.TextCtrl(panel)

        self.tel_label = wx.StaticText(panel, label="Teléfono:")
        self.tel_text = wx.TextCtrl(panel)

        self.direccion_label = wx.StaticText(panel, label="Dirección:")
        self.direccion_text = wx.TextCtrl(panel)

        self.fecha_nac_label = wx.StaticText(panel, label="Fecha de Nacimiento:")
        self.fecha_picker = wx.adv.DatePickerCtrl(panel, style=wx.adv.DP_DROPDOWN | wx.adv.DP_SHOWCENTURY)

        # Create buttons
        self.guardar_button = wx.Button(panel, label="Guardar")
        self.modificar_button = wx.Button(panel, label="Modificar")
        self.eliminar_button = wx.Button(panel, label="Eliminar")
        self.buscar_button = wx.Button(panel, label="Buscar")
        self.limpiar_button = wx.Button(panel, label="Limpiar")

        # Create ListCtrl to show existing coordinators
        self.coordinadores_list = wx.ListCtrl(panel, style=wx.LC_REPORT | wx.LC_SORT_ASCENDING)
        self.coordinadores_list.InsertColumn(0, "DNI", width=80)
        self.coordinadores_list.InsertColumn(1, "Nombre y Apellido", width=150)
        self.coordinadores_list.InsertColumn(2, "Teléfono", width=100)
        self.coordinadores_list.InsertColumn(3, "Dirección", width=150)
        self.coordinadores_list.InsertColumn(4, "Fecha de Nacimiento", width=120)

        # Arrange controls in sizers
        grid_sizer = wx.GridBagSizer(5, 5)
        grid_sizer.Add(self.dni_label, pos=(0, 0), flag=wx.ALIGN_RIGHT)
        grid_sizer.Add(self.dni_text, pos=(0, 1), flag=wx.EXPAND)
        grid_sizer.Add(self.nom_ape_label, pos=(1, 0), flag=wx.ALIGN_RIGHT)
        grid_sizer.Add(self.nom_ape_text, pos=(1, 1), flag=wx.EXPAND)
        grid_sizer.Add(self.tel_label, pos=(2, 0), flag=wx.ALIGN_RIGHT)
        grid_sizer.Add(self.tel_text, pos=(2, 1), flag=wx.EXPAND)
        grid_sizer.Add(self.direccion_label, pos=(3, 0), flag=wx.ALIGN_RIGHT)
        grid_sizer.Add(self.direccion_text, pos=(3, 1), flag=wx.EXPAND)
        grid_sizer.Add(self.fecha_nac_label, pos=(4, 0), flag=wx.ALIGN_RIGHT)
        grid_sizer.Add(self.fecha_picker, pos=(4, 1), flag=wx.EXPAND)
        grid_sizer.Add(self.guardar_button, pos=(5, 0))
        grid_sizer.Add(self.modificar_button, pos=(5, 1))
        grid_sizer.Add(self.eliminar_button, pos=(5, 2))
        grid_sizer.Add(self.buscar_button, pos=(5, 3))
        grid_sizer.Add(self.limpiar_button, pos=(5, 4))

        groupBoxSizer.Add(grid_sizer, proportion=1, flag=wx.EXPAND | wx.ALL, border=10)
        sizer.Add(groupBoxSizer, proportion=1, flag=wx.EXPAND | wx.ALL, border=10)
        sizer.Add(self.coordinadores_list, proportion=2, flag=wx.EXPAND | wx.ALL, border=10)

        panel.SetSizer(sizer)

        self.SetSize((750, 500))
        self.SetTitle("Formulario Coordinadores")

        # Bind events
        self.guardar_button.Bind(wx.EVT_BUTTON, self.on_guardar)
        self.modificar_button.Bind(wx.EVT_BUTTON, self.on_modificar)
        self.eliminar_button.Bind(wx.EVT_BUTTON, self.on_eliminar)
        self.buscar_button.Bind(wx.EVT_BUTTON, self.on_buscar)
        self.limpiar_button.Bind(wx.EVT_BUTTON, self.on_limpiar)
        self.coordinadores_list.Bind(wx.EVT_LIST_ITEM_SELECTED, self.on_item_selected)

        # Set up database connection
        self.conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="123456789",
            database="tesina"
        )
        self.cursor = self.conn.cursor()

        # Load existing coordinators
        self.load_coordinadores()

    def load_coordinadores(self):
        self.coordinadores_list.DeleteAllItems()
        query = "SELECT Dni, Nom_ape, Tel, Direccion, fecha_nac FROM Coordinadores"
        try:
            self.cursor.execute(query)
            for row in self.cursor.fetchall():
                self.coordinadores_list.Append(row)
        except mysql.connector.Error as err:
            wx.MessageBox(f'Error al cargar datos: {err}', 'Error', wx.OK | wx.ICON_ERROR)

    def on_guardar(self, event):
        dni = self.dni_text.GetValue()
        nom_ape = self.nom_ape_text.GetValue()
        tel = self.tel_text.GetValue()
        direccion = self.direccion_text.GetValue()
        fecha_nac = self.fecha_picker.GetValue().FormatISODate()  # Get the date from DatePickerCtrl
        query = "INSERT INTO Coordinadores (Dni, Nom_ape, Tel, Direccion, fecha_nac) VALUES (%s, %s, %s, %s, %s)"
        try:
            self.cursor.execute(query, (dni, nom_ape, tel, direccion, fecha_nac))
            self.conn.commit()
            wx.MessageBox('Datos guardados correctamente', 'Info', wx.OK | wx.ICON_INFORMATION)
            self.load_coordinadores()
        except mysql.connector.Error as err:
            wx.MessageBox(f'Error al guardar datos: {err}', 'Error', wx.OK | wx.ICON_ERROR)

    def on_modificar(self, event):
        dni = self.dni_text.GetValue()
        nom_ape = self.nom_ape_text.GetValue()
        tel = self.tel_text.GetValue()
        direccion = self.direccion_text.GetValue()
        fecha_nac = self.fecha_picker.GetValue().FormatISODate()  # Get the date from DatePickerCtrl
        query = "UPDATE Coordinadores SET Nom_ape=%s, Tel=%s, Direccion=%s, fecha_nac=%s WHERE Dni=%s"
        try:
            self.cursor.execute(query, (nom_ape, tel, direccion, fecha_nac, dni))
            self.conn.commit()
            wx.MessageBox('Datos modificados correctamente', 'Info', wx.OK | wx.ICON_INFORMATION)
            self.load_coordinadores()
        except mysql.connector.Error as err:
            wx.MessageBox(f'Error al modificar datos: {err}', 'Error', wx.OK | wx.ICON_ERROR)

    def on_eliminar(self, event):
        dni = self.dni_text.GetValue()
        query = "DELETE FROM Coordinadores WHERE Dni=%s"
        try:
            self.cursor.execute(query, (dni,))
            self.conn.commit()
            wx.MessageBox('Datos eliminados correctamente', 'Info', wx.OK | wx.ICON_INFORMATION)
            self.load_coordinadores()
        except mysql.connector.Error as err:
            wx.MessageBox(f'Error al eliminar datos: {err}', 'Error', wx.OK | wx.ICON_ERROR)

    def on_buscar(self, event):
        dni = self.dni_text.GetValue()
        query = "SELECT Dni, Nom_ape, Tel, Direccion, fecha_nac FROM Coordinadores WHERE Dni=%s"
        try:
            self.cursor.execute(query, (dni,))
            result = self.cursor.fetchone()
            if result:
                self.nom_ape_text.SetValue(result[1])
                self.tel_text.SetValue(result[2])
                self.direccion_text.SetValue(result[3])
                fecha_nac = result[4] # Set the date to DatePickerCtrl
                if wx.DateTime.ParseISODate(fecha_nac):
                    self.fecha_picker.SetValue(wx.DateTime.ParseISODate(fecha_nac))
                else:
                    wx.MessageBox('Fecha inválida en la base de datos.', 'Error', wx.OK | wx.ICON_ERROR)
            else:
                wx.MessageBox('No se encontraron datos para el DNI especificado.', 'Información', wx.OK | wx.ICON_INFORMATION)
        except mysql.connector.Error as err:
            wx.MessageBox(f'Error al buscar datos: {err}', 'Error', wx.OK | wx.ICON_ERROR)

    def on_limpiar(self, event):
        self.dni_text.SetValue("")
        self.nom_ape_text.SetValue("")
        self.tel_text.SetValue("")
        self.direccion_text.SetValue("")
        self.fecha_picker.SetValue(wx.DateTime.Now())  # Set to current date

    def on_item_selected(self, event):
        selected_index = event.GetIndex()
        dni = self.coordinadores_list.GetItemText(selected_index, 0)
        nom_ape = self.coordinadores_list.GetItemText(selected_index, 1)
        tel = self.coordinadores_list.GetItemText(selected_index, 2)
        direccion = self.coordinadores_list.GetItemText(selected_index, 3)
        fecha_nac = self.coordinadores_list.GetItemText(selected_index, 4)

        self.dni_text.SetValue(dni)
        self.nom_ape_text.SetValue(nom_ape)
        self.tel_text.SetValue(tel)
        self.direccion_text.SetValue(direccion)
        
        date = wx.DateTime() 
        if date.ParseISODate(fecha_nac):
           self.fecha_picker.SetValue(date)
        else:
            wx.MessageBox('Fecha inválida', 'Error', wx.OK | wx.ICON_ERROR)   

if __name__ == "__main__":
    app = wx.App(False)
    frame = FormularioCoordinadores(None)
    frame.Show()
    app.MainLoop()