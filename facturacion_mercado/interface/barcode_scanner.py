import keyboard
from inventory.inventory_manager import InventoryManager

class BarcodeScanner:
    def __init__(self, on_barcode_scanned):
        self.barcode = ""
        self.on_barcode_scanned = on_barcode_scanned
        self.inventory = InventoryManager()
        
    def start_listening(self):
        keyboard.on_press(self._on_key_press)
        
    def stop_listening(self):
        keyboard.unhook_all()
        
    def _on_key_press(self, event):
        if event.name == 'enter':
            self._process_barcode()
        elif event.name.isdigit() or event.name in ['-', '.']:
            self.barcode += event.name
            
    def _process_barcode(self):
        if len(self.barcode) > 3:  # Mínimo 4 caracteres para ser un código válido
            product = self.inventory.get_product_by_barcode(self.barcode)
            if product:
                self.on_barcode_scanned(product)
            else:
                print(f"Producto no encontrado con código: {self.barcode}")
        self.barcode = ""