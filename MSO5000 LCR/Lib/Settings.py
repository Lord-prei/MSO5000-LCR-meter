# Lib for all the TEMP stuff

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
import  Lib.Output  as O


# -------------------------------------------------- Settings Variables

Rounded =           0  # Decimal places for rounding
Time_Delay =        0  # Time Delay for better UX
Debug =             0  # Debug Variable
Debug_Calc =        0  # Debug Variable for Calculations
Number_Display =    0  # Variable for Displaying Numbers in different formats (Normal, Eng, SI)

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

# --------------------------------------------------------------------------- Settings
# Here Come all of the Functions
# region Settings

# -------------------------------------------------- Layer 1

# Functions Layer 1
# region Functions Layer 1

def Settings(Type, What, dfData):  # Calling Settings from Excel File
    match Type:
        case "Default":

            file_path = os.path.join(Settings_Path, "Settings_Default.xlsx")
            dfSettings = pd.read_excel(file_path, header=None, index_col=None)

            if What == "Load":  # Load Default Settings

                Settings_Load(dfSettings)

                file_path_current = os.path.join(Settings_Path, "Settings_Current.xlsx")
                dfSettingsCurrent = dfSettings
                dfSettingsCurrent.to_excel(file_path_current, index=False, header=None)

        case "Custom":

            file_path = os.path.join(Settings_Path, "Settings_Custom.xlsx")
            dfSettings = pd.read_excel(file_path, header=None, index_col=None)

            if What == "Load":  # Load Custom Settings

                Settings_Load(dfSettings)

                file_path_current = os.path.join(Settings_Path, "Settings_Current.xlsx")
                dfSettingsCurrent = dfSettings
                dfSettingsCurrent.to_excel(file_path_current, index=False, header=None)

            if What == "Save":  # Save Custom Settings
                dfSettings = dfData
                file_path_current = os.path.join(Settings_Path, "Settings_Current.xlsx")
                dfSettings.to_excel(file_path, index=False, header=None)
                dfSettings.to_excel(file_path_current, index=False, header=None)

        case "Current":

            file_path = os.path.join(Settings_Path, "Settings_Current.xlsx")
            dfSettings = pd.read_excel(file_path, header=None, index_col=None)

            if What == "Show":  # Show Current Settings
                print(dfSettings)

            if What == "Save":  # Save Current Settings
                dfData.to_excel(file_path, index=False, header=None)

            if What == "Load":  # Load Current Settings
                Settings_Load(dfSettings)

# endregion Functions Layer 1

# -------------------------------------------------- Layer 2

# Functions Layer 2
# region Functions Layer 2

def Settings_Load(dfSettings):

    global Rounded, Time_Delay, Debug, Debug_Calc, Number_Display

    Rounded =           int(dfSettings.iloc[0, 1])
    Time_Delay =        float(dfSettings.iloc[1, 1])
    Debug =             str(dfSettings.iloc[2, 1])
    Debug_Calc =        str(dfSettings.iloc[3, 1])
    Number_Display =    str(dfSettings.iloc[4, 1])

