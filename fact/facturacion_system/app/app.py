from views.main_view import FacturacionView
import tkinter as tk
from models.database import initialize_database

def main():
    # Inicializar la base de datos
    initialize_database()
    
    # Crear ventana principal
    root = tk.Tk()
    app = FacturacionView(root)
    root.mainloop()

if __name__ == "__main__":
    main()