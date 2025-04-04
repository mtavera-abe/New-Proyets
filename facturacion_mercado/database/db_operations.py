import pymysql
from sqlalchemy import create_engine
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

def create_database_connection():
    try:
        connection = pymysql.connect
        host=config['database']['host'],
        user=config['database']['user'],
        password=config['database']['password'],
        database=config['database']['database'],
        port=int(config['database']['port'])
        return connection
    except Exception as e:
        print(f"Error al conectar a la base de datos: {e}")
        return None

def create_tables():
    conn = create_database_connection()
    if conn:
        try:
            with conn.cursor() as cursor:
                # Tabla de productos
                cursor.execute("""
                CREATE TABLE IF NOT EXISTS productos (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    codigo_barras VARCHAR(50) UNIQUE,
                    nombre VARCHAR(100) NOT NULL,
                    descripcion TEXT,
                    precio DECIMAL(10, 2) NOT NULL,
                    stock INT NOT NULL,
                    categoria VARCHAR(50),
                    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
                """)
                
                # Tabla de ventas
                cursor.execute("""
                CREATE TABLE IF NOT EXISTS ventas (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    total DECIMAL(10, 2) NOT NULL,
                    metodo_pago VARCHAR(50),
                    cliente_id INT
                )
                """)
                
                # Tabla de detalles de venta
                cursor.execute("""
                CREATE TABLE IF NOT EXISTS detalle_venta (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    venta_id INT NOT NULL,
                    producto_id INT NOT NULL,
                    cantidad INT NOT NULL,
                    precio_unitario DECIMAL(10, 2) NOT NULL,
                    subtotal DECIMAL(10, 2) NOT NULL,
                    FOREIGN KEY (venta_id) REFERENCES ventas(id),
                    FOREIGN KEY (producto_id) REFERENCES productos(id)
                )
                """)
                
                # Tabla de clientes (opcional)
                cursor.execute("""
                CREATE TABLE IF NOT EXISTS clientes (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    nombre VARCHAR(100) NOT NULL,
                    telefono VARCHAR(20),
                    email VARCHAR(100),
                    direccion TEXT
                )
                """)
                
            conn.commit()
            print("Tablas creadas exitosamente")
        except Exception as e:
            print(f"Error al crear tablas: {e}")
        finally:
            conn.close()

if __name__ == "__main__":
    create_tables()