def Settings_Change(dfData):

    # 20260222, MODIFICATION, V0.0.1, LZerres: Added new setting for Debug Messages for Calculations and added this to the settings menu
    global Rounded, Time_Delay, Debug, Debug_Calc, Number_Display

    again = 1
    while again == 1:
        again = 0
        O.Clear_CLI()
        print("Change Settings")
        
        print   (
                "What Settings do you wanna change?\n\n"
                "1 : Decimal places for rounding (Current: " + str(Rounded) + ")\n"
                "2 : Time Delay when going back (Current: " + str(Time_Delay) + "s)\n"
                "3 : Debug Messages (Current: " + str(Debug) + ")\n"
                "4 : Debug Messages for Calculations (Current: " + str(Debug_Calc) + ")\n"
                "5 : Number Format for Display (Current: " + str(Number_Display) + ")\n"
                "99: Go back\n\n"
                )

        User_Input = input("Your Input: ")

        # 20260225, MODIFICATION, V0.0.3, LZerres: Added this to Validate User Input (when wrong it returns "FALSE")
        processedInput = userInputValidation(User_Input, "number")

        match processedInput:
            case "1":  # Change Decimal Places
                O.Clear_CLI()
                print("Change Decimal Places")
                New_Value = input("Enter new value (Current: " + str(Rounded) + "): ")

                # 20260225, MODIFICATION, V0.0.3, LZerres: Added this to Validate User Input (when wrong it returns "FALSE")
                processedNewValue = userInputValidation(New_Value, "number")

                if processedNewValue == "FALSE":
                    O.Wrong_Input(New_Value)
                    again = 1

                else:
                    Rounded = int(New_Value)
                    dfData.iloc[0, 1] = Rounded
                    print("Decimal Places changed to: ", Rounded)
                    print("\n\ndo you wana change more settings?")
                    again = input("2 = yes / 1 = no: ")

                    tempAgain = userInputValidation(again, "number")

                    if tempAgain == "FALSE":
                        O.Wrong_Input(again)
                        again = 1
                    else:
                        again = int(tempAgain) - 1

            case "2":  # Change Time Delay
                O.Clear_CLI()
                print("Change Time Delay")
                New_Value = input("Enter new value (Current: " + str(Time_Delay) + "s): ")

                # 20260225, MODIFICATION, V0.0.3, LZerres: Added this to Validate User Input (when wrong it returns "FALSE")
                processedNewValue = userInputValidation(New_Value, "float")

                if processedNewValue == "FALSE":
                    O.Wrong_Input(New_Value)
                    again = 1

                else:
                    Time_Delay = float(New_Value)
                    dfData.iloc[1, 1] = Time_Delay
                    print("Time Delay changed to: ", Time_Delay, "s")
                    print("\n\ndo you wana change more settings?")
                    again = input("2 = yes / 1 = no: ")

                    tempAgain = userInputValidation(again, "number")

                    if tempAgain == "FALSE":
                        O.Wrong_Input(again)
                        again = 1
                    else:
                        again = int(tempAgain) - 1

            case "3":  # Debug Messages
                O.Clear_CLI()
                print("Do u want Debug Messages")
                New_Value = input("Enter new value (Current: " + str(Debug) + ") (2 = Yes/ 1 = No): ")

                # 20260225, MODIFICATION, V0.0.3, LZerres: Added this to Validate User Input (when wrong it returns "FALSE")
                processedNewValue = userInputValidation(New_Value, "number")

                if processedNewValue == "FALSE":
                    O.Wrong_Input(New_Value)
                    again = 1
                    
                else:
                    # 20260222, MODIFICATION, V0.0.2, LZerres: Added this so all settings can be change by numbers (UX)
                    if New_Value == "1":
                        New_Value = "no"
                    elif New_Value == "2":
                        New_Value = "yes"

                    if (New_Value == "yes") or (New_Value == "no"):
                        Debug = str(New_Value)
                        dfData.iloc[2, 1] = Debug
                        print("Debug Messages changed to: ", Debug)
                    print("\n\ndo you wana change more Settings?")
                    again = input("2 = yes / 1 = no: ")

                    tempAgain = userInputValidation(again, "number")

                    if tempAgain == "FALSE":
                        O.Wrong_Input(again)
                        again = 1
                    else:
                        again = int(tempAgain) - 1

            # 20260222, MODIFICATION, V0.0.2, LZerres: Added new setting for Debug Messages for Calculations
            case "4":  # Debug Calc Messages
                O.Clear_CLI()
                print("Do u want Debug Messages")
                New_Value = input("Enter new value (Current: " + str(Debug_Calc) + ") (2 = Yes / 1 = No): ")

                # 20260225, MODIFICATION, V0.0.3, LZerres: Added this to Validate User Input (when wrong it returns "FALSE")
                processedNewValue = userInputValidation(New_Value, "number")

                if processedNewValue == "FALSE":
                    O.Wrong_Input(New_Value)
                    again = 1

                else:
                    if New_Value == "1":
                        New_Value = "no"
                    elif New_Value == "2":
                        New_Value = "yes"

                    if (New_Value == "yes") or (New_Value == "no"):
                        Debug_Calc = str(New_Value)
                        dfData.iloc[3, 1] = Debug_Calc
                        print("Debug Messages changed to: ", Debug_Calc)
                    print("\n\ndo you wana change more Settings?")
                    again = input("2 = yes / 1 = no: ")

                    tempAgain = userInputValidation(again, "number")

                    if tempAgain == "FALSE":
                        O.Wrong_Input(again)
                        again = 1
                    else:
                        again = int(tempAgain) - 1

            # 20260222, MODIFICATION, V0.0.2, LZerres: Added new Setting for Number Display Format (Normal, Eng, SI) and added this to the settings menu
            case "5":  # Number Display Format
                O.Clear_CLI()
                print("Do u want Debug Messages")
                New_Value = input("Enter new value (Current: " + str(Number_Display) + ") (3 = SI / 2 = ENG / 1 = NORMAL): ")

                # 20260225, MODIFICATION, V0.0.3, LZerres: Added this to Validate User Input (when wrong it returns "FALSE")
                processedNewValue = userInputValidation(New_Value, "number")

                if processedNewValue == "FALSE":
                    O.Wrong_Input(New_Value)
                    again = 1

                else:
                    if New_Value == "1":
                        New_Value = "normal"
                    elif New_Value == "2":
                        New_Value = "eng"
                    elif New_Value == "3":
                        New_Value = "si"

                    if ((New_Value == "normal") or (New_Value == "eng") or (New_Value == "si")):
                        Number_Display = str(New_Value)
                        dfData.iloc[4, 1] = Number_Display
                        print("Debug Messages changed to: ", Number_Display)
                    print("\n\ndo you wana change more Settings?")
                    again = input("2 = yes / 1 = no: ")

                    tempAgain = userInputValidation(again, "number")

                    if tempAgain == "FALSE":
                        O.Wrong_Input(again)
                        again = 1
                    else:
                        again = int(tempAgain) - 1

            case "99":  # Go back
                O.Clear_CLI()
                again = 0
                print("Go back")
                time.sleep(Time_Delay)

            case "FALSE": # 20260225, MODIFICATION, V0.0.3, LZerres: Added for input Validation
                        O.Wrong_Input(User_Input)
                        again = 1

# endregion Functions Layer 2

# -------------------------------------------------- Layer 3

# Functions Layer 3
# region Functions Layer 3

def userInputValidation(input, type):
    match type:
        case "number":

            check = checkUserInputNumber(input)

            if check == "TRUE":
                return input
            elif check == "FALSE":
                return check

        case "float":
            
            check = checkUserInputFloat(input)

            if check == "TRUE":
                return input
            elif check == "FALSE":
                return check

# endregion Functions Layer 3

# -------------------------------------------------- Layer 4

# Functions Layer 4
# region Functions Layer 4

def checkUserInputNumber(input):
    if input.isdigit(): # Check if input is a number (excluds floating and negative numbers)
        if Debug == "yes":
            print(f"good boy ;) {input}")
        return "TRUE"
    if Debug == "yes":
        print(f"bad boy {input}")
    return "FALSE"

def checkUserInputFloat(input):
    try:
        float(input)
        return "TRUE"
    except ValueError:
        return "FALSE"

# endregion Functions Layer 4

# endregion Settings
# --------------------------------------------------------------------------- End Settings
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