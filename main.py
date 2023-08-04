# --------------------------------------------------------------------------------------------------------------------------------------------------------------
# Imports
import cProfile
import ctypes
import os
import platform
import time
import webbrowser
import psutil
import win32com.client
import wmi
from colorama import init

ctypes.windll.kernel32.SetConsoleTitleW("PyDmidecode By Yup")
c = wmi.WMI()
init()
# --------------------------------------------------------------------------------------------------------------------------------------------------------------
# BIOS INFO
def get_bios_info():
    bios_info = {}
    wmi = win32com.client.GetObject("winmgmts:\\\\.\\root\\cimv2")
    for bios in wmi.ExecQuery("SELECT * FROM Win32_BIOS"):
        bios_info["Manufacturer"] = bios.Manufacturer
        bios_info["Name"] = bios.Name
        bios_info["Version"] = bios.Version
        bios_info["SerialNumber"] = bios.SerialNumber
        bios_info["Description"] = bios.Description
    return bios_info
# --------------------------------------------------------------------------------------------------------------------------------------------------------------
# OS INFO
def get_os_info():
    os_info = {}
    wmi = win32com.client.GetObject("winmgmts:\\\\.\\root\\cimv2")
    for os in wmi.ExecQuery("SELECT * FROM Win32_OperatingSystem"):
        os_info["Caption"] = os.Caption,
        os_info["Version"] = os.Version,
        os_info["Architecture"] = os.OSArchitecture,
        os_info["RegisteredOwner"] = os.RegisteredUser,
        os_info["RegisteredOrganization"] = os.Organization
        os_info["InstallDate"] = os.InstallDate
        os_info["LastBootUpTime"] = os.LastBootUpTime
    return os_info
# --------------------------------------------------------------------------------------------------------------------------------------------------------------
print("")
# --------------------------------------------------------------------------------------------------------------------------------------------------------------
# CPU INFO
def get_processor_info():
    processor_info = []
    wmi = win32com.client.GetObject("winmgmts:\\\\.\\root\\cimv2")

    for processor in wmi.ExecQuery("SELECT * FROM Win32_Processor"):
        processor_info.append({
            "Name": processor.Name,
            "Manufacturer": processor.Manufacturer,
            "Description": processor.Description,
            "Max Clock Speed": processor.MaxClockSpeed,
            "Number Of Cores": processor.NumberOfCores,
            "Number Of Logical Processors": processor.NumberOfLogicalProcessors
        })

    return processor_info
# --------------------------------------------------------------------------------------------------------------------------------------------------------------
print("")
# --------------------------------------------------------------------------------------------------------------------------------------------------------------
# GPU INFO
def get_gpu_info():
    gpu_info = []
    wmi = win32com.client.GetObject("winmgmts:\\\\.\\root\\cimv2")

    for gpu in wmi.ExecQuery("SELECT * FROM Win32_VideoController"):
        gpu_info.append({
            "Name": gpu.Name,
            "AdapterRAM": gpu.AdapterRAM,
            "DriverVersion": gpu.DriverVersion,
            "VideoModeDescription": gpu.VideoModeDescription,
            "PNPDeviceID": gpu.PNPDeviceID,
        })

    return gpu_info
# --------------------------------------------------------------------------------------------------------------------------------------------------------------
print("")
# --------------------------------------------------------------------------------------------------------------------------------------------------------------
# RAM INFO
def get_ram_info():
    ram_info = []
    wmi = win32com.client.GetObject("winmgmts:\\\\.\\root\\cimv2")

    for ram in wmi.ExecQuery("SELECT * FROM Win32_PhysicalMemory"):
        ram_info.append({
            "DeviceLocator": ram.DeviceLocator,
            "Capacity": int(ram.Capacity) // (1024 ** 3),  # Bytes to GB
            "Manufacturer": ram.Manufacturer,
            "PartNumber": ram.PartNumber,
            "SerialNumber": ram.SerialNumber,
        })
    return ram_info
