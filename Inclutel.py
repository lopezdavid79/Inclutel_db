import wx
import os
import sys
import Tablas
from module.ReproductorSonido import ReproductorSonido 
from views.fr_ListReclamo import   ListReclamo
class MyApp(wx.App):
    def OnInit(self):
        Tablas.crear_tablas()
        self.frame = ListReclamo(None, title="Inclutel")
        self.frame.Show()
        self.SetTopWindow(self.frame)
        return True

    
if __name__ == "__main__":
    app = MyApp()
    app.MainLoop()