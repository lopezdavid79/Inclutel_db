import wx
import re
from module.GestionSocio import GestionSocio
gestion_socio= GestionSocio()
class AgregarSocioDialog(wx.Dialog):
    def __init__(self, parent, id=None, title="Nuevo socio"):
        super().__init__(parent, id=wx.ID_ANY, title=title)

        self.id = id
        self.SetTitle(title)

        vbox = wx.BoxSizer(wx.VERTICAL)
        panel = wx.Panel(self)
        grid = wx.GridBagSizer(5, 5)

        # Nombre
        grid.Add(wx.StaticText(panel, label="Nombre:"), pos=(0, 0), flag=wx.ALL, border=5)
        self.txt_nombre = wx.TextCtrl(panel)
        grid.Add(self.txt_nombre, pos=(0, 1), flag=wx.EXPAND | wx.ALL, border=5)

        # Domicilio
        grid.Add(wx.StaticText(panel, label="Domicilio:"), pos=(1, 0), flag=wx.ALL, border=5)
        self.txt_domicilio = wx.TextCtrl(panel)
        grid.Add(self.txt_domicilio, pos=(1, 1), flag=wx.EXPAND | wx.ALL, border=5)

        # Telefono
        grid.Add(wx.StaticText(panel, label="Telefono:"), pos=(2, 0), flag=wx.ALL, border=5)
        self.txt_telefono = wx.TextCtrl(panel)
        grid.Add(self.txt_telefono, pos=(2, 1), flag=wx.EXPAND | wx.ALL, border=5)

        # Numero de socio
        grid.Add(wx.StaticText(panel, label="Numero de socio:"), pos=(3, 0), flag=wx.ALL, border=5)
        self.txt_n_socio = wx.TextCtrl(panel)
        grid.Add(self.txt_n_socio, pos=(3, 1), flag=wx.EXPAND | wx.ALL, border=5)

      
        # Botones
        btn_ok = wx.Button(panel, label="Guardar")
        btn_cancel = wx.Button(panel, wx.ID_CANCEL, "Cancelar")
        btn_ok.Bind(wx.EVT_BUTTON, self.guardar_socio)
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox.Add(btn_ok, flag=wx.RIGHT, border=10)
        hbox.Add(btn_cancel)

        vbox.Add(grid, proportion=1, flag=wx.ALL | wx.EXPAND, border=10)
        vbox.Add(hbox, flag=wx.ALIGN_CENTER | wx.ALL, border=10)
        panel.SetSizer(vbox)
        self.Bind(wx.EVT_CHAR_HOOK, self.on_key_down)
        self.Centre()

    def on_key_down(self, event):
        key_code = event.GetKeyCode()
        control_presionado = event.ControlDown()

        if control_presionado and key_code == ord("G"):
            self.guardar_socio(None)
        elif control_presionado and key_code == ord("C"):
            self.Close()
        event.Skip()

    def guardar_socio(self, event):
        nombre = self.txt_nombre.GetValue().strip()
        domicilio = self.txt_domicilio.GetValue().strip()
        telefono = self.txt_telefono.GetValue().strip()
        n_socio = self.txt_n_socio.GetValue().strip()
        if not self.validar_socio(nombre,domicilio,telefono):
            return
        try:
            

            gestion_socio.registrar_socio( nombre, domicilio, telefono, n_socio)
            print(f"Socio guardado: Nombre={nombre}, Domicilio={domicilio}, Telefono={telefono}, Numero de socio={n_socio}")
            self.mostrar_mensaje("Socio guardado con éxito.", wx.ICON_INFORMATION)
# Llamar a la función de actualización en la ventana principal si está disponible
            self.txt_nombre.SetValue("")
            self.txt_domicilio.SetValue("")
            self.txt_telefono.SetValue("")
            self.txt_n_socio.SetValue("")                       
            self.Close()
        except Exception as e:
            self.mostrar_mensaje(f"Error al guardar el socio: {e}", wx.ICON_ERROR)


    def validar_socio(self, nombre, domicilio, telefono):
        """
        Valida los datos del socio.

        Args:
            nombre (str): Nombre del socio.
            domicilio (str): Domicilio del socio.
            telefono (str): Número de teléfono del socio.
            n_socio (str): Número de socio.

        Returns:
            bool: True si los datos son válidos, False en caso contrario.
        """

        # Validación de campos obligatorios
        if not nombre or not domicilio or not telefono :
            self.mostrar_mensaje("Error: Todos los campos son obligatorios.", wx.ICON_ERROR)
            return False

        # Validación de formato del número de teléfono
        patron_telefono = re.compile(r'^\d{10}$')
        if not patron_telefono.match(telefono):
            self.mostrar_mensaje("Error: El número de teléfono no es válido.", wx.ICON_ERROR)
            return False

        # Validación de formato del número de socio (ejemplo: solo dígitos)
        # Validación de caracteres alfanuméricos en nombre y domicilio (opcional)
        patron_alfanumerico = re.compile(r'^[\w\s]+$')
        if not patron_alfanumerico.match(nombre) or not patron_alfanumerico.match(domicilio):
            self.mostrar_mensaje("Error: El nombre y domicilio solo pueden contener caracteres alfanuméricos.", wx.ICON_ERROR)
            return False

        return True

    def mostrar_mensaje(self, mensaje, tipo=wx.ICON_ERROR):
        wx.MessageBox(mensaje, "Información", style=tipo)