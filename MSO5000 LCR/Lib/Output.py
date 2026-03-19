# Lib for all the Output stuff

import  sys
import  os
import  time
import  subprocess
import  math
import  pyvisa
import  msvcrt
import  shutil
import  psutil
import  platform
from    calendar    import c
from    re          import DEBUG
from    turtle      import clear
from    enum        import Enum
import  pandas      as pd
import  matplotlib.pyplot as plt
import  numpy       as np
import  Lib.Debug   as D
import  Lib.Settings as S

# --------------------------------------------------------------------------- define Paths

# define Paths
# region Paths

if getattr(sys, "frozen", False):
    # Running as PyInstaller EXE
    Base_Dir =  os.path.dirname(sys.executable)
    Lib_Dir =   os.path.join(Base_Dir, "Lib")
else:
    # Running as normal Python script
    Lib_Dir =   os.path.dirname(os.path.abspath(__file__))
    Base_Dir =  os.path.dirname(Lib_Dir)

Settings_Path = os.path.join(Base_Dir, "Settings")
Data_Path =     os.path.join(Base_Dir, "Data")

# endregion Paths

class enum(Enum):
    # All of the text dialog variables
    START_TEXT = 1
    PICK_TEXT1 = 2
    PICK_TEXT2 = 3
    PICK_TEXT3 = 4
    ABOUT_TEXT = 5

VERSION_SW = 0
def whatVersion(VERSION): # 20260301, MODIFICATION, V0.1.0, LZerres: Function to get Version from main
    global VERSION_SW
    VERSION_SW = VERSION

# --------------------------------------------------------------------------- Formating
# Here Come all of the Functions
# region Formating

columns, rows = shutil.get_terminal_size()
# print(f"Your CMD is {columns} characters wide and {rows} lines tall.")

# -------------------------------------------------- Layer 1

# Functions Layer 1
# region Functions Layer 1

def TXT_Dialog(n):  # All of the text dialog stuff
    match n:
        case enum.START_TEXT:  # Starting Text
            print   (
                    "Hello and Welcome to DIE (Debug Instrument Engine)\n"
                    "This tool helps you to measure and analyze LCR components with the MSO5000 (Maybe more lator)\n\n\n"
                    )

        case enum.PICK_TEXT1:  # Main Menu
            print   ("What do u wanna do? (Pick from List)\n\n")
            print   (
                    "1 : Measure LCR Component\n"
                    "2 : Analyze / Calculate existing Measurement\n"
                    "3 : Settings\n"
                    "4 : Connect to Oscilloscope\n"
                    "98: About\n"
                    "99: Exit Program\n\n"
                    )

        case enum.PICK_TEXT2:  # Analyze / Calculate existing Measurement Menu
            print   ("What do u wanna do? (Pick from List)\n\n")
            print   (
                    "1 : Calculate Data and export as Excel Files\n"
                    "2 : Plot Data\n"
                    "3 : Both Calculate and Plot Data\n"
                    "99: Go back\n\n"
                    )

        case enum.PICK_TEXT3:  # Settings Menu
            print   (
                    "Settings Menu\n\n"
                    "1 : Load Default Settings\n"
                    "2 : Load Custom Settings\n"
                    "3 : Show Current Settings\n"
                    "4 : Change Settings\n"
                    "5 : Save Current Settings as Custom Settings\n"
                    "99: Go back\n\n"
                    )

        case enum.ABOUT_TEXT:  # About Text
            # 20260301, MODIFICATION, V0.1.0, LZerres: New Text for About Section
            print   (
                    "DIE (Debug Instrument Engine) | Formaly known as MSO5000 LCR Meter\n"
                    "Version: V"+ VERSION_SW + "\n\n"
                    "This tool helps you to measure and analyze LCR components with the MSO5000 (Maybe more lator)\n\n"
                    "Created by Lord_prei in 2025\n"
                    "GitHub: https://github.com/Lord-prei/MSO5000-LCR-meter\n\n"
                    )
            Get_System_Info() # 20260301, MODIFICATION, V0.1.1, LZerres: Call to new Function to get System Information

def Wrong_Input(wrongInput):  # Wrong Input Text
    # 20260301, MODIFICATION, V0.1.1, LZerres: New Function to print Wrong Input the user typed
    Clear_CLI()
    print(f"Invalid Input you typed: (\x1b[31m{wrongInput}\x1b[0m), try again idiot")
    waitForKeypress()
            
# endregion Functions Layer 1

# -------------------------------------------------- Layer 2

# Functions Layer 2
# region Functions Layer 2

