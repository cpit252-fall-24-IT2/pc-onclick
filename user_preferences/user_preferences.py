import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from ..pc.pc import PCBuilder
from ..pc.pc import PC


class UserPreferences:
    def __init__(self):
        self.user_choice = None 
        self.use_case = None
        self.budget = None
        self.build_preferences = {}




    def user_choice_(self):
        print("Welcome to PC ONCLICK!")

        # Step 1: Build Type Selection
        
        self.user_choice = input("\nSelect an option to begin: \n 1. Start New Build  \n 2. View Saved Build \n 3. Exit")




        



# If The user choose to create a new build 

    def get_user_preferences(self):
    
        # Step 1: Build Type Selection
        print("\nWhat type of build would you like to create?")
        print('Gaming \n Content Creation\n General Purpose ')
        print('Or specify what programs you want to run or what the PC will be used for.')
        self.use_case = input("\nPlease describe your needs:")


        # Step 2: Budget Setting
        print("\nDefine Your Budget:")
        self.budget = input("Enter your budget : ")
        

        


#example builds

    def initialize_example_builds(self):
        # Create PC objects for each example build using the PCBuilder class
        gaming_build = PCBuilder().set_cpu("AMD Ryzen 5 5600X", 199, 6).set_gpu("NVIDIA RTX 3060 Ti", 399, "Ampere").set_ram(
            "Corsair Vengeance LPX 16GB DDR4-3200", 79, 16, 3200, "DDR4"
        ).set_storage("Kingston NV2 1TB NVMe SSD", 59, "1TB").set_motherboard(
            "MSI B550 TOMAHAWK", 149, "AM4"
        ).set_psu(
            "EVGA 600W 80+ Bronze", 49, "80+ Bronze", 600, False
        ).build() 

        print(gaming_build) 
        # Store builds as a list of PC objects
        return [gaming_build]



fitcher = UserPreferences()
fitcher.initialize_example_builds()