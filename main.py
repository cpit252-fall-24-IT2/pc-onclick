# main.py
import requests
import pandas as pd
from io import StringIO
from data.web_data_set import baseComponentRetrieval  # Use relative import

from user_preferences.user_preferences import UserPreferences

def main():
    # Create an instance of the AIAgentManager JUST FOR *TESTING*

    user = UserPreferences()
    user.user_choice_()
    # Example usage
1
if __name__ == "__main__":
    main()