# --------------------------------------------------------------------------------------------------------------------------------------------------------------
print("")
# --------------------------------------------------------------------------------------------------------------------------------------------------------------
# MOTHERBOARD INFO
def get_motherboard_info():
    motherboard_info = {}
    wmi = win32com.client.GetObject("winmgmts:\\\\.\\root\\cimv2")

    for board in wmi.ExecQuery("SELECT * FROM Win32_Baseboard"):
        motherboard_info["Manufacturer"] = board.Manufacturer
        motherboard_info["Product"] = board.Product
        motherboard_info["Version"] = board.Version
        motherboard_info["SerialNumber"] = board.Serialnumber
        motherboard_info["Caption"] = board.Caption

    return motherboard_info
# --------------------------------------------------------------------------------------------------------------------------------------------------------------
print("")
# --------------------------------------------------------------------------------------------------------------------------------------------------------------
# STORAGE INFO
def get_storage_info():
    storage_info = []
    wmi = win32com.client.GetObject("winmgmts:\\\\.\\root\\cimv2")

    for drive in wmi.ExecQuery("SELECT * FROM Win32_DiskDrive"):
        storage_info.append({
            "Model": drive.model,
            "InterfaceType": drive.InterfaceType,
            "Capacity": int(drive.Size) // (1024 ** 3),  # Bytes to GB
            "SerialNumber": drive.SerialNumber
        })
    return storage_info
# --------------------------------------------------------------------------------------------------------------------------------------------------------------
# NETWORK ADAPTER INFO
def get_network_adapter_info():
    network_adapter_info = []
    wmi = win32com.client.GetObject("winmgmts:\\\\.\\root\\cimv2")

    for adapter in wmi.ExecQuery("SELECT * FROM Win32_NetworkAdapter WHERE PhysicalAdapter=True"):
        adapter_config = wmi.ExecQuery(
            f"SELECT IPAddress FROM Win32_NetworkAdapterConfiguration WHERE MACAddress='{adapter.MACAddress}'")
        ip_address = adapter_config[0].IPAddress[0] if adapter_config and adapter_config[0].IPAddress else "N/A"

        network_adapter_info.append({
            "Name": adapter.Name,
            "MACAddress": adapter.MACAddress,
            "AdapterType": adapter.AdapterType,
            "Speed": adapter.Speed,
            "IPAddress": ip_address if hasattr(adapter, "IPAddress") else "N/A",
        })
    return network_adapter_info
print("")
# --------------------------------------------------------------------------------------------------------------------------------------------------------------
print("")
# --------------------------------------------------------------------------------------------------------------------------------------------------------------
# SOUND DEVICE INFO
def get_sound_device_info():
    sound_device_info = []
    wmi = win32com.client.GetObject("winmgmts:\\\\.\\root\\cimv2")

    for sound_device in wmi.ExecQuery("SELECT * FROM Win32_SoundDevice"):
        try:
            pnp_entities = wmi.ExecQuery(
                f"ASSOCIATORS OF {{Win32_SoundDevice.DeviceID='{sound_device.DeviceID}'}} WHERE AssocClass = Win32_PnPEntity")
            driver_version = pnp_entities[0].DriverVersion if pnp_entities else "N/A"
        except IndexError:
            driver_version = "N/A"

        sound_device_info.append({
            "Name": sound_device.Caption,
            "Manufacturer": sound_device.Manufacturer,
            "DriverVersion": driver_version,
        })
    return sound_device_info
# --------------------------------------------------------------------------------------------------------------------------------------------------------------
print("")
# --------------------------------------------------------------------------------------------------------------------------------------------------------------
# SCREEN INFO
def get_monitor_info():
    monitor_info = []
    wmi = win32com.client.GetObject("winmgmts:\\\\.\\root\\cimv2")

    for monitor in wmi.ExecQuery("SELECT * FROM Win32_DesktopMonitor"):
        try:
            refresh_rate = monitor.CurrentRefreshRate
        except AttributeError:
            refresh_rate = "N/A"

        try:

            pnp_entities = wmi.ExecQuery(
                f"ASSOCIATORS OF {{Win32_DesktopMonitor.DeviceID='{monitor.DeviceID}'}} WHERE AssocClass = Win32_PnPEntity")
            manufacturer = pnp_entities[0].Manufacturer if pnp_entities else "N/A"
        except IndexError:
            manufacturer = "N/A"

        monitor_info.append({
            "Name": monitor.Caption,
            "Manufacturer": manufacturer,
            "ScreenHeight": monitor.ScreenHeight,
            "ScreenWidth": monitor.ScreenWidth,
            "MonitorType": monitor.MonitorType,
            "RefreshRate": refresh_rate,
        })

    return monitor_info
