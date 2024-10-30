class GPU:
    def __init__(self, name, price, chipset):
        self.name = name
        self.price = price
        self.chipset = chipset

    def __str__(self):
        return f"GPU Name: {self.name}, Price: ${self.price}, Chipset: {self.chipset}"