import json
import urllib.parse
import webbrowser


import datetime
import os
import re
import sys
import wx
import wx.lib.mixins.listctrl as listmix
from module.ReproductorSonido import ReproductorSonido
from views.dl_AgregarReclamo import AgregarReclamoDialog
from views.fr_ListSocio import ListSocio,AgregarSocioDialog
from module.GestionReclamo import GestionReclamo
from module.GestionSocio import GestionSocio
gestion_reclamo = GestionReclamo()
gestion_socio = GestionSocio()
class ListReclamo(wx.Frame, listmix.ListCtrlAutoWidthMixin):
    def __init__(self, parent, id=None, title="Gestión de Reclamos", *args, **kwds):
        super().__init__(parent, id=wx.ID_ANY, title=title, *args, **kwds)

        panel = wx.Panel(self)
        self.nombre_archivo_productos = 'data/productos.json'
        # Botón desplegable
        self.btn_menu = wx.Button(panel, label="&Menú", pos=(10, 260))
        self.btn_menu.Bind(wx.EVT_BUTTON, self.on_mostrar_menu)
        # Lista de reclamos
        self.list_ctrl = wx.ListCtrl(panel, style=wx.LC_REPORT | wx.BORDER_SUNKEN, pos=(10, 10), size=(600, 250))
        self.list_ctrl.InsertColumn(0, 'ID', width=50)
        self.list_ctrl.InsertColumn(1, 'Fecha', width=100)
        self.list_ctrl.InsertColumn(2, 'Socio', width=150)
        self.list_ctrl.InsertColumn(3, 'Servicio', width=150) #Agregamos la columna servicio.
        self.list_ctrl.InsertColumn(4, 'Detalle', width=200)
        self.list_ctrl.InsertColumn(5, 'Estado', width=100)
        self.cargar_reclamos()
        self.list_ctrl.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.mostrar_detalle_reclamo)

        # Botones
        btn_nuevo = wx.Button(panel, label="Nuevo Reclamo", pos=(50, 300))
        btn_nuevo.Bind(wx.EVT_BUTTON, self.abrir_dialogo_nuevo)
        btn_cerrar = wx.Button(panel, label="Cerrar", pos=(300, 300))
        btn_cerrar.Bind(wx.EVT_BUTTON, self.cerrar_ventana)
        btn_actualizar = wx.Button(panel, label="Actualizar", pos=(175, 300))
        btn_actualizar.Bind(wx.EVT_BUTTON, self.actualizar_lista)
        # Vinculación de la tecla F2
        self.Bind(wx.EVT_MENU, self.on_add_socios, id=wx.ID_NEW)
        accel_tbl = wx.AcceleratorTable([(wx.ACCEL_NORMAL, wx.WXK_F2, wx.ID_NEW)])
        self.SetAcceleratorTable(accel_tbl)

        self.Show()

    def actualizar_lista(self, event):
        self.cargar_reclamos()
        print("Lista actualizada en la interfaz")
        sys.stdout.flush()
        ReproductorSonido.reproducir("refresh.wav")

    def cargar_reclamos(self):
        self.list_ctrl.DeleteAllItems()
        reclamos = gestion_reclamo.obtener_todos()

        if reclamos:
            for index, datos in enumerate(reclamos.values()):
                nombre_socio = gestion_reclamo.obtener_nombre_socio(datos["socio"])
                if nombre_socio is None:
                    nombre_socio = "Socio no encontrado"
                fecha_str = datos.get("fecha", "")
                fecha_formateada=self.obtener_fecha(fecha_str)
                self.list_ctrl.InsertItem(index, str(datos["id"]))
                self.list_ctrl.SetItem(index, 1, fecha_formateada)
                self.list_ctrl.SetItem(index, 2, str(nombre_socio))
                self.list_ctrl.SetItem(index, 3, datos["servicio"])
                self.list_ctrl.SetItem(index, 4, datos["detalle"])
                self.list_ctrl.SetItem(index, 5, datos["estado"])    

    def obtener_fecha  (self,fecha_str):
        fecha_obj = datetime.datetime.strptime(fecha_str, "%Y-%m-%d").date()
        fecha_formateada = fecha_obj.strftime("%d-%m-%Y")
        return fecha_formateada

                
    def mostrar_detalle_reclamo(self, event):
        index = event.GetIndex()
        id_reclamo = self.list_ctrl.GetItemText(index)

        reclamos = gestion_reclamo.obtener_todos()
        if id_reclamo in reclamos:
            datos = reclamos[id_reclamo]
            dialogo = DetalleReclamoDialog(self, id_reclamo, datos)
            dialogo.ShowModal()
            dialogo.Destroy()
            self.cargar_reclamos()

    def abrir_dialogo_nuevo(self, event):
        ReproductorSonido.reproducir("screenCurtainOn.wav")
        dialogo = AgregarReclamoDialog(self)
        if dialogo.ShowModal() == wx.ID_OK:
            self.cargar_reclamos()
        dialogo.Destroy()

    def cerrar_ventana(self, event):
        ReproductorSonido.reproducir("screenCurtainOff.wav")
        self.Close()

    def on_mostrar_menu(self, event):
        menu = wx.Menu()
        ver_socio_item = menu.Append(wx.ID_ANY, "Ver Socios")
        self.Bind(wx.EVT_MENU, self.on_ver_socios, ver_socio_item)
        add_socio_item = menu.Append(wx.ID_ANY, "Agregar Socio...F2")
        self.Bind(wx.EVT_MENU, self.on_add_socios, add_socio_item)
        exit_socio_item = menu.Append(wx.ID_ANY, "Salir")
        self.Bind(wx.EVT_MENU, self.cerrar_ventana, exit_socio_item)
        self.PopupMenu(menu, self.btn_menu.GetPosition())
        menu.Destroy()

    def on_ver_socios(self, event):
        frame_socios = ListSocio(self) # Crea una instancia de fr_listSocio
        frame_socios.Show()
        
    def on_add_socios(self, event):
        add_socios = AgregarSocioDialog(self) # Crea una instancia de fr_listSocio
        if add_socios.ShowModal() == wx.ID_OK:
            self.actualizar_lista_socios()
        add_socios.Destroy()
        


