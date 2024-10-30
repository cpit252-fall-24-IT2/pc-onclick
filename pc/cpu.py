class CPU:
    def __init__(self, name, price, core_count):
        self.name = name
        self.price = price
        self.core_count = core_count

    def __str__(self):
        return f"CPU Name: {self.name}, Price: ${self.price}, Core Count: {self.core_count}"