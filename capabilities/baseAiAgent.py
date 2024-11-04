from abc import ABC, abstractmethod

class BaseAIAgent(ABC):
    def __init__(self, api_key):
        self.api_key = api_key

    @abstractmethod
    def select_component(self, user_input):
        pass

    @abstractmethod
    def check_compatibility(self, user_input):
        pass
