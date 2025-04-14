import cv2
from pyzbar import pyzbar
import tkinter as tk
from tkinter import messagebox

def read_barcode():
    """
    Leer código de barras desde la cámara
    Retorna el código leído o None si no se leyó nada
    """
    # Configurar la cámara
    cap = cv2.VideoCapture(0)
    cap.set(3, 640)  # Ancho
    cap.set(4, 480)  # Alto
    
    barcode_detected = None
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        # Buscar códigos de barras en el frame
        barcodes = pyzbar.decode(frame)
        
        for barcode in barcodes:
            # Extraer datos y tipo del código de barras
            barcode_data = barcode.data.decode("utf-8")
            barcode_type = barcode.type
            
            # Dibujar rectángulo y texto en el frame
            (x, y, w, h) = barcode.rect
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(frame, f"{barcode_type}: {barcode_data}", (x, y - 10), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            
            barcode_detected = barcode_data
        
        # Mostrar el frame
        cv2.imshow("Lector de Código de Barras - Presione 'q' para salir", frame)
        
        # Salir si se presiona 'q' o se detecta un código
        if cv2.waitKey(1) & 0xFF == ord('q') or barcode_detected is not None:
            break
    
    # Liberar recursos
    cap.release()
    cv2.destroyAllWindows()
    
    return barcode_detected

class BarcodeReaderApp:
    """Aplicación simple para leer códigos de barras"""
    def __init__(self, root):
        self.root = root
        self.root.title("Lector de Código de Barras")
        
        tk.Label(root, text="Presione el botón para escanear un código de barras").pack(pady=10)
        tk.Button(root, text="Escanear", command=self.scan).pack(pady=5)
        
        self.result_var = tk.StringVar()
        tk.Label(root, text="Resultado:").pack()
        tk.Entry(root, textvariable=self.result_var, state='readonly', width=30).pack(pady=10)
        
        tk.Button(root, text="Cerrar", command=root.quit).pack(pady=5)
    
    def scan(self):
        code = read_barcode()
        if code:
            self.result_var.set(code)
        else:
            messagebox.showinfo("Información", "No se detectó ningún código de barras")

if __name__ == "__main__":
    root = tk.Tk()
    app = BarcodeReaderApp(root)
    root.mainloop()