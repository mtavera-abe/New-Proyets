import tkinter as tk
from tkinter import ttk, messagebox
from models.product_model import Producto
from models.invoice_model import Factura
from datetime import datetime

class FacturacionView:
    def __init__(self, root):
        self.root = root
        self.setup_ui()
        self.current_invoice_items = []
        self.current_client = None
    
    def setup_ui(self):
        self.root.title("Sistema de Facturación")
        self.root.geometry("1000x700")
        
        # Frame principal
        main_frame = tk.Frame(self.root, padx=10, pady=10)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Frame de información de cliente
        client_frame = tk.LabelFrame(main_frame, text="Información del Cliente", padx=5, pady=5)
        client_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(client_frame, text="NIT:").grid(row=0, column=0, sticky=tk.W)
        self.nit_entry = tk.Entry(client_frame, width=20)
        self.nit_entry.grid(row=0, column=1, padx=5)
        
        tk.Label(client_frame, text="Nombre:").grid(row=0, column=2, sticky=tk.W)
        self.client_name_entry = tk.Entry(client_frame, width=30)
        self.client_name_entry.grid(row=0, column=3, padx=5)
        
        tk.Label(client_frame, text="Dirección:").grid(row=1, column=0, sticky=tk.W)
        self.client_address_entry = tk.Entry(client_frame, width=20)
        self.client_address_entry.grid(row=1, column=1, padx=5)
        
        tk.Button(client_frame, text="Buscar Cliente", command=self.search_client).grid(row=0, column=4, padx=5)
        tk.Button(client_frame, text="Nuevo Cliente", command=self.new_client).grid(row=1, column=4, padx=5)
        
        # Frame de búsqueda de productos
        search_frame = tk.LabelFrame(main_frame, text="Búsqueda de Productos", padx=5, pady=5)
        search_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(search_frame, text="Código de Barras:").grid(row=0, column=0, sticky=tk.W)
        self.barcode_entry = tk.Entry(search_frame, width=20)
        self.barcode_entry.grid(row=0, column=1, padx=5)
        self.barcode_entry.bind("<Return>", lambda e: self.search_product())
        
        tk.Label(search_frame, text="Nombre:").grid(row=0, column=2, sticky=tk.W)
        self.product_name_entry = tk.Entry(search_frame, width=30)
        self.product_name_entry.grid(row=0, column=3, padx=5)
        self.product_name_entry.bind("<Return>", lambda e: self.search_product_by_name())
        
        tk.Button(search_frame, text="Buscar", command=self.search_product).grid(row=0, column=4, padx=5)
        tk.Button(search_frame, text="Escanear", command=self.scan_barcode).grid(row=0, column=5, padx=5)
        
        # Frame de productos encontrados
        products_frame = tk.Frame(main_frame)
        products_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        self.products_tree = ttk.Treeview(products_frame, columns=("ID", "Código", "Nombre", "Precio", "Stock"), show="headings")
        
        self.products_tree.heading("ID", text="ID")
        self.products_tree.heading("Código", text="Código")
        self.products_tree.heading("Nombre", text="Nombre")
        self.products_tree.heading("Precio", text="Precio")
        self.products_tree.heading("Stock", text="Stock")
        
        self.products_tree.column("ID", width=50, anchor=tk.CENTER)
        self.products_tree.column("Código", width=120)
        self.products_tree.column("Nombre", width=250)
        self.products_tree.column("Precio", width=100, anchor=tk.E)
        self.products_tree.column("Stock", width=80, anchor=tk.CENTER)
        
        scrollbar = ttk.Scrollbar(products_frame, orient=tk.VERTICAL, command=self.products_tree.yview)
        self.products_tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.products_tree.pack(fill=tk.BOTH, expand=True)
        
        # Frame de cantidad
        qty_frame = tk.Frame(main_frame)
        qty_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(qty_frame, text="Cantidad:").pack(side=tk.LEFT)
        self.qty_spinbox = tk.Spinbox(qty_frame, from_=1, to=100, width=5)
        self.qty_spinbox.pack(side=tk.LEFT, padx=5)
        tk.Button(qty_frame, text="Agregar a Factura", command=self.add_to_invoice).pack(side=tk.LEFT, padx=5)
        
        # Frame de factura
        invoice_frame = tk.LabelFrame(main_frame, text="Factura", padx=5, pady=5)
        invoice_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        self.invoice_tree = ttk.Treeview(invoice_frame, columns=("ID", "Código", "Nombre", "Cantidad", "Precio", "Subtotal"), show="headings")
        
        self.invoice_tree.heading("ID", text="ID")
        self.invoice_tree.heading("Código", text="Código")
        self.invoice_tree.heading("Nombre", text="Nombre")
        self.invoice_tree.heading("Cantidad", text="Cantidad")
        self.invoice_tree.heading("Precio", text="Precio Unit.")
        self.invoice_tree.heading("Subtotal", text="Subtotal")
        
        self.invoice_tree.column("ID", width=50, anchor=tk.CENTER)
        self.invoice_tree.column("Código", width=120)
        self.invoice_tree.column("Nombre", width=250)
        self.invoice_tree.column("Cantidad", width=80, anchor=tk.CENTER)
        self.invoice_tree.column("Precio", width=100, anchor=tk.E)
        self.invoice_tree.column("Subtotal", width=100, anchor=tk.E)
        
        scrollbar_invoice = ttk.Scrollbar(invoice_frame, orient=tk.VERTICAL, command=self.invoice_tree.yview)
        self.invoice_tree.configure(yscroll=scrollbar_invoice.set)
        scrollbar_invoice.pack(side=tk.RIGHT, fill=tk.Y)
        self.invoice_tree.pack(fill=tk.BOTH, expand=True)
        
        # Frame de totales
        totals_frame = tk.Frame(invoice_frame)
        totals_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(totals_frame, text="Subtotal:").pack(side=tk.LEFT)
        self.subtotal_var = tk.StringVar(value="0.00")
        tk.Label(totals_frame, textvariable=self.subtotal_var).pack(side=tk.LEFT, padx=10)
        
        tk.Label(totals_frame, text="IVA (12%):").pack(side=tk.LEFT)
        self.iva_var = tk.StringVar(value="0.00")
        tk.Label(totals_frame, textvariable=self.iva_var).pack(side=tk.LEFT, padx=10)
        
        tk.Label(totals_frame, text="Total:").pack(side=tk.LEFT)
        self.total_var = tk.StringVar(value="0.00")
        tk.Label(totals_frame, textvariable=self.total_var, font=('Arial', 10, 'bold')).pack(side=tk.LEFT, padx=10)
        
        # Frame de botones
        buttons_frame = tk.Frame(main_frame)
        buttons_frame.pack(fill=tk.X, pady=5)
        
        tk.Button(buttons_frame, text="Eliminar Item", command=self.remove_item).pack(side=tk.LEFT, padx=5)
        tk.Button(buttons_frame, text="Generar Factura", command=self.generate_invoice).pack(side=tk.LEFT, padx=5)
        tk.Button(buttons_frame, text="Cancelar Factura", command=self.cancel_invoice).pack(side=tk.LEFT, padx=5)
        tk.Button(buttons_frame, text="Salir", command=self.root.quit).pack(side=tk.RIGHT, padx=5)
        
        # Menú superior
        menubar = tk.Menu(self.root)
        
        # Menú Archivo
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Gestión de Productos", command=self.open_product_management)
        file_menu.add_separator()
        file_menu.add_command(label="Salir", command=self.root.quit)
        menubar.add_cascade(label="Archivo", menu=file_menu)
        
        self.root.config(menu=menubar)
    
    def search_client(self):
        """Buscar cliente por NIT"""
        nit = self.nit_entry.get()
        if not nit:
            messagebox.showwarning("Advertencia", "Ingrese un NIT para buscar")
            return
        
        # Aquí iría la lógica para buscar el cliente en la base de datos
        # Por ahora simulamos un cliente encontrado
        self.current_client = {
            'nit': nit,
            'nombre': "CLIENTE EJEMPLO",
            'direccion': "DIRECCIÓN EJEMPLO"
        }
        
        self.client_name_entry.delete(0, tk.END)
        self.client_name_entry.insert(0, self.current_client['nombre'])
        self.client_address_entry.delete(0, tk.END)
        self.client_address_entry.insert(0, self.current_client['direccion'])
    
    def new_client(self):
        """Crear nuevo cliente"""
        # Limpiar campos
        self.nit_entry.delete(0, tk.END)
        self.client_name_entry.delete(0, tk.END)
        self.client_address_entry.delete(0, tk.END)
        self.current_client = None
        
        # En una implementación real, aquí se guardaría el nuevo cliente en la BD
        messagebox.showinfo("Información", "Complete los datos del nuevo cliente")
    
    def search_product(self):
        """Buscar producto por código de barras"""
        codigo = self.barcode_entry.get()
        if not codigo:
            messagebox.showwarning("Advertencia", "Ingrese un código de barras")
            return
        
        producto = Producto.get_by_barcode(codigo)
        if producto:
            # Limpiar treeview
            for i in self.products_tree.get_children():
                self.products_tree.delete(i)
            
            # Mostrar producto encontrado
            self.products_tree.insert("", tk.END, values=producto)
        else:
            messagebox.showinfo("Información", "Producto no encontrado")
    
    def search_product_by_name(self):
        """Buscar productos por nombre"""
        nombre = self.product_name_entry.get()
        if not nombre:
            messagebox.showwarning("Advertencia", "Ingrese un nombre para buscar")
            return
        
        # Limpiar treeview
        for i in self.products_tree.get_children():
            self.products_tree.delete(i)
        
        # Buscar productos (simulación)
        productos = [
            (1, "123456789", "PRODUCTO 1", 10.50, 100, "CATEGORIA A"),
            (2, "987654321", "PRODUCTO 2", 15.75, 50, "CATEGORIA B")
        ]
        
        for prod in productos:
            if nombre.lower() in prod[2].lower():
                self.products_tree.insert("", tk.END, values=prod)
    
    def scan_barcode(self):
        """Escanear código de barras"""
        from utils.barcode_reader import read_barcode
        codigo = read_barcode()
        if codigo:
            self.barcode_entry.delete(0, tk.END)
            self.barcode_entry.insert(0, codigo)
            self.search_product()
    
    def add_to_invoice(self):
        """Agregar producto a la factura"""
        selected = self.products_tree.focus()
        if not selected:
            messagebox.showwarning("Advertencia", "Seleccione un producto")
            return
        
        values = self.products_tree.item(selected, "values")
        try:
            cantidad = int(self.qty_spinbox.get())
            if cantidad <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Cantidad debe ser un número entero positivo")
            return
        
        id_producto = values[0]
        codigo = values[1]
        nombre = values[2]
        precio = float(values[3])
        subtotal = precio * cantidad
        
        # Verificar si el producto ya está en la factura
        for item in self.current_invoice_items:
            if item['id_producto'] == id_producto:
                # Actualizar cantidad y subtotal
                item['cantidad'] += cantidad
                item['subtotal'] = item['precio'] * item['cantidad']
                self.update_invoice_display()
                return
        
        # Agregar nuevo item
        self.current_invoice_items.append({
            'id_producto': id_producto,
            'codigo': codigo,
            'nombre': nombre,
            'cantidad': cantidad,
            'precio': precio,
            'subtotal': subtotal
        })
        
        self.update_invoice_display()
    
    def update_invoice_display(self):
        """Actualizar la visualización de la factura"""
        # Limpiar treeview
        for i in self.invoice_tree.get_children():
            self.invoice_tree.delete(i)
        
        # Agregar items
        subtotal = 0
        for item in self.current_invoice_items:
            self.invoice_tree.insert("", tk.END, values=(
                item['id_producto'],
                item['codigo'],
                item['nombre'],
                item['cantidad'],
                f"{item['precio']:.2f}",
                f"{item['subtotal']:.2f}"
            ))
            subtotal += item['subtotal']
        
        # Calcular totales
        iva = subtotal * 0.12
        total = subtotal + iva
        
        self.subtotal_var.set(f"{subtotal:.2f}")
        self.iva_var.set(f"{iva:.2f}")
        self.total_var.set(f"{total:.2f}")
    
    def remove_item(self):
        """Eliminar item seleccionado de la factura"""
        selected = self.invoice_tree.focus()
        if not selected:
            messagebox.showwarning("Advertencia", "Seleccione un item para eliminar")
            return
        
        item_id = self.invoice_tree.item(selected, "values")[0]
        self.current_invoice_items = [item for item in self.current_invoice_items 
                                     if str(item['id_producto']) != item_id]
        self.update_invoice_display()
    
    def generate_invoice(self):
        """Generar la factura"""
        if not self.current_invoice_items:
            messagebox.showwarning("Advertencia", "No hay items en la factura")
            return
        
        if not self.current_client:
            messagebox.showwarning("Advertencia", "Seleccione o registre un cliente")
            return
        
        # Aquí iría la lógica para guardar la factura en la base de datos
        # Por ahora solo mostramos un mensaje
        numero_factura = f"FAC-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
        messagebox.showinfo("Factura Generada", 
                          f"Factura {numero_factura} generada exitosamente\n"
                          f"Cliente: {self.current_client['nombre']}\n"
                          f"Total: {self.total_var.get()}")
        
        self.cancel_invoice()
    
    def cancel_invoice(self):
        """Cancelar la factura actual"""
        self.current_invoice_items = []
        self.update_invoice_display()
        self.subtotal_var.set("0.00")
        self.iva_var.set("0.00")
        self.total_var.set("0.00")
    
    def open_product_management(self):
        """Abrir ventana de gestión de productos"""
        from views.product_view import ProductosView
        top = tk.Toplevel(self.root)
        ProductosView(top)

if __name__ == "__main__":
    root = tk.Tk()
    app = FacturacionView(root)
    root.mainloop()