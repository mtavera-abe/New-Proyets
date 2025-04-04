from database.db_operations import create_database_connection
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

class InventoryManager:
    def __init__(self):
        self.conn = create_database_connection()
        
    def add_product(self, barcode, name, description, price, stock, category):
        try:
            with self.conn.cursor() as cursor:
                sql = """
                INSERT INTO productos 
                (codigo_barras, nombre, descripcion, precio, stock, categoria) 
                VALUES (%s, %s, %s, %s, %s, %s)
                """
                cursor.execute(sql, (barcode, name, description, price, stock, category))
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Error al agregar producto: {e}")
            return False
            
    def update_stock(self, product_id, quantity):
        try:
            with self.conn.cursor() as cursor:
                sql = "UPDATE productos SET stock = stock + %s WHERE id = %s"
                cursor.execute(sql, (quantity, product_id))
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Error al actualizar stock: {e}")
            return False
            
    def get_product_by_barcode(self, barcode):
        try:
            with self.conn.cursor() as cursor:
                sql = "SELECT * FROM productos WHERE codigo_barras = %s"
                cursor.execute(sql, (barcode,))
                return cursor.fetchone()
        except Exception as e:
            print(f"Error al buscar producto: {e}")
            return None
            
    def get_all_products(self):
        try:
            with self.conn.cursor() as cursor:
                sql = "SELECT * FROM productos ORDER BY nombre"
                cursor.execute(sql)
                return cursor.fetchall()
        except Exception as e:
            print(f"Error al obtener productos: {e}")
            return []
            
    def __del__(self):
        if self.conn:
            self.conn.close()