class DetalleReclamoDialog(wx.Dialog):
    def __init__(self, parent, id_reclamo, datos):
        super().__init__(parent, title="Detalle del Reclamo", size=(300, 250))
        self.id_reclamo = id_reclamo
        self.datos=datos

        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        vbox.Add(wx.StaticText(panel, label=f"ID: {id_reclamo}"), flag=wx.LEFT | wx.TOP, border=10)
        vbox.Add(wx.StaticText(panel, label=f"Fecha: {datos['fecha']}"), flag=wx.LEFT | wx.TOP, border=10)
        vbox.Add(wx.StaticText(panel, label=f"socio: {datos['socio']}"), flag=wx.LEFT | wx.TOP, border=10)
        
        vbox.Add(wx.StaticText(panel, label=f"Detalle: {datos['detalle']}"), flag=wx.LEFT | wx.TOP, border=10)
        vbox.Add(wx.StaticText(panel, label=f"Estado: {datos['estado']}"), flag=wx.LEFT | wx.TOP, border=10)

        btn_editar = wx.Button(panel, label="Editar")
        btn_editar.Bind(wx.EVT_BUTTON, self.editar_reclamo)
        btn_delete = wx.Button(panel, label="Eliminar")
        btn_delete.Bind(wx.EVT_BUTTON, self.eliminar_reclamo)
        btn_whatsapp= wx.Button(panel, label="Enviar por whatsapp")
        btn_whatsapp.Bind(wx.EVT_BUTTON, self.enviar_reclamo_whatsapp)
        btn_cerrar = wx.Button(panel, wx.ID_CANCEL, "Cerrar")

        hbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox.Add(btn_editar, flag=wx.RIGHT, border=10)
        hbox.Add(btn_delete, flag=wx.RIGHT, border=10)
        hbox.Add(btn_whatsapp, flag=wx.RIGHT, border=10)
        hbox.Add(btn_cerrar)

        vbox.Add(hbox, flag=wx.ALIGN_CENTER | wx.TOP | wx.BOTTOM, border=10)
        panel.SetSizer(vbox)




    def editar_reclamo(self, event):
        dialogo = EditarReclamoDialog(self, self.id_reclamo)
        if dialogo.ShowModal() == wx.ID_OK:
            self.EndModal(wx.ID_OK)
        dialogo.Destroy()

    def eliminar_reclamo(self, event):
        dialogo = EliminarReclamoDialog(self, self.id_reclamo, gestion_reclamo)
        if dialogo.ShowModal() == wx.ID_OK:
            self.EndModal(wx.ID_OK)
        dialogo.Destroy()


    def enviar_reclamo_whatsapp(self, event):
        id_socio=self.datos.get("socio", "servicio no disponible")
        datos_socios=gestion_socio.buscar_socio(id_socio)
        print(datos_socios)
        servicio = self.datos.get("servicio", "servicio no disponible")
        detalle = self.datos.get("detalle", "detalle no disponible")
        nombre = datos_socios.get("nombre", "Nombre no disponible")
        domicilio = datos_socios.get("domicilio", "Domicilio no disponible")
        telefono = datos_socios.get("telefono", "Teléfono no disponible")

        mensaje = f"Reclamo de {servicio}:\nDetalle: {detalle}\nNombre: {nombre}\nDomicilio: {domicilio}\nTeléfono: {telefono}"
        mensaje_codificado = urllib.parse.quote(mensaje)
        #numero_telefono = "5493534294632"  # Reemplaza con el número
        numero_telefono =""
        

        url = f"https://wa.me/{numero_telefono}?text={mensaje_codificado}"
        webbrowser.open_new_tab(url)



