# ----------------------------------------------------------------------------------------------------
#       Project: DIE (Debug Instrument Engine) | Formaly known as MSO5000 LCR Meter
#       Purpose: To automate LCR analisys for my Oscilloscope
#       Version: V0.0.2
# ----------------------------------------------------------------------------------------------------
#       Version control
# --------------------------------------------------------------------------- Copypaste
#
#       VERSIONNAME
#
#       JJJJMMDD, MODIFICATION, Vx.x.x, LZerres:  
#           CHANGE 1
#           CHANGE 2
#           CHANGE 3
#
# --------------------------------------------------------------------------- V0.0.1
#
#       Initial Release
#
#       20260222, MODIFICATION, V0.0.1, LZerres:  
#           Navigatable CLI
#           Added some calculations
#           Added settings
#           Made some Libs: Input, Process, Output and added structure in them
#
# --------------------------------------------------------------------------- V0.0.2
#
#       VERSIONNAME
#
#       20260222, MODIFICATION, V0.0.2, LZerres:  
#           Added Version Number to be displayed in the future
#           Added Debug Messages for better understanding of the code and to be able to find bugs easier
#           Added Number Format for Display in the Settings
#           Changed Project name to DIE (Debug Instrument Engine) because it sounds cooler and more general, maybe i can add more instruments in the future
#
# ---------------------------------------------------------------------------

import  sys
import  os
import  time
import  subprocess
import  math
import  pyvisa
import  msvcrt
from    calendar    import c
from    re          import DEBUG
from    turtle      import clear
from    enum        import Enum
import  pandas      as pd
import  matplotlib.pyplot as plt
import  numpy       as np
import  Lib.Input   as I
import  Lib.Process as P
import  Lib.Output  as O
from    Lib.Output  import S

VERSION_SW = "0.0.2"    # 20260222, MODIFICATION, V0.0.2, LZerres: Added to be displayed in the futur

print(f"\x1b]0;DIE V{VERSION_SW}\x07");

# --------------------------------------------------------------------------- Variables

repeat      = 0     # Variable for repeating loops

# --------------------------------------------------------------------------- Constants

class constant(Enum):
    # For Graphing
    VOLTAGE =       0  # Voltage for Graphing
    CURRENT =       1  # Current for Graphing
    FREQUENCY =     2  # Frequency for Graphing
    PHASE_OFFSET =  3  # Phase Offset for Graphing
    IMPEDANCE_ABS = 4  # Impedance for Graphing
    IMPEDANCE =     5  # Complex Impedance for Graphing
    RESISTANCE =    6  # Resistance for Graphing
    BLIND =         7  # Blindwiderstand for Graphing

    # Random ah

# --------------------------------------------------------------------------- define Paths

if (True): # define Paths
    if getattr(sys, "frozen", False):
        Base_Dir = os.path.dirname(sys.executable)
    else:
        Base_Dir = os.path.dirname(os.path.abspath(__file__))

    Settings_Path = os.path.join(Base_Dir, "Settings")
    Data_Path =     os.path.join(Base_Dir, "Data")

# --------------------------------------------------------------------------- Init

P.Settings("Custom", "Load", 0) # Load Custom Settings
O.Clear_CLI()
O.dprintDir()                   # Printing Debug message
P.createExcel(0, 0, "Test")

# --------------------------------------------------------------------------- Main Loop

while True: # Main Loop
    O.Clear_CLI()
    O.TXT_Dialog(S.START_TEXT)  # Starting Text
    O.TXT_Dialog(S.PICK_TEXT1)  # pick from list text

    n = input("Your Input: ")   # User Input
    
    match n:
        case "1":   # Measure LCR Component (WIP)
            O.Clear_CLI()
            print("Measure LCR Component")
            
        case "2":   # Analyze / Calculate existing Measurement
            O.Clear_CLI()
            print("Analyze / Calculate existing Measurement")

            repeat = 1

            while (repeat == 1):
                O.Clear_CLI()
                O.TXT_Dialog(S.PICK_TEXT2)          # pick from list text
                User_Input = input("Your Input: ")  # User Input
                
                match User_Input:

                    case "1":   # Calculate Data and export as Excel Files
                        O.Clear_CLI()
                        print("Calculate Data and export as Excel Files")
                        P.Impedance_Calculation(P.Rounded)

                    case "2":   # Plot Data (WIP)
                        O.Clear_CLI()
                        print("Plot Data")

                    case "3":   # Both Calculate and Plot Data (WIP)
                        O.Clear_CLI()
                        print("Both Calculate and Plot Data")

                    case "99":  # Go back
                        O.Clear_CLI()
                        repeat = 0
                        print("Exit to Main Menu")
                        time.sleep(P.Time_Delay)

        case "3":   # Settings
            O.Clear_CLI()

            repeat = 1

            while (repeat == 1):
                O.Clear_CLI()
                O.TXT_Dialog(S.PICK_TEXT3)
                User_Input = input("Your Input: ")

                match User_Input:
                    case "1":   # Load Default Settings
                        O.Clear_CLI()
                        print("Loaded Default Settings")

                        P.Settings("Default", "Load", 0)

                        time.sleep(P.Time_Delay)

                    case "2":   # Load Custom Settings
                        O.Clear_CLI()
                        print("Loaded Custom Settings")

                        P.Settings("Custom", "Load", 0)

                        time.sleep(P.Time_Delay)

                    case "3":   # Show Current Settings
                        O.Clear_CLI()
                        print("Current Settings:\n\n")

                        P.Settings("Current", "Show", 0)

                        O.waitForKeypress()

                    case "4":   # Change Settings
                        file_path = os.path.join(Settings_Path, "Settings_Current.xlsx")
                        dfData = pd.read_excel(file_path, header=None, index_col=None)

                        P.Settings_Change(dfData)
                        P.Settings ("Current", "Save", dfData)

                    case "5":   # Save Current Settings as Custom Settings
                        O.Clear_CLI()
                        print("Save Current Settings as Custom Settings")
                        file_path = os.path.join(Settings_Path, "Settings_Current.xlsx")
                        dfData = pd.read_excel(file_path, header=None, index_col=None)

                        P.Settings("Custom", "Save", dfData)
                        print("\nCurrent Settings saved as Custom Settings")
                        time.sleep(P.Time_Delay)

                    case "99":
                        O.Clear_CLI()
                        repeat = 0
                        print("Exit to Main Menu")
                        time.sleep(P.Time_Delay)

        case "99":  # Exit Program
            O.Clear_CLI()
            print("Program about to DIE")
            time.sleep(P.Time_Delay)  # Short Delay for better UX
            sys.exit()