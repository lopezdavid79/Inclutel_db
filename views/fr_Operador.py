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
        # Combobox para seleccionar el operador
        vbox.Add(wx.StaticText(panel, label="Seleccionar Operador:"), flag=wx.LEFT | wx.TOP, border=10)
        self.combo_operador = wx.ComboBox(panel, choices=self.obtener_nombres_operadores(), style=wx.CB_READONLY)
        vbox.Add(self.combo_operador, flag=wx.EXPAND | wx.LEFT | wx.RIGHT, border=10)
        # Establecer un valor por defecto (opcional)
        if self.combo_operador.GetCount() > 0:
            self.combo_operador.SetSelection(3)

    
#fecha
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
        nombre = self.combo_operador.GetStringSelection().strip()  # Obtener el nombre del combobox 
        fecha = self.txt_fecha.GetValue().strip()
        comienzo = self.txt_hora_comienzo.GetValue().strip()
        fin = self.txt_hora_fin.GetValue().strip()
        operador_id = gestion_OperadorTurno.obtener_operador_id(nombre)
        if not fecha or not comienzo or not fin:
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

        existe, dentro_horario = gestion_OperadorTurno.existe_y_esta_dentro_del_horario(fecha, comienzo, fin,operador_id)

        if existe and dentro_horario:
            self.abrir_list_reclamo(fecha, fin,operador_id)
            return
        elif existe and not dentro_horario:
            wx.MessageBox("⚠️ Ya existe un turno en esa fecha, pero el horario no coincide. No se puede registrar.", "Conflicto de horario", wx.OK | wx.ICON_WARNING)
            return

        
        print(operador_id)
        operador = OperadorTurno(fecha, comienzo, fin, operador_id)
        exito = gestion_OperadorTurno.registrar_operador(operador)

        if exito:
            self.txt_resultado.SetLabel(f"✅ Turno guardado: {nombre} {fecha} ({comienzo} - {fin})")
            self.abrir_list_reclamo(fecha, fin,operador_id)
        else:
            self.txt_resultado.SetLabel("❌ Error al guardar el turno. Ver logs.")

        turno = gestion_OperadorTurno.obtener_todos()
#        print(turno)

    def abrir_list_reclamo(self, fecha, hora_fin, operador_id):
        self.list_reclamo = ListReclamo(None,  fecha=fecha, hora_fin=hora_fin, operador_id=operador_id)
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

    def obtener_nombres_operadores(self):
        """Obtiene los nombres de los operadores usando la clase de gestión."""
        return gestion_OperadorTurno.obtener_nombres_operadores()
