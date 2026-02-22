# Lib for all the Output stuff

import  sys
import  os
import  time
import  subprocess
import  math
import  pyvisa
import  msvcrt
import  shutil
from    calendar    import c
from    re          import DEBUG
from    turtle      import clear
from    enum        import Enum
import  pandas      as pd
import  matplotlib.pyplot as plt
import  numpy       as np
import  Lib.Input   as I
import  Lib.Process as P

# --------------------------------------------------------------------------- define Paths

if (True):  # define Paths
    if getattr(sys, "frozen", False):
        # Running as PyInstaller EXE
        Base_Dir = os.path.dirname(sys.executable)
        Lib_Dir  = os.path.join(Base_Dir, "Lib")
    else:
        # Running as normal Python script
        Lib_Dir  = os.path.dirname(os.path.abspath(__file__))
        Base_Dir = os.path.dirname(Lib_Dir)

    Settings_Path = os.path.join(Base_Dir, "Settings")
    Data_Path =     os.path.join(Base_Dir, "Data")

class S(Enum):
    # All of the text dialog variables
    START_TEXT = 1
    PICK_TEXT1 = 2
    PICK_TEXT2 = 3
    PICK_TEXT3 = 4
    PICK_TEXT_SETTINGS = 5


# --------------------------------------------------------------------------- Formating
# Here Come all of the Functions

columns, rows = shutil.get_terminal_size()
# print(f"Your CMD is {columns} characters wide and {rows} lines tall.")

# -------------------------------------------------- Layer 1

# Functions Layer 1

if(True):
    def linePrint():
        print("-" * columns)
    def waitForKeypress():          # Wait for a keypress
        print("\nPress anything to continue")
        msvcrt.getch()
    def Clear_CLI():                    # Clear screen + move cursor to top-left
        print("\033[2J\033[H", end='')
    def TXT_Dialog(n):                  # All of the text dialog stuff
        match n:
            case S.START_TEXT:          # Starting Text
                print(  "Hello and Welcome to the MSO5000 LCR Measurement Tool\n"
                        "This tool helps you to measure and analyze LCR components with the MSO5000\n\n\n")

            case S.PICK_TEXT1:          # Main Menu
                print(  "What do u wanna do? (Pick from List)\n\n")
                print(  "1 : Measure LCR Component\n"
                        "2 : Analyze / Calculate existing Measurement\n"
                        "3 : Settings\n"
                        "99: Exit Program\n\n")

            case S.PICK_TEXT2:          # Analyze / Calculate existing Measurement Menu
                print(  "What do u wanna do? (Pick from List)\n\n")
                print(  "1 : Calculate Data and export as Excel Files\n"
                        "2 : Plot Data\n"
                        "3 : Both Calculate and Plot Data\n"
                        "99: Go back\n\n")

            case S.PICK_TEXT3:          # Settings Menu
                print(  "Settings Menu\n\n"
                        "1 : Load Default Settings\n"
                        "2 : Load Custom Settings\n"
                        "3 : Show Current Settings\n"
                        "4 : Change Settings\n"
                        "5 : Save Current Settings as Custom Settings\n"
                        "99: Go back\n\n")

            case S.PICK_TEXT_SETTINGS:   # Settings changing menu
                print(  "What Settings do you wanna change?\n\n"
                        "1 : Decimal places for rounding (Current: " + str(P.Rounded) + ")\n"
                        "2 : Time Delay when going back (Current: " + str(P.Time_Delay) + "s)\n"
                        "3 : Debug Messages (Current: " + str(P.Debug) + ")\n"
                        "4 : Debug Messages for Calculations (Current: " + str(P.Debug_Calc) + ")\n"
                        "5 : Number Format for Display (Current: " + str(P.Number_Display) + ")\n"
                        "99: Go back\n\n")

# -------------------------------------------------- Layer 2

# Functions Layer 2

# if(True): 
#     print(1)

# -------------------------------------------------- Layer 3

# Functions Layer 3

# if(True): 
#     print(1)

# --------------------------------------------------------------------------- End Formating
# ----------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------- Debug
# Here Come all of the Functions

# -------------------------------------------------- Layer 1

# Functions Layer 1

if(True):
    def dprintDir(): # printing debug for paths
        if(P.Debug == "yes"):
            linePrint()
            print("All of the important Paths:\n")
            print("Base Dir = \t\t", Base_Dir)
            print("Lib Dir = \t\t", Lib_Dir)
            print("Settings Path = \t", Settings_Path)
            print("Data Path = \t\t", Data_Path)
            print("\b")
            print("End of Debug Paths")
            linePrint()
            waitForKeypress()

    # 20260222, MODIFICATION, V0.0.2, LZerres: Debug messages for Calculations
    def dprintCalc(
                    X, Y,
                    Rounded_Voltage_Ue,
                    Rounded_Voltage_Ua,
                    Rounded_Current,
                    Rounded_Frequeny,
                    Rounded_PhaseOffset,
                    Rounded_Impedance_abs,
                    Rounded_Resistance,
                    Rounded_Blind,
                    Rounded_Impedance,
                    Rounded_H,
                    Rounded_H_db,
                    ): 
        if(P.Debug == "yes"):
            print(
                f"row:\t{Y:06d}\t| "
                f"col:\t{X:06d}\t| "
                f"Ue:\t{P.select_number_format(Rounded_Voltage_Ue)}V\t| "
                f"Ua:\t{P.select_number_format(Rounded_Voltage_Ua)}V\t| "
                f"I:\t{P.select_number_format(Rounded_Current)}A\t| "
                f"f:\t{P.select_number_format(Rounded_Frequeny)}Hz\t| "
                f"φ:\t{P.select_number_format(Rounded_PhaseOffset)}°\t| "
                f"|Z|:\t{P.select_number_format(Rounded_Impedance_abs)}Ω\t| "
                f"R:\t{P.select_number_format(Rounded_Resistance)}Ω\t| "
                f"X:\t{P.select_number_format(Rounded_Blind)}Ω\t| "
                f"Z:\t{P.select_number_format(Rounded_Impedance)}Ω\t| "
                f"H:\t{P.select_number_format(Rounded_H)}\t| "
                f"H(dB):\t{P.select_number_format(Rounded_H_db)}dB"
                )


# -------------------------------------------------- Layer 2

# Functions Layer 2

# if(True):
#     print(1)

# -------------------------------------------------- Layer 3

# Functions Layer 3

# if(True): 
#     print(1)

# --------------------------------------------------------------------------- End Debug
# ----------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------
# Here Come all of the Functions

# -------------------------------------------------- Layer 1

# Functions Layer 1

# if(True):
#     print(1)

# -------------------------------------------------- Layer 2

# Functions Layer 2

# if(True): 
#     print(1)

# -------------------------------------------------- Layer 3

# Functions Layer 3

# if(True): 
#     print(1)

# ---------------------------------------------------------------------------