from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.llms import OpenAI as LangChainOpenAI
from baseAiAgent import BaseAIAgent

class AIAgent(BaseAIAgent):
    def __init__(self, api_key, base_url):
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
