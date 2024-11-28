from pydantic import BaseModel, Field, ValidationError
from typing import Dict, Optional, Any
import logging

import sys
import os
import json
from abc import ABC, abstractmethod
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from langchain.llms import Ollama
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
    components: str


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
        self.llm = Ollama(model=self.model_name)

        # Define prompts
        self.select_component_prompt = PromptTemplate(
            input_variables=["components", "usage"],
            template=(
            """**Respond only with a Python dictionary format in this exact format:** no there text, nothing else. Your Role is to select PC components. Based on the user's components {components} and usage {usage}, 
            select the best component for each category in components that are compatible with each other.\n\n
            {{
                "CPU": "name",
                "GPU": "name",
                "Motherboard": "name",
                "PSU": "name",
                "RAM": "name",
                "Storage": "name"
            }}
            """
            )
        )

        self.check_compatibility_prompt = PromptTemplate(
            input_variables=["components"],
            template=(
            "You are a PC component compatibility assistant. Based on the user's selected components provided in the following JSON format:\n"
            "{components}\n"
            "Check if the components are compatible. Respond with 'yes' if they are compatible, otherwise respond with 'no'."
            )
        )

        self.budget_allocation_prompt = PromptTemplate(
            input_variables=["budget", "usage"],
            template=(
            "As a PC expert, you are tasked with allocating a budget of: ${budget} \nfor a PC used for {usage}."
            "Split the budget {budget} for a PC used for {usage}."
            "Return a Python dictionary in this format:\n\n- **Respond only with a Python dictionary in this exact format:**"
            "{{\n"
            "    'CPU': amount,\n"
            "    'GPU': amount,\n"
            "    'Motherboard': amount,\n"
            "    'RAM': amount,\n"
            "    'Storage': amount,\n"
            "    'PSU': amount\n"
            "}}\n"
            "Only return the dictionary."
            )
        )

    def select_component(self, components: ComponentOutput, usage: str) -> ComponentOutput:
        # Convert ComponentOutput to dictionary for prompt
        # Removed unused variable components_dict
        
        input_data = ComponentSelectionInput(
            components={
                "CPU": components.CPU,
                "GPU": components.GPU,
                "Motherboard": components.Motherboard,
                "PSU": components.PSU,
                "RAM": components.RAM,
                "Storage": components.Storage
            },
            usage=usage
        )
        
        prompt = self.select_component_prompt.format(**input_data.model_dump())
        response = self.llm.invoke(prompt)
        print(response)
        response = response.strip().strip('```python').strip('```')
        try:
            component_dict = ComponentOutput(**json.loads(response))
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid component response: {response}") from e
            
        return component_dict

    def check_compatibility(self, components: ComponentOutput) -> str:
        # Convert ComponentOutput to JSON string for prompt
        input_data = ComponentCompatibilityInput(components=json.dumps(components.model_dump()))
        prompt = self.check_compatibility_prompt.format(**input_data.model_dump())
        response = self.llm.invoke(prompt)
        return response.strip()

    def budget_allocation(self, budget: float, usage: str) -> Dict[str, float]:
        input_data = BudgetAllocationInput(budget=budget, usage=usage)
        prompt = self.budget_allocation_prompt.format(**input_data.model_dump())
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
        components_str = {
            'CPU': str(fetcher.get_component('CPU', budget_dict['CPU'], manufacturer='')),
            'GPU': str(fetcher.get_component('GPU', budget_dict['GPU'], manufacturer='')),
            'Motherboard': str(fetcher.get_component('Motherboard', budget_dict['Motherboard'], manufacturer='')),
            'PSU': str(fetcher.get_component('PSU', budget_dict['PSU'], manufacturer='')),
            'RAM': str(fetcher.get_component('RAM', budget_dict['RAM'], manufacturer='')),
            'Storage': str(fetcher.get_component('Storage', budget_dict['Storage'], manufacturer=''))
        }
        components_dict = {
            'CPU': fetcher.get_component('CPU', budget_dict['CPU'], manufacturer='')[0],
            'GPU': fetcher.get_component('GPU', budget_dict['GPU'], manufacturer='')[0],
            'Motherboard': fetcher.get_component('Motherboard', budget_dict['Motherboard'], manufacturer='')[0],
            'PSU': fetcher.get_component('PSU', budget_dict['PSU'], manufacturer='')[0],
            'RAM': fetcher.get_component('RAM', budget_dict['RAM'], manufacturer='')[0],
            'Storage': fetcher.get_component('Storage', budget_dict['Storage'], manufacturer='')[0]
        }
        
        return components_dict ,ComponentOutput(**components_str)
        

    def get_full_component_details(self, component_dict: ComponentOutput) -> Dict[str, Dict[str, Any]]:
        fetcher = PCComponentFetcher()
        component_details = {}

        # Iterate over the attributes of component_dict
        for component_type in component_dict.__annotations__.keys():
            component_name = getattr(component_dict, component_type)
            try:
                component_details[component_type] = fetcher.get_component_details(component_type, component_name)
            except ValueError as e:
                logging.error(f"Error fetching details for {component_type}: {e}")
                component_details[component_type] = None  # or handle it as needed

        return component_details

# Test

# Example usage
agent = AIAgent(model_name='llama3.2')

# Budget Allocation Example
allocation = agent.budget_allocation(1500, "gaming")
print("\n\n")
print(allocation['CPU'])

component_dict, components_str = agent.fetch_component(allocation)
print(type(components_str.GPU))
print(type(components_str))
print(components_str.GPU)
print(components_str.CPU)
print("\n\n")
X = agent.select_component(components_str, "gaming")

print(agent.check_compatibility(components_str))
print(X.GPU)
components_str = X  # Use the entire object, not just the CPU attribute
components = agent.get_full_component_details(components_str)

print(agent.check_compatibility(components))
print(type(components))

print(components['CPU'])
print("\n\n")
print(components['GPU'])
print("\n\n")
print(components['Motherboard'])
print("\n\n")
print(components['PSU'])
print("\n\n")
print(components['RAM'])
print("\n\n")
print(components['Storage'])




## only now we need to make code in web_data_set.py so we can get the full information from the CSV files.