# --------------------------------------------------------------------------------------------------------------------------------------------------------------
print("")
# --------------------------------------------------------------------------------------------------------------------------------------------------------------
# Function to print the ASCII art as credits
def print_credits():
    os.system("cls" if os.name == "nt" else "clear")  # Clear the screen
    print(r'''
 ____  __ __  ___    ___ ___  ____  ___      ___    __   ___   ___      ___  
|    \|  |  ||   \  |   |   ||    ||   \    /  _]  /  ] /   \ |   \    /  _] 
|  o  )  |  ||    \ | _   _ | |  | |    \  /  [_  /  / |     ||    \  /  [_  
|   _/|  ~  ||  D  ||  \_/  | |  | |  D  ||    _]/  /  |  O  ||  D  ||    _] 
|  |  |___, ||     ||   |   | |  | |     ||   [_/   \_ |     ||     ||   [_  
|  |  |     ||     ||   |   | |  | |     ||     \     ||     ||     ||     | 
|__|  |____/ |_____||___|___||____||_____||_____|\____| \___/ |_____||_____| 



 _____  _____  _____  _____  _____  _____  _____  _____  _____  _____  _____ 
|     ||     ||     ||     ||     ||     ||     ||     ||     ||     ||     |
|_____||_____||_____||_____||_____||_____||_____||_____||_____||_____||_____|



  ____  __ __  ______  __ __   ___   ____           __ __  __ __  ____       
 /    ||  |  ||      ||  |  | /   \ |    \  __     |  |  ||  |  ||    \      
|  o  ||  |  ||      ||  |  ||     ||  D  )|  |    |  |  ||  |  ||  o  )     
|     ||  |  ||_|  |_||  _  ||  O  ||    / |__|    |  ~  ||  |  ||   _/      
|  _  ||  :  |  |  |  |  |  ||     ||    \  __     |___, ||  :  ||  |        
|  |  ||     |  |  |  |  |  ||     ||  .  \|  |    |     ||     ||  |        
|__|__| \__,_|  |__|  |__|__| \___/ |__|\_||__|    |____/  \__,_||__|        


''')
# *START SCREEN*
def start_screen():
    os.system("cls" if platform.system() == "Windows" else "clear")  # Clear the screen
    print("______     ______           _     _                    _       ")
    print("| ___ \\    |  _  \\         (_)   | |                  | |      ")
    print("| |_/ /   _| | | |_ __ ___  _  __| | ___  ___ ___   __| | ___  ")
    print("|  __/ | | | | | | '_ ` _ \\| |/ _` |/ _ \\/ __/ _ \\ / _` |/ _ \\ ")
    print("| |  | |_| | |/ /| | | | | | | (_| |  __/ (_| (_) | (_| |  __/ ")
    print("\\_|   \\__, |___/ |_| |_| |_|_|\\__,_|\\___|\\___\\___/ \\__,_|\\___| ")
    print("       __/ |                                                   ")
    print("      |___/                                                    ")
    print("__________________________________________________________________________")
    print("|                                                                        |")
    print("|   1. Extract All Info                                                  |")
    print("|   2. Specific Info                                                     |")
    print("|   3. Github                                                            |")
    print("|   4. View Credits                                                      |")
    print("|   5. Settings                                                          |")
    print("|   6. Help                                                              |")
    print("|   7. Exit                                                              |")
    print("|________________________________________________________________________|")