class EditarReclamoDialog(wx.Dialog):
    def __init__(self, parent, id_reclamo):
        super().__init__(parent, title="Editar Reclamo", size=(300, 250))
        self.id_reclamo = id_reclamo

        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        reclamos = gestion_reclamo.obtener_todos()
        datos = reclamos.get(id_reclamo, {})

        vbox.Add(wx.StaticText(panel, label="Fecha:"), flag=wx.LEFT | wx.TOP, border=10)
        self.txt_fecha = wx.TextCtrl(panel, value=datos.get("fecha", ""))
        vbox.Add(self.txt_fecha, flag=wx.EXPAND | wx.LEFT | wx.RIGHT, border=10)

        vbox.Add(wx.StaticText(panel, label="socio:"), flag=wx.LEFT | wx.TOP, border=10)
        socio_id = datos.get("socio") #Obtiene el id del socio guardado en el reclamo.
        socio=gestion_socio.buscar_socio(socio_id)
        nombre_socio = socio.get("nombre", "Socio no encontrado") #Obtiene el nombre        
        self.txt_socio = wx.TextCtrl(panel, value=nombre_socio)
        self.socio_id = datos.get("socio") #Obtiene el id del socio guardado en el reclamo.
        vbox.Add(self.txt_socio, flag=wx.EXPAND | wx.LEFT | wx.RIGHT, border=10)

        vbox.Add(wx.StaticText(panel, label="Detalle:"), flag=wx.LEFT | wx.TOP, border=10)
        self.txt_detalle = wx.TextCtrl(panel, value=datos.get("detalle", ""), style=wx.TE_MULTILINE)
        vbox.Add(self.txt_detalle, flag=wx.EXPAND | wx.LEFT | wx.RIGHT, border=10)

        vbox.Add(wx.StaticText(panel, label="Estado:"), flag=wx.LEFT | wx.TOP, border=10)
        self.combo_estado = wx.ComboBox(panel, choices=["Pendiente", "Realizado", "En Proceso", "Cancelado", "Finalizado"], style=wx.CB_READONLY)
        self.combo_estado.SetValue(datos.get("estado", ""))
        vbox.Add(self.combo_estado, flag=wx.EXPAND | wx.LEFT | wx.RIGHT, border=10)

        hbox = wx.BoxSizer(wx.HORIZONTAL)
        btn_ok = wx.Button(panel, wx.ID_OK, "Guardar")
        btn_cancel = wx.Button(panel, wx.ID_CANCEL, "Cancelar")
        hbox.Add(btn_ok, flag=wx.RIGHT, border=10)
        hbox.Add(btn_cancel)

        vbox.Add(hbox, flag=wx.ALIGN_CENTER | wx.TOP | wx.BOTTOM, border=10)
        panel.SetSizer(vbox)

        self.Bind(wx.EVT_BUTTON, self.guardar_cambios, btn_ok)

    def guardar_cambios(self, event):
        fecha = self.txt_fecha.GetValue().strip()
        socio = self.socio_id
        detalle = self.txt_detalle.GetValue().strip()
        estado = self.combo_estado.GetValue().strip()

        if not fecha or not socio or not detalle or not estado:
            wx.MessageBox("Todos los campos son obligatorios", "Error", wx.OK | wx.ICON_ERROR)
            return

        try:
            gestion_reclamo.editar_reclamo(self.id_reclamo, fecha, socio, detalle, estado)
            wx.MessageBox("Reclamo actualizado con éxito", "Éxito", wx.OK | wx.ICON_INFORMATION)
            self.EndModal(wx.ID_OK)
        except Exception as e:
            wx.MessageBox(str(e), "Error", wx.OK | wx.ICON_ERROR)

