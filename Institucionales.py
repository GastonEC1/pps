import wx
import mysql.connector
from jugadores import FormularioJugadores

class FormularioInstitucionales(wx.Frame):
    def __init__(self, parent, title):
        super(FormularioInstitucionales, self).__init__(parent, title=title, size=(800, 600))

        panel = wx.Panel(self)
        sizer = wx.BoxSizer(wx.VERTICAL)

        # Crear formulario para agregar nuevas instituciones
        form_sizer = wx.GridBagSizer(5, 5)

        self.nombre_label = wx.StaticText(panel, label="Nombre:")
        self.nombre_text = wx.TextCtrl(panel)
        form_sizer.Add(self.nombre_label, pos=(0, 0), flag=wx.ALIGN_RIGHT)
        form_sizer.Add(self.nombre_text, pos=(0, 1), flag=wx.EXPAND)

        self.tipo_label = wx.StaticText(panel, label="Tipo:")
        self.tipo_text = wx.TextCtrl(panel)
        form_sizer.Add(self.tipo_label, pos=(1, 0), flag=wx.ALIGN_RIGHT)
        form_sizer.Add(self.tipo_text, pos=(1, 1), flag=wx.EXPAND)

        self.direccion_label = wx.StaticText(panel, label="Dirección:")
        self.direccion_text = wx.TextCtrl(panel)
        form_sizer.Add(self.direccion_label, pos=(2, 0), flag=wx.ALIGN_RIGHT)
        form_sizer.Add(self.direccion_text, pos=(2, 1), flag=wx.EXPAND)

        self.tel_label = wx.StaticText(panel, label="Teléfono:")
        self.tel_text = wx.TextCtrl(panel)
        form_sizer.Add(self.tel_label, pos=(3, 0), flag=wx.ALIGN_RIGHT)
        form_sizer.Add(self.tel_text, pos=(3, 1), flag=wx.EXPAND)

        self.correo_label = wx.StaticText(panel, label="Correo:")
        self.correo_text = wx.TextCtrl(panel)
        form_sizer.Add(self.correo_label, pos=(4, 0), flag=wx.ALIGN_RIGHT)
        form_sizer.Add(self.correo_text, pos=(4, 1), flag=wx.EXPAND)

        button_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.agregar_button = wx.Button(panel, label="Agregar Institución")

        self.buscar_button = wx.Button(panel, label="Buscar Institución")

        self.modificar_button = wx.Button(panel, label="Modificar Institución")
        self.eliminar_button = wx.Button(panel, label="Eliminar Institución")
        self.limpiar_button = wx.Button(panel, label="Limpiar Campos")  # Nuevo botón de limpiar

        button_sizer.Add(self.agregar_button, flag=wx.EXPAND)
        button_sizer.Add(self.buscar_button, flag=wx.EXPAND)
        button_sizer.Add(self.modificar_button, flag=wx.EXPAND)
        button_sizer.Add(self.eliminar_button, flag=wx.EXPAND)
        button_sizer.Add(self.limpiar_button, flag=wx.EXPAND)  # Añadir botón de limpiar al sizer

        form_sizer.Add(button_sizer, pos=(5, 0), span=(1, 2), flag=wx.EXPAND | wx.ALIGN_CENTER_VERTICAL, border=10)

        sizer.Add(form_sizer, flag=wx.EXPAND | wx.ALL, border=10)

        # Crear grilla de instituciones
        self.instituciones_list = wx.ListCtrl(panel, style=wx.LC_REPORT | wx.LC_SORT_ASCENDING)
        self.instituciones_list.InsertColumn(0, "ID", width=50)
        self.instituciones_list.InsertColumn(1, "Nombre", width=150)
        self.instituciones_list.InsertColumn(2, "Tipo", width=100)
        self.instituciones_list.InsertColumn(3, "Dirección", width=150)
        self.instituciones_list.InsertColumn(4, "Teléfono", width=100)
        self.instituciones_list.InsertColumn(5, "Correo", width=150)

        sizer.Add(self.instituciones_list, proportion=1, flag=wx.EXPAND | wx.ALL, border=10)

        self.ver_jugadores_button = wx.Button(panel, label="Ver Integrantes")
        sizer.Add(self.ver_jugadores_button, flag=wx.EXPAND | wx.ALL, border=10)

        panel.SetSizer(sizer)

        self.Bind(wx.EVT_BUTTON, self.on_agregar_institucion, self.agregar_button)
        self.Bind(wx.EVT_BUTTON, self.on_buscar_institucion, self.buscar_button)
        self.Bind(wx.EVT_BUTTON, self.on_modificar_institucion, self.modificar_button)
        self.Bind(wx.EVT_BUTTON, self.on_eliminar_institucion, self.eliminar_button)
        self.Bind(wx.EVT_BUTTON, self.on_limpiar, self.limpiar_button)  
        self.Bind(wx.EVT_BUTTON, self.on_ver_jugadores, self.ver_jugadores_button)
        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.on_item_selected, self.instituciones_list)

        # Set up database connection
        self.conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="1234",
            database="tesina"
        )
        self.cursor = self.conn.cursor()

        # Load existing instituciones data
        self.load_instituciones()

    def load_instituciones(self):
        self.instituciones_list.DeleteAllItems()
        query = "SELECT Id, Nombre, Tipo, Direccion, Tel, Correo FROM Institucional"
        try:
            self.cursor.execute(query)
            for row in self.cursor.fetchall():
                self.instituciones_list.Append(row)
        except mysql.connector.Error as err:
            wx.MessageBox(f'Error al cargar datos: {err}', 'Error', wx.OK | wx.ICON_ERROR)

    def on_agregar_institucion(self, event):
        nombre = self.nombre_text.GetValue().strip()
        tipo = self.tipo_text.GetValue().strip()
        direccion = self.direccion_text.GetValue().strip()
        tel = self.tel_text.GetValue().strip()
        correo = self.correo_text.GetValue().strip()

        if not all([nombre, tipo, direccion, tel, correo]):
            wx.MessageBox('Todos los campos deben estar completos.', 'Información', wx.OK | wx.ICON_WARNING)
            return

        query = "INSERT INTO Institucional (Nombre, Tipo, Direccion, Tel, Correo) VALUES (%s, %s, %s, %s, %s)"
        try:
            self.cursor.execute(query, (nombre, tipo, direccion, tel, correo))
            self.conn.commit()
            wx.MessageBox('Institución agregada correctamente', 'Info', wx.OK | wx.ICON_INFORMATION)
            self.load_instituciones()
            self.on_limpiar(None)  # Limpiar los campos después de agregar
        except mysql.connector.Error as err:
            wx.MessageBox(f'Error al agregar institución: {err}', 'Error', wx.OK | wx.ICON_ERROR)

    def on_buscar_institucion(self, event):
        nombre = wx.GetTextFromUser("Ingrese el nombre de la institución:", "Buscar Institución")
        if nombre:
            query = "SELECT Id, Nombre, Tipo, Direccion, Tel, Correo FROM Institucional WHERE Nombre LIKE %s"
            try:
                self.cursor.execute(query, (f'%{nombre}%',))
                self.instituciones_list.DeleteAllItems()
                for row in self.cursor.fetchall():
                    self.instituciones_list.Append(row)
            except mysql.connector.Error as err:
                wx.MessageBox(f'Error al buscar institución: {err}', 'Error', wx.OK | wx.ICON_ERROR)

    def on_modificar_institucion(self, event):
        selected_index = self.instituciones_list.GetFirstSelected()
        if selected_index == -1:
            wx.MessageBox('Seleccione una institución para modificar.', 'Información', wx.OK | wx.ICON_WARNING)
            return

        institucion_id = self.instituciones_list.GetItemText(selected_index, 0)
        nombre = wx.GetTextFromUser("Ingrese el nuevo nombre de la institución:", "Modificar Institución", 
                                   self.instituciones_list.GetItemText(selected_index, 1))
        tipo = wx.GetTextFromUser("Ingrese el nuevo tipo de la institución:", "Modificar Institución", 
                                  self.instituciones_list.GetItemText(selected_index, 2))
        direccion = wx.GetTextFromUser("Ingrese la nueva dirección de la institución:", "Modificar Institución", 
                                       self.instituciones_list.GetItemText(selected_index, 3))
        tel = wx.GetTextFromUser("Ingrese el nuevo teléfono de la institución:", "Modificar Institución", 
                                 self.instituciones_list.GetItemText(selected_index, 4))
        correo = wx.GetTextFromUser("Ingrese el nuevo correo de la institución:", "Modificar Institución", 
                                    self.instituciones_list.GetItemText(selected_index, 5))

        if not all([nombre, tipo, direccion, tel, correo]):
            wx.MessageBox('Todos los campos deben estar completos.', 'Información', wx.OK | wx.ICON_WARNING)
            return

        query = "UPDATE Institucional SET Nombre=%s, Tipo=%s, Direccion=%s, Tel=%s, Correo=%s WHERE Id=%s"
        try:
            self.cursor.execute(query, (nombre, tipo, direccion, tel, correo, institucion_id))
            self.conn.commit()
            wx.MessageBox('Institución modificada correctamente', 'Info', wx.OK | wx.ICON_INFORMATION)
            self.load_instituciones()
            self.on_limpiar(None)  # Limpiar los campos después de modificar
        except mysql.connector.Error as err:
            wx.MessageBox(f'Error al modificar institución: {err}', 'Error', wx.OK | wx.ICON_ERROR)

    def on_eliminar_institucion(self, event):
        selected_index = self.instituciones_list.GetFirstSelected()
        if selected_index == -1:
            wx.MessageBox('Seleccione una institución para eliminar.', 'Información', wx.OK | wx.ICON_WARNING)
            return

        institucion_id = self.instituciones_list.GetItemText(selected_index, 0)
        dialog = wx.MessageDialog(self, '¿Está seguro que desea eliminar esta institución?', 
                                  'Confirmar Eliminación', wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION)
        if dialog.ShowModal() == wx.ID_YES:
            query = "DELETE FROM Institucional WHERE Id=%s"
            try:
                self.cursor.execute(query, (institucion_id,))
                self.conn.commit()
                wx.MessageBox('Institución eliminada correctamente', 'Info', wx.OK | wx.ICON_INFORMATION)
                self.load_instituciones()
                self.on_limpiar(None)  # Limpiar los campos después de eliminar
            except mysql.connector.Error as err:
                wx.MessageBox(f'Error al eliminar institución: {err}', 'Error', wx.OK | wx.ICON_ERROR)
        dialog.Destroy()

    def on_limpiar(self, event):
        self.nombre_text.Clear()
        self.tipo_text.Clear()
        self.direccion_text.Clear()
        self.tel_text.Clear()
        self.correo_text.Clear()

    def on_item_selected(self, event):
        selected_index = self.instituciones_list.GetFirstSelected()
        if selected_index != -1:
            self.nombre_text.SetValue(self.instituciones_list.GetItemText(selected_index, 1))
            self.tipo_text.SetValue(self.instituciones_list.GetItemText(selected_index, 2))
            self.direccion_text.SetValue(self.instituciones_list.GetItemText(selected_index, 3))
            self.tel_text.SetValue(self.instituciones_list.GetItemText(selected_index, 4))
            self.correo_text.SetValue(self.instituciones_list.GetItemText(selected_index, 5))

    def on_ver_jugadores(self, event):
        selected_index = self.instituciones_list.GetFirstSelected()
        if selected_index == -1:
            wx.MessageBox('Seleccione una institución para ver los jugadores.', 'Información', wx.OK | wx.ICON_WARNING)
            return

        id_institucional = self.instituciones_list.GetItemText(selected_index, 0)
        nombre_institucional = self.instituciones_list.GetItemText(selected_index, 1)

        jugadores_form = FormularioJugadores(None, id_institucional, nombre_institucional)
        jugadores_form.Show()

app = wx.App(False)
frame = FormularioInstitucionales(None, "Gestión de Instituciones")
frame.Show()
app.MainLoop()
