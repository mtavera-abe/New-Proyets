class Factura:
    """Clase que representa una factura en el sistema"""
    def __init__(self, numero=None, cliente=None, fecha=None, items=None):
        self.numero = numero
        self.cliente = cliente
        self.fecha = fecha
        self.items = items or []
    
    def agregar_item(self, producto, cantidad, precio):
        # Método para agregar items a la factura
        self.items.append({
            'producto': producto,
            'cantidad': cantidad,
            'precio': precio
        })
    
    def calcular_total(self):
        return sum(item['precio'] * item['cantidad'] for item in self.items)