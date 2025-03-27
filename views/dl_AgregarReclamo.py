import webbrowser
import urllib.parse

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
        grid.Add(wx.StaticText(panel, label="socio:"), pos=(2, 0), flag=wx.ALL, border=5)
        self.txt_socio = wx.TextCtrl(panel)
        grid.Add(self.txt_socio, pos=(2, 1), flag=wx.EXPAND | wx.ALL, border=5)
        # Lista desplegable para mostrar los socios encontrados
        self.list_socios = wx.ListBox(panel, style=wx.LB_SINGLE)
        grid.Add(self.list_socios, pos=(3, 1), flag=wx.EXPAND | wx.ALL, border=5)
        self.list_socios.Hide()  # Ocultar la lista al inicio

        # Cargar socios
        self.socios_dict = self.cargar_socios()

        # Bindear el evento de cambio de texto
        self.txt_socio.Bind(wx.EVT_TEXT, self.buscar_socio)
        self.list_socios.Bind(wx.EVT_LISTBOX, self.seleccionar_socio)
        self.list_socios.Bind(wx.EVT_CHAR_HOOK, self.on_char_hook) # Captura la tecla Enter
        # Control para mostrar los datos del socio
        grid.Add(wx.StaticText(panel, label="Datos del Socio:"), pos=(4, 0), flag=wx.ALL, border=5)
        self.datos_socios_txt = wx.TextCtrl(panel, style=wx.TE_MULTILINE | wx.TE_READONLY)
        grid.Add(self.datos_socios_txt, pos=(4, 1), flag=wx.EXPAND | wx.ALL, border=5)

        # Estado (combo box) - MOVED TO BEFORE BUTTONS
        grid.Add(wx.StaticText(panel, label="Estado:"), pos=(5, 0), flag=wx.ALL, border=5)
        self.combo_estado = wx.ComboBox(panel, choices=["Pendiente", "Realizado", "En Proceso", "Cancelado", "Finalizado"], style=wx.CB_READONLY)
        grid.Add(self.combo_estado, pos=(5, 1), flag=wx.EXPAND | wx.ALL, border=5)

        # Botones
        btn_ok = wx.Button(panel, label="Guardar")
        btn_cancel = wx.Button(panel, wx.ID_CANCEL, "Cancelar")
        btn_ok.Bind(wx.EVT_BUTTON, self.guardar_reclamo)
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox.Add(btn_ok, flag=wx.RIGHT, border=10)
        hbox.Add(btn_cancel)

        vbox.Add(grid, proportion=1, flag=wx.ALL | wx.EXPAND, border=10)
        vbox.Add(hbox, flag=wx.ALIGN_CENTER | wx.ALL, border=10)
        panel.SetSizer(vbox)
        self.Bind(wx.EVT_CHAR_HOOK, self.on_key_down)
        self.Centre()


    #cargar los socios
    def cargar_socios(self):
        self.list_socios.Clear()
        socios = gestion_socio.obtener_todos()
        socios_dict = {}

        if socios:
            for id_socio, socio in socios.items():  # Cambiado para iterar sobre items()
                item_text = f"Código: {id_socio} - {socio['nombre']} - Domicilio: {socio['domicilio']} - Teléfono: {socio['telefono']}"  # Usar id_socio directamente
                self.list_socios.Append(item_text)
                socios_dict[id_socio] = socio  # Usar id_socio como clave

        return socios_dict
    #buscar los socios
    def buscar_socio(self, event):
        """Busca socios en la base de datos por nombre."""
        socio_ingresado = self.txt_socio.GetValue().lower()
        self.list_socios.Clear()

        if socio_ingresado:
            socios_encontrados =         gestion_socio.buscar_socio_por_nombre_parcial(socio_ingresado)
            print("socios encontrados:")
            print(socios_encontrados)

            if socios_encontrados:
                items = []
                for socio in socios_encontrados:
                    self.list_socios.Append(socio['nombre'], clientData=(socio['nombre'], socio['id']))
                self.list_socios.Show()
            else:
                self.list_socios.Hide()
        else:
            self.list_socios.Hide()        #seleccionar los socios 
    def seleccionar_socio(self, event):
        """Selecciona un socio de la lista."""
        seleccion_index = self.list_socios.GetSelection()

        if seleccion_index != wx.NOT_FOUND: # Verifica si se ha seleccionado un elemento
            nombre_socio, socio_id = self.list_socios.GetClientData(seleccion_index)
            self.txt_socio.SetValue(nombre_socio)
            self.list_socios.Hide()
            self.mostrar_datos_socio(nombre_socio)
            print(f"Socio ID seleccionado: {socio_id}")
        else:
            print("Error: No se ha seleccionado ningún socio.")

    def mostrar_datos_socio(self, nombre_socio):
        """Muestra los datos del socio (ejemplo)."""
        print(f"Datos del socio: {nombre_socio}")

    def on_char_hook(self, event):
        """Captura la tecla Enter."""
        if event.GetKeyCode() == wx.WXK_RETURN:
            seleccion = self.list_socios.GetStringSelection()
            if seleccion: # Verifica que haya una selección
                self.seleccionar_socio(event)
            else:
                print("Error: No hay ningún socio seleccionado.")
        else:
            event.Skip()

#teclas rapidas
    def on_key_down(self, event):
        key_code = event.GetKeyCode()
        control_presionado = event.ControlDown()

        if control_presionado and key_code == ord("G"):
            self.guardar_reclamo(None)
        elif control_presionado and key_code == ord("C"):
            self.Close()
        event.Skip()

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
            self.mostrar_mensaje("Reclamo guardado con éxito.", wx.ICON_INFORMATION)
            datos=gestion_socio.buscar_socio(socio_id) 
            
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

