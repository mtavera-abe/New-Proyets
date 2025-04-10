from models.database import create_connection
from datetime import datetime

class Producto:
    def __init__(self, codigo_barras, nombre, descripcion, precio, stock, categoria=None):
        self.codigo_barras = codigo_barras
        self.nombre = nombre
        self.descripcion = descripcion
        self.precio = precio
        self.stock = stock
        self.categoria = categoria
    
    def save(self):
        """Guardar producto en la base de datos"""
        conn = create_connection("data/facturacion.db")
        sql = '''INSERT INTO productos(codigo_barras, nombre, descripcion, precio, stock, categoria)
                 VALUES(?,?,?,?,?,?)'''
        try:
            cur = conn.cursor()
            cur.execute(sql, (self.codigo_barras, self.nombre, self.descripcion, 
                             self.precio, self.stock, self.categoria))
            conn.commit()
            return cur.lastrowid
        except Exception as e:
            print(f"Error al guardar producto: {e}")
            return None
        finally:
            conn.close()
    
    @staticmethod
    def get_all():
        """Obtener todos los productos"""
        conn = create_connection("data/facturacion.db")
        sql = "SELECT * FROM productos ORDER BY nombre"
        try:
            cur = conn.cursor()
            cur.execute(sql)
            rows = cur.fetchall()
            return rows
        except Exception as e:
            print(f"Error al obtener productos: {e}")
            return []
        finally:
            conn.close()
    
    @staticmethod
    def get_by_barcode(codigo_barras):
        """Obtener producto por código de barras"""
        conn = create_connection("data/facturacion.db")
        sql = "SELECT * FROM productos WHERE codigo_barras = ?"
        try:
            cur = conn.cursor()
            cur.execute(sql, (codigo_barras,))
            row = cur.fetchone()
            return row
        except Exception as e:
            print(f"Error al buscar producto: {e}")
            return None
        finally:
            conn.close()
    
    @staticmethod
    def update_stock(id_producto, cantidad):
        """Actualizar el stock de un producto"""
        conn = create_connection("data/facturacion.db")
        sql = "UPDATE productos SET stock = stock - ? WHERE id = ?"
        try:
            cur = conn.cursor()
            cur.execute(sql, (cantidad, id_producto))
            conn.commit()
            return True
        except Exception as e:
            print(f"Error al actualizar stock: {e}")
            return False
        finally:
            conn.close()