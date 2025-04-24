import webbrowser
import urllib.parse
from module.ReproductorSonido import ReproductorSonido
import wx
import re
from module.GestionSocio import GestionSocio
from module.GestionReclamo import GestionReclamo
gestion_socio= GestionSocio()
gestion_reclamo= GestionReclamo()

class AgregarReclamoDialog(wx.Dialog):
    def __init__(self, parent, id=None, title="Nuevo Reclamo"):
        super().__init__(parent, id=wx.ID_ANY, title=title)

        self.id = id
        self.SetTitle(title)

        vbox = wx.BoxSizer(wx.VERTICAL)
        panel = wx.Panel(self)
        grid = wx.GridBagSizer(5, 5)

        # servicio de Reclamo (combo box)
        grid.Add(wx.StaticText(panel, label="servicio de Reclamo:"), pos=(0, 0), flag=wx.ALL, border=5)
        self.combo_servicio = wx.ComboBox(panel, choices=["Energía", "Agua", "Internet", "Cable","Sociales","Telefonía"], style=wx.CB_READONLY)
        grid.Add(self.combo_servicio, pos=(0, 1), flag=wx.EXPAND | wx.ALL, border=5)

        # Detalle (multilínea)
        grid.Add(wx.StaticText(panel, label="Detalle:"), pos=(1, 0), flag=wx.ALL, border=5)
        self.txt_detalle = wx.TextCtrl(panel, style=wx.TE_MULTILINE)
        grid.Add(self.txt_detalle, pos=(1, 1), flag=wx.EXPAND | wx.ALL, border=5)

        # socio
        # Etiqueta de socio
        grid.Add(wx.StaticText(panel, label="Socio:"), pos=(2, 0), flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL, border=5)

    # Campo de búsqueda
        self.txt_socio = wx.TextCtrl(panel)
        grid.Add(self.txt_socio, pos=(2, 1), flag=wx.EXPAND | wx.ALL, border=5)

        # Botón Filtrar
        self.btn_filtrar_socio = wx.Button(panel, label="Filtrar")
        grid.Add(self.btn_filtrar_socio, pos=(2, 2), flag=wx.ALL, border=5)

    # Lista de resultados
        self.list_socios = wx.ListBox(panel, style=wx.LB_SINGLE)
        grid.Add(self.list_socios, pos=(3, 1), span=(1, 2), flag=wx.EXPAND | wx.ALL, border=5)
        self.list_socios.Hide()  # Oculta al inicio

    # Botón Seleccionar Socio
        self.btn_seleccionar_socio = wx.Button(panel, label="Seleccionar &Socio")
        grid.Add(self.btn_seleccionar_socio, pos=(4, 2), flag=wx.ALIGN_RIGHT | wx.ALL, border=5)

        # Diccionario de socios
        self.socios_dict = self.cargar_socios()

    # Eventos
        self.btn_filtrar_socio.Bind(wx.EVT_BUTTON, self.filtrar_socios)
        self.btn_seleccionar_socio.Bind(wx.EVT_BUTTON, self.seleccionar_socio)
        self.txt_socio.Bind(wx.EVT_KEY_DOWN, self.on_key_socio)
        self.list_socios.Bind(wx.EVT_KEY_DOWN, self.on_key_lista_socio)

        #self.list_socios.Bind(wx.EVT_LISTBOX, self.seleccionar_socio)
        #self.list_socios.Bind(wx.EVT_CHAR_HOOK, self.on_char_hook)

        grid.AddGrowableCol(1)

        # Control para mostrar los datos del socio
        grid.Add(wx.StaticText(panel, label="Datos del Socio:"), pos=(4, 0), flag=wx.ALL, border=5)
        self.datos_socios_txt = wx.TextCtrl(panel, style=wx.TE_MULTILINE | wx.TE_READONLY)
        grid.Add(self.datos_socios_txt, pos=(4, 1), flag=wx.EXPAND | wx.ALL, border=5)

        #estado
        grid.Add(wx.StaticText(panel, label="Estado:"), pos=(5, 0), flag=wx.ALL, border=5)
        self.combo_estado = wx.ComboBox(panel, choices=["Pendiente", "Realizado", "En Proceso", "Cancelado", "Finalizado"], style=wx.CB_READONLY)
        self.combo_estado.SetSelection(0)
        grid.Add(self.combo_estado, pos=(5, 1), flag=wx.EXPAND | wx.ALL, border=5)

        # Botones
        btn_ok = wx.Button(panel, label="%&Guardar")
        btn_cancel = wx.Button(panel, wx.ID_CANCEL, "Cancelar")
        btn_ok.Bind(wx.EVT_BUTTON, self.guardar_reclamo)
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox.Add(btn_ok, flag=wx.RIGHT, border=10)
        hbox.Add(btn_cancel)

        vbox.Add(grid, proportion=1, flag=wx.ALL | wx.EXPAND, border=10)
        vbox.Add(hbox, flag=wx.ALIGN_CENTER | wx.ALL, border=10)
        panel.SetSizer(vbox)
        #self.Bind(wx.EVT_CHAR_HOOK, self.on_key_down)
        self.Centre()


    #cargar los socios
    def cargar_socios(self):
        
        try:
            self.socios_dict = gestion_socio.obtener_todos()
            self.list_socios.Clear()
            for id_socio, datos in self.socios_dict.items():
                self.list_socios.Append(f"{datos['nombre']} ({datos['domicilio']} - {datos['telefono']})")
        except Exception as e:
            print(f"Error al cargar socios: {e}")


    def filtrar_socios(self, event):
        filtro = self.txt_socio.GetValue()
        print(f"Filtrando socios con: '{filtro}'")
        self.list_socios.Clear()
        try:
            socios_filtrados = gestion_socio.obtener_socios_filtrados(filtro)
            self.socios_dict = socios_filtrados  # ✅ IMPORTANTE: actualizar el dict interno
            for id_socio, datos in socios_filtrados.items():
                self.list_socios.Append(f"{datos['nombre']} ({datos['domicilio']} - {datos['telefono']})")
            if self.list_socios.GetCount() > 0:
                self.list_socios.SetFocus()
        except Exception as e:
            print(f"Error al filtrar socios: {e}")


    def seleccionar_socio(self, event=None):
        seleccion = self.list_socios.GetStringSelection()
        if seleccion:
            nombre_socio = seleccion.split(' (')[0]
            self.txt_socio.SetValue(seleccion.split(' (')[0])
            self.txt_socio.SetFocus()
            print("Intentando setear el foco en txt_socio")
            self.anunciar_seleccion_socio()
            self.mostrar_datos_socio(nombre_socio)  # Mostramos info

    def on_key_socio(self, event):
        keycode = event.GetKeyCode()
        print(f"Tecla presionada en txt_socio: {keycode}")

        if keycode == wx.WXK_RETURN:
            print("Enter presionado en txt_socio")
            self.seleccionar_socio()
            self.txt_socio.SetFocus()
        elif keycode in [wx.WXK_UP, wx.WXK_DOWN]:
            event.Skip()
        else:
            event.Skip()

    def on_key_lista_socio(self, event):
        keycode = event.GetKeyCode()
        print(f"Tecla presionada en lista socios: {keycode}")
        if keycode == wx.WXK_RETURN or keycode == 307:
            print("Enter presionado en lista socios")
            self.seleccionar_socio()
            self.datos_socios_txt.SetFocus()
        else:
            event.Skip()

    def anunciar_seleccion_socio(self):
        """Fuerza la lectura de la selección de socio en lectores de pantalla."""
        seleccion = self.list_socios.GetStringSelection()
        if seleccion:
            wx.CallAfter(self.list_socios.SetLabel, seleccion)

    
    #guardar un reclamo
    def guardar_reclamo(self, event):
        servicio = self.combo_servicio.GetValue().strip()
        detalle = self.txt_detalle.GetValue().strip()
        socio_nombre = self.txt_socio.GetValue().strip()
        estado = self.combo_estado.GetValue().strip()

        socio_id = self.validar_reclamo(servicio, detalle, socio_nombre, estado)
        if socio_id is False:  # Cambio: Verificar si socio_id es False
            return

        try:
            gestion_reclamo.registrar_reclamo(None, servicio, detalle, socio_id, estado)
            print(f"Reclamo guardado: servicio={servicio}, socio={socio_id}, Detalle={detalle}, Estado={estado}")
            #self.mostrar_mensaje("Reclamo guardado con éxito.", wx.ICON_INFORMATION)
            datos=gestion_socio.buscar_socio(socio_id) 
            ReproductorSonido.reproducir("ok.wav")    
            # self.actualizar_lista_socios()  # Cambio: Comentado para evitar errores

            # Enviar reclamo por WhatsApp
            self.enviar_reclamo_whatsapp(servicio, detalle, datos)  # Cambio: Comentado para evitar errores

            # Limpiar los campos después de guardar
            self.combo_servicio.SetSelection(0)
            self.txt_detalle.SetValue("")
            self.txt_socio.SetValue("")
            self.combo_estado.SetSelection(0)
            self.Close()
        except Exception as e:
            self.mostrar_mensaje(f"Error al guardar el reclamo: {e}", wx.ICON_ERROR)

    def validar_reclamo(self, servicio, detalle, socio_nombre, estado):
        if not servicio or not detalle or not socio_nombre or not estado:
            self.mostrar_mensaje("Error: Todos los campos son obligatorios.", wx.ICON_ERROR)
            return False  # Cambio: Devolver False en lugar de un valor no booleano

        # Buscar el ID del socio por su nombre
        socio_id = None
        for id_socio, datos_socio in self.socios_dict.items():
            if datos_socio['nombre'] == socio_nombre:
                socio_id = id_socio
                break

        if socio_id is None:
            self.mostrar_mensaje(f"Error: No se encontró el socio '{socio_nombre}'.", wx.ICON_ERROR)
            return False  # Cambio: Devolver False en lugar de un valor no booleano

        return socio_id
    
    
    def mostrar_mensaje(self, mensaje, tipo=wx.ICON_ERROR):
        wx.MessageBox(mensaje, "Información", style=tipo)


    def mostrar_datos_socio(self, nombre_socio):
        try:
            # Obtener los datos del socio desde la base de datos
            socio = gestion_socio.obtener_socio_por_nombre(nombre_socio)

            if socio:
                # Formatear los datos del socio como una cadena
                datos_str = "\n".join([f"{clave}: {valor}" for clave, valor in socio.items()])
                self.datos_socios_txt.SetValue(datos_str)
            else:
                self.datos_socios_txt.SetValue("Socio no encontrado.")
        except Exception as e:
            self.datos_socios_txt.SetValue(f"Error al obtener datos del socio: {e}")

    def enviar_reclamo_whatsapp(self, servicio, detalle, datos):
        nombre = datos.get("nombre", "Nombre no disponible")
        domicilio = datos.get("domicilio", "Domicilio no disponible")
        telefono = datos.get("telefono", "Teléfono no disponible")

        mensaje = f"Reclamo de {servicio}:\nDetalle: {detalle}\nNombre: {nombre}\nDomicilio: {domicilio}\nTeléfono: {telefono}"
        mensaje_codificado = urllib.parse.quote(mensaje)
        #numero_telefono = "5493534294632"  # Reemplaza con el número
        numero_telefono =""
        

        url = f"https://wa.me/{numero_telefono}?text={mensaje_codificado}"
        webbrowser.open_new_tab(url)

