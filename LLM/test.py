from langchain_ollama import OllamaLLM
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate
from pydantic import BaseModel, Field
import json

# Step 1: Define the desired data structure using Pydantic
class MoonLandingInfo(BaseModel):
    astronaut: str = Field(description="Name of the astronaut who first landed on the moon")
    year: int = Field(description="Year when the first moon landing occurred")

# Step 2: Set up the output parser
parser = JsonOutputParser(pydantic_object=MoonLandingInfo)

# Step 3: Create a prompt template with format instructions
prompt = PromptTemplate(
    template="Answer the user query.\n{format_instructions}\n{query}\n",
    input_variables=["query"],
    partial_variables={"format_instructions": parser.get_format_instructions()},
)

# Step 4: Initialize the OllamaLLM model
llm = OllamaLLM(model="llama3.2")

# Combine the prompt, model, and parser into a chain
chain = prompt | llm | parser

# Input query
query = "Who was the first man on the moon, and in which year did the landing occur?"

# Invoke the chain with the query
result = chain.invoke({"query": query})

# Output the structured JSON response
print(json.dumps(result, indent=4))
