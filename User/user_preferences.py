import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from LLM.AIagent import AIAgent
from pc.pc import PCBuilder
from pc.pc import PC
import time
import threading

class UserPreferences:
    def __init__(self):
        self.user_choice = None 
        self.budget = None
        self.build_preferences = {}
        self.agent = AIAgent(model_name='llama3.2')
        #TODO     self.saved_builds = []

    def user_choice_(self):
        print("Welcome to PC ONCLICK!")
        while True:
            self.user_choice = input("\nSelect an option to begin: \n 1. Start New Build  \n 2. View Saved Build \n 3. Exit\n> ")
            if self.user_choice == '1':
                self.get_user_preferences()
            elif self.user_choice == '2':
                self.view_saved_build()
            elif self.user_choice == '3':
                print("Exiting...")
                sys.exit()
            else:
                print("Invalid choice. Please try again.")

    def loading_animation(self, stop_event):
        # Unicode spinner characters for smooth animation
        spinner = ["[   ]", "[=  ]", "[== ]", "[===]", "[ ==]", "[  =]", "[   ]"]
        # ANSI color codes
        colors = [
            '\033[20m',      # Green
            '\033[92m',      # Light Green
            '\033[1;32m',    # Bold Green
            '\033[0;32m',    # Dark Green
            '\033[2;32m',    # Dim Green
            '\033[38;5;34m'  # Custom Green
        ]
        color_reset = '\033[0m'
        i = 0
        start_time = time.time()

        try:
            while not stop_event.is_set() and (time.time() - start_time) < 35:
                color = colors[i % len(colors)]
                frame = spinner[i % len(spinner)]
                print(f"\r{color}Loading {frame}{color_reset}", end="", flush=True)
                time.sleep(0.1)
                i += 1
        except Exception as e:
            print(f"\nAn error occurred: {e}")
        
        # Clear the line when done
        print("\r", end="", flush=True)

    def get_user_preferences(self):
        print("\nWhat type of build would you like to create?")
        print('Gaming\nContent Creation\nGeneral Purpose')
        print('Or specify what programs you want to run or what the PC will be used for.')
        self.use_case = input("\nPlease describe your needs:\n> ")

        self.budget = float(input("Enter your budget:\n> "))

        # Start loading animation
        stop_event = threading.Event()
        loading_thread = threading.Thread(target=self.loading_animation, args=(stop_event,))
        loading_thread.start()

        # Call AIAgent methods
        #--------------------------------- AI Agent Methods ---------------------------------#
        # Allocate budget
        allocation = self.agent.budget_allocation(self.budget, self.use_case)
        # Fetch components
        components_dict, components_str = self.agent.fetch_component(allocation)
        # Select components
        selected_components = self.agent.select_component(components_str, self.use_case)
        # Get details
        full_component_details = self.agent.get_full_component_details(selected_components)
        # Check compatibility
        compatibility = self.agent.check_compatibility(full_component_details)
        # Build PC
        parts_details = self.agent.get_full_component_details(selected_components)
        build = self.building(parts_details)
        #TODO self.save_build(build)
        #--------------------------------- AI Agent Methods ---------------------------------#
        
        # Stop loading animation
        stop_event.set()
        loading_thread.join()

        print("\nBased on your use case and budget, here's your recommended build:\n")
        print(build.__str__())
        print("Compatibility Check: ", compatibility)

        # Ask if the user wants to save the build   
        def save_build():
                save_choice = input("Would you like to save this build? (yes/no):\n> ")
                if save_choice.lower() == 'yes':
                    with open('saved_builds.txt', 'a') as file:
                        file.write(build.__str__() + '\n')
                        print("Build saved to 'saved_builds.txt'.")
                else:
                    print("Build not saved.")
                 
    def building(self,parts):
        gaming_build = PCBuilder().set_cpu(
            parts['CPU']['name'], parts['CPU']['price'], parts['CPU']['core_count']
        ).set_gpu(
            parts['GPU']['name'], parts['GPU']['price'], parts['GPU']['chipset']
        ).set_ram(
            parts['RAM']['name'], parts['RAM']['price'], parts['RAM']['speed'], parts['RAM']['speed']).set_storage(
            parts['Storage']['name'], parts['Storage']['price'], parts['Storage']['capacity']
        ).set_motherboard(
            parts['Motherboard']['name'], parts['Motherboard']['price'], parts['Motherboard']['socket']
        ).set_psu(
            parts['PSU']['name'], parts['PSU']['price'], parts['PSU']['efficiency'], parts['PSU']['wattage'], parts['PSU']['modular']
        ).build()

        return gaming_build


# Example usage
if __name__ == "__main__":
    user_preferences = UserPreferences()
    user_preferences.user_choice_()
