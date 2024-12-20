import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from LLM.AIagent import AIAgent
from pc.pc import PCBuilder
from pc.pc import PC
import time
import threading
from User.Memento import Memento

class UserPreferences:
    def __init__(self):
        self.user_choice = None 
        self.budget = None
        self.build_preferences = {}
        self.agent = AIAgent(model_name='llama3.2')
        self.builds = [] 
        self.Memento_list = []  

    def user_choice_(self):
        print("Welcome to PC ONCLICK!")
        while True:
            self.user_choice = input("\nSelect an option to begin: \n 1. Start New Build  \n 2. view saved builds \n 3. Restore Previous Build \n 4. Exit\n> ")
            if self.user_choice == '1':
                self.get_user_preferences()
            elif self.user_choice == '2':
                self.view_saved_build()
            elif self.user_choice == '3':
                if not self.Memento_list:
                 print("\nNo saved Memento found. Returning to the main menu.")
                 continue  

                self.view_saved_pc_states()
                index = int(input("Enter the build number to restore: ")) - 1
                restored_pc =self.restore_pc_state(index)
                print("Restored Build:\n")
                print(restored_pc.__str__())
                self.save_build(restored_pc)  
            elif self.user_choice == '4':
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
            while not stop_event.is_set() and (time.time() - start_time) < 30:
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
        print('"Gaming"\n"Content Creation"\n"General Purpose"')
        print('Or specify what programs you want to run or what the PC will be used for.')
        self.use_case = input("Please describe your needs:\n> ")

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

        



        #--------------------------------- AI Agent Methods ---------------------------------#
        1
        # Stop loading animation
        stop_event.set()
        loading_thread.join()

        print(build.__str__())
        print("Compatibility Check: ", compatibility)
        self.save_build(build)    





        # Ask if the user wants to save the build   
    def save_build(self ,build):
                save_choice = input("\nWould you like to save this build? (yes/no):\n> ")
                if save_choice.lower() == 'yes':
                    self.builds.append(build)  # Save the build to the array
                    print("Build saved in memory.")
                else:
                     # Save the PC object to a memento
                     self.Memento_list.append(build)
                     print("Build not saved.")
    
    # print the saved build for the user
    def view_saved_build(self):
        if not self.builds:
            print("\nNo saved builds found.")
            return None

        print("\nSaved Builds:")
        for i, build in enumerate(self.builds, 1):
            print(f"\nBuild {i}:")
            print(build.__str__())  





        #Memento Methods 
        #---------------------------------------------------------------------------------------
        #---------------------------------------------------------------------------------------
    

        # Save the current state in a memento
    def save_pc_state(self, pc):
        ## Save the current PC object as a memento.
         memento = Memento(pc)
         self.Memento_list.append(memento)
         print("PC build state has been saved.")



        #Restore a PC object from a memento.
    def restore_pc_state(self, index=-1):
        if not self.validate_index(index):
            return None
        
        # Get the memento back form the list
        memento = self.Memento_list[index]
        # Remove the memento from the list
        self.remove_memento(index)
        print(f"Restored and removed PC build at index {index + 1}.")
        return memento

        #Display all saved PC states.
    def view_saved_pc_states(self):
        if not self.validate_List:
            return None


        print("\nSaved PC Builds:")
        for i, memento in enumerate(self.Memento_list, 1):
            previous = Memento(memento)
            pc = previous.get_pc_state()
            print(f"Build {i}:")
            print(pc.__str__())  

    
    def remove_memento(self, index):
        #Remove the memento from the list.
        del self.Memento_list[index]
    
    
       #Validate the index for the memento list. 
    def validate_index(self, index):
     
     if not self.Memento_list:
        print("No saved PC builds to restore.")
        return False

     if index < 0 or index >= len(self.Memento_list):
        print("Invalid index. Please try again.")
        return False

     return True
    
    def validate_List(self):
     
     if not self.Memento_list:
        print("No saved PC builds to restore.")
        return False
     
     return True
        #--------------------------------------------------------------------------------------
        #---------------------------------------------------------------------------------------


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