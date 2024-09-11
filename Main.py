import wx

class Principal(wx.Frame):
    def __init__(self, *args, **kw):
        super(Principal, self).__init__(*args, **kw)

        panel = wx.Panel(self)
        panel.SetBackgroundColour(wx.Colour(50, 50, 50))  # Fondo gris oscuro

        sizer = wx.BoxSizer(wx.VERTICAL)

        # Load images and create buttons with icons and text
        self.viajes_icon = wx.Bitmap("Icons/Viajes.png", wx.BITMAP_TYPE_PNG)
        self.clientes_icon = wx.Bitmap("Icons/Clientes.png", wx.BITMAP_TYPE_PNG)
        self.instituciones_icon = wx.Bitmap("Icons/Instituciones.png", wx.BITMAP_TYPE_PNG)
        self.caja_icon = wx.Bitmap("Icons/Caja.png", wx.BITMAP_TYPE_PNG)
        self.empleados_icon = wx.Bitmap("Icons/Empleados.png", wx.BITMAP_TYPE_PNG)

        # Create buttons with icon and text
        self.viajes_button = wx.Button(panel, label="Viajes", style=wx.BU_LEFT)
        self.clientes_button = wx.Button(panel, label="Clientes", style=wx.BU_LEFT)
        self.instituciones_button = wx.Button(panel, label="Instituciones", style=wx.BU_LEFT)
        self.caja_button = wx.Button(panel, label="Caja", style=wx.BU_LEFT)
        self.empleados_button = wx.Button(panel, label="Empleados", style=wx.BU_LEFT)

        # Set icons for buttons
        self.viajes_button.SetBitmap(self.viajes_icon, wx.LEFT)
        self.clientes_button.SetBitmap(self.clientes_icon, wx.LEFT)
        self.instituciones_button.SetBitmap(self.instituciones_icon, wx.LEFT)
        self.caja_button.SetBitmap(self.caja_icon, wx.LEFT)
        self.empleados_button.SetBitmap(self.empleados_icon, wx.LEFT)

        # Set button sizes
        self.viajes_button.SetSize((120, 60))
        self.clientes_button.SetSize((120, 60))
        self.instituciones_button.SetSize((120, 60))
        self.caja_button.SetSize((120, 60))
        self.empleados_button.SetSize((120, 60))

        # Bind buttons to events
        self.viajes_button.Bind(wx.EVT_BUTTON, self.on_viajes)
        self.clientes_button.Bind(wx.EVT_BUTTON, self.on_clientes)
        self.instituciones_button.Bind(wx.EVT_BUTTON, self.on_instituciones)
        self.caja_button.Bind(wx.EVT_BUTTON, self.on_caja)
        self.empleados_button.Bind(wx.EVT_BUTTON, self.on_empleados)

        # Create sizer for buttons
        top_sizer = wx.BoxSizer(wx.HORIZONTAL)
        top_sizer.Add(self.viajes_button, proportion=1, flag=wx.EXPAND | wx.ALL, border=10)
        top_sizer.Add(self.clientes_button, proportion=1, flag=wx.EXPAND | wx.ALL, border=10)
        top_sizer.Add(self.instituciones_button, proportion=1, flag=wx.EXPAND | wx.ALL, border=10)

        bottom_sizer = wx.BoxSizer(wx.HORIZONTAL)
        bottom_sizer.Add(self.caja_button, proportion=1, flag=wx.EXPAND | wx.ALL, border=10)
        bottom_sizer.Add(self.empleados_button, proportion=1, flag=wx.EXPAND | wx.ALL, border=10)

        # Add sizers to the main sizer
        sizer.Add(top_sizer, proportion=1, flag=wx.EXPAND)
        sizer.Add(bottom_sizer, proportion=1, flag=wx.EXPAND)

        panel.SetSizer(sizer)
        self.SetSize((800, 600))  # Ajusta el tamaño de la ventana principal
        self.SetTitle("Principal")
        self.Center()

    def on_viajes(self, event):
        from Viajes import ViajesApp
        frame = ViajesApp(None)
        frame.Show()

    def on_clientes(self, event):
       from Clientes import FormularioClientes
       frame = FormularioClientes(None)
       frame.Show()

    def on_instituciones(self, event):
       from Institucionales import FormularioInstitucionales
       frame = FormularioInstitucionales(None, "Formulario de Instituciones")
       frame.Show()

    def on_caja(self, event):
        from Caja import FormularioCaja  # Importa la clase FormularioCaja desde caja.py
        frame = FormularioCaja(None)  # Crea una instancia de FormularioCaja
        frame.Show()

    def on_empleados(self, event):
       from CRUDCoordinadores import FormularioCoordinadores
       frame = FormularioCoordinadores(None)
       frame.Show()

if __name__ == "__main__":
    app = wx.App(False)
    frame = Principal(None)
    frame.Show()
    app.MainLoop()
