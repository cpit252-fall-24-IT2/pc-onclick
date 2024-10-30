class Motherboard:
    def __init__(self,name,price,socket):
        self.name = name
        self.price = price
        self.socket = socket

    def __str__(self):
        return f"Motherboard Name: {self.name}, Price: ${self.price}, Socket: {self.socket}"
