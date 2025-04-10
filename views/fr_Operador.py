from datetime import datetime
import re
import wx
from views.fr_ListReclamo import ListReclamo
from module.OperadorTurno import OperadorTurno, GestionOperadorTurno

gestion_OperadorTurno = GestionOperadorTurno()

class TurnoFrame(wx.Frame):
    def __init__(self, parent, id=None, title="Gestión de Reclamos", *args, **kwds):
        super().__init__(parent, id=wx.ID_ANY, title=title, *args, **kwds)
        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        vbox.Add(wx.StaticText(panel, label="Nombre del Operador:"), flag=wx.LEFT | wx.TOP, border=10)
        self.txt_nombre = wx.TextCtrl(panel, value="Mara")
        vbox.Add(self.txt_nombre, flag=wx.EXPAND | wx.LEFT | wx.RIGHT, border=10)

        vbox.Add(wx.StaticText(panel, label="Fecha :"), flag=wx.LEFT | wx.TOP, border=10)
        self.txt_fecha = wx.TextCtrl(panel, value=datetime.now().strftime("%Y-%m-%d"))
        vbox.Add(self.txt_fecha, flag=wx.EXPAND | wx.LEFT | wx.RIGHT, border=10)

        vbox.Add(wx.StaticText(panel, label="Hora de comienzo (HH:MM):"), flag=wx.LEFT | wx.TOP, border=10)
        self.txt_hora_comienzo = wx.TextCtrl(panel, value=datetime.now().strftime("%H:%M"))
        vbox.Add(self.txt_hora_comienzo, flag=wx.EXPAND | wx.LEFT | wx.RIGHT, border=10)

        vbox.Add(wx.StaticText(panel, label="Hora de fin (HH:MM):"), flag=wx.LEFT | wx.TOP, border=10)
        self.txt_hora_fin = wx.TextCtrl(panel, value="18:00")
        vbox.Add(self.txt_hora_fin, flag=wx.EXPAND | wx.LEFT | wx.RIGHT, border=10)

        hbox_botones = wx.BoxSizer(wx.HORIZONTAL)
        self.btn_guardar = wx.Button(panel, label="&Iniciar Turno")
        self.btn_guardar.Bind(wx.EVT_BUTTON, self.guardar_turno)
        hbox_botones.Add(self.btn_guardar, flag=wx.RIGHT, border=10)

        self.btn_cerrar = wx.Button(panel, label="Cerrar")
        self.btn_cerrar.Bind(wx.EVT_BUTTON, self.cerrar_ventana)
        hbox_botones.Add(self.btn_cerrar)

        vbox.Add(hbox_botones, flag=wx.ALL | wx.ALIGN_CENTER, border=10)
        self.txt_resultado = wx.StaticText(panel, label="")
        vbox.Add(self.txt_resultado, flag=wx.ALL | wx.ALIGN_CENTER, border=10)

        panel.SetSizer(vbox)
        self.Centre()
        self.Show()

    def cerrar_ventana(self, event):
        self.Close()

    def guardar_turno(self, event):
        nombre = self.txt_nombre.GetValue().strip()
        fecha = self.txt_fecha.GetValue().strip()
        comienzo = self.txt_hora_comienzo.GetValue().strip()
        fin = self.txt_hora_fin.GetValue().strip()

        if not nombre or not fecha or not comienzo or not fin:
            wx.MessageBox("Por favor, completá todos los campos.", "Faltan datos", wx.OK | wx.ICON_WARNING)
            return

        if not TurnoFrame.validar_fecha(fecha):
            wx.MessageBox("La fecha no es válida. Usá el formato YYYY-MM-DD.", "Fecha inválida", wx.OK | wx.ICON_WARNING)
            return

        if not TurnoFrame.validar_hora(comienzo) or not TurnoFrame.validar_hora(fin):
            wx.MessageBox("Las horas ingresadas no son válidas. Usá el formato HH:MM (por ejemplo, 08:30).", "Hora inválida", wx.OK | wx.ICON_WARNING)
            return

        hora_inicio = datetime.strptime(comienzo, "%H:%M")
        hora_fin = datetime.strptime(fin, "%H:%M")
        if hora_fin <= hora_inicio:
            wx.MessageBox("La hora de fin debe ser posterior a la de comienzo.", "Hora inválida", wx.OK | wx.ICON_WARNING)
            return

        existe, dentro_horario = gestion_OperadorTurno.existe_y_esta_dentro_del_horario(nombre, fecha, comienzo, fin)

        if existe and dentro_horario:
            self.abrir_list_reclamo(nombre, fecha, fin)
            return
        elif existe and not dentro_horario:
            wx.MessageBox("⚠️ Ya existe un turno en esa fecha, pero el horario no coincide. No se puede registrar.", "Conflicto de horario", wx.OK | wx.ICON_WARNING)
            return

        operador = OperadorTurno(nombre, fecha, comienzo, fin)
        exito = gestion_OperadorTurno.registrar_operador(operador)

        if exito:
            self.txt_resultado.SetLabel(f"✅ Turno guardado: {nombre} {fecha} ({comienzo} - {fin})")
            self.abrir_list_reclamo(nombre, fecha, fin)
        else:
            self.txt_resultado.SetLabel("❌ Error al guardar el turno. Ver logs.")

        turno = gestion_OperadorTurno.obtener_todos()
        print(turno)

    def abrir_list_reclamo(self, nombre, fecha, hora_fin):
        self.list_reclamo = ListReclamo(None, nombre=nombre, fecha=fecha, hora_fin=hora_fin)
        self.list_reclamo.Show()
        self.Close()

    @staticmethod
    def validar_hora(hora_str):
        patron = r"^([01]?\d|2[0-3]):([0-5]\d)$"
        return bool(re.match(patron, hora_str))

    @staticmethod
    def validar_fecha(fecha_str):
        try:
            datetime.strptime(fecha_str, "%Y-%m-%d")
            return True
        except ValueError:
            return False
