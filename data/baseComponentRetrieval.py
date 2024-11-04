from abc import ABC, abstractmethod

class baseComponentRetrieval(ABC):
    @abstractmethod
    def get_best_options(self, url, budget=None, manufacturer=None, columns=None):
        pass

    @abstractmethod
    def get_component(self, component_type, budget, manufacturer):
        pass