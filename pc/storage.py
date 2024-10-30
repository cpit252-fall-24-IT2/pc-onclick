class Storage:
    def __init__(self, name: str, price: float,  capacity: str):
        self.name = name              
        self.price = price                   
        self.capacity = capacity       



    def __str__(self):
        return (
            f"Storage Name: {self.name}, Price: ${self.price},  Capacity: {self.capacity}"
        )