def show_credits():
    os.system("cls" if os.name == "nt" else "clear")  # Clear the screen
    print("____________________________________________________________________________")
    print("| Credits:                                                                 |")
    print("|                                                                          |")
    print("|                                                                          |")
    print("| Created by Yup/https://github.com/Hiiiyup                              |")
    print("|__________________________________________________________________________|")

def help_screen():
    os.system("cls" if platform.system() == "Windows" else "clear")  # Clear the screen
    print("______     ______           _     _                    _       ")
    print("| ___ \\    |  _  \\         (_)   | |                  | |      ")
    print("| |_/ /   _| | | |_ __ ___  _  __| | ___  ___ ___   __| | ___  ")
    print("|  __/ | | | | | | '_ ` _ \\| |/ _` |/ _ \\/ __/ _ \\ / _` |/ _ \\ ")
    print("| |  | |_| | |/ /| | | | | | | (_| |  __/ (_| (_) | (_| |  __/ ")
    print("\\_|   \\__, |___/ |_| |_| |_|_|\\__,_|\\___|\\___\\___/ \\__,_|\\___| ")
    print("       __/ |                                                   ")
    print("      |___/                                                    ")
    print("____________________________________________________________________________")
    print("| 1. \033[1mExtract All Info\033[0m                                                      |")
    print("|    - Extract All Info From Both Your PC Components And Bios.             |")
    print("| 2. \033[1mSpecific Info:\033[0m                                                        |")
    print("|    - Extract Info From A Specific Chosen Component                       |")
    print("| 3. \033[1mGithub\033[0m                                                                |")
    print("|    - Take A Look At The Github Repository                                |")
    print("| 4. \033[1mView Credits\033[0m                                                          |")
    print("|    - Hmm I Wonder Who Wrote All Of This?                                 |")
    print("| 5. \033[1mSettings\033[0m                                                              |")
    print("|    - Specific Settings That Only Some People Need                        |")
    print("| 6. \033[1mHelp\033[0m                                                                  |")
    print("|    - You Know What This Does Since You're Here!                          |")
    print("| 7. \033[1mExit\033[0m                                                                  |")
    print("|    - Way better then ALT+F4 right?                                       |")
    print("|__________________________________________________________________________|")

