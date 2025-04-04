import tkinter as tk
from tkinter import ttk, messagebox
from inventory.inventory_manager import InventoryManager
from interface.barcode_scanner import BarcodeScanner
from reports.invoice_generator import generate_invoice

class BillingSystemGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Facturación - Mercado")
        self.root.geometry("1200x800")
        
        self.inventory = InventoryManager()
        self.current_sale = []
        self.setup_ui()
        
    def setup_ui(self):
        # Frame superior para productos
        top_frame = tk.Frame(self.root)
        top_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Lista de productos
        self.products_tree = ttk.Treeview(top_frame, columns=('ID', 'Código', 'Nombre', 'Precio', 'Stock'), show='headings')
        self.products_tree.heading('ID', text='ID')
        self.products_tree.heading('Código', text='Código Barras')
        self.products_tree.heading('Nombre', text='Nombre')
        self.products_tree.heading('Precio', text='Precio')
        self.products_tree.heading('Stock', text='Stock')
        self.products_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(top_frame, orient="vertical", command=self.products_tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.products_tree.configure(yscrollcommand=scrollbar.set)
        
        # Frame inferior para la venta actual
        bottom_frame = tk.Frame(self.root)
        bottom_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Lista de productos en la venta actual
        self.sale_tree = ttk.Treeview(bottom_frame, columns=('ID', 'Nombre', 'Cantidad', 'Precio', 'Subtotal'), show='headings')
        self.sale_tree.heading('ID', text='ID')
        self.sale_tree.heading('Nombre', text='Nombre')
        self.sale_tree.heading('Cantidad', text='Cantidad')
        self.sale_tree.heading('Precio', text='Precio Unit.')
        self.sale_tree.heading('Subtotal', text='Subtotal')
        self.sale_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Frame de controles
        control_frame = tk.Frame(bottom_frame)
        control_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=5)
        
        # Total de la venta
        self.total_var = tk.StringVar(value="$0.00")
        tk.Label(control_frame, text="Total:", font=('Arial', 14)).pack(pady=5)
        tk.Label(control_frame, textvariable=self.total_var, font=('Arial', 16, 'bold')).pack(pady=5)
        
        # Botones
        tk.Button(control_frame, text="Agregar Producto", command=self.add_product_dialog).pack(fill=tk.X, pady=5)
        tk.Button(control_frame, text="Finalizar Venta", command=self.finalize_sale).pack(fill=tk.X, pady=5)
        tk.Button(control_frame, text="Cancelar Venta", command=self.cancel_sale).pack(fill=tk.X, pady=5)
        
        # Barra de búsqueda
        search_frame = tk.Frame(self.root)
        search_frame.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Label(search_frame, text="Buscar:").pack(side=tk.LEFT)
        self.search_entry = tk.Entry(search_frame)
        self.search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        self.search_entry.bind('<KeyRelease>', self.search_products)
        
        # Iniciar escáner de código de barras
        self.barcode_scanner = BarcodeScanner(self.on_barcode_scanned)
        self.barcode_scanner.start_listening()
        
        # Cargar productos
        self.load_products()
        
    def load_products(self):
        for item in self.products_tree.get_children():
            self.products_tree.delete(item)
            
        products = self.inventory.get_all_products()
        for product in products:
            self.products_tree.insert('', tk.END, values=(
                product[0], product[1], product[2], f"${product[4]:.2f}", product[5]
            ))
            
    def search_products(self, event):
        query = self.search_entry.get().lower()
        for item in self.products_tree.get_children():
            product = self.products_tree.item(item, 'values')
            if query in product[2].lower() or query in product[1].lower():
                self.products_tree.selection_set(item)
                self.products_tree.see(item)
                break
                
    def on_barcode_scanned(self, product):
        self.add_to_sale(product)
        
    def add_to_sale(self, product):
        # Buscar si el producto ya está en la venta
        for item in self.sale_tree.get_children():
            item_values = self.sale_tree.item(item, 'values')
            if int(item_values[0]) == product[0]:
                # Actualizar cantidad
                new_quantity = int(item_values[2]) + 1
                subtotal = new_quantity * float(product[4])
                self.sale_tree.item(item, values=(
                    item_values[0], item_values[1], new_quantity, item_values[3], f"${subtotal:.2f}"
                ))
                self.update_total()
                return
                
        # Si no está, agregarlo nuevo
        subtotal = float(product[4])
        self.sale_tree.insert('', tk.END, values=(
            product[0], product[2], 1, f"${float(product[4]):.2f}", f"${subtotal:.2f}"
        ))
        self.update_total()
        
    def update_total(self):
        total = 0.0
        for item in self.sale_tree.get_children():
            subtotal = float(self.sale_tree.item(item, 'values')[4].replace('$', ''))
            total += subtotal
            
        self.total_var.set(f"${total:.2f}")
        
    def finalize_sale(self):
        if not self.sale_tree.get_children():
            messagebox.showwarning("Venta vacía", "No hay productos en la venta actual")
            return
            
        # Aquí iría la lógica para guardar la venta en la base de datos
        # y generar la factura
        
        # Generar factura (simplificado)
        items = []
        for item in self.sale_tree.get_children():
            values = self.sale_tree.item(item, 'values')
            items.append({
                'name': values[1],
                'quantity': values[2],
                'price': values[3],
                'subtotal': values[4]
            })
            
        total = self.total_var.get()
        generate_invoice(items, total)
        
        messagebox.showinfo("Venta completada", f"Venta finalizada con total: {total}")
        self.cancel_sale()
        
    def cancel_sale(self):
        for item in self.sale_tree.get_children():
            self.sale_tree.delete(item)
        self.total_var.set("$0.00")
        
    def add_product_dialog(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Agregar Producto")
        
        tk.Label(dialog, text="Código de Barras:").grid(row=0, column=0, padx=5, pady=5)
        barcode_entry = tk.Entry(dialog)
        barcode_entry.grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(dialog, text="Nombre:").grid(row=1, column=0, padx=5, pady=5)
        name_entry = tk.Entry(dialog)
        name_entry.grid(row=1, column=1, padx=5, pady=5)
        
        tk.Label(dialog, text="Descripción:").grid(row=2, column=0, padx=5, pady=5)
        desc_entry = tk.Entry(dialog)
        desc_entry.grid(row=2, column=1, padx=5, pady=5)
        
        tk.Label(dialog, text="Precio:").grid(row=3, column=0, padx=5, pady=5)
        price_entry = tk.Entry(dialog)
        price_entry.grid(row=3, column=1, padx=5, pady=5)
        
        tk.Label(dialog, text="Stock Inicial:").grid(row=4, column=0, padx=5, pady=5)
        stock_entry = tk.Entry(dialog)
        stock_entry.grid(row=4, column=1, padx=5, pady=5)
        
        tk.Label(dialog, text="Categoría:").grid(row=5, column=0, padx=5, pady=5)
        category_entry = tk.Entry(dialog)
        category_entry.grid(row=5, column=1, padx=5, pady=5)
        
        def save_product():
            try:
                barcode = barcode_entry.get()
                name = name_entry.get()
                description = desc_entry.get()
                price = float(price_entry.get())
                stock = int(stock_entry.get())
                category = category_entry.get()
                
                if self.inventory.add_product(barcode, name, description, price, stock, category):
                    messagebox.showinfo("Éxito", "Producto agregado correctamente")
                    self.load_products()
                    dialog.destroy()
                else:
                    messagebox.showerror("Error", "No se pudo agregar el producto")
            except ValueError:
                messagebox.showerror("Error", "Precio y stock deben ser números válidos")
                
        tk.Button(dialog, text="Guardar", command=save_product).grid(row=6, columnspan=2, pady=10)