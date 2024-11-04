import os
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.llms import OpenAI as LangChainOpenAI
from baseAiAgent import BaseAIAgent
from baseAiAgent import AgentManager
from dotenv import load_dotenv, find_dotenv


class AIAgentManager(AgentManager):
    # Implement the load_api_key method

    def __init__(self, env_dir='LLM', env_file='.env', api_key_var='OPENAI_API_KEY'):
        self.dotenv_path = os.path.join(os.getcwd(), env_dir, env_file)
        self.api_key_var = api_key_var
        self.api_key = self.load_api_key()
        self.agent = self.initialize_agent()

    def load_api_key(self):
        # Load the API key from the .env file
        load_dotenv(self.dotenv_path)
        api_key = os.getenv(self.api_key_var)
        if not api_key:
            raise ValueError(f"API key not found. Please set the {self.api_key_var} environment variable.")
        return api_key

    def initialize_agent(self):
        # Initialize the AI agent with the API key
        return AIAgent(api_key=self.api_key)




class AIAgent(BaseAIAgent):
    # Implement the select_component and check_compatibility methods
    def __init__(self, api_key ):
        super().__init__(api_key)
        self.llm = LangChainOpenAI(api_key=api_key)

        self.select_component_prompt = PromptTemplate(
            input_variables=["user_input"],
            template="You are a PC component recommendation assistant. Based on the user's budget and preferences, suggest the best component. Only provide the name of the component.\nUser: {user_input}\nAssistant:"
        )
        self.select_component_chain = LLMChain(
            llm=self.llm,
            prompt=self.select_component_prompt
        )
        self.check_compatibility_prompt = PromptTemplate(
            input_variables=["user_input"],
            template="You are a PC component compatibility assistant. Based on the user's selected components, check if they are compatible. Only provide a yes or no answer.\nUser: {user_input}\nAssistant:"
        )
        self.check_compatibility_chain = LLMChain(
            llm=self.llm,
            prompt=self.check_compatibility_prompt
        )
    def select_component(self, user_input):
        response = self.select_component_chain.invoke(user_input)
        component_name = response['text'].strip()
        return component_name

    def check_compatibility(self, user_input):
        response = self.check_compatibility_chain.invoke(user_input)
        compatibility = response['text'].strip()
        return compatibility










# Create an instance of the AIAgentManager JUST FOR *TESTING*
agent_manager = AIAgentManager()

# Example user inputs
component_input = "I have a budget of $150 for a graphics card."
compatibility_input = "I have selected a GTX 1660 and a Ryzen 5 CPU. Are they compatible?"

# Interact with the agent
selected_component = agent_manager.agent.select_component(component_input)
compatibility = agent_manager.agent.check_compatibility(compatibility_input)

# Output the results
print(f"Selected Component: {selected_component}")
print(f"Compatibility: {compatibility}")