def component_info_menu():
    while True:
        os.system("cls" if os.name == "nt" else "clear")
        print("______     ______           _     _                    _       ")
        print("| ___ \\    |  _  \\         (_)   | |                  | |      ")
        print("| |_/ /   _| | | |_ __ ___  _  __| | ___  ___ ___   __| | ___  ")
        print("|  __/ | | | | | | '_ ` _ \\| |/ _` |/ _ \\/ __/ _ \\ / _` |/ _ \\ ")
        print("| |  | |_| | |/ /| | | | | | | (_| |  __/ (_| (_) | (_| |  __/ ")
        print("\\_|   \\__, |___/ |_| |_| |_|_|\\__,_|\\___|\\___\\___/ \\__,_|\\___| ")
        print("       __/ |                                                   ")
        print("      |___/                                                    ")
        print("_________________________________________")
        print("| Component Info Menu:                  |")
        print("|                                       |")
        print("|   1. View CPU Information             |")
        print("|   2. View GPU Information             |")
        print("|   3. View RAM Information             |")
        print("|   4. View Motherboard Information     |")
        print("|   5. View Storage Information         |")
        print("|   6. View Network Adapter Information |")
        print("|   7. View Sound Device Information    |")
        print("|   8. View Monitor Information         |")
        print("|   9. Back to Main Menu                |")
        print("|_______________________________________|")

        choice = input("Enter your choice: ")

        if choice == "1":
            print("\033[4m\033[1mCPU Information\033[0m\033[0m")
            processor_info = get_processor_info()
            for index, processor in enumerate(processor_info, start=1):
                print(f"Processor {index}:")
                for key, value in processor.items():
                    print(f"{key}: {value}")
            input("Press Enter to continue...")

        elif choice == "2":
            print("\033[4m\033[1mGPU Information\033[0m\033[0m")
            gpu_info = get_gpu_info()
            for index, gpu in enumerate(gpu_info, start=1):
                print(f"GPU {index}:")
                for key, value in gpu.items():
                    print(f"{key}: {value}")
            input("Press Enter to continue...")

        elif choice == "3":
            print("\033[4m\033[1mRAM Information\033[0m\033[0m")
            ram_info = get_ram_info()
            for index, ram in enumerate(ram_info, start=1):
                print(f"RAM Stick {index}:")
                for key, value in ram.items():
                    print(f"{key}: {value} GB")
            input("Press Enter to continue...")

        elif choice == "4":
            print("\033[4m\033[1mMotherboard Information\033[0m\033[0m")
            motherboard_info = get_motherboard_info()
            for key, value in motherboard_info.items():
                print(f"{key}: {value}")
            input("Press Enter to continue...")

        elif choice == "5":
            print("\033[4m\033[1mStorage Information\033[0m\033[0m")
            storage_info = get_storage_info()
            for index, storage in enumerate(storage_info, start=1):
                print(f"Disk {index}:")
                for key, value in storage.items():
                    print(f"{key}: {value} GB")
            input("Press Enter to continue...")

        elif choice == "6":
            print("\033[4m\033[1mNetwork Adapter Information\033[0m\033[0m")
            network_adapter_info = get_network_adapter_info()
            for index, adapter in enumerate(network_adapter_info, start=1):
                print(f"Network Adapter {index}:")
                for key, value in adapter.items():
                    print(f"{key}: {value}")
            input("Press Enter to continue...")

        elif choice == "7":
            print("\033[4m\033[1mSound Device Information\033[0m\033[0m")
            sound_device_info = get_sound_device_info()
            for index, sound_device in enumerate(sound_device_info, start=1):
                print(f"Sound Device {index}:")
                for key, value in sound_device.items():
                    print(f"{key}: {value}")
            input("Press Enter to continue...")

        elif choice == "8":
            print("\033[4m\033[1mMonitor Information\033[0m\033[0m")
            monitor_info = get_monitor_info()
            for index, monitor in enumerate(monitor_info, start=1):
                print(f"Monitor {index}:")
                for key, value in monitor.items():
                    print(f"{key}: {value}")
            input("Press Enter to continue...")

        elif choice == "9":
            return  # Return to the main menu

        else:
            print("Invalid choice. Please try again.")

def get_battery_info():
    battery = psutil.sensors_battery()
    if battery is None:
        return None

    battery_info = {
        "Percentage": battery.percent,
        "Status": "Charging" if battery.power_plugged else "Discharging",
    }
    return battery_info


def format_data(data, level=0):
    indentation = "\t" * level
    formatted_data = ""
    for key, value in data.items():
        if isinstance(value, dict):
            formatted_data += f"{indentation}{key}:\n"
            formatted_data += format_data(value, level + 1)
        elif isinstance(value, list):
            formatted_data += f"{indentation}{key}:\n"
            for item in value:
                formatted_data += format_data(item, level + 2)
        else:
            formatted_data += f"{indentation}{key}: {value}\n"
    return formatted_data

def export_data(data):
    if not export_data_setting:
        print("Export data setting is disabled.")
        return

    elif export_data_setting == True:
        formatted_data = format_data(data)
        with open("hardware_info.txt", "w") as txt_file:
            txt_file.write(formatted_data)
        print("Hardware Information has been exported to hardware_info.txt")


def gather_hardware_info(laptop_mode):
    hardware_info = {}

    # Gather all the hardware information into the hardware_info dictionary
    hardware_info["BIOS Information"] = get_bios_info()
    hardware_info["OS Information"] = get_os_info()
    hardware_info["CPU Information"] = get_processor_info()
    hardware_info["GPU Information"] = get_gpu_info()
    hardware_info["RAM Information"] = get_ram_info()
    hardware_info["Motherboard Information"] = get_motherboard_info()
    hardware_info["Storage Information"] = get_storage_info()
    hardware_info["Network Adapter Information"] = get_network_adapter_info()
    hardware_info["Sound Device Information"] = get_sound_device_info()
    hardware_info["Monitor Information"] = get_monitor_info()
    if laptop_mode:
        hardware_info["Battery Information"] = get_battery_info()

    return hardware_info


