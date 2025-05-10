import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from models.payment import Payment
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

class PaymentView:
    def __init__(self, root, on_close_callback=None):
        self.root = root
        self.on_close_callback = on_close_callback
        self.setup_database()
        self.setup_ui()
        self.load_payments()
    
    def setup_database(self):
        """Configurar la conexión a la base de datos"""
        self.engine = create_engine('sqlite:///payments.db')
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
        Payment.metadata.create_all(self.engine)
    
    def setup_ui(self):
        self.root.title("Sistema de Pagos")
        self.root.geometry("800x600")
        self.root.resizable(False, False)
        
        # Frame principal
        main_frame = tk.Frame(self.root, padx=10, pady=10)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Frame de formulario
        form_frame = tk.LabelFrame(main_frame, text="Información del Pago", padx=5, pady=5)
        form_frame.pack(fill=tk.X, pady=5)
        
        # Campos del formulario
        tk.Label(form_frame, text="Monto:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.amount_entry = tk.Entry(form_frame, width=30)
        self.amount_entry.grid(row=0, column=1, pady=2, padx=5)
        
        tk.Label(form_frame, text="Método de Pago:").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.payment_method = ttk.Combobox(form_frame, values=["Efectivo", "Tarjeta", "Transferencia"], width=27)
        self.payment_method.grid(row=1, column=1, pady=2, padx=5)
        
        tk.Label(form_frame, text="Referencia:").grid(row=2, column=0, sticky=tk.W, pady=2)
        self.reference_entry = tk.Entry(form_frame, width=30)
        self.reference_entry.grid(row=2, column=1, pady=2, padx=5)
        
        tk.Label(form_frame, text="Descripción:").grid(row=3, column=0, sticky=tk.W, pady=2)
        self.description_entry = tk.Entry(form_frame, width=30)
        self.description_entry.grid(row=3, column=1, pady=2, padx=5)
        
        # Botones del formulario
        button_frame = tk.Frame(form_frame)
        button_frame.grid(row=4, column=0, columnspan=2, pady=10)
        
        tk.Button(button_frame, text="Guardar", command=self.save_payment).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Limpiar", command=self.clear_form).pack(side=tk.LEFT, padx=5)
    
        # Treeview para mostrar pagos
        tree_frame = tk.Frame(main_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        self.tree = ttk.Treeview(tree_frame, columns=("ID", "Monto", "Método", "Fecha", "Estado", "Referencia"), show="headings")
        
        # Configurar columnas
        self.tree.heading("ID", text="ID")
        self.tree.heading("Monto", text="Monto")
        self.tree.heading("Método", text="Método")
        self.tree.heading("Fecha", text="Fecha")
        self.tree.heading("Estado", text="Estado")
        self.tree.heading("Referencia", text="Referencia")
        
        self.tree.column("ID", width=50, anchor=tk.CENTER)
        self.tree.column("Monto", width=100, anchor=tk.CENTER)
        self.tree.column("Método", width=100, anchor=tk.CENTER)
        self.tree.column("Fecha", width=150, anchor=tk.CENTER)
        self.tree.column("Estado", width=100, anchor=tk.CENTER)
        self.tree.column("Referencia", width=150, anchor=tk.CENTER)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.pack(fill=tk.BOTH, expand=True)
        
        # Bind para selección
        self.tree.bind("<ButtonRelease-1>", self.on_payment_select)
        
        # Botón de cerrar
        tk.Button(main_frame, text="Cerrar", command=self.on_close).pack(side=tk.RIGHT, pady=5)
    
    def load_payments(self):
        """Cargar pagos en el Treeview"""
        for i in self.tree.get_children():
            self.tree.delete(i)
            
        payments = self.session.query(Payment).all()
        for payment in payments:
            self.tree.insert("", tk.END, values=(
                payment.id,
                f"${payment.amount:.2f}",
                payment.payment_method,
                payment.payment_date.strftime("%Y-%m-%d %H:%M"),
                payment.status,
                payment.reference
            ))
    
    def save_payment(self):
        """Guardar pago en la base de datos"""
        try:
            amount = float(self.amount_entry.get())
            payment_method = self.payment_method.get()
            reference = self.reference_entry.get()
            description = self.description_entry.get()
            
            if not amount or not payment_method:
                messagebox.showerror("Error", "El monto y el método de pago son obligatorios")
                return
            
            payment = Payment(
                amount=amount,
                payment_method=payment_method,
                reference=reference,
                description=description,
                status='completado'
            )
            
            self.session.add(payment)
            self.session.commit()
            
            messagebox.showinfo("Éxito", "Pago registrado correctamente")
            self.load_payments()
            self.clear_form()
            
        except ValueError:
            messagebox.showerror("Error", "El monto debe ser un número válido")
        except Exception as e:
            self.session.rollback()
            messagebox.showerror("Error", f"Error al guardar el pago: {str(e)}")
    
    def clear_form(self):
        """Limpiar el formulario"""
        self.amount_entry.delete(0, tk.END)
        self.payment_method.set('')
        self.reference_entry.delete(0, tk.END)
        self.description_entry.delete(0, tk.END)
    
    def on_payment_select(self, event):
        """Cargar datos del pago seleccionado en el formulario"""
        selected = self.tree.focus()
        if selected:
            values = self.tree.item(selected, "values")
            self.clear_form()
            
            payment = self.session.query(Payment).get(values[0])
            if payment:
                self.amount_entry.insert(0, str(payment.amount))
                self.payment_method.set(payment.payment_method)
                self.reference_entry.insert(0, payment.reference or '')
                self.description_entry.insert(0, payment.description or '')
    
    def on_close(self):
        """Manejar el cierre de la ventana"""
        self.session.close()
        if self.on_close_callback:
            self.on_close_callback()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = PaymentView(root)
    root.mainloop()