# 20260301, MODIFICATION, V0.1.1, LZerres: New Function to get System Information for About Section
def Get_System_Info():
    systemPlattform = sys.platform
    systemInfo = platform.platform()
    osBuildNumber = platform.version()
    systemArchitecure = platform.architecture()[0]
    systemProcessor = platform.processor()
    systemThreadCount = os.cpu_count()
    systemCoreCount = os.cpu_count() // 2  # Assuming hyperthreading, this is a common way to estimate core count
    systemRAMusage = psutil.virtual_memory().used / (1024 ** 3)  # RAM usage in GB
    systemRAMtotal = psutil.virtual_memory().total / (1024 ** 3)  # Total RAM in GB
    systemRAMpercent = psutil.virtual_memory().percent  # RAM usage percentage
    systemRAMfree = psutil.virtual_memory().free / (1024 ** 3)  # Free RAM in GB
    linePrint()
    print("\nYour System Information:\n")
    print(f"Your System Info is: \t\t{systemInfo}")
    print(f"Your System Plattform is: \t{systemPlattform}")
    print(f"Your OS Build Number is: \t{osBuildNumber}")
    print(f"Your System Architecure is: \t{systemArchitecure}")
    print(f"Your System Processor is: \t{systemProcessor}")
    print(f"Your System Core Count is: \t{systemCoreCount}")
    print(f"Your System Thread Count is: \t{systemThreadCount}")
    print(f"Your System Total RAM is: \t{systemRAMtotal:.2f} GB")
    print(f"Your System Free RAM is: \t{systemRAMfree:.2f} GB")
    print(f"Your System RAM Usage is: \t{systemRAMusage:.2f} GB")
    print(f"Your System RAM Usage % is: \t{systemRAMpercent:.2f}%")

# endregion Functions Layer 2

# -------------------------------------------------- Layer 3

# Functions Layer 3
# region Functions Layer 3

def linePrint():
    print("-" * columns)

def waitForKeypress():  # Wait for a keypress
    print("\nPress anything to continue")
    msvcrt.getch()

def Clear_CLI():  # Clear screen + move cursor to top-left
    print("\033[2J\033[H", end="")

# endregion Functions Layer 3
# endregion Formating
# --------------------------------------------------------------------------- End Formating
# ----------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------- Excel / CSV
# Here Come all of the Functions
# region Functions

# -------------------------------------------------- Layer 1

# Functions Layer 1
# region Functions Layer 1

def Export_Excel(fileFolderPath, fileName, df):
    filePath = os.path.join(fileFolderPath, fileName)
    df.to_excel(filePath, index=False)

def Create_Excel_Clean(type, lenght, name):
    df = pd.DataFrame()
    X = 0

    df.insert(X, f"Ue_[V]", pd.Series(np.zeros(lenght, dtype=np.float64)))
    df.insert(X + 1, f"Ua_[V]", pd.Series(np.zeros(lenght, dtype=np.float64)))
    df.insert(X + 2, f"Ie_[A]", pd.Series(np.zeros(lenght, dtype=np.float64)))
    df.insert(X + 3, f"F_[Hz]", pd.Series(np.zeros(lenght, dtype=np.float64)))
    df.insert(X + 4, f"φ_[°]", pd.Series(np.zeros(lenght, dtype=np.float64)))
    df.insert(X + 5, f"|Z|_[Ω]", pd.Series(np.zeros(lenght, dtype=np.float64)))
    df.insert(X + 6, f"Z_[Ω]", pd.Series(np.zeros(lenght, dtype=np.complex128)))
    df.insert(X + 7, f"R_[Ω]", pd.Series(np.zeros(lenght, dtype=np.float64)))
    df.insert(X + 8, f"X_[Ω]", pd.Series(np.zeros(lenght, dtype=np.float64)))
    df.insert(X + 9, f"H_[1]", pd.Series(np.zeros(lenght, dtype=np.float64)))
    df.insert(X + 10, f"H_[db]", pd.Series(np.zeros(lenght, dtype=np.float64)))

    file_path = os.path.join(Data_Path, f"{name}.xlsx")  # Exporting calculated data to Excel File
    df.to_excel(file_path, index=False)

def Export_CSV(fileFolderPath, fileName, df):
    filePath = os.path.join(fileFolderPath, fileName)
    df.to_csv(filePath, index=False, encoding="utf-8")

