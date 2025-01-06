from pypresence import Presence
import time
import json
import os
import utils
import requests
import sys


System_URL = "https://presence.archerdev.xyz/"

    

class main:
    def __init__(self):
        self.config = self.main_load()
        self.name = self.config['name']
        self.depts = self.loadable_departments()
        self.chosen_dept = None
        self.client_id = None
        self.RPC = None
        self.invite_link = False
        self.badge_num = None
        self.rank = None
        self.pos_type = None
        self.callsign = None

    def main_load(self):
        utils.clear_screen()
        # get config
        if "config.json" not in os.listdir("data"):
            # Create Config
            # Get Name
            print("Please Enter You're Name")
            name = input("Name: ")
            print("Saving Data")
            with open("data/config.json", "w") as config_raw:
                config_to_load = {
                    "name" : f"{name}"
                }
                json.dump(config_to_load, config_raw)
            
        config_raw = open("data/config.json")
        config = json.load(config_raw)
        return config
    
    def loadable_departments(self):
        depts = requests.get(f"{System_URL}/get_dept")
        load_ = depts.content.decode()

        with open("data/depts.json", "w") as new_:
            new_.write(load_.replace("'", '"'))
        
        try:
            depts = []
            file = open("data/depts.json")
            congif = json.load(file)
            for dept in congif['depts']:
                depts.append(dept)
        except Exception as e:
            print(e)
            sys.exit()
        return depts

    def get_dept_secret(self, choice):
        client = requests.get(f"{System_URL}/presence/{choice}")
        return client
    
    def main(self):
        while True:
            utils.clear_screen()
            print(f"Welcome: {self.name}")
            print("Please Select a Department Below")
            count = 1
            for i in self.depts:
                print(f"{count}. {i}")
                count += 1

            choice = input("Please Select One: ")
            if choice == "DEV":
                print("ENTERING DEV MODE")
                sys.exit()
            self.chosen_dept = int(choice) - 1

            result = self.Init_Dept()

            if result == False:
                self.Init_Dept()
            self.RPC_START()

    def Init_Dept(self):
        utils.clear_screen()
        choice = self.chosen_dept 
        choice_sub = self.depts[choice]
        client = self.get_dept_secret(choice_sub)
        if client == "ERROR":
            print("A Error Occured")
            return sys.exit()
        self.client_id = client.content.decode()
        # Create Client Config
        if f"{choice_sub}DP.json" not in os.listdir("data"):
            print(f"Please Enter Badge Number for the selected department: {choice_sub}")
            self.badge_num = input("Badge Number EXAMPLE: (00010): ")
            if choice_sub == "pbpd":
                self.invite_link = True
            print("Please Enter Your Rank: EXAMPLE: (Chief Of Police):")
            self.rank = input("Rank: ")
            print("Position Type? (HC, LC, Supervisor, Officer, Cadet, ETC):")
            self.pos_type = input("Position Type: ")
            print("Callsign? Example: (1K-01)")
            self.callsign = input("Callsign: ")

            print(f"Setup for {choice_sub} complete!")
            setup = {
                "badge" : f"{self.badge_num}",
                "rank" : f"{self.rank}",
                "post" : f"{self.pos_type}",
                "call" : f"{self.callsign}"
            }
            try:
                with open(f"data/{choice_sub}DP.json", "w") as file_:
                    json.dump(setup, file_)
            except Exception as e:
                print(e)
                sys.exit()
            return True

        with open(f"data/{choice_sub}DP.json", "r") as file_:
            config = json.load(file_)
            self.badge_num = config['badge']
            self.callsign = config['call']
            self.pos_type = config['post']
            self.rank = config['rank']
        current_info = f"{self.name} | {self.callsign} | {self.badge_num} | {self.rank} | {self.pos_type}"
        print(f"{current_info}")
        print(f"Is this correct for {choice_sub}? Y OR N")
        choice_ = input("")
        if choice_.lower() == "n":
            os.remove(f"data/{choice_sub}DP.json")
            return False

        
        else:
            return True

    def RPC_START(self):
        utils.clear_screen()
        choice = self.chosen_dept 
        choice_sub = self.depts[choice]
        print(f"Now Starting Presence for {choice_sub} with the following data: {self.name} | {self.callsign} | {self.badge_num} | {self.rank} | {self.pos_type}")
        try:
            print(self.client_id)
            RPC = Presence(client_id=self.client_id)

            RPC.connect()
            if self.invite_link:
                RPC.update(
                    state=f"{self.rank} | {self.pos_type} | {self.callsign}",
                    details=f"{self.name} | {self.badge_num}",
                    buttons=[{"label" : "Join Paleto Bay?", "url": "https://discord.gg/C9zcgZhH"}],
                    start=time.time()
                )
            else:
                RPC.update(
                    state=f"{self.rank} | {self.pos_type} | {self.callsign}",
                    details=f"{self.name} | {self.badge_num}",
                    start=time.time()
                )
        except Exception as e:
            print("A Fatal Error Occured")
            print(e)
            input("Press Enter To Close")
            sys.exit()

        input("Press Enter To Close Presence System")
        sys.exit()
        
main().main()