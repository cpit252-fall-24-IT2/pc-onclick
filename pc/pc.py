from pc.cpu import CPU
from pc.gpu import GPU
from pc.motherboard import Motherboard
from pc.PSU import PSU
from pc.RAM import RAM
from pc.storage import Storage

class PC:
    def __init__(self, cpu=None, gpu=None, motherboard=None, psu=None, ram=None, storage=None):
        self.cpu = cpu
        self.gpu = gpu
        self.motherboard = motherboard
        self.psu = psu
        self.ram = ram
        self.storage = storage

    def __str__(self):
      
        return (
            "\nBased on your use case and budget, here's your recommended build:\n"
            "PC Build Components:\n"
            f"CPU: \n{self.cpu.name} || core_count: {self.cpu.core_count} || Price: ${self.cpu.price:.2f}  \n========================================\n"
            f"GPU: \n{self.gpu.name} || chipset: {self.gpu.chipset} || Price: $ {self.gpu.price:.2f}  \n========================================\n"
            f"RAM: \n{self.ram.name} || capacity: {self.ram.capacity} || speed:{self.ram.speed} || Price: ${self.ram.price:.2f}\n========================================\n"
            f"Storage: \n{self.storage.name} || capacity:{self.storage.capacity} || Price: ${self.storage.price:.2f}\n========================================\n"
            f"Motherboard: \n{self.motherboard.name} || Price: ${self.motherboard.price:.2f}\n========================================\n"
            f"PSU: \n{self.psu.name} || wattage:{self.psu.wattage} || Price: ${self.psu.price:.2f}\n========================================\n"
           
        )

class PCBuilder:
    def __init__(self):
        self.reset()

    def reset(self):
        self._pc = PC()

    def set_cpu(self, name, price, core_count):
        self._pc.cpu = CPU(name, price, core_count)
        return self

    def set_gpu(self, name, price, chipset):
        self._pc.gpu = GPU(name, price, chipset)
        return self

    def set_motherboard(self, name, price, socket):
        self._pc.motherboard = Motherboard(name, price, socket)
        return self

    def set_psu(self, name, price, efficiency, wattage, modular):
        self._pc.psu = PSU(name, price, efficiency, wattage, modular)
        return self

    def set_ram(self, name, price, capacity, speed):
        self._pc.ram = RAM(name, price, capacity, speed)
        return self

    def set_storage(self, name, price, capacity):
        self._pc.storage = Storage(name, price, capacity)
        return self

    def build(self):
        pc = self._pc
        self.reset()  # Prepare builder for a new PC
        return pc