def Create_CSV_Clean(type, lenght, name):
    df = pd.DataFrame()
    X = 0
    df.insert(X, f"Ue_[V]", pd.Series(np.zeros(lenght, dtype=np.float64)))
    df.insert(X + 1, f"Ua_[V]", pd.Series(np.zeros(lenght, dtype=np.float64)))
    df.insert(X + 2, f"Ie_[A]", pd.Series(np.zeros(lenght, dtype=np.float64)))
    df.insert(X + 3, f"F_[Hz]", pd.Series(np.zeros(lenght, dtype=np.float64)))
    df.insert(X + 4, f"φ_[°]", pd.Series(np.zeros(lenght, dtype=np.float64)))
    df.insert(X + 5, f"|Z|_[Ω]", pd.Series(np.zeros(lenght, dtype=np.float64)))
    df.insert(X + 6, f"Z_[Ω]", pd.Series(np.zeros(lenght, dtype=np.complex128)))
    df.insert(X + 7, f"R_[Ω]", pd.Series(np.zeros(lenght, dtype=np.float64)))
    df.insert(X + 8, f"X_[Ω]", pd.Series(np.zeros(lenght, dtype=np.float64)))
    df.insert(X + 9, f"H_[1]", pd.Series(np.zeros(lenght, dtype=np.float64)))
    df.insert(X + 10, f"H_[db]", pd.Series(np.zeros(lenght, dtype=np.float64)))

    file_path = os.path.join(Data_Path, f"{name}.csv")  # Exporting calculated data to CSV File
    df.to_csv(file_path, index=False)

def Export_Pretty_txt(fileFolderPath, fileName, df):
    filePath = os.path.join(fileFolderPath, fileName)

    # convert all values to strings
    df_str = df.astype(str)

    # determine column widths
    col_widths = []
    for col in df_str.columns:
        max_width = max(df_str[col].map(len).max(), len(col))
        col_widths.append(max_width)

    with open(filePath, "w", encoding="utf-8") as f:

        # header
        header = " | ".join(
            col.ljust(width) for col, width in zip(df_str.columns, col_widths)
        )
        f.write(header + "\n")

        # separator
        sep_len = len(header)
        f.write("-" * sep_len + "\n")

        # rows
        for _, row in df_str.iterrows():
            line = " | ".join(
                val.ljust(width) for val, width in zip(row, col_widths)
            )
            f.write(line + "\n")

def Create_Clean():
    df = pd.DataFrame()
    X = 0
    lenght = 0
    df.insert(X, f"Ue_[V]", pd.Series(np.zeros(lenght, dtype=np.float64)))
    df.insert(X + 1, f"Ua_[V]", pd.Series(np.zeros(lenght, dtype=np.float64)))
    df.insert(X + 2, f"Ie_[A]", pd.Series(np.zeros(lenght, dtype=np.float64)))
    df.insert(X + 3, f"F_[Hz]", pd.Series(np.zeros(lenght, dtype=np.float64)))
    df.insert(X + 4, f"φ_[°]", pd.Series(np.zeros(lenght, dtype=np.float64)))
    df.insert(X + 5, f"|Z|_[Ω]", pd.Series(np.zeros(lenght, dtype=np.float64)))
    df.insert(X + 6, f"Z_[Ω]", pd.Series(np.zeros(lenght, dtype=np.complex128)))
    df.insert(X + 7, f"R_[Ω]", pd.Series(np.zeros(lenght, dtype=np.float64)))
    df.insert(X + 8, f"X_[Ω]", pd.Series(np.zeros(lenght, dtype=np.float64)))
    df.insert(X + 9, f"H_[1]", pd.Series(np.zeros(lenght, dtype=np.float64)))
    df.insert(X + 10, f"H_[db]", pd.Series(np.zeros(lenght, dtype=np.float64)))

    return df

# endregion Functions Layer 1

# -------------------------------------------------- Layer 2

# Functions Layer 2
# region Functions Layer 2

# Code for Functions Layer 2

# endregion Functions Layer 2

# -------------------------------------------------- Layer 3

# Functions Layer 3
# region Functions Layer 3

# Code for Functions Layer 3

# endregion Functions Layer 3

# endregion Functions
# --------------------------------------------------------------------------- End Excel / CSV
# ----------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------- 
# Here Come all of the Functions
# region Functions

# -------------------------------------------------- Layer 1

# Functions Layer 1
# region Functions Layer 1

# Code for Functions Layer 1

# endregion Functions Layer 1

# -------------------------------------------------- Layer 2

# Functions Layer 2
# region Functions Layer 2

# Code for Functions Layer 2

# endregion Functions Layer 2

# -------------------------------------------------- Layer 3

# Functions Layer 3
# region Functions Layer 3

# Code for Functions Layer 3

# endregion Functions Layer 3

# endregion Functions
# --------------------------------------------------------------------------- 