def main_menu():
    global github_repo_opened
    global export_data_setting
    global laptop_mode  # Add this line to use the global variable

    program_state = "menu"
    export_data_setting = False
    laptop_mode = False
    hardware_info = None

    while True:
        if program_state == "menu":
            start_screen()
            choice = input("Enter your choice: ")

            if choice == "1":
                hardware_info = gather_hardware_info(laptop_mode)
                program_state = "running"
                if export_data_setting:
                    export_data(hardware_info)
            elif choice == "2":
                program_state = "component_info_menu"
            elif choice == "3":
                program_state = "github"
            elif choice == "4":
                program_state = "credits"
            elif choice == "5":
                program_state = "settings"
            elif choice == "6":
                program_state = "help"
            elif choice == "7":
                print("Goodbye!")
                time.sleep(1)  # Add a 5-second delay
                os._exit(0)  # Forcefully exit the Python process
            else:
                print("Invalid choice. Please try again.")

        elif program_state == "settings":
            os.system("cls" if os.name == "nt" else "clear")
            print("____________________________________")
            print("|            Settings:             |")
            print("|                                  |")
            print(f"|    1. Enable Laptop Mode  {'[X]' if laptop_mode else '[ ]'}    |")
            print(f"|    2. Enable Export Data  {'[X]' if export_data_setting else '[ ]'}    |")
            print("|    3. Back to Main Menu          |")
            print("|__________________________________|")

            settings_choice = input("Enter your choice: ")

            if settings_choice == "1":
                laptop_mode = not laptop_mode  # Toggle laptop mode on/off
                print("Laptop Mode has been", "enabled." if laptop_mode else "disabled.")
                time.sleep(1)

            elif settings_choice == "2":
                export_data_setting = not export_data_setting
                print("Export Data has been", "enabled." if export_data_setting else "disabled.")
                time.sleep(1)


            elif settings_choice == "3":
                program_state = "menu"

            else:
                print("Invalid choice. Please try again.")


        elif program_state == "credits":
            print_credits()
            input("Press Enter to continue...")
            program_state = "menu"


        elif program_state == "help":
            help_screen()
            input("Press Enter to continue...")
            program_state = "menu"

        elif program_state == "running":
            os.system("cls" if os.name == "nt" else "clear")
            # Calls functions to retrieve hardware information
            program_state = "menu"
            bios_info = get_bios_info()
            processor_info = get_processor_info()
            gpu_info = get_gpu_info()
            ram_info = get_ram_info()
            motherboard_info = get_motherboard_info()
            storage_info = get_storage_info()
            network_adapter_info = get_network_adapter_info()
            os_info = get_os_info()
            sound_device_info = get_sound_device_info()
            monitor_info = get_monitor_info()
            battery_info = get_battery_info() if laptop_mode else None
            # Display the gathered hardware information here
            # ...
            # PRINT BIOS INFO
            print("______     ______           _     _                    _       ")
            print("| ___ \\    |  _  \\         (_)   | |                  | |      ")
            print("| |_/ /   _| | | |_ __ ___  _  __| | ___  ___ ___   __| | ___  ")
            print("|  __/ | | | | | | '_ ` _ \\| |/ _` |/ _ \\/ __/ _ \\ / _` |/ _ \\ ")
            print("| |  | |_| | |/ /| | | | | | | (_| |  __/ (_| (_) | (_| |  __/ ")
            print("\\_|   \\__, |___/ |_| |_| |_|_|\\__,_|\\___|\\___\\___/ \\__,_|\\___| ")
            print("       __/ |                                                   ")
            print("      |___/                                                    ")
            print("___________________________________________________________________________________________________")
            print("___________________________________________________________________________________________________")
            print("\033[4m\033[1mBIOS Information\033[0m\033[0m")
            for key, value in bios_info.items():
                print(f"{key}: {value}")
            print("___________________________________________________________________________________________________")

            # PRINT OS INFO
            print("___________________________________________________________________________________________________")
            print("\033[4m\033[1mOS Information\033[0m\033[0m")
            for key, value in os_info.items():
                print(f"{key}: {value}")
            print("___________________________________________________________________________________________________")

            # PRINT CPU Info
            print("___________________________________________________________________________________________________")
            print("\033[4m\033[1mCPU Information\033[0m\033[0m")
            for index, processor in enumerate(processor_info, start=1):
                print(f"Processor {index}:")
                for key, value in processor.items():
                    print(f"{key}: {value}")
            print("___________________________________________________________________________________________________")

            # PRINT GPU INFO
            print("___________________________________________________________________________________________________")
            print("\033[4m\033[1mCPU Information\033[0m\033[0m")
            for index, processor in enumerate(processor_info, start=1):
                print(f"Processor {index}:")
                for key, value in processor.items():
                    print(f"{key}: {value}")
            print("___________________________________________________________________________________________________")
            # PRINT RAM INFO
            print("___________________________________________________________________________________________________")
            print("\033[4m\033[1mRam Information\033[0m\033[0m")
            for index, ram in enumerate(ram_info, start=1):
                print(f"Ram Stick, {index}:")
                for key, value in ram.items():
                    print(f"{key}: {value}")
            print("___________________________________________________________________________________________________")

            # PRINT MOTHERBOARD INFO
            print("___________________________________________________________________________________________________")
            print("\033[4m\033[1mMotherboard Information:\033[0m\033[0m")
            for key, value in motherboard_info.items():
                print(f"{key}: {value}")
            print("___________________________________________________________________________________________________")

            # PRINT STORAGE INFO
            print("___________________________________________________________________________________________________")
            print("\033[4m\033[1mStorage Information\033[0m\033[0m")
            for index, storage in enumerate(storage_info, start=1):
                print(f"Disk {index}")
                for key, value in storage.items():
                    print(f"{key}: {value}")
            print("___________________________________________________________________________________________________")

            # PRINT ADAPTER INFO
            print("___________________________________________________________________________________________________")
            print("\033[4m\033[1mNetwork Adapters Information\033[0m\033[0m")
            for index, adapter in enumerate(network_adapter_info, start=1):
                print(f"Network Adapter {index}:")
                for key, value in adapter.items():
                    print(f"{key}: {value}")
            print("___________________________________________________________________________________________________")

            # PRINT SOUND DEVICE INFO
            print("___________________________________________________________________________________________________")
            print("\033[4m\033[1mSound Device Information\033[0m\033[0m")
            for index, sound_device in enumerate(sound_device_info, start=1):
                print(f"Sound Device {index}:")
                for key, value in sound_device.items():
                    print(f"{key}: {value}")
            print("___________________________________________________________________________________________________")

            # PRINT MONITOR INFO
            print("___________________________________________________________________________________________________")
            print("\033[4m\033[1mMonitor Information\033[0m\033[0m")
            for index, monitor in enumerate(monitor_info, start=1):
                print(f"Monitor {index}:")
                for key, value in monitor.items():
                    print(f"{key}: {value}")
            print("___________________________________________________________________________________________________")
            print("___________________________________________________________________________________________________")
            print("")

            if laptop_mode and battery_info is not None:
                print(f"Battery Percentage: {battery_info['Percentage']}%")
                print(f"Battery Status: {battery_info['Status']}")

            input("Press Enter to continue...")
            program_state = "menu"


        elif program_state == "github":
            open_github_repo()
            program_state = "menu"

        elif program_state == "component_info_menu":
            component_info_menu()
            program_state = "menu"

        elif program_state == "credits":
            show_credits()
            input("Press Enter to continue...")
            program_state = "menu"


github_repo_opened = False
def open_github_repo():
    repo_url = "https://github.com/Hiiiyup/PyDmidecode"
    webbrowser.open(repo_url)
    github_repo_opened = True

if __name__ == "__main__":
    cProfile.run("main_menu()")