import wx
import wx.adv
import mysql.connector
import datetime

class FormularioClientes(wx.Frame):
    def __init__(self, *args, **kw):
        super(FormularioClientes, self).__init__(*args, **kw)

        panel = wx.Panel(self)
        sizer = wx.BoxSizer(wx.VERTICAL)

        # Create a static box for client form
        formGroupBox = wx.StaticBox(panel, label="Datos del Cliente")
        formGroupBoxSizer = wx.StaticBoxSizer(formGroupBox, wx.VERTICAL)

        # Create form controls
        self.dni_label = wx.StaticText(panel, label="DNI:")
        self.dni_text = wx.TextCtrl(panel)

        self.nom_ape_label = wx.StaticText(panel, label="Nombre y Apellido:")
        self.nom_ape_text = wx.TextCtrl(panel)

        self.fecha_nac_label = wx.StaticText(panel, label="Fecha de Nacimiento:")
        self.fecha_picker = wx.adv.DatePickerCtrl(panel, style=wx.adv.DP_DROPDOWN | wx.adv.DP_SHOWCENTURY)

        self.domicilio_label = wx.StaticText(panel, label="Domicilio:")
        self.domicilio_text = wx.TextCtrl(panel)

        self.discapacidad_label = wx.StaticText(panel, label="Discapacidad:")
        self.discapacidad_text = wx.TextCtrl(panel)

        self.correo_label = wx.StaticText(panel, label="Correo:")
        self.correo_text = wx.TextCtrl(panel)

        self.tel_label = wx.StaticText(panel, label="Teléfono:")
        self.tel_text = wx.TextCtrl(panel)

        # Create buttons
        self.guardar_button = wx.Button(panel, label="Guardar")
        self.modificar_button = wx.Button(panel, label="Modificar")
        self.eliminar_button = wx.Button(panel, label="Eliminar")
        self.buscar_button = wx.Button(panel, label="Buscar")
        self.limpiar_button = wx.Button(panel, label="Limpiar")
        self.agregar_viaje_button = wx.Button(panel, label="Agregar a viaje")
        self.agregar_viaje_button.Disable()  # Start with the button disabled

        # Create ListCtrl to show existing clients
        self.clientes_list = wx.ListCtrl(panel, style=wx.LC_REPORT | wx.LC_SORT_ASCENDING)
        self.clientes_list.InsertColumn(0, "DNI", width=80)
        self.clientes_list.InsertColumn(1, "Nombre y Apellido", width=150)
        self.clientes_list.InsertColumn(2, "Fecha de Nacimiento", width=120)
        self.clientes_list.InsertColumn(3, "Domicilio", width=150)
        self.clientes_list.InsertColumn(4, "Discapacidad", width=100)
        self.clientes_list.InsertColumn(5, "Correo", width=150)
        self.clientes_list.InsertColumn(6, "Teléfono", width=100)

        # Arrange controls in sizers
        grid_sizer = wx.GridBagSizer(5, 5)
        grid_sizer.Add(self.dni_label, pos=(0, 0), flag=wx.ALIGN_RIGHT)
        grid_sizer.Add(self.dni_text, pos=(0, 1), flag=wx.EXPAND)
        grid_sizer.Add(self.nom_ape_label, pos=(1, 0), flag=wx.ALIGN_RIGHT)
        grid_sizer.Add(self.nom_ape_text, pos=(1, 1), flag=wx.EXPAND)
        grid_sizer.Add(self.fecha_nac_label, pos=(2, 0), flag=wx.ALIGN_RIGHT)
        grid_sizer.Add(self.fecha_picker, pos=(2, 1), flag=wx.EXPAND)
        grid_sizer.Add(self.domicilio_label, pos=(3, 0), flag=wx.ALIGN_RIGHT)
        grid_sizer.Add(self.domicilio_text, pos=(3, 1), flag=wx.EXPAND)
        grid_sizer.Add(self.discapacidad_label, pos=(4, 0), flag=wx.ALIGN_RIGHT)
        grid_sizer.Add(self.discapacidad_text, pos=(4, 1), flag=wx.EXPAND)
        grid_sizer.Add(self.correo_label, pos=(5, 0), flag=wx.ALIGN_RIGHT)
        grid_sizer.Add(self.correo_text, pos=(5, 1), flag=wx.EXPAND)
        grid_sizer.Add(self.tel_label, pos=(6, 0), flag=wx.ALIGN_RIGHT)
        grid_sizer.Add(self.tel_text, pos=(6, 1), flag=wx.EXPAND)
        grid_sizer.Add(self.guardar_button, pos=(7, 0))
        grid_sizer.Add(self.modificar_button, pos=(7, 1))
        grid_sizer.Add(self.eliminar_button, pos=(7, 2))
        grid_sizer.Add(self.buscar_button, pos=(7, 3))
        grid_sizer.Add(self.limpiar_button, pos=(7, 4))
        grid_sizer.Add(self.agregar_viaje_button, pos=(7, 5))  # Add the button to the sizer

        formGroupBoxSizer.Add(grid_sizer, proportion=1, flag=wx.EXPAND | wx.ALL, border=10)
        sizer.Add(formGroupBoxSizer, proportion=1, flag=wx.EXPAND | wx.ALL, border=10)
        sizer.Add(self.clientes_list, proportion=2, flag=wx.EXPAND | wx.ALL, border=10)

        panel.SetSizer(sizer)

        self.SetSize((900, 500))
        self.SetTitle("Formulario Clientes")
        self.Center()

        # Bind events
        self.guardar_button.Bind(wx.EVT_BUTTON, self.on_guardar)
        self.modificar_button.Bind(wx.EVT_BUTTON, self.on_modificar)
        self.eliminar_button.Bind(wx.EVT_BUTTON, self.on_eliminar)
        self.buscar_button.Bind(wx.EVT_BUTTON, self.on_buscar)
        self.limpiar_button.Bind(wx.EVT_BUTTON, self.on_limpiar)
        self.clientes_list.Bind(wx.EVT_LIST_ITEM_SELECTED, self.on_item_selected)
        self.agregar_viaje_button.Bind(wx.EVT_BUTTON, self.on_agregar_viaje)

        # Set up database connection
        self.conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="1234",
            database="tesina"
        )
        self.cursor = self.conn.cursor()

        # Load existing clients
        self.load_clientes()

    def load_clientes(self):
        self.clientes_list.DeleteAllItems()
        query = "SELECT Dni, Nom_ape, Fecha_Nac, Domicilio, Discapacidad, Correo, Tel FROM Cliente"
        try:
            self.cursor.execute(query)
            for row in self.cursor.fetchall():
                self.clientes_list.Append(row)
        except mysql.connector.Error as err:
            wx.MessageBox(f'Error al cargar datos: {err}', 'Error', wx.OK | wx.ICON_ERROR)

    def on_guardar(self, event):
        dni = self.dni_text.GetValue().strip()
        nom_ape = self.nom_ape_text.GetValue().strip()
        fecha_nac = self.fecha_picker.GetValue().FormatISODate()
        domicilio = self.domicilio_text.GetValue().strip()
        discapacidad = self.discapacidad_text.GetValue().strip()
        correo = self.correo_text.GetValue().strip()
        tel = self.tel_text.GetValue().strip()

        if not all([dni, nom_ape, fecha_nac, domicilio, discapacidad, correo, tel]):
            wx.MessageBox('Todos los campos deben estar completos.', 'Información', wx.OK | wx.ICON_WARNING)
            return

        query = "INSERT INTO Cliente (Dni, Nom_ape, Fecha_Nac, Domicilio, Discapacidad, Correo, Tel) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        try:
            self.cursor.execute(query, (dni, nom_ape, fecha_nac, domicilio, discapacidad, correo, tel))
            self.conn.commit()
            wx.MessageBox('Datos guardados correctamente', 'Info', wx.OK | wx.ICON_INFORMATION)
            self.load_clientes()
        except mysql.connector.Error as err:
            wx.MessageBox(f'Error al guardar datos: {err}', 'Error', wx.OK | wx.ICON_ERROR)

    def on_modificar(self, event):
        dni = self.dni_text.GetValue().strip()
        nom_ape = self.nom_ape_text.GetValue().strip()
        fecha_nac = self.fecha_picker.GetValue().FormatISODate()
        domicilio = self.domicilio_text.GetValue().strip()
        discapacidad = self.discapacidad_text.GetValue().strip()
        correo = self.correo_text.GetValue().strip()
        tel = self.tel_text.GetValue().strip()

        if not all([dni, nom_ape, fecha_nac, domicilio, discapacidad, correo, tel]):
            wx.MessageBox('Todos los campos deben estar completos.', 'Información', wx.OK | wx.ICON_WARNING)
            return

        query = "UPDATE Cliente SET Nom_ape=%s, Fecha_Nac=%s, Domicilio=%s, Discapacidad=%s, Correo=%s, Tel=%s WHERE Dni=%s"
        try:
            self.cursor.execute(query, (nom_ape, fecha_nac, domicilio, discapacidad, correo, tel, dni))
            self.conn.commit()
            wx.MessageBox('Datos modificados correctamente', 'Info', wx.OK | wx.ICON_INFORMATION)
            self.load_clientes()
        except mysql.connector.Error as err:
            wx.MessageBox(f'Error al modificar datos: {err}', 'Error', wx.OK | wx.ICON_ERROR)

    def on_eliminar(self, event):
        dni = self.dni_text.GetValue().strip()

        if not dni:
            wx.MessageBox('Debe ingresar el DNI del cliente a eliminar.', 'Información', wx.OK | wx.ICON_WARNING)
            return

        query = "DELETE FROM Cliente WHERE Dni=%s"
        try:
            self.cursor.execute(query, (dni,))
            self.conn.commit()
            wx.MessageBox('Cliente eliminado correctamente', 'Info', wx.OK | wx.ICON_INFORMATION)
            self.load_clientes()
        except mysql.connector.Error as err:
            wx.MessageBox(f'Error al eliminar cliente: {err}', 'Error', wx.OK | wx.ICON_ERROR)

    def on_buscar(self, event):
        dni = self.dni_text.GetValue().strip()

        if not dni:
           wx.MessageBox('Debe ingresar el DNI del cliente a buscar.', 'Información', wx.OK | wx.ICON_WARNING)
           return

        query = "SELECT Dni, Nom_ape, Fecha_Nac, Domicilio, Discapacidad, Correo, Tel FROM Cliente WHERE Dni=%s"
        try:
            self.cursor.execute(query, (dni,))
            result = self.cursor.fetchone()

            if result:
               self.clientes_list.DeleteAllItems()
               self.clientes_list.Append(result)
               self.dni_text.SetValue(str(result[0]))  # Convert to string
               self.nom_ape_text.SetValue(str(result[1]))  # Convert to string

            # Convert the date from ISO format (assuming the date is in YYYY-MM-DD format)
               fecha_nac_str = result[2].strftime('%Y-%m-%d') if isinstance(result[2], datetime.date) else result[2]
               fecha_nac_date = wx.DateTime()
               fecha_nac_date.ParseDate(fecha_nac_str)
               self.fecha_picker.SetValue(fecha_nac_date)

               self.domicilio_text.SetValue(str(result[3]))  # Convert to string
               self.discapacidad_text.SetValue(str(result[4]))  # Convert to string
               self.correo_text.SetValue(str(result[5]))  # Convert to string
               self.tel_text.SetValue(str(result[6]))  # Convert to string
             
               self.agregar_viaje_button.Enable()  # Enable the button when a client is found
            else:
                wx.MessageBox('No se encontró el cliente.', 'Información', wx.OK | wx.ICON_INFORMATION)
                self.clientes_list.DeleteAllItems()
                self.agregar_viaje_button.Disable()  # Disable the button if no client is found
        except mysql.connector.Error as err:
         wx.MessageBox(f'Error al buscar cliente: {err}', 'Error', wx.OK | wx.ICON_ERROR)

    def on_item_selected(self, event):
        self.agregar_viaje_button.Enable()  # Enable the button when an item is selected

    def on_limpiar(self, event):
        self.dni_text.Clear()
        self.nom_ape_text.Clear()
        self.fecha_picker.SetValue(wx.DateTime.Now())
        self.domicilio_text.Clear()
        self.discapacidad_text.Clear()
        self.correo_text.Clear()
        self.tel_text.Clear()
        self.clientes_list.DeleteAllItems()
        self.agregar_viaje_button.Disable()  # Disable the button on clear

    def on_agregar_viaje(self, event):
        # Define functionality for adding client to a trip here
        wx.MessageBox('Función "Agregar a viaje" no implementada.', 'Información', wx.OK | wx.ICON_INFORMATION)

    def __del__(self):
        self.cursor.close()
        self.conn.close()

if __name__ == "__main__":
    app = wx.App()
    frame = FormularioClientes(None)
    frame.Show()
    app.MainLoop()
