import wx
import pandas as pd

# Datos simulados
turnos = pd.DataFrame([
    {"id_turno": 1, "fecha": "2025-04-08", "hora_inicio": "14:00", "hora_fin": "18:00", "operador": "Mara"},
    {"id_turno": 2, "fecha": "2025-04-08", "hora_inicio": "18:00", "hora_fin": "22:00", "operador": "Juan"},
])

reclamos = pd.DataFrame([
    {"id_turno": 1, "categoria": "Técnica", "descripcion": "Problemas con el router"},
    {"id_turno": 1, "categoria": "Comercial", "descripcion": "Error en la factura"},
    {"id_turno": 2, "categoria": "Técnica", "descripcion": "No hay conexión"},
])

class ReporteTurnosFrame(wx.Frame):
    def __init__(self, parent, title="Reporte de Turnos y Reclamos"):
        super().__init__(parent, title=title, size=(600, 500))

        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        # Filtro de fecha
        hbox_fecha = wx.BoxSizer(wx.HORIZONTAL)
        hbox_fecha.Add(wx.StaticText(panel, label="Fecha (YYYY-MM-DD): "))
        self.txt_fecha = wx.TextCtrl(panel)
        hbox_fecha.Add(self.txt_fecha, proportion=1)
        vbox.Add(hbox_fecha, flag=wx.EXPAND | wx.ALL, border=10)

        # Filtro de categoría
        hbox_categoria = wx.BoxSizer(wx.HORIZONTAL)
        hbox_categoria.Add(wx.StaticText(panel, label="Categoría: "))
        self.cmb_categoria = wx.ComboBox(panel, choices=["Todas", "Técnica", "Comercial"], style=wx.CB_READONLY)
        self.cmb_categoria.SetSelection(0)
        hbox_categoria.Add(self.cmb_categoria, proportion=1)
        vbox.Add(hbox_categoria, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, border=10)

        # Botón de filtrar
        self.btn_filtrar = wx.Button(panel, label="Filtrar")
        self.btn_filtrar.Bind(wx.EVT_BUTTON, self.generar_reporte)
        vbox.Add(self.btn_filtrar, flag=wx.ALIGN_CENTER | wx.ALL, border=10)

        # Área de resultado
        self.txt_resultado = wx.TextCtrl(panel, style=wx.TE_MULTILINE | wx.TE_READONLY)
        vbox.Add(self.txt_resultado, proportion=1, flag=wx.EXPAND | wx.ALL, border=10)

        panel.SetSizer(vbox)
        self.Centre()
        self.Show()

    def generar_reporte(self, event):
        fecha = self.txt_fecha.GetValue().strip()
        categoria = self.cmb_categoria.GetValue()

        resultado = ""

        turnos_filtrados = turnos
        if fecha:
            turnos_filtrados = turnos_filtrados[turnos_filtrados["fecha"] == fecha]

        for _, turno in turnos_filtrados.iterrows():
            resultado += f"\n📅 Fecha: {turno['fecha']}\n🕒 Horario: {turno['hora_inicio']} - {turno['hora_fin']}\n👤 Operador: {turno['operador']}\n"
            reclamos_turno = reclamos[reclamos["id_turno"] == turno["id_turno"]]
            if categoria != "Todas":
                reclamos_turno = reclamos_turno[reclamos_turno["categoria"] == categoria]
            for _, r in reclamos_turno.iterrows():
                resultado += f"  - [{r['categoria']}] {r['descripcion']}\n"
        if not resultado:
            resultado = "No se encontraron resultados con los filtros aplicados."

        self.txt_resultado.SetValue(resultado)

if __name__ == '__main__':
    app = wx.App()
    ReporteTurnosFrame(None)
    app.MainLoop()
