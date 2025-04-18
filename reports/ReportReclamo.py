import wx
import pandas as pd
import wx.adv
from datetime import datetime
from module.GestionReclamo import GestionReclamo
gestion_reclamo=GestionReclamo()
class ReporteReclamosFrame(wx.Frame):
    def __init__(self, parent, title="Reporte de Reclamos"):
        super().__init__(parent, title=title, size=(800, 600))
        #self.gestion_reclamo = gestion_reclamo  # Recibe la instancia de gestión de reclamos
        self.panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        # Controles para seleccionar rango de fechas
        hbox_fechas = wx.BoxSizer(wx.HORIZONTAL)

        hbox_inicio = wx.BoxSizer(wx.VERTICAL)
        hbox_inicio.Add(wx.StaticText(self.panel, label="Fecha Inicio:"), flag=wx.BOTTOM, border=5)
        self.date_picker_inicio = wx.adv.DatePickerCtrl(self.panel, style=wx.adv.DP_DROPDOWN | wx.adv.DP_SHOWCENTURY)
        hbox_inicio.Add(self.date_picker_inicio)
        hbox_fechas.Add(hbox_inicio, proportion=1, flag=wx.RIGHT, border=10)

        hbox_fin = wx.BoxSizer(wx.VERTICAL)
        hbox_fin.Add(wx.StaticText(self.panel, label="Fecha Fin:"), flag=wx.BOTTOM, border=5)
        self.date_picker_fin = wx.adv.DatePickerCtrl(self.panel, style=wx.adv.DP_DROPDOWN | wx.adv.DP_SHOWCENTURY)
        hbox_fin.Add(self.date_picker_fin)
        hbox_fechas.Add(hbox_fin, proportion=1)

        vbox.Add(hbox_fechas, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, border=10)

        # Botón de filtrar
        self.btn_filtrar = wx.Button(self.panel, label="Filtrar Reclamos")
        self.btn_filtrar.Bind(wx.EVT_BUTTON, self.on_filtrar_reclamos)
        vbox.Add(self.btn_filtrar, flag=wx.ALIGN_CENTER | wx.ALL, border=10)

        # Lista para mostrar los reclamos
        self.list_ctrl = wx.ListCtrl(self.panel, style=wx.LC_REPORT | wx.BORDER_SUNKEN)
        vbox.Add(self.list_ctrl, proportion=1, flag=wx.EXPAND | wx.ALL, border=10)

        self.txt_total_reclamos = wx.StaticText(self.panel, label="Total Reclamos: 0")
        vbox.Add(self.txt_total_reclamos, flag=wx.ALIGN_RIGHT | wx.ALL, border=10)

        self.panel.SetSizer(vbox)
        self.Centre()
        self.Show()
        self.cargar_reclamos() # Cargar todos los reclamos al inicio

    def cargar_reclamos(self, fecha_inicio=None, fecha_fin=None):
        try:
            if gestion_reclamo:
                df = gestion_reclamo.obtener_reclamos_rango_pandas(fecha_inicio, fecha_fin)
                self.mostrar_dataframe_en_lista(df)
                if not df.empty:
                    total_reclamos = len(df)
                    self.txt_total_reclamos.SetLabel(f"Total Reclamos: {total_reclamos}")
                else:
                    self.txt_total_reclamos.SetLabel("Total Reclamos: 0")
            else:
                wx.MessageBox("Error: No se recibió la instancia de gestión de reclamos.", "Error", wx.OK | wx.ICON_ERROR)
        except Exception as e:
            wx.MessageBox(f"Error al cargar reclamos: {e}", "Error", wx.OK | wx.ICON_ERROR)

    def mostrar_dataframe_en_lista(self, df):
        self.list_ctrl.ClearAll()

        if df.empty:
            self.list_ctrl.InsertColumn(0, "Información")
            self.list_ctrl.InsertItem(0, "No se encontraron reclamos en el rango seleccionado.")
            return

        # Crear columnas
        for col_idx, col in enumerate(df.columns):
            self.list_ctrl.InsertColumn(col_idx, col, width=150)

        # Agregar filas
        for row_idx, row in df.iterrows():
            index = self.list_ctrl.InsertItem(row_idx, str(row[0]))  # Primera columna
            for col_idx in range(1, len(df.columns)):
                self.list_ctrl.SetItem(index, col_idx, str(row[col_idx]))

        # Ajustar ancho
        for i in range(len(df.columns)):
            self.list_ctrl.SetColumnWidth(i, wx.LIST_AUTOSIZE_USEHEADER)

    def on_filtrar_reclamos(self, event):
        fecha_inicio = self.date_picker_inicio.GetValue().FormatISODate()
        fecha_fin = self.date_picker_fin.GetValue().FormatISODate()
        self.cargar_reclamos(fecha_inicio, fecha_fin)
