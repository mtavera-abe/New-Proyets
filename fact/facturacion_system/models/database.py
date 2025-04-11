import sqlite3
from sqlite3 import Error

class Database:
    def __init__(self):
        self.connection = sqlite3.connect('facturacion.db3')
        self.create_tables()
    
    def create_tables(self):
        # Código para crear tablas
        pass

def create_connection(db_file):
    """Crear una conexión a la base de datos SQLite"""
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(f"Conexión exitosa a SQLite ({db_file})")
        return conn
    except Error as e:
        print(e)
    
    return conn

def create_tables(conn):
    """Crear tablas necesarias en la base de datos"""
    try:
        c = conn.cursor()
        
        # Tabla de productos
        c.execute('''CREATE TABLE IF NOT EXISTS productos (
                     id INTEGER PRIMARY KEY AUTOINCREMENT,
                     codigo_barras TEXT UNIQUE,
                     nombre TEXT NOT NULL,
                     descripcion TEXT,
                     precio REAL NOT NULL,
                     stock INTEGER NOT NULL,
                     categoria TEXT,
                     fecha_creacion TEXT DEFAULT CURRENT_TIMESTAMP
                     )''')
        
        # Tabla de clientes
        c.execute('''CREATE TABLE IF NOT EXISTS clientes (
                     id INTEGER PRIMARY KEY AUTOINCREMENT,
                     nombre TEXT NOT NULL,
                     nit TEXT,
                     direccion TEXT,
                     telefono TEXT,
                     email TEXT,
                     fecha_registro TEXT DEFAULT CURRENT_TIMESTAMP
                     )''')
        
        # Tabla de facturas
        c.execute('''CREATE TABLE IF NOT EXISTS facturas (
                     id INTEGER PRIMARY KEY AUTOINCREMENT,
                     numero_factura TEXT UNIQUE NOT NULL,
                     cliente_id INTEGER,
                     fecha TEXT DEFAULT CURRENT_TIMESTAMP,
                     subtotal REAL NOT NULL,
                     iva REAL NOT NULL,
                     total REAL NOT NULL,
                     estado TEXT DEFAULT 'PENDIENTE',
                     FOREIGN KEY (cliente_id) REFERENCES clientes (id)
                     )''')
        
        # Tabla de detalles de factura
        c.execute('''CREATE TABLE IF NOT EXISTS detalles_factura (
                     id INTEGER PRIMARY KEY AUTOINCREMENT,
                     factura_id INTEGER NOT NULL,
                     producto_id INTEGER NOT NULL,
                     cantidad INTEGER NOT NULL,
                     precio_unitario REAL NOT NULL,
                     subtotal REAL NOT NULL,
                     FOREIGN KEY (factura_id) REFERENCES facturas (id),
                     FOREIGN KEY (producto_id) REFERENCES productos (id)
                     )''')
        
        conn.commit()
        print("Tablas creadas exitosamente")
    except Error as e:
        print(e)

def initialize_database():
    """Inicializar la base de datos"""
    database = "data/facturacion.db"
    conn = create_connection(database)
    
    if conn is not None:
        create_tables(conn)
        conn.close()
    else:
        print("Error al conectar con la base de datos")

if __name__ == '__main__':
    initialize_database()