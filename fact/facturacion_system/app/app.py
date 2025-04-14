from fact.facturacion_system.views.main_view import FacturacionView
import tkinter as tk
from fact.facturacion_system.models.database import initialize_database
import sys
from pathlib import Path

# Añade la ruta del proyecto al PYTHONPATH
sys.path.append(str(Path(__file__).parent.parent))

from views.main_view import FacturacionView
def main():
    # Inicializar la base de datos
    initialize_database()
    
    # Crear ventana principal
    root = tk.Tk()
    app = FacturacionView(root)
    root.mainloop()

if __name__ == "__main__":
    main()