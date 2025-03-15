
import re
import sys
import wx
import wx.lib.mixins.listctrl as listmix
from module.ReproductorSonido import ReproductorSonido
from module.GestionSocio import GestionSocio

gestion_socio= GestionSocio()

class ListSocio(wx.Frame, listmix.ListCtrlAutoWidthMixin):
    def __init__(self, parent, id=None, title="Gestión de Socios", *args, **kwds):
        super().__init__(parent, id=wx.ID_ANY, title=title, *args, **kwds)

        panel = wx.Panel(self)

        # Lista de socios
        self.list_ctrl = wx.ListCtrl(panel, style=wx.LC_REPORT | wx.BORDER_SUNKEN, pos=(10, 10), size=(600, 250))
        self.list_ctrl.InsertColumn(0, 'ID', width=50)
        self.list_ctrl.InsertColumn(1, 'Nombre', width=100)
        self.list_ctrl.InsertColumn(2, 'Domicilio', width=150)
        self.list_ctrl.InsertColumn(3, 'Teléfono', width=200)
        
        self.cargar_socios()
        self.list_ctrl.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.mostrar_detalle_socio)

        # Botones
        btn_nuevo = wx.Button(panel, label="Nuevo socio", pos=(50, 300))
        btn_nuevo.Bind(wx.EVT_BUTTON, self.abrir_dialogo_nuevo)
        btn_cerrar = wx.Button(panel, label="Cerrar", pos=(300, 300))
        btn_cerrar.Bind(wx.EVT_BUTTON, self.cerrar_ventana)
        btn_actualizar = wx.Button(panel, label="Actualizar", pos=(175, 300))
        btn_actualizar.Bind(wx.EVT_BUTTON, self.actualizar_lista)

        self.Show()

    def actualizar_lista(self, event):
        self.cargar_socios()
        print("Lista actualizada en la interfaz")
        sys.stdout.flush()
        ReproductorSonido.reproducir("refresh.wav")
    def cargar_socios(self):
        """Carga los socios desde SQLite en la interfaz."""
        self.list_ctrl.DeleteAllItems()
        socios = gestion_socio.obtener_todos()
        for id_socio, datos in socios.items():
            index = self.list_ctrl.InsertItem(self.list_ctrl.GetItemCount(), str(id_socio))
            self.list_ctrl.SetItem(index, 1, datos["nombre"])
            self.list_ctrl.SetItem(index, 2, datos["domicilio"])
            self.list_ctrl.SetItem(index, 3, str(datos["telefono"]))

    def mostrar_detalle_socio(self, event):
        """Muestra los detalles de un socio."""
        index = event.GetIndex()
        id_socio = self.list_ctrl.GetItemText(index)

        datos = gestion_socio.buscar_socio(id_socio)
        if datos:
            dialogo = DetalleSocioDialog(self, id_socio, datos)
            dialogo.ShowModal()
            dialogo.Destroy()
            self.cargar_socios()

    def abrir_dialogo_nuevo(self, event):
        """Abre el diálogo para agregar un nuevo socio."""
        ReproductorSonido.reproducir("screenCurtainOn.wav")
        dialogo = AgregarSocioDialog(self)
        if dialogo.ShowModal() == wx.ID_OK:
            self.cargar_socios()
        dialogo.Destroy()

    def cerrar_ventana(self, event):
        """Cierra la ventana actual."""
        ReproductorSonido.reproducir("screenCurtainOff.wav")
        self.Close() 
class DetalleSocioDialog(wx.Dialog):
    def __init__(self, parent, id_socio, datos):
        super().__init__(parent, title="Detalle del socio", size=(300, 250))
        self.id_socio = id_socio

        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        vbox.Add(wx.StaticText(panel, label=f"ID: {id_socio}"), flag=wx.LEFT | wx.TOP, border=10)
        vbox.Add(wx.StaticText(panel, label=f"Nombre: {datos['nombre']}"), flag=wx.LEFT | wx.TOP, border=10)
        vbox.Add(wx.StaticText(panel, label=f"Domicilio: {datos['domicilio']}"), flag=wx.LEFT | wx.TOP, border=10)
        vbox.Add(wx.StaticText(panel, label=f"Telefono: {datos['telefono']}"), flag=wx.LEFT | wx.TOP, border=10)
        vbox.Add(wx.StaticText(panel, label=f"Numero de socio: {datos['n_socio']}"), flag=wx.LEFT | wx.TOP, border=10)

        btn_editar = wx.Button(panel, label="Editar")
        btn_editar.Bind(wx.EVT_BUTTON, self.editar_socio)
        btn_delete = wx.Button(panel, label="Eliminar")
        btn_delete.Bind(wx.EVT_BUTTON, self.eliminar_socio)
        btn_cerrar = wx.Button(panel, wx.ID_CANCEL, "Cerrar")

        hbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox.Add(btn_editar, flag=wx.RIGHT, border=10)
        hbox.Add(btn_delete, flag=wx.RIGHT, border=10)
        hbox.Add(btn_cerrar)

        vbox.Add(hbox, flag=wx.ALIGN_CENTER | wx.TOP | wx.BOTTOM, border=10)
        panel.SetSizer(vbox)

    def editar_socio(self, event):
        dialogo = EditarSocioDialog(self, self.id_socio)
        if dialogo.ShowModal() == wx.ID_OK:
            self.EndModal(wx.ID_OK)
        dialogo.Destroy()

    def eliminar_socio(self, event):
        dialogo = EliminarSocioDialog(self, self.id_socio, gestion_socio)
        if dialogo.ShowModal() == wx.ID_OK:
            self.EndModal(wx.ID_OK)
        dialogo.Destroy()

