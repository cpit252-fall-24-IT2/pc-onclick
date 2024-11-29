class RAM:
    def __init__(self, name, price, capacity, speed: str):
        self.name = name          
        self.price = price       
        self.capacity = capacity  
        self.speed = speed        

    def __str__(self):
        return (
            f"RAM Name: {self.name}, Price: ${self.price}, Capacity: {self.capacity},Speed: {self.speed} MHz"
        )