class EliminarReclamoDialog(wx.Dialog):
    def __init__(self, parent, id_reclamo, gestion_reclamo):
        super().__init__(parent, title="Eliminar Reclamo", size=(300, 150))
        self.id_reclamo = id_reclamo
        self.parent = parent
        self.gestion_reclamo = gestion_reclamo

        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        reclamos = self.gestion_reclamo.obtener_todos()
        reclamo = reclamos.get(str(id_reclamo))

        if reclamo:
            mensaje = f"¿Estás seguro de que deseas eliminar el reclamo con ID '{reclamo['id']}'?"
            vbox.Add(wx.StaticText(panel, label=mensaje), flag=wx.ALL, border=10)

            hbox = wx.BoxSizer(wx.HORIZONTAL)
            btn_ok = wx.Button(panel, wx.ID_OK, "Eliminar")
            btn_cancel = wx.Button(panel, wx.ID_CANCEL, "Cancelar")
            hbox.Add(btn_ok, flag=wx.RIGHT, border=10)
            hbox.Add(btn_cancel)

            vbox.Add(hbox, flag=wx.ALIGN_CENTER | wx.TOP | wx.BOTTOM, border=10)
            panel.SetSizer(vbox)

            self.Bind(wx.EVT_BUTTON, self.eliminar_reclamo, btn_ok)
        else:
            wx.MessageBox(f"No se encontró el reclamo con ID {id_reclamo}", "Error", wx.OK | wx.ICON_ERROR)
            self.EndModal(wx.ID_CANCEL)

    def eliminar_reclamo(self, event):
        try:
            self.gestion_reclamo.eliminar_reclamo(self.id_reclamo)
            wx.MessageBox("Reclamo eliminado con éxito", "Éxito", wx.OK | wx.ICON_INFORMATION)
            self.EndModal(wx.ID_OK)
            if hasattr(self.parent, "cargar_reclamos"):
                self.parent.cargar_reclamos()
        except Exception as e:
            wx.MessageBox(str(e), "Error", wx.OK | wx.ICON_ERROR)


