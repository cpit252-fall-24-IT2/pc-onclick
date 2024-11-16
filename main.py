# main.py

import sys
from LLM.AIagent import AIAgentManager
from pc.pc import PCBuilder

class Main:
    def __init__(self):
        self.agent_manager = AIAgentManager()
        self.pc_builder = PCBuilder()
        self.saved_build = None
        self.run()

    def run(self):
        while True:
            self.show_main_menu()
            choice = input("> ").strip()
            if choice == '1':
                self.start_new_build()
            elif choice == '2':
                self.view_saved_build()
            elif choice == '3':
                print("Exiting...")
                sys.exit()
            else:
                print("Invalid choice. Please try again.")

    def show_main_menu(self):
        print("Welcome to PC Builder Basic!")
        print("Select an option to begin:")
        print("1. Start New Build")
        print("2. View Saved Build")
        print("3. Exit")

    def start_new_build(self):
        build_type = self.select_build_type()
        budget = self.set_budget()
        self.generate_initial_build(build_type, budget)
        # Implement further customization steps here

    def select_build_type(self):
        print("Choose the type of build:")
        print("1. Gaming")
        print("2. Content Creation")
        print("3. General Purpose")
        choice = input("> ").strip()
        if choice == '1':
            return "Gaming"
        elif choice == '2':
            return "Content Creation"
        elif choice == '3':
            return "General Purpose"
        else:
            print("Invalid choice. Defaulting to General Purpose.")
            return "General Purpose"

    def set_budget(self):
        print("Enter your budget (press Enter to skip):")
        budget_input = input("> ").strip()
        if budget_input == '':
            return None
        try:
            budget = float(budget_input)
            return budget
        except ValueError:
            print("Invalid budget input. Skipping budget.")
            return None

    def generate_initial_build(self, build_type, budget):
        # Use the AI agent to get recommendations based on build type and budget
        user_input = f"I want to build a {build_type} PC with a budget of ${budget if budget else 'no limit'}."
        recommended_components = self.agent_manager.agent.select_component(user_input)
        # Use PCBuilder to construct the PC with recommended components
        # self.pc_builder.set_cpu(...)
        # self.pc_builder.set_gpu(...)
        # Implement the component setting logic here
        print("Generated initial build based on recommendations.")

    def view_saved_build(self):
        if self.saved_build:
            print("Here is your saved build:")
            print(self.saved_build)
        else:
            print("No saved build found.")

if __name__ == "__main__":
    Main()