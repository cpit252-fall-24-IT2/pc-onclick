class PSU:
    def __init__(self, name, price, efficiency, wattage, modular):
        self.name = name             
        self.price = price            
        self.efficiency = efficiency   
        self.wattage = wattage         
        self.modular = modular        



    def __str__(self):
        modular_status = "Modular" if self.modular else "Non-Modular"
        return (
            f"Power Supply Name: {self.name}, Price: ${self.price}, Efficiency: {self.efficiency},Wattage: {self.wattage}W, Type: {modular_status}"
        )