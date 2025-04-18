import wx.adv
import wx  # Necesario para wx.Config
import sys
import os

class ReproductorSonido:
    """Clase para gestionar la reproducción de sonidos en la aplicación."""
    sonido = None  # Referencia al sonido actual (opcional si querés detenerlo)

    @staticmethod
    def sonido_habilitado():
        config = wx.Config("MiApp")
        return config.ReadBool("sonido", True)

    @staticmethod
    def reproducir(archivo):
        """Reproduce un archivo de sonido .wav si está habilitado en la config."""
        if not ReproductorSonido.sonido_habilitado():
            return  # No hacer nada si los sonidos están desactivados

        try:
            ruta_base = getattr(sys, '_MEIPASS', os.path.abspath('.'))
            ruta_sonido = os.path.join(ruta_base, 'Sounds', archivo)

            sonido = wx.adv.Sound(ruta_sonido)
            if sonido.IsOk():
                ReproductorSonido.sonido = sonido
                sonido.Play(wx.adv.SOUND_ASYNC)
            else:
                print(f"Error: No se pudo cargar el archivo de sonido '{ruta_sonido}'.")
        except Exception as e:
            print(f"Error al reproducir sonido: {e}")

    @staticmethod
    def detener():
        """Detiene la reproducción del sonido actual, si existe."""
        if ReproductorSonido.sonido:
            ReproductorSonido.sonido.Stop()
