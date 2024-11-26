from pydantic import BaseModel, Field, ValidationError
from typing import Dict, Optional, Any
import sys
import os
import json
from abc import ABC, abstractmethod
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from langchain_ollama import OllamaLLM
from langchain.prompts import PromptTemplate
from data.web_data_set import PCComponentFetcher
import ast


# Pydantic Models
class BudgetAllocationInput(BaseModel):
    budget: float
    usage: str


class ComponentSelectionInput(BaseModel):
    components: Dict[str, Any]
    usage: str


class ComponentCompatibilityInput(BaseModel):
    user_input: str


class ComponentOutput(BaseModel):
    CPU: str
    GPU: str
    Motherboard: str
    PSU: str
    RAM: str
    Storage: str


# Abstract Base Class
class BaseAIAgent(ABC):
    @abstractmethod
    def select_component(self, user_input: ComponentSelectionInput) -> ComponentOutput:
        pass

    @abstractmethod
    def check_compatibility(self, user_input: ComponentCompatibilityInput) -> str:
        pass


# Main AIAgent Class
class AIAgent(BaseAIAgent):
    def __init__(self, model_name='llama3.2'):
        self.model_name = model_name
        self.llm = OllamaLLM(model=self.model_name)

        # Define prompts
        self.select_component_prompt = PromptTemplate(
            input_variables=["components", "usage"],
            template=(
                "You are a PC component selection assistant. Based on the user's components {components} and usage {usage}, "
                "select the best component for each category (CPU, GPU, Motherboard, RAM, Storage, and PSU).that are compatible with each other.\n\n"
                "Return the selected components as a Python dictionary in this exact format:\n\n"
                "Only return the dictionary, nothing else."
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
                "Only return the dictionary, nothing else."
            )
        )

    def select_component(self, components: ComponentOutput, usage: str) -> ComponentOutput:
        # Convert ComponentOutput to dictionary for prompt
        components_dict = components.model_dump()
        
        input_data = ComponentSelectionInput(
            components=components_dict,
            usage=usage
        )
        
        prompt = self.select_component_prompt.format(**input_data.dict())
        response = self.llm.invoke(prompt)
        response = response.strip().strip('```python').strip('```')
        try:
            component_dict = ComponentOutput(**ast.literal_eval(response.strip()))
        except Exception as e:
            raise ValueError(f"Invalid component response: {response}") from e
            
        return component_dict

    def check_compatibility(self, user_input: str) -> str:
        input_data = ComponentCompatibilityInput(user_input=user_input)
        prompt = self.check_compatibility_prompt.format(user_input=input_data.user_input)
        response = self.llm.invoke(prompt)
        return response.strip()

    def budget_allocation(self, budget: float, usage: str) -> Dict[str, float]:
        input_data = BudgetAllocationInput(budget=budget, usage=usage)
        prompt = self.budget_allocation_prompt.format(**input_data.dict())
        response = self.llm.invoke(prompt)
        try:
            budget_dict = eval(response.strip())
        except Exception as e:
            raise ValueError(f"Error parsing budget allocation response: {response}") from e
        return budget_dict

    def check_budget(self, budget: Dict[str, float]) -> str:
        fetcher = PCComponentFetcher()
        components = ['CPU', 'GPU', 'Motherboard', 'PSU', 'RAM', 'Storage']
        for component in components:
            min_price, max_price = fetcher.get_price_ranges(component)
            component_budget = budget.get(component)
            if component_budget is None or component_budget < min_price or component_budget > max_price:
                return "fail"
        return "pass"

    def fetch_component(self, budget_dict: Dict[str, float]) -> ComponentOutput:
        fetcher = PCComponentFetcher()
        
        # Get component data and extract first item (name) from each tuple
        components = {
            'CPU': str(fetcher.get_component('CPU', budget_dict['CPU'], manufacturer='')),
            'GPU': str(fetcher.get_component('GPU', budget_dict['GPU'], manufacturer='')),
            'Motherboard': str(fetcher.get_component('Motherboard', budget_dict['Motherboard'], manufacturer='')),
            'PSU': str(fetcher.get_component('PSU', budget_dict['PSU'], manufacturer='')),
            'RAM': str(fetcher.get_component('RAM', budget_dict['RAM'], manufacturer='')),
            'Storage': str(fetcher.get_component('Storage', budget_dict['Storage'], manufacturer=''))
        }
        
        return ComponentOutput(**components)

    def get_full_component_details(self, selected_components: ComponentOutput) -> Dict[str, Dict[str, Any]]:
        fetcher = PCComponentFetcher()
        component_details = {}

        component_details['CPU'] = fetcher.get_component_details('CPU', selected_components.CPU)
        component_details['GPU'] = fetcher.get_component_details('GPU', selected_components.GPU)
        component_details['Motherboard'] = fetcher.get_component_details('Motherboard', selected_components.Motherboard)
        component_details['PSU'] = fetcher.get_component_details('PSU', selected_components.PSU)
        component_details['RAM'] = fetcher.get_component_details('RAM', selected_components.RAM)
        component_details['Storage'] = fetcher.get_component_details('Storage', selected_components.Storage)

        return component_details


# Example usage
agent = AIAgent(model_name='llama3.2')

# Budget Allocation Example
allocation = agent.budget_allocation(1500, "gaming")
print("\n\n\n\n\n\n\n\n")
print(allocation['CPU'])



components = agent.fetch_component(allocation)  
print(components.CPU)
print("\n\n\n\n\n\n\n\n")
X = agent.select_component(components, "gaming")
print(X.CPU)




## only now we need to make code in web_data_set.py so we can get the full information from the CSV files.