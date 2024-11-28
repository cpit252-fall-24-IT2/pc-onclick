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
        self.use_case = None
        self.budget = None
        self.build_preferences = {}
        self.agent = AIAgent(model_name='llama3.2')

    def user_choice_(self):
        print("Welcome to PC ONCLICK!")
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
            self.user_choice_()

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
            while not stop_event.is_set() and (time.time() - start_time) < 15:
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
        allocation = self.agent.budget_allocation(self.budget, self.use_case)
        components_dict, components_str = self.agent.fetch_component(allocation)
        selected_components = self.agent.select_component(components_str, self.use_case)
        full_component_details = self.agent.get_full_component_details(selected_components)
        compatibility = self.agent.check_compatibility(full_component_details)

        # Stop loading animation
        stop_event.set()
        loading_thread.join()

        print("\nBased on your use case and budget, here's your recommended build:\n")
        print("💻 Recommended Build:\n")
        print("PC Build Components:\n")
        print(f"CPU: \n{selected_components.CPU} || Price: ${allocation['CPU']:.2f}\n========================================")
        print(f"GPU: \n{selected_components.GPU} || Price: ${allocation['GPU']:.2f}\n========================================")
        print(f"RAM: \n{selected_components.RAM} || Price: ${allocation['RAM']:.2f}\n========================================")
        print(f"Storage: \n{selected_components.Storage} || Price: ${allocation['Storage']:.2f}\n========================================")
        print(f"Motherboard: \n{selected_components.Motherboard} || Price: ${allocation['Motherboard']:.2f}\n========================================")
        print(f"PSU: \n{selected_components.PSU} || Price: ${allocation['PSU']:.2f}\n========================================\n")
        print("Compatibility Check: ", compatibility)

            

    def view_saved_build(self):
        # Implement the logic to view saved builds
        print("Viewing saved builds...")

    def initialize_example_builds(self):
        gaming_build = PCBuilder().set_cpu("AMD Ryzen 5 5600X", 199, 6).set_gpu("NVIDIA RTX 3060 Ti", 399, "Ampere").set_ram(
            "Corsair Vengeance LPX 16GB DDR4-3200", 79, 16, 3200, "DDR4"
        ).set_storage("Kingston NV2 1TB NVMe SSD", 59, "1TB").set_motherboard(
            "MSI B550 TOMAHAWK", 149, "AM4"
        ).set_psu(
            "EVGA 600W 80+ Bronze", 49, "80+ Bronze", 600, False
        ).build() 

        return [gaming_build]

# Example usage
if __name__ == "__main__":
    user_preferences = UserPreferences()
    user_preferences.user_choice_()
