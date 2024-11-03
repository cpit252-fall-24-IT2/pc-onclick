import os
from openai import OpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.llms import OpenAI as LangChainOpenAI

class AIAgent:
    def __init__(self, api_key, base_url):
        self.client = OpenAI(
            api_key=api_key,
            base_url=base_url,
        )
        self.select_component_prompt = PromptTemplate(
            input_variables=["user_input"],
            template="You are a PC component recommendation assistant. Based on the user's budget and preferences, suggest the best component. Only provide the name of the component.\nUser: {user_input}\nAssistant:"
        )
        self.check_compatibility_prompt = PromptTemplate(
            input_variables=["user_input"],
            template="You are a PC component compatibility assistant. Based on the user's selected components, check if they are compatible. Only provide a yes or no answer.\nUser: {user_input}\nAssistant:"
        )
        self.select_component_chain = LLMChain(
            llm=LangChainOpenAI(api_key=api_key),
            prompt=self.select_component_prompt
        )
        self.check_compatibility_chain = LLMChain(
            llm=LangChainOpenAI(api_key=api_key),
            prompt=self.check_compatibility_prompt
        )

    def select_component(self, user_input):
        response = self.select_component_chain.invoke(user_input)
        component_name = response['text'].strip()  # Assuming the response is in the 'text' field
        print(type(component_name))
        return component_name

    def check_compatibility(self, user_input):
        response = self.check_compatibility_chain.invoke(user_input)
        compatibility = response['text'].strip()  # Assuming the response is in the 'text' field
        return compatibility

if __name__ == "__main__":
    api_key = "k"
    base_url = "https://api.x.ai/v1"
    
    agent = AIAgent(api_key, base_url)
    
    user_input = "I want some recommendations for a CPU under $500 from Intel"
    component_name = agent.select_component(user_input)
    print(f"Selected component: {component_name}")
    
    compatibility_input = "Is Intel Core i7-9700K compatible with ASUS ROG Maximus XI Hero?"
    compatibility = agent.check_compatibility(compatibility_input)
    print(f"Compatibility check: {compatibility}")