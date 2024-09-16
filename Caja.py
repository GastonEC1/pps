import wx
import wx.adv as adv
import mysql.connector
from mysql.connector import Error
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import pandas as pd
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

        self.viaje_label = wx.StaticText(panel, label="Destino de Viaje:")
        self.viaje_combo = wx.ComboBox(panel, style=wx.CB_READONLY)

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
        self.caja_list.InsertColumn(5, "Destino Viaje", width=150)

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
        formGridSizer.Add(self.viaje_combo, pos=(4, 1), flag=wx.EXPAND)
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

        # Load existing Viajes data into ComboBox
        self.load_viajes()

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
            viaje_id INT,
            FOREIGN KEY (viaje_id) REFERENCES viajes(Id)
        )
        """
        try:
            self.cursor.execute(query)
            self.conn.commit()
        except Error as err:
            wx.MessageBox(f'Error al crear la tabla Historial: {err}', 'Error', wx.OK | wx.ICON_ERROR)

    def load_viajes(self):
        query = "SELECT Id, Destino FROM viajes"
        try:
            self.cursor.execute(query)
            viajes = self.cursor.fetchall()
            self.viaje_combo.Clear()
            for viaje in viajes:
                self.viaje_combo.Append(f"{viaje[1]} (ID: {viaje[0]})", viaje[0])
        except Error as err:
            wx.MessageBox(f'Error al cargar datos de viajes: {err}', 'Error', wx.OK | wx.ICON_ERROR)

    def load_caja(self):
        self.caja_list.DeleteAllItems()
        query = """
        SELECT Caja.Id, Caja.tipo, Caja.monto, Caja.fecha, Caja.descripcion, viajes.Destino
        FROM Caja
        JOIN viajes ON Caja.viaje_id = viajes.Id
        """
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
        viaje_id = self.viaje_combo.GetClientData(self.viaje_combo.GetSelection())

        # Validate that all fields are filled
        if not all([tipo, monto, descripcion, viaje_id]):
            wx.MessageBox('Todos los campos deben estar completos.', 'Información', wx.OK | wx.ICON_WARNING)
            return

        query = "INSERT INTO Caja (tipo, monto, fecha, descripcion, viaje_id) VALUES (%s, %s, %s, %s, %s)"
        try:
            self.cursor.execute(query, (tipo, monto, fecha, descripcion, viaje_id))
            self.conn.commit()

            # Also insert into Historial
            query_historial = "INSERT INTO Historial (tipo, monto, fecha, descripcion, viaje_id) VALUES (%s, %s, %s, %s, %s)"
            self.cursor.execute(query_historial, (tipo, monto, fecha, descripcion, viaje_id))
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
        viaje_id = self.viaje_combo.GetClientData(self.viaje_combo.GetSelection())

        # Validate that all fields are filled
        if not all([tipo, monto, descripcion, viaje_id]):
            wx.MessageBox('Todos los campos deben estar completos.', 'Información', wx.OK | wx.ICON_WARNING)
            return

        query = """
        UPDATE Caja
        SET tipo = %s, monto = %s, fecha = %s, descripcion = %s, viaje_id = %s
        WHERE Id = %s
        """
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

        if wx.MessageBox('¿Está seguro de que desea eliminar esta entrada?', 'Confirmación', wx.YES_NO | wx.ICON_QUESTION) == wx.YES:
            query = "DELETE FROM Caja WHERE Id = %s"
            try:
                self.cursor.execute(query, (id_caja,))
                self.conn.commit()
                wx.MessageBox('Entrada eliminada correctamente', 'Info', wx.OK | wx.ICON_INFORMATION)
                self.load_caja()
            except Error as err:
                wx.MessageBox(f'Error al eliminar datos: {err}', 'Error', wx.OK | wx.ICON_ERROR)

    def on_buscar(self, event):
        search_dialog = wx.TextEntryDialog(self, "Ingrese el ID de la entrada de caja a buscar:", "Buscar Entrada")
        if search_dialog.ShowModal() == wx.ID_OK:
            search_id = search_dialog.GetValue().strip()
            query = """
            SELECT Caja.Id, Caja.tipo, Caja.monto, Caja.fecha, Caja.descripcion, viajes.Destino
            FROM Caja
            JOIN viajes ON Caja.viaje_id = viajes.Id
            WHERE Caja.Id = %s
            """
            try:
                self.cursor.execute(query, (search_id,))
                result = self.cursor.fetchone()
                if result:
                    self.caja_list.DeleteAllItems()
                    self.caja_list.Append(result)
                else:
                    wx.MessageBox('No se encontraron resultados.', 'Información', wx.OK | wx.ICON_INFORMATION)
            except Error as err:
                wx.MessageBox(f'Error al buscar datos: {err}', 'Error', wx.OK | wx.ICON_ERROR)

    def on_limpiar(self, event):
        self.tipo_combo.SetValue('')
        self.monto_text.SetValue('')
        self.fecha_picker.SetValue(wx.DateTime.Now())
        self.descripcion_text.SetValue('')
        self.viaje_combo.SetSelection(-1)

    def on_finalizar_dia(self, event):
        # Generar el informe PDF para el día actual
        fecha = wx.DateTime.Now().FormatISODate()
        file_name = f"Informe_{fecha}.pdf"

        c = canvas.Canvas(file_name, pagesize=letter)
        width, height = letter

        c.drawString(100, height - 100, f"Informe del Día {fecha}")
        c.drawString(100, height - 120, "Detalles de Caja:")

        query = """
        SELECT Caja.Id, Caja.tipo, Caja.monto, Caja.fecha, Caja.descripcion, viajes.Destino
        FROM Caja
        JOIN viajes ON Caja.viaje_id = viajes.Id
        WHERE Caja.fecha = %s
        """
        try:
            self.cursor.execute(query, (fecha,))
            y = height - 140
            for row in self.cursor.fetchall():
                line = f"ID: {row[0]}, Tipo: {row[1]}, Monto: {row[2]}, Fecha: {row[3]}, Descripción: {row[4]}, Destino: {row[5]}"
                c.drawString(100, y, line)
                y -= 20
            c.save()

            wx.MessageBox(f'Informe del día generado: {file_name}', 'Info', wx.OK | wx.ICON_INFORMATION)
        except Error as err:
            wx.MessageBox(f'Error al generar el informe: {err}', 'Error', wx.OK | wx.ICON_ERROR)

    def on_historial(self, event):
        historial_dialog = wx.Dialog(self, title="Historial de Caja", size=(800, 600))

        sizer = wx.BoxSizer(wx.VERTICAL)

        # Create date range selectors
        date_sizer = wx.BoxSizer(wx.HORIZONTAL)
        start_date_label = wx.StaticText(historial_dialog, label="Fecha de Inicio:")
        end_date_label = wx.StaticText(historial_dialog, label="Fecha de Fin:")
        self.start_date_picker = adv.DatePickerCtrl(historial_dialog, style=adv.DP_DROPDOWN | adv.DP_SHOWCENTURY)
        self.end_date_picker = adv.DatePickerCtrl(historial_dialog, style=adv.DP_DROPDOWN | adv.DP_SHOWCENTURY)
        filter_button = wx.Button(historial_dialog, label="Filtrar")
        export_button = wx.Button(historial_dialog, label="Exportar a Excel")

        date_sizer.Add(start_date_label, flag=wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, border=5)
        date_sizer.Add(self.start_date_picker, flag=wx.EXPAND | wx.RIGHT, border=10)
        date_sizer.Add(end_date_label, flag=wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, border=5)
        date_sizer.Add(self.end_date_picker, flag=wx.EXPAND | wx.RIGHT, border=10)
        date_sizer.Add(filter_button)
        date_sizer.Add(export_button, flag=wx.LEFT, border=10)

        # Create ListCtrl for historial
        historial_list = wx.ListCtrl(historial_dialog, style=wx.LC_REPORT | wx.LC_SORT_ASCENDING)
        historial_list.InsertColumn(0, "ID", width=50)
        historial_list.InsertColumn(1, "Tipo", width=100)
        historial_list.InsertColumn(2, "Monto", width=100)
        historial_list.InsertColumn(3, "Fecha", width=120)
        historial_list.InsertColumn(4, "Descripción", width=200)
        historial_list.InsertColumn(5, "Destino Viaje", width=150)

        def on_filter(event):
            start_date = self.start_date_picker.GetValue().FormatISODate()
            end_date = self.end_date_picker.GetValue().FormatISODate()

            query = """
            SELECT Historial.Id, Historial.tipo, Historial.monto, Historial.fecha, Historial.descripcion, viajes.Destino
            FROM Historial
            JOIN viajes ON Historial.viaje_id = viajes.Id
            WHERE Historial.fecha BETWEEN %s AND %s
            """
            try:
                self.cursor.execute(query, (start_date, end_date))
                historial_list.DeleteAllItems()
                for row in self.cursor.fetchall():
                    historial_list.Append(row)
            except Error as err:
                wx.MessageBox(f'Error al cargar datos del historial: {err}', 'Error', wx.OK | wx.ICON_ERROR)

        def on_export(event):
            start_date = self.start_date_picker.GetValue().FormatISODate()
            end_date = self.end_date_picker.GetValue().FormatISODate()

            query = """
            SELECT Historial.Id, Historial.tipo, Historial.monto, Historial.fecha, Historial.descripcion, viajes.Destino
            FROM Historial
            JOIN viajes ON Historial.viaje_id = viajes.Id
            WHERE Historial.fecha BETWEEN %s AND %s
            """
            try:
                self.cursor.execute(query, (start_date, end_date))
                rows = self.cursor.fetchall()
                df = pd.DataFrame(rows, columns=["ID", "Tipo", "Monto", "Fecha", "Descripción", "Destino Viaje"])
                file_name = f"Historial_{start_date}_to_{end_date}.xlsx"
                df.to_excel(file_name, index=False)
                wx.MessageBox(f'Historial exportado a Excel: {file_name}', 'Info', wx.OK | wx.ICON_INFORMATION)
            except Error as err:
                wx.MessageBox(f'Error al exportar datos a Excel: {err}', 'Error', wx.OK | wx.ICON_ERROR)

        filter_button.Bind(wx.EVT_BUTTON, on_filter)
        export_button.Bind(wx.EVT_BUTTON, on_export)

        sizer.Add(date_sizer, flag=wx.EXPAND | wx.ALL, border=10)
        sizer.Add(historial_list, proportion=1, flag=wx.EXPAND | wx.ALL, border=10)
        historial_dialog.SetSizer(sizer)
        historial_dialog.ShowModal()
        historial_dialog.Destroy()

    def on_item_selected(self, event):
        selected_index = self.caja_list.GetFirstSelected()
        if selected_index != -1:
            id_caja = self.caja_list.GetItemText(selected_index, 0)
            query = "SELECT tipo, monto, fecha, descripcion, viaje_id FROM Caja WHERE Id = %s"
            try:
                self.cursor.execute(query, (id_caja,))
                result = self.cursor.fetchone()
                if result:
                    self.tipo_combo.SetValue(result[0])
                    self.monto_text.SetValue(str(result[1]))
                    self.fecha_picker.SetValue(wx.DateTimeFromISODate(result[2]))
                    self.descripcion_text.SetValue(result[3])
                    viaje_index = self.viaje_combo.FindClientData(result[4])
                    self.viaje_combo.SetSelection(viaje_index)
            except Error as err:
                wx.MessageBox(f'Error al seleccionar datos: {err}', 'Error', wx.OK | wx.ICON_ERROR)

if __name__ == '__main__':
    app = wx.App()
    frame = FormularioCaja(None)
    frame.Show()
    app.MainLoop()
