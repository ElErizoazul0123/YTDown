import os
import sys
if getattr(sys, "frozen", False):
    os.chdir(os.path.dirname(sys.executable))
from Modulos.UI.ventana_principal import ventana_principal

app = ventana_principal()




app.mainloop()


