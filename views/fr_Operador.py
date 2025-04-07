import wx
from views.fr_ListReclamo import   ListReclamo
from datetime import datetime
from module.OperadorTurno import OperadorTurno, GestionOperadorTurno

gestion_OperadorTurno = GestionOperadorTurno()

class TurnoFrame(wx.Frame):
    def __init__(self, parent, id=None, title="Gestión de Reclamos", *args, **kwds):
        super().__init__(parent, id=wx.ID_ANY, title=title, *args, **kwds)

        panel = wx.Panel(self)

        vbox = wx.BoxSizer(wx.VERTICAL)

        # Nombre
        vbox.Add(wx.StaticText(panel, label="Nombre del Operador:"), flag=wx.LEFT | wx.TOP, border=10)
        self.txt_nombre = wx.TextCtrl(panel, value="Mara"   )
        vbox.Add(self.txt_nombre, flag=wx.EXPAND | wx.LEFT | wx.RIGHT, border=10)

        # Fecha del turno
        vbox.Add(wx.StaticText(panel, label="Fecha :"), flag=wx.LEFT | wx.TOP, border=10)
        self.txt_fecha = wx.TextCtrl(panel, value=datetime.now().strftime("%Y-%m-%d"))
        vbox.Add(self.txt_fecha, flag=wx.EXPAND | wx.LEFT | wx.RIGHT, border=10)

        # Hora comienzo
        vbox.Add(wx.StaticText(panel, label="Hora de comienzo (HH:MM):"), flag=wx.LEFT | wx.TOP, border=10)
        self.txt_hora_comienzo = wx.TextCtrl(panel, value="14:00")
        vbox.Add(self.txt_hora_comienzo, flag=wx.EXPAND | wx.LEFT | wx.RIGHT, border=10)

        # Hora fin
        vbox.Add(wx.StaticText(panel, label="Hora de fin (HH:MM):"), flag=wx.LEFT | wx.TOP, border=10)
        self.txt_hora_fin = wx.TextCtrl(panel, value="18:00")
        vbox.Add(self.txt_hora_fin, flag=wx.EXPAND | wx.LEFT | wx.RIGHT, border=10)

        # Botones
        hbox_botones = wx.BoxSizer(wx.HORIZONTAL)

        self.btn_guardar = wx.Button(panel, label="&Iniciar  Turno")
        self.btn_guardar.Bind(wx.EVT_BUTTON, self.guardar_turno)
        hbox_botones.Add(self.btn_guardar, flag=wx.RIGHT, border=10)

        self.btn_cerrar = wx.Button(panel, label="Cerrar")
        self.btn_cerrar.Bind(wx.EVT_BUTTON, self.cerrar_ventana)
        hbox_botones.Add(self.btn_cerrar)

        vbox.Add(hbox_botones, flag=wx.ALL | wx.ALIGN_CENTER, border=10)

        # Resultado
        self.txt_resultado = wx.StaticText(panel, label="")
        vbox.Add(self.txt_resultado, flag=wx.ALL | wx.ALIGN_CENTER, border=10)

        panel.SetSizer(vbox)
        self.turno_actual = None  # (nombre, fecha)
        
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

        # Verificar si existe y si está dentro del horario
        existe, dentro_horario = gestion_OperadorTurno.existe_y_esta_dentro_del_horario(nombre, fecha, comienzo, fin)

        if existe and dentro_horario:
            wx.MessageBox("ℹ️ Ya hay un turno registrado para este operador en ese horario. Se continuará normalmente.", "Turno vigente", wx.OK | wx.ICON_INFORMATION)
            self.abrir_list_reclamo(nombre, fecha, fin)
            return

        elif existe and not dentro_horario:
            wx.MessageBox("⚠️ Ya existe un turno en esa fecha, pero el horario no coincide. No se puede registrar.", "Conflicto de horario", wx.OK | wx.ICON_WARNING)
            return

        # Si no existe, se registra
        operador = OperadorTurno(nombre, fecha, comienzo, fin)
        exito = gestion_OperadorTurno.registrar_operador(operador)

        if exito:
            self.txt_resultado.SetLabel(f"✅ Turno guardado: {nombre} {fecha} ({comienzo} - {fin})")
            #self.turno_actual = (nombre, fecha)           # <--- Guarda turno activo
            #self.temporizador.Start(1000)                 # <--- Arranca temporizador cada 1 segundo            
            self.abrir_list_reclamo(nombre, fecha, fin)
        else:
            self.txt_resultado.SetLabel("❌ Error al guardar el turno. Ver logs.")

        turno = gestion_OperadorTurno.obtener_todos()
        print(turno)


    def abrir_list_reclamo(self, nombre, fecha, hora_fin):
        self.list_reclamo = ListReclamo(None, nombre=nombre, fecha=fecha, hora_fin=hora_fin)
        self.list_reclamo.Show()
