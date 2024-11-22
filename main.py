# main.py
import requests
import pandas as pd
from io import StringIO
from data import baseComponentRetrieval  # Use relative import

from LLM.AIagent import AIAgentManager

def main():
    # Create an instance of the AIAgentManager JUST FOR *TESTING*
    agent_manager = AIAgentManager()

    # Example usage
    print(agent_manager.agent.fetch_web_data())

if __name__ == "__main__":
    main()