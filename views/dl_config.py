import wx
import wx.adv
import wx.lib.intctrl
from module.OperadorTurno import GestionOperadorTurno

gesstion_operador_turno = GestionOperadorTurno()  # corregido nombre

class ConfigDialog(wx.Dialog):
    def __init__(self, parent):
        super().__init__(parent, title="Configuración", size=(300, 300))

        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        # Checkbox para sonidos
        self.chk_sonido = wx.CheckBox(panel, label="Habilitar sonidos")
        vbox.Add(self.chk_sonido, flag=wx.ALL | wx.EXPAND, border=10)

        # Horario de inicio
        hbox_inicio = wx.BoxSizer(wx.HORIZONTAL)
        hbox_inicio.Add(wx.StaticText(panel, label="Inicio del turno:"), flag=wx.RIGHT, border=8)
        self.tp_inicio = wx.adv.TimePickerCtrl(panel)
        hbox_inicio.Add(self.tp_inicio, proportion=1)
        vbox.Add(hbox_inicio, flag=wx.ALL | wx.EXPAND, border=10)

        # Horario de fin
        hbox_fin = wx.BoxSizer(wx.HORIZONTAL)
        hbox_fin.Add(wx.StaticText(panel, label="Fin del turno:"), flag=wx.RIGHT, border=8)
        self.tp_fin = wx.adv.TimePickerCtrl(panel)
        hbox_fin.Add(self.tp_fin, proportion=1)
        vbox.Add(hbox_fin, flag=wx.ALL | wx.EXPAND, border=10)

        # Selector de operador predeterminado
        self.nombres_operadores = gesstion_operador_turno.obtener_nombres_operadores()
        vbox.Add(wx.StaticText(panel, label="Operador predeterminado:"), flag=wx.LEFT | wx.TOP, border=10)
        self.combo_operador = wx.ComboBox(panel, choices=self.nombres_operadores, style=wx.CB_READONLY)
        vbox.Add(self.combo_operador, flag=wx.EXPAND | wx.LEFT | wx.RIGHT, border=10)

        # Botones
        btn_guardar = wx.Button(panel, label="Guardar")
        btn_cancelar = wx.Button(panel, label="Cancelar")
        hbox_botones = wx.BoxSizer(wx.HORIZONTAL)
        hbox_botones.Add(btn_guardar, flag=wx.RIGHT, border=10)
        hbox_botones.Add(btn_cancelar)
        vbox.Add(hbox_botones, flag=wx.ALIGN_CENTER | wx.ALL, border=10)

        panel.SetSizer(vbox)

        self.CargarConfiguracion()

        # Eventos
        btn_guardar.Bind(wx.EVT_BUTTON, self.OnGuardar)
        btn_cancelar.Bind(wx.EVT_BUTTON, lambda event: self.Close())

    def CargarConfiguracion(self):
        config = wx.Config("MiApp")
        self.chk_sonido.SetValue(config.ReadBool("sonido", True))

        hora_inicio = config.Read("hora_inicio", "08:00")
        hora_fin = config.Read("hora_fin", "16:00")

        h_ini, m_ini = map(int, hora_inicio.split(":"))
        h_fin, m_fin = map(int, hora_fin.split(":"))

        self.tp_inicio.SetTime(h_ini, m_ini, 0)
        self.tp_fin.SetTime(h_fin, m_fin, 0)

        operador_predeterminado = config.Read("operador_predeterminado", "")
        if operador_predeterminado in self.nombres_operadores:
            self.combo_operador.SetStringSelection(operador_predeterminado)

    def OnGuardar(self, event):
        config = wx.Config("MiApp")
        config.WriteBool("sonido", self.chk_sonido.GetValue())

        h_ini, m_ini, _ = self.tp_inicio.GetTime()
        h_fin, m_fin, _ = self.tp_fin.GetTime()

        config.Write("hora_inicio", f"{h_ini:02}:{m_ini:02}")
        config.Write("hora_fin", f"{h_fin:02}:{m_fin:02}")

        operador_seleccionado = self.combo_operador.GetStringSelection()
        config.Write("operador_predeterminado", operador_seleccionado)

        config.Flush()

        wx.MessageBox("Configuración guardada", "Info", wx.OK | wx.ICON_INFORMATION)
        self.Close()
