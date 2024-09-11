import wx
import mysql.connector
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.units import inch
from reportlab.lib import colors
from io import BytesIO

class FormularioJugadores(wx.Frame):
    def __init__(self, parent, id_institucional, nombre_institucional):
        super(FormularioJugadores, self).__init__(parent, title="Gestión de Integrantes", size=(800, 600))

        self.id_institucional = id_institucional
        self.nombre_institucional = nombre_institucional

        panel = wx.Panel(self)
        sizer = wx.BoxSizer(wx.VERTICAL)

        # Crear formulario para agregar nuevos jugadores
        form_sizer = wx.GridBagSizer(5, 5)

        self.nombre_label = wx.StaticText(panel, label="Nombre:")
        self.nombre_text = wx.TextCtrl(panel)
        form_sizer.Add(self.nombre_label, pos=(0, 0), flag=wx.ALIGN_RIGHT)
        form_sizer.Add(self.nombre_text, pos=(0, 1), flag=wx.EXPAND)

        self.tipo_label = wx.StaticText(panel, label="Tipo:")
        self.tipo_text = wx.TextCtrl(panel)
        form_sizer.Add(self.tipo_label, pos=(1, 0), flag=wx.ALIGN_RIGHT)
        form_sizer.Add(self.tipo_text, pos=(1, 1), flag=wx.EXPAND)

        self.fecha_nac_label = wx.StaticText(panel, label="Fecha de Nacimiento:")
        self.fecha_nac_text = wx.TextCtrl(panel)
        form_sizer.Add(self.fecha_nac_label, pos=(2, 0), flag=wx.ALIGN_RIGHT)
        form_sizer.Add(self.fecha_nac_text, pos=(2, 1), flag=wx.EXPAND)

        self.direccion_label = wx.StaticText(panel, label="Dirección:")
        self.direccion_text = wx.TextCtrl(panel)
        form_sizer.Add(self.direccion_label, pos=(3, 0), flag=wx.ALIGN_RIGHT)
        form_sizer.Add(self.direccion_text, pos=(3, 1), flag=wx.EXPAND)

        self.tel_label = wx.StaticText(panel, label="Teléfono:")
        self.tel_text = wx.TextCtrl(panel)
        form_sizer.Add(self.tel_label, pos=(4, 0), flag=wx.ALIGN_RIGHT)
        form_sizer.Add(self.tel_text, pos=(4, 1), flag=wx.EXPAND)

        self.correo_label = wx.StaticText(panel, label="Correo:")
        self.correo_text = wx.TextCtrl(panel)
        form_sizer.Add(self.correo_label, pos=(5, 0), flag=wx.ALIGN_RIGHT)
        form_sizer.Add(self.correo_text, pos=(5, 1), flag=wx.EXPAND)

        self.dni_label = wx.StaticText(panel, label="DNI:")
        self.dni_text = wx.TextCtrl(panel)
        form_sizer.Add(self.dni_label, pos=(6, 0), flag=wx.ALIGN_RIGHT)
        form_sizer.Add(self.dni_text, pos=(6, 1), flag=wx.EXPAND)

        button_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.agregar_button = wx.Button(panel, label="Agregar Jugador")
        self.modificar_button = wx.Button(panel, label="Modificar Jugador")
        self.eliminar_button = wx.Button(panel, label="Eliminar Jugador")
        self.limpiar_button = wx.Button(panel, label="Limpiar Campos")
        self.generar_pdf_button = wx.Button(panel, label="Generar PDF")

        button_sizer.Add(self.agregar_button, flag=wx.EXPAND)
        button_sizer.Add(self.modificar_button, flag=wx.EXPAND)
        button_sizer.Add(self.eliminar_button, flag=wx.EXPAND)
        button_sizer.Add(self.limpiar_button, flag=wx.EXPAND)
        button_sizer.Add(self.generar_pdf_button, flag=wx.EXPAND)

        form_sizer.Add(button_sizer, pos=(7, 0), span=(1, 2), flag=wx.EXPAND | wx.ALIGN_CENTER_VERTICAL, border=10)

        sizer.Add(form_sizer, flag=wx.EXPAND | wx.ALL, border=10)

        # Crear grilla de jugadores
        self.jugadores_list = wx.ListCtrl(panel, style=wx.LC_REPORT | wx.LC_SORT_ASCENDING)
        self.jugadores_list.InsertColumn(0, "ID", width=50)
        self.jugadores_list.InsertColumn(1, "Nombre", width=150)
        self.jugadores_list.InsertColumn(2, "Tipo", width=100)
        self.jugadores_list.InsertColumn(3, "Fecha de Nacimiento", width=120)
        self.jugadores_list.InsertColumn(4, "Dirección", width=150)
        self.jugadores_list.InsertColumn(5, "Teléfono", width=100)
        self.jugadores_list.InsertColumn(6, "Correo", width=150)
        self.jugadores_list.InsertColumn(7, "DNI", width=100)

        sizer.Add(self.jugadores_list, proportion=1, flag=wx.EXPAND | wx.ALL, border=10)

        panel.SetSizer(sizer)

        self.Bind(wx.EVT_BUTTON, self.on_agregar_jugador, self.agregar_button)
        self.Bind(wx.EVT_BUTTON, self.on_modificar_jugador, self.modificar_button)
        self.Bind(wx.EVT_BUTTON, self.on_eliminar_jugador, self.eliminar_button)
        self.Bind(wx.EVT_BUTTON, self.on_limpiar, self.limpiar_button)
        self.Bind(wx.EVT_BUTTON, self.on_generar_pdf, self.generar_pdf_button)
        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.on_item_selected, self.jugadores_list)

        # Set up database connection
        self.conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="123456789",
            database="tesina"
        )
        self.cursor = self.conn.cursor()

        # Load existing jugadores data
        self.load_jugadores()

    def load_jugadores(self):
        self.jugadores_list.DeleteAllItems()
        query = "SELECT Id, Nombre, Tipo, Fecha_Nac, Direccion, Tel, Correo, Dni FROM Jugadores WHERE Institucional_Id = %s"
        try:
            self.cursor.execute(query, (self.id_institucional,))
            for row in self.cursor.fetchall():
                self.jugadores_list.Append(row)
        except mysql.connector.Error as err:
            wx.MessageBox(f'Error al cargar datos: {err}', 'Error', wx.OK | wx.ICON_ERROR)

    def on_agregar_jugador(self, event):
        nombre = self.nombre_text.GetValue().strip()
        tipo = self.tipo_text.GetValue().strip()
        fecha_nac = self.fecha_nac_text.GetValue().strip()
        direccion = self.direccion_text.GetValue().strip()
        tel = self.tel_text.GetValue().strip()
        correo = self.correo_text.GetValue().strip()
        dni = self.dni_text.GetValue().strip()

        if not all([nombre, tipo, fecha_nac, direccion, tel, correo, dni]):
            wx.MessageBox('Todos los campos deben estar completos.', 'Información', wx.OK | wx.ICON_WARNING)
            return

        query = "INSERT INTO Jugadores (Nombre, Tipo, Fecha_Nac, Direccion, Tel, Correo, Dni, Institucional_Id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        try:
            self.cursor.execute(query, (nombre, tipo, fecha_nac, direccion, tel, correo, dni, self.id_institucional))
            self.conn.commit()
            wx.MessageBox('Jugador agregado correctamente', 'Info', wx.OK | wx.ICON_INFORMATION)
            self.load_jugadores()
            self.on_limpiar(None)  # Limpiar los campos después de agregar
        except mysql.connector.Error as err:
            wx.MessageBox(f'Error al agregar jugador: {err}', 'Error', wx.OK | wx.ICON_ERROR)

    def on_modificar_jugador(self, event):
        selected_index = self.jugadores_list.GetFirstSelected()
        if selected_index == -1:
            wx.MessageBox('Seleccione un jugador para modificar.', 'Información', wx.OK | wx.ICON_WARNING)
            return

        jugador_id = self.jugadores_list.GetItemText(selected_index, 0)
        nombre = wx.GetTextFromUser("Ingrese el nuevo nombre del jugador:", "Modificar Jugador", 
                                   self.jugadores_list.GetItemText(selected_index, 1))
        tipo = wx.GetTextFromUser("Ingrese el nuevo tipo del jugador:", "Modificar Jugador", 
                                  self.jugadores_list.GetItemText(selected_index, 2))
        fecha_nac = wx.GetTextFromUser("Ingrese la nueva fecha de nacimiento del jugador (YYYY-MM-DD):", "Modificar Jugador", 
                                       self.jugadores_list.GetItemText(selected_index, 3))
        direccion = wx.GetTextFromUser("Ingrese la nueva dirección del jugador:", "Modificar Jugador", 
                                       self.jugadores_list.GetItemText(selected_index, 4))
        tel = wx.GetTextFromUser("Ingrese el nuevo teléfono del jugador:", "Modificar Jugador", 
                                 self.jugadores_list.GetItemText(selected_index, 5))
        correo = wx.GetTextFromUser("Ingrese el nuevo correo del jugador:", "Modificar Jugador", 
                                    self.jugadores_list.GetItemText(selected_index, 6))
        dni = wx.GetTextFromUser("Ingrese el nuevo DNI del jugador:", "Modificar Jugador", 
                                 self.jugadores_list.GetItemText(selected_index, 7))

        if not all([nombre, tipo, fecha_nac, direccion, tel, correo, dni]):
            wx.MessageBox('Todos los campos deben estar completos.', 'Información', wx.OK | wx.ICON_WARNING)
            return

        query = "UPDATE Jugadores SET Nombre=%s, Tipo=%s, Fecha_Nac=%s, Direccion=%s, Tel=%s, Correo=%s, Dni=%s WHERE Id=%s"
        try:
            self.cursor.execute(query, (nombre, tipo, fecha_nac, direccion, tel, correo, dni, jugador_id))
            self.conn.commit()
            wx.MessageBox('Jugador modificado correctamente', 'Info', wx.OK | wx.ICON_INFORMATION)
            self.load_jugadores()
        except mysql.connector.Error as err:
            wx.MessageBox(f'Error al modificar jugador: {err}', 'Error', wx.OK | wx.ICON_ERROR)

    def on_eliminar_jugador(self, event):
        selected_index = self.jugadores_list.GetFirstSelected()
        if selected_index == -1:
            wx.MessageBox('Seleccione un jugador para eliminar.', 'Información', wx.OK | wx.ICON_WARNING)
            return

        jugador_id = self.jugadores_list.GetItemText(selected_index, 0)
        dlg = wx.MessageDialog(self, f'¿Está seguro de que desea eliminar el jugador con ID {jugador_id}?', 
                               'Confirmar Eliminación', wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION)
        if dlg.ShowModal() == wx.ID_YES:
            query = "DELETE FROM Jugadores WHERE Id=%s"
            try:
                self.cursor.execute(query, (jugador_id,))
                self.conn.commit()
                wx.MessageBox('Jugador eliminado correctamente', 'Info', wx.OK | wx.ICON_INFORMATION)
                self.load_jugadores()
            except mysql.connector.Error as err:
                wx.MessageBox(f'Error al eliminar jugador: {err}', 'Error', wx.OK | wx.ICON_ERROR)

    def on_limpiar(self, event):
        self.nombre_text.SetValue("")
        self.tipo_text.SetValue("")
        self.fecha_nac_text.SetValue("")
        self.direccion_text.SetValue("")
        self.tel_text.SetValue("")
        self.correo_text.SetValue("")
        self.dni_text.SetValue("")

    def on_generar_pdf(self, event):
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        styles = getSampleStyleSheet()
        
        title_style = ParagraphStyle(name='TitleStyle', fontSize=18, alignment=1, spaceAfter=12)
        normal_style = styles['Normal']
        normal_style.alignment = 0
        normal_style.fontSize = 10
        
        title = Paragraph(f"Listado de Integrantes - {self.nombre_institucional}", title_style)
        
        data = [["ID", "Nombre", "Tipo", "Fecha de Nacimiento", "Dirección", "Teléfono", "Correo", "DNI"]]
        
        query = "SELECT Id, Nombre, Tipo, Fecha_Nac, Direccion, Tel, Correo, Dni FROM Jugadores WHERE Institucional_Id = %s"
        try:
            self.cursor.execute(query, (self.id_institucional,))
            for row in self.cursor.fetchall():
                data.append(row)
        except mysql.connector.Error as err:
            wx.MessageBox(f'Error al cargar datos: {err}', 'Error', wx.OK | wx.ICON_ERROR)
            return
        
        table = Table(data)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONT', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONT', (0, 1), (-1, -1), 'Helvetica'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))

        content = [title, table]

        doc.build(content)
        
        buffer.seek(0)
        
        with open("listado_integrantes.pdf", "wb") as f:
            f.write(buffer.read())
        
        wx.MessageBox('PDF generado correctamente', 'Información', wx.OK | wx.ICON_INFORMATION)

    def on_item_selected(self, event):
        selected_index = self.jugadores_list.GetFirstSelected()
        if selected_index != -1:
            self.nombre_text.SetValue(self.jugadores_list.GetItemText(selected_index, 1))
            self.tipo_text.SetValue(self.jugadores_list.GetItemText(selected_index, 2))
            self.fecha_nac_text.SetValue(self.jugadores_list.GetItemText(selected_index, 3))
            self.direccion_text.SetValue(self.jugadores_list.GetItemText(selected_index, 4))
            self.tel_text.SetValue(self.jugadores_list.GetItemText(selected_index, 5))
            self.correo_text.SetValue(self.jugadores_list.GetItemText(selected_index, 6))
            self.dni_text.SetValue(self.jugadores_list.GetItemText(selected_index, 7))

if __name__ == "__main__":
    app = wx.App(False)
    frame = FormularioJugadores(None, 1, "Institución de Ejemplo")
    frame.Show()
    app.MainLoop()
