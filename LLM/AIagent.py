import sys
import os
import json
from abc import ABC, abstractmethod
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from langchain_ollama import OllamaLLM
from langchain.prompts import PromptTemplate
from data.web_data_set import PCComponentFetcher

class BaseAIAgent(ABC):
    def __init__(self):
        super().__init__()  # Call the parent class constructor

    @abstractmethod
    def select_component(self, user_input):
        pass

    @abstractmethod
    def check_compatibility(self, user_input):
        pass

class AIAgent(BaseAIAgent):
    def __init__(self, model_name='llama3.2'):
        self.model_name = model_name  # Initialize model_name
        self.llm = OllamaLLM(model=self.model_name)  # Initialize OllamaLLM

        self.select_component_prompt = PromptTemplate(
            input_variables=["components", "usage"],
            template=(
            "You are a PC component recommendation assistant. Based on the user's intended usage '{usage}', "
            "select the best components from the available options '{components}', ensuring compatibility between them. "
            "Provide (only one name) of the recommended component only, Only return the name, nothing else.."
            )
        )
        self.check_compatibility_prompt = PromptTemplate(
            input_variables=["user_input"],
            template=(
                "You are a PC component compatibility assistant. Based on the user's selected components, "
                "check if they are compatible. Only provide a yes or no answer.\nUser: {user_input}\nAssistant:"
            )
        )
        self.budget_allocation_prompt = PromptTemplate(
            input_variables=["budget", "usage"],
            template=(
                "You are a budget allocation assistant for building a PC. The user has a budget of {budget} and plans to use the PC for {usage}. Based on this information, allocate the budget for each component (CPU, GPU, Motherboard, RAM, Storage, and PSU) and return the budget as a Python dictionary in this exact format:\n\n"
                "\n\n"
                "Only return the dictionary, nothing else."
            )

        )

    def select_component(self, components, usage):
        print(type(components))
        input_data = {"components": components.get('CPU'), "usage": usage}
        prompt = self.select_component_prompt.format(**input_data)
        response = self.llm.invoke(prompt)
        component_name = response.strip()
        return component_name
        
    def check_compatibility(self, user_input):
        prompt = self.check_compatibility_prompt.format(user_input=user_input)
        response = self.llm.invoke(prompt)
        compatibility = response.strip()
        return compatibility

    def budget_allocation(self, budget, usage):
        input_data = {"budget": budget, "usage": usage}
        prompt = self.budget_allocation_prompt.format(**input_data)
        response = self.llm.invoke(prompt)
        try:
            budget_dict = eval(response.strip())  # Convert response to dictionary
        except Exception as e:
            raise ValueError(f"Error parsing budget allocation response: {response}") from e
        print(budget_dict)
        if self.check_budget(budget_dict) == "pass":
            components = self.fetch_component(budget_dict)
            print(self.select_component(components, usage))
        else:
            raise ValueError("Budget allocation check failed")
        return budget_dict  
        
    
    def check_budget(self, budget):
        fetcher = PCComponentFetcher()
        components = ['CPU', 'GPU', 'Motherboard', 'PSU', 'RAM', 'Storage']
        for component in components:
            min_price, max_price = fetcher.get_price_ranges(component)
            component_budget = budget.get(component)
            if component_budget is None or component_budget < min_price or component_budget > max_price:
                return "fail"
        return "pass"

    def fetch_component(self, budget_dict):
        # Create an instance of PCComponentFetcher
        fetcher = PCComponentFetcher()
        
        # Use the instance to call the get_component method
        allocation = budget_dict
        CPU = fetcher.get_component('CPU', allocation.get('CPU'), manufacturer='')
        GPU = fetcher.get_component('GPU', allocation.get('GPU'), manufacturer='')
        motherboard = fetcher.get_component('Motherboard', allocation.get('Motherboard'), manufacturer='')
        PSU = fetcher.get_component('PSU', allocation.get('PSU'), manufacturer='')
        RAM = fetcher.get_component('RAM', allocation.get('RAM'), manufacturer='')
        Storage = fetcher.get_component('Storage', allocation.get('Storage'), manufacturer='')

        components = {
            'CPU': CPU,
            'GPU': GPU,
            'Motherboard': motherboard,
            'PSU': PSU,
            'RAM': RAM,
            'Storage': Storage
        }
        return components

# Create an instance of the AIAgent JUST FOR *TESTING*
agent = AIAgent(model_name='llama3.2')  # Pass the model_name


# Example usage
allocation = agent.budget_allocation(1500, "editing")
print(allocation)
print(f"Type of allocation: {type(allocation)}")

print(f"CPU Allocation: {allocation.get('CPU', 'CPU not found')}")
print(allocation.get('GPU'))