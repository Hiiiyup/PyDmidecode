
# PyDmidecode

---
a Python-Based Windows 10 tool designed to extract detailed information about the hardware components and BIOS of the machine


## Features

---
- View BIOS Information
- View OS Information
- View CPU Information
- View GPU Information
- View RAM Information
- View Motherboard Information
- View Storage Information
- View Network Adapter Information
- View Sound Device Information
- View Monitor Information
- Laptop Mode - Optionally view Battery Information

## Prerequisites

---
Before running PyDmidecode, ensure you have the following software installed:

1. Python (recommended version: 3.6+)
2. Colorama (Python package)
3. Psutil (Python package)
4. WMI (Python package)
5. Ctypes (Python package)
6. Win32com.client (Python package)
7. CPUInfo (Python package)


You can install the required Python packages using pip:

```bash
pip install colorama psutil wmi cpuinfo
```

## Usage

---
To run PyDmidecode, simply execute the script from the command line:

```bash
python main.py
```

Upon launching, you will be presented with a main menu with several options:

1. **Extract All Info**: Gather and display all hardware information about your computer.
2. **Specific Info**: Extract information from a specific chosen component.
3. **GitHub**: Open the GitHub repository 
4. **View Credits**: See credits for the creator of this tool.
5. **Settings**: Access settings to enable Laptop Mode or Data Export.
6. **Help**: Display the help screen to learn more about the options.
7. **Exit**: Terminate the program.

## Options

---
### Specific Info

When selecting "Specific Info" from the main menu, you will have the option to view detailed information for the following components:

- CPU
- GPU
- RAM
- Motherboard
- Storage
- Network Adapter
- Sound Device
- Monitor

### Laptop Mode

Laptop Mode enables the display of battery information, such as percentage and status (charging or discharging). To enable or disable Laptop Mode, navigate to "Settings" in the main menu.

### Data Export

PyDmidecode provides the option to export hardware information to a text file. By default, this feature is disabled. To enable data export, navigate to "Settings" in the main menu.

## Credits

---

PyDmidecode is created and maintained by Yup ([GitHub](https://github.com/Hiiiyup)). 

## Disclaimer

---
I do not take any responsibility for any misuse or damage caused by this tool.

## License

---
PyDmidecode is open-source software licensed under the [MIT License](https://opensource.org/licenses/MIT).