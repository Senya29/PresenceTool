from pypresence import Presence
import time
import json
import os
import utils
import requests
import sys


System_URL = "https://presence.archerdev.xyz/"

VERSION = 2.2

GITAccessToken = "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"

class update():
    def __init__(self):
        self.current_version = VERSION  # Ensure VERSION is defined elsewhere in your code
        self.latest_version_url = "https://raw.githubusercontent.com/Senya29/PBPDRelease/release/version.txt"
        self.update_url = "https://raw.githubusercontent.com/Senya29/PBPDRelease/release/main.py"
        self.headers = {
            'Authorization': f'Bearer {GITAccessToken}'
        }

    def check_for_update(self):
        try:
            # Request the latest version
            latest_version_response = requests.get(self.latest_version_url, headers=self.headers)
            
            # Check if the request was successful
            if latest_version_response.status_code == 200:
                # Get the version number from the response content
                latest_version = latest_version_response.content.decode().strip()

                try:
                    # Try to convert the version string to a float
                    latest_version = float(latest_version)

                    if latest_version > self.current_version:
                        print("Update Available!")
                        print("Downloading Update")
                        time.sleep(2)
                        self.download_update()
                    else:
                        print("No Update Available")
                        time.sleep(2)
                except ValueError:
                    # If the version string is not a valid number, handle it gracefully
                    print(f"Error: Invalid version format received: {latest_version}")
                    input("Press Enter To Continue")
            else:
                # If the request was not successful, print the error message
                print(f"Error: Failed to fetch version. HTTP status code: {latest_version_response.status_code}")
                print(f"Response: {latest_version_response.text}")
                input("Press Enter To Continue")
        except Exception as e:
            print(e)
            print("Failed to check for update")
            input("Press Enter To Continue")

    def download_update(self):
        try:
            # Request the update file (main.py)
            update = requests.get(self.update_url, headers=self.headers)
            
            # Check if the response is valid
            if update.status_code == 200:
                with open("main.py", "w") as file:
                    file.write(update.content.decode())
                print("Update Complete")
                time.sleep(2)
                os.execl("start.bat", "start.bat")  # Assuming start.bat is in the correct directory
                sys.exit()
            else:
                print("Failed to download update. HTTP status code:", update.status_code)
                input("Press Enter To Continue")
                sys.exit()
        except Exception as e:
            print(e)
            print("Failed to download update")
            input("Press Enter To Continue")
            sys.exit()

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
            print(f"Welcome to the Presence System Version: {VERSION}")
            print(f"Name: {self.name}")
            print(f"Avaliable Presences: {len(self.depts)}")
            print("Please Select a Option")
            print("1. Select Department")
            print("2. Change My Name")
            print("3. Options")
            print("4. Exit")
            choice = input("Please Select One: ")
            if choice == "1":
                self.select_department_run()
            elif choice == "2":
                print("Please Enter You're Name")
                name = input("Name: ")
                print("Saving Data")
                with open("data/config.json", "w") as config_raw:
                    config_to_load = {
                        "name" : f"{name}"
                    }
                    json.dump(config_to_load, config_raw)
                self.name = name
            elif choice == "3":
                options(self.name).main()
            elif choice == "4":
                sys.exit()
            else:
                print("Invalid Choice")
                input("Press Enter To Continue")

    def select_department_run(self):
        while True:
            utils.clear_screen()
            print(f"Welcome: {self.name}")
            print("Please Select a Department Below | EXIT To Return to Main Menu")
            count = 1
            for i in self.depts:
                print(f"{count}. {i}")
                count += 1

            choice = input("Please Select One: ")
            if choice.lower() == "exit":
                return
            
            if choice.isdigit() == False:
                print("Invalid Choice")
                input("Press Enter To Continue")
            self.chosen_dept = int(choice) - 1

            result = self.Init_Dept()

            if result == False:
                self.Init_Dept()
            self.RPC_START()
            return

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
        RPC.close()



class options:
    def __init__(self, name):
        self.name = name
    
    def main(self, main_class: main):
        while True:
            utils.clear_screen()
            print(f"Welcome to the Options Menu {self.name}")
            print("Please Select a Option")
            print("1. Update")
            print("2. Factory Reset")
            print("3. Join ADC Discord")
            print("4. Reload Departments")
            print("5. Exit")
            choice = input("Please Select One: ")
            if choice == "1":
                print("Passing Update, and installing latest version")
                update().download_update()
                sys.exit()
            elif choice == "2":
                self.factory_reset()
            elif choice == "3":
                print("Opening ADC Discord")
                os.system("start https://discord.gg/Wvs8TuBUBE")
            elif choice == "4":
                main_class.depts = main_class.loadable_departments()
                print("Reloaded Departments")
                time.sleep(2)
            elif choice == "5":
                return
            else:
                print("Invalid Choice")
                input("Press Enter To Continue")
    
    def factory_reset(self):
        for file in os.listdir("data"):
            os.remove(f"data/{file}")
        print("Factory Reset Complete")
        time.sleep(2)
        os.execl("start.bat", "start.bat")  # Assuming start.bat is in the correct directory
        sys.exit()
        

update().check_for_update()
main().main()
