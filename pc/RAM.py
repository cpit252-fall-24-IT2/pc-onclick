class RAM:
    def __init__(self, name, price, capacity, speed, ram_type: str):
        self.name = name          
        self.price = price       
        self.capacity = capacity  
        self.speed = speed       
        self.ram_type = ram_type  

    def __str__(self):
        return (
            f"RAM Name: {self.name}, Price: ${self.price}, Capacity: {self.capacity},Speed: {self.speed} MHz, Type: {self.ram_type}"
        )