import wx
import wx.adv
import wx.lib.intctrl
from module.OperadorTurno import GestionOperadorTurno

gesstion_operador_turno = GestionOperadorTurno()  # corregido nombre

class ConfigDialog(wx.Dialog):
    def __init__(self, parent):
        super().__init__(parent, title="Configuración", size=(300, 300))

        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        # Checkbox para sonidos
        self.chk_sonido = wx.CheckBox(panel, label="Habilitar sonidos")
        vbox.Add(self.chk_sonido, flag=wx.ALL | wx.EXPAND, border=10)

        # Horario de inicio
        hbox_inicio = wx.BoxSizer(wx.HORIZONTAL)
        hbox_inicio.Add(wx.StaticText(panel, label="Inicio del turno:"), flag=wx.RIGHT, border=8)
        self.tp_inicio = wx.adv.TimePickerCtrl(panel)
        hbox_inicio.Add(self.tp_inicio, proportion=1)
        vbox.Add(hbox_inicio, flag=wx.ALL | wx.EXPAND, border=10)

        # Horario de fin
        hbox_fin = wx.BoxSizer(wx.HORIZONTAL)
        hbox_fin.Add(wx.StaticText(panel, label="Fin del turno:"), flag=wx.RIGHT, border=8)
        self.tp_fin = wx.adv.TimePickerCtrl(panel)
        hbox_fin.Add(self.tp_fin, proportion=1)
        vbox.Add(hbox_fin, flag=wx.ALL | wx.EXPAND, border=10)

        # Selector de operador predeterminado
        self.nombres_operadores = gesstion_operador_turno.obtener_nombres_operadores()
        vbox.Add(wx.StaticText(panel, label="Operador predeterminado:"), flag=wx.LEFT | wx.TOP, border=10)
        self.combo_operador = wx.ComboBox(panel, choices=self.nombres_operadores, style=wx.CB_READONLY)
        vbox.Add(self.combo_operador, flag=wx.EXPAND | wx.LEFT | wx.RIGHT, border=10)

        # Botones
        btn_guardar = wx.Button(panel, label="Guardar")
        btn_cancelar = wx.Button(panel, label="Cancelar")
        hbox_botones = wx.BoxSizer(wx.HORIZONTAL)
        hbox_botones.Add(btn_guardar, flag=wx.RIGHT, border=10)
        hbox_botones.Add(btn_cancelar)
        vbox.Add(hbox_botones, flag=wx.ALIGN_CENTER | wx.ALL, border=10)

        panel.SetSizer(vbox)

        self.CargarConfiguracion()

        # Eventos
        btn_guardar.Bind(wx.EVT_BUTTON, self.OnGuardar)
        btn_cancelar.Bind(wx.EVT_BUTTON, lambda event: self.Close())

    def CargarConfiguracion(self):
        config = wx.Config("MiApp")
        self.chk_sonido.SetValue(config.ReadBool("sonido", True))

        hora_inicio = config.Read("hora_inicio", "08:00")
        hora_fin = config.Read("hora_fin", "16:00")

        h_ini, m_ini = map(int, hora_inicio.split(":"))
        h_fin, m_fin = map(int, hora_fin.split(":"))

        self.tp_inicio.SetTime(h_ini, m_ini, 0)
        self.tp_fin.SetTime(h_fin, m_fin, 0)

        operador_predeterminado = config.Read("operador_predeterminado", "")
        if operador_predeterminado in self.nombres_operadores:
            self.combo_operador.SetStringSelection(operador_predeterminado)

    def OnGuardar(self, event):
        config = wx.Config("MiApp")
        config.WriteBool("sonido", self.chk_sonido.GetValue())

        h_ini, m_ini, _ = self.tp_inicio.GetTime()
        h_fin, m_fin, _ = self.tp_fin.GetTime()

        config.Write("hora_inicio", f"{h_ini:02}:{m_ini:02}")
        config.Write("hora_fin", f"{h_fin:02}:{m_fin:02}")

        operador_seleccionado = self.combo_operador.GetStringSelection()
        config.Write("operador_predeterminado", operador_seleccionado)

        config.Flush()

        wx.MessageBox("Configuración guardada", "Info", wx.OK | wx.ICON_INFORMATION)
        self.Close()
