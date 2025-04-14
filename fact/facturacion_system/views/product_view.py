import tkinter as tk
from tkinter import ttk, messagebox
from models.product_model import Producto

class ProductosView:
    def __init__(self, root, on_close_callback=None):
        self.root = root
        self.on_close_callback = on_close_callback
        self.setup_ui()
        self.load_products()
    
    def setup_ui(self):
        self.root.title("Gestión de Productos")
        self.root.geometry("800x600")
        self.root.resizable(False, False)
        
        # Frame principal
        main_frame = tk.Frame(self.root, padx=10, pady=10)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Frame de formulario
        form_frame = tk.LabelFrame(main_frame, text="Información del Producto", padx=5, pady=5)
        form_frame.pack(fill=tk.X, pady=5)
        
        # Campos del formulario
        tk.Label(form_frame, text="Código de Barras:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.codigo_entry = tk.Entry(form_frame, width=30)
        self.codigo_entry.grid(row=0, column=1, pady=2, padx=5)
        
        tk.Label(form_frame, text="Nombre:").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.nombre_entry = tk.Entry(form_frame, width=30)
        self.nombre_entry.grid(row=1, column=1, pady=2, padx=5)
        
        tk.Label(form_frame, text="Descripción:").grid(row=2, column=0, sticky=tk.W, pady=2)
        self.descripcion_entry = tk.Entry(form_frame, width=30)
        self.descripcion_entry.grid(row=2, column=1, pady=2, padx=5)
        
        tk.Label(form_frame, text="Precio:").grid(row=3, column=0, sticky=tk.W, pady=2)
        self.precio_entry = tk.Entry(form_frame, width=30)
        self.precio_entry.grid(row=3, column=1, pady=2, padx=5)
        
        tk.Label(form_frame, text="Stock:").grid(row=4, column=0, sticky=tk.W, pady=2)
        self.stock_entry = tk.Entry(form_frame, width=30)
        self.stock_entry.grid(row=4, column=1, pady=2, padx=5)
        
        tk.Label(form_frame, text="Categoría:").grid(row=5, column=0, sticky=tk.W, pady=2)
        self.categoria_entry = tk.Entry(form_frame, width=30)
        self.categoria_entry.grid(row=5, column=1, pady=2, padx=5)
        
        # Botones del formulario
        button_frame = tk.Frame(form_frame)
        button_frame.grid(row=6, columnspan=2, pady=10)
        
        tk.Button(button_frame, text="Guardar", command=self.save_product).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Limpiar", command=self.clear_form).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Escanear Código", command=self.scan_barcode).pack(side=tk.LEFT, padx=5)
        
        # Treeview para mostrar productos
        tree_frame = tk.Frame(main_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        self.tree = ttk.Treeview(tree_frame, columns=("ID", "Código", "Nombre", "Precio", "Stock", "Categoría"), show="headings")
        
        # Configurar columnas
        self.tree.heading("ID", text="ID")
        self.tree.heading("Código", text="Código Barras")
        self.tree.heading("Nombre", text="Nombre")
        self.tree.heading("Precio", text="Precio")
        self.tree.heading("Stock", text="Stock")
        self.tree.heading("Categoría", text="Categoría")
        
        self.tree.column("ID", width=50, anchor=tk.CENTER)
        self.tree.column("Código", width=120)
        self.tree.column("Nombre", width=200)
        self.tree.column("Precio", width=80, anchor=tk.E)
        self.tree.column("Stock", width=80, anchor=tk.CENTER)
        self.tree.column("Categoría", width=150)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.pack(fill=tk.BOTH, expand=True)
        
        # Bind para selección
        self.tree.bind("<ButtonRelease-1>", self.on_product_select)
        
        # Botón de cerrar
        tk.Button(main_frame, text="Cerrar", command=self.on_close).pack(side=tk.RIGHT, pady=5)
    
    def load_products(self):
        """Cargar productos en el Treeview"""
        for i in self.tree.get_children():
            self.tree.delete(i)
            
        productos = Producto.get_all()
        for prod in productos:
            self.tree.insert("", tk.END, values=prod)
    
    def save_product(self):
        """Guardar producto en la base de datos"""
        codigo = self.codigo_entry.get()
        nombre = self.nombre_entry.get()
        descripcion = self.descripcion_entry.get()
        precio = self.precio_entry.get()
        stock = self.stock_entry.get()
        categoria = self.categoria_entry.get()
        
        # Validaciones básicas
        if not codigo or not nombre or not precio or not stock:
            messagebox.showerror("Error", "Los campos Código, Nombre, Precio y Stock son obligatorios")
            return
        
        try:
            precio = float(precio)
            stock = int(stock)
        except ValueError:
            messagebox.showerror("Error", "Precio debe ser un número y Stock un entero")
            return
        
        producto = Producto(codigo, nombre, descripcion, precio, stock, categoria)
        if producto.save():
            messagebox.showinfo("Éxito", "Producto guardado correctamente")
            self.load_products()
            self.clear_form()
        else:
            messagebox.showerror("Error", "No se pudo guardar el producto")
    
    def clear_form(self):
        """Limpiar el formulario"""
        self.codigo_entry.delete(0, tk.END)
        self.nombre_entry.delete(0, tk.END)
        self.descripcion_entry.delete(0, tk.END)
        self.precio_entry.delete(0, tk.END)
        self.stock_entry.delete(0, tk.END)
        self.categoria_entry.delete(0, tk.END)
    
    def on_product_select(self, event):
        """Cargar datos del producto seleccionado en el formulario"""
        selected = self.tree.focus()
        if selected:
            values = self.tree.item(selected, "values")
            self.clear_form()
            
            self.codigo_entry.insert(0, values[1])
            self.nombre_entry.insert(0, values[2])
            self.descripcion_entry.insert(0, values[3] if len(values) > 3 and values[3] != "None" else "")
            self.precio_entry.insert(0, values[4] if len(values) > 4 else "")
            self.stock_entry.insert(0, values[5] if len(values) > 5 else "")
            self.categoria_entry.insert(0, values[6] if len(values) > 6 and values[6] != "None" else "")
    
    def scan_barcode(self):
        """Simular escaneo de código de barras (implementación real en utils/barcode_reader.py)"""
        # Esta es una simulación - la implementación real se verá más adelante
        from utils.barcode_reader import read_barcode
        codigo = read_barcode()
        if codigo:
            self.codigo_entry.delete(0, tk.END)
            self.codigo_entry.insert(0, codigo)
            
            # Buscar si el producto ya existe
            producto = Producto.get_by_barcode(codigo)
            if producto:
                self.clear_form()
                self.codigo_entry.insert(0, producto[1])
                self.nombre_entry.insert(0, producto[2])
                self.descripcion_entry.insert(0, producto[3] if producto[3] else "")
                self.precio_entry.insert(0, producto[4])
                self.stock_entry.insert(0, producto[5])
                self.categoria_entry.insert(0, producto[6] if producto[6] else "")
                messagebox.showinfo("Información", "Producto encontrado en la base de datos")
    
    def on_close(self):
        """Manejar el cierre de la ventana"""
        if self.on_close_callback:
            self.on_close_callback()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = ProductosView(root)
    root.mainloop()