class EditarSocioDialog(wx.Dialog):
    def __init__(self, parent, id_socio):
        super().__init__(parent, title="Editar socio", size=(300, 250))
        self.id_socio = id_socio

        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        socios = gestion_socio.obtener_todos()
        datos = socios.get(id_socio, {})

        vbox.Add(wx.StaticText(panel, label="Nombre:"), flag=wx.LEFT | wx.TOP, border=10)
        self.txt_nombre = wx.TextCtrl(panel, value=datos.get("nombre", ""))
        vbox.Add(self.txt_nombre, flag=wx.EXPAND | wx.LEFT | wx.RIGHT, border=10)

        vbox.Add(wx.StaticText(panel, label="Domicilio:"), flag=wx.LEFT | wx.TOP, border=10)
        self.txt_domicilio = wx.TextCtrl(panel, value=datos.get("domicilio", ""))
        vbox.Add(self.txt_domicilio, flag=wx.EXPAND | wx.LEFT | wx.RIGHT, border=10)

        vbox.Add(wx.StaticText(panel, label="Telefono:"), flag=wx.LEFT | wx.TOP, border=10)
        self.txt_telefono = wx.TextCtrl(panel, value=str(datos.get("telefono", "")))
        vbox.Add(self.txt_telefono, flag=wx.EXPAND | wx.LEFT | wx.RIGHT, border=10)

        vbox.Add(wx.StaticText(panel, label="Numero de socio:"), flag=wx.LEFT | wx.TOP, border=10)
        self.txt_n_socio = wx.TextCtrl(panel, value=datos.get("n_socio", ""))
        vbox.Add(self.txt_n_socio, flag=wx.EXPAND | wx.LEFT | wx.RIGHT, border=10)

        hbox = wx.BoxSizer(wx.HORIZONTAL)
        btn_ok = wx.Button(panel, wx.ID_OK, "Guardar")
        btn_cancel = wx.Button(panel, wx.ID_CANCEL, "Cancelar")
        hbox.Add(btn_ok, flag=wx.RIGHT, border=10)
        hbox.Add(btn_cancel)

        vbox.Add(hbox, flag=wx.ALIGN_CENTER | wx.TOP | wx.BOTTOM, border=10)
        panel.SetSizer(vbox)

        self.Bind(wx.EVT_BUTTON, self.guardar_cambios, btn_ok)

    def guardar_cambios(self, event):
        nombre = self.txt_nombre.GetValue().strip()
        domicilio = self.txt_domicilio.GetValue().strip()
        telefono = self.txt_telefono.GetValue().strip()
        n_socio = self.txt_n_socio.GetValue().strip()

        if not nombre or not domicilio or not telefono or not n_socio:
            wx.MessageBox("Todos los campos son obligatorios", "Error", wx.OK | wx.ICON_ERROR)
            return

        try:
            gestion_socio.editar_socio(self.id_socio, nombre, domicilio, telefono, n_socio)
            wx.MessageBox("Socio actualizado con éxito", "Éxito", wx.OK | wx.ICON_INFORMATION)
            self.EndModal(wx.ID_OK)
        except Exception as e:
            wx.MessageBox(str(e), "Error", wx.OK | wx.ICON_ERROR)

import wx

class EliminarSocioDialog(wx.Dialog):
    def __init__(self, parent, id_socio, gestion_socio):
        super().__init__(parent, title="Eliminar socio", size=(300, 150))
        self.id_socio = id_socio
        self.parent = parent
        self.gestion_socio = gestion_socio

        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        socio = self.gestion_socio.buscar_socio(id_socio)
        

        if socio:
            mensaje = f"¿Estás seguro de que deseas eliminar el socio con ID '{socio['id']}'?"
            vbox.Add(wx.StaticText(panel, label=mensaje), flag=wx.ALL, border=10)

            hbox = wx.BoxSizer(wx.HORIZONTAL)
            btn_ok = wx.Button(panel, wx.ID_OK, "Eliminar")
            btn_cancel = wx.Button(panel, wx.ID_CANCEL, "Cancelar")
            hbox.Add(btn_ok, flag=wx.RIGHT, border=10)
            hbox.Add(btn_cancel)

            vbox.Add(hbox, flag=wx.ALIGN_CENTER | wx.TOP | wx.BOTTOM, border=10)
            panel.SetSizer(vbox)

            self.Bind(wx.EVT_BUTTON, self.eliminar_socio, btn_ok)
        else:
            wx.MessageBox(f"No se encontró el socio con ID {id_socio}", "Error", wx.OK | wx.ICON_ERROR)
            self.EndModal(wx.ID_CANCEL)

    def eliminar_socio(self, event):
        try:
            self.gestion_socio.eliminar_socio(self.id_socio)
            wx.MessageBox("Socio eliminado con éxito", "Éxito", wx.OK | wx.ICON_INFORMATION) #linea corregida
            self.EndModal(wx.ID_OK)
            if hasattr(self.parent, "cargar_socios"):
                self.parent.cargar_socios()
        except Exception as e:
            wx.MessageBox(str(e), "Error", wx.OK | wx.ICON_ERROR)

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
        if not nombre or not domicilio or not telefono :
            self.mostrar_mensaje("Error: Todos los campos son obligatorios.", wx.ICON_ERROR)
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

        except Exception as e:
            self.mostrar_mensaje(f"Error al guardar el socio: {e}", wx.ICON_ERROR)

    def mostrar_mensaje(self, mensaje, tipo=wx.ICON_ERROR):
        wx.MessageBox(mensaje, "Información", style=tipo)