# this is a test file to test the model
from langchain_ollama import OllamaLLM

llm = OllamaLLM(model="llama3.2")

response = llm.invoke("The first man on the moon was ...")
print(response)