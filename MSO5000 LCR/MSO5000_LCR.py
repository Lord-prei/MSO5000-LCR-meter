# ----------------------------------------------------------------------------------------------------
#       Project: DIE (Debug Instrument Engine) | Formaly known as MSO5000 LCR Meter
#       Purpose: To automate LCR analisys for my Oscilloscope
#       Version: V0.2.0
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
#       Number Format for Display in the Settings
#
#       20260222, MODIFICATION, V0.0.2, LZerres:
#           Added Version Number to be displayed in the future
#           Added Debug Messages for better understanding of the code and to be able to find bugs easier
#           Added Number Format for Display in the Settings
#           Changed Project name to DIE (Debug Instrument Engine) because it sounds cooler and more general, maybe i can add more instruments in the future
#
# --------------------------------------------------------------------------- V0.0.3
#
#       Bugfixes and Code cleaned
#
#       20260225, MODIFICATION, V0.0.3, LZerres:
#           Replaced all if True statements with region so it still has the same effects but is more structured and easier to read
#           Fixed the bug for when the user types the frong input it crashes the program, now it returns "Invalid Input" and asks the user to try again
#
# --------------------------------------------------------------------------- V0.1.0
#
#       Last Bugfixes and Code cleaned
#
#       20260301, MODIFICATION, V0.1.0, LZerres:
#           Fixed last bug for craing when user types wrong input in the Settings Menu
#           Added About Text in the Main Menu
#           Added new case for connection to Oscilloscope (this is still WIP and will be added in the future)
#
# --------------------------------------------------------------------------- V0.1.1
#
#       Expanded select menu and complete overhaul to code structure
#
#       20260301, MODIFICATION, V0.1.1, LZerres:
#           Added System info to the About Text
#           Changed the entire code structures so it actually follows IPO principle
#           Added multiple new functions for better structure and readability of the code
#           Made 2 New Libs: Settings and Debug (to not break the IPO principle)
#
# --------------------------------------------------------------------------- V0.1.2
#
#       File format change
#
#       20260311, MODIFICATION, V0.1.2, LZerres:
#           Change from .xlsx to .csv and .txt for better performace / industry standards
#
# --------------------------------------------------------------------------- V0.2.0
#
#       Simple graphing function
#
#       20260318, MODIFICATION, V0.2.0, LZerres:
#           Added a simple graphing function
#
# --------------------------------------------------------------------------- 

import  sys
import  os
import  time
import  subprocess
import  math
from matplotlib.lines import lineStyles
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
from    Lib.Output  import enum
from    Lib.Process import GC
import  Lib.Settings as S
import  Lib.Debug   as D

VERSION_SW = "0.2.0"  # 20260222, MODIFICATION, V0.0.2, LZerres: Added to be displayed in the futur
O.whatVersion(VERSION_SW) # 20260301, MODIFICATION, V0.1.0, LZerres: Added this function so the Version Number can be used in other Libs

print(f"\x1b]0;DIE V{VERSION_SW}\x07") # 20260222, MODIFICATION, V0.0.2, LZerres: Added Version Number to be displayed in CLI title

# --------------------------------------------------------------------------- Variables

repeat1 = 0     # Variable for repeating loops 1
repeat2 = 0     # Variable for repeating loops 2
repeat3 = 0     # Variable for repeating loops 3

# --------------------------------------------------------------------------- Constants


class constants(Enum):
    temp = 0

    # Random ah


# --------------------------------------------------------------------------- define Paths

# define Paths
if getattr(sys, "frozen", False):
    Base_Dir =  os.path.dirname(sys.executable)
else:
    Base_Dir =  os.path.dirname(os.path.abspath(__file__))

Settings_Path = os.path.join(Base_Dir, "Settings")
Data_Path =     os.path.join(Base_Dir, "Data")

# --------------------------------------------------------------------------- Init

S.Settings("Custom", "Load", 0)  # Load Custom Settings
O.Clear_CLI()
D.printDir()                    # Printing Debug message
O.Create_CSV_Clean(0, 0, "Test")

# ---------------------------------------------------------------------------------------------------- Functions
# --------------------------------------------------------------------------- Calculations
# Here Come all of the Functions
# region Functions

# -------------------------------------------------- Layer 1

# Functions Layer 1
# region Functions Layer 1

def Calculate_All():
    dfCalculations = I.Import_CSV(Data_Path, "Clean.csv")    # Data from Oscilloscope cleaned.
    dfCalculationsRounded = dfCalculations.copy()
    dfCalculationsPretty = dfCalculations.astype(str) # 20260312, MODIFICATION, V0.2.0, LZerres: This is for the pretty txt file, so all values are saved as strings with the unit at the end
    

    Xmax = dfCalculations.shape[1]                              # Number of columns
    Ymax = dfCalculations.shape[0] - 1                          # Number of rows
    X = 0
    Y = 0   

    # Debug Messages
    if S.Debug == "yes":
        print("Xmax =", Xmax)
        print("Ymax =", Ymax)

    print("\nCalculating...")

    # Remove the old float64 column
    dfCalculations.drop(dfCalculations.columns[X + 6], axis=1, inplace=True)
    dfCalculationsRounded.drop(dfCalculationsRounded.columns[X + 6], axis=1, inplace=True)

    # Insert a new complex column at the same position as a Complex number
    dfCalculations.insert(
        X + 6,
        f"Z_[Ω]",
        pd.Series(np.zeros(len(dfCalculations), dtype=np.complex128), index=dfCalculations.index),)

    dfCalculationsRounded.insert(
        X + 6,
        f"Z_[Ω]",
        pd.Series(np.zeros(len(dfCalculationsRounded), dtype=np.complex128), index=dfCalculationsRounded.index,),)

    while Y <= Ymax:

        # Reading all the Data from the Excel File, these are needed for the calculations
        voltageUE =         I.Read_Voltage_Ue(dfCalculations, X, Y)
        voltageUA =         I.Read_Voltage_Ua(dfCalculations, X, Y)
        currentI =          I.Read_Current(dfCalculations, X, Y)
        frequency =         I.Read_Frequenzy(dfCalculations, X, Y)
        phaseOffset =       I.Read_PhaseOffset(dfCalculations, X, Y)
        phaseOffsetH =      I.Read_Phase_Offset_H(dfCalculations, X, Y)

        # Calculations
        impedanceABS =      P.Calc_Impedance(voltageUE, currentI)
        resistance =        P.Calc_Resistance(phaseOffset, impedanceABS)
        blind =             P.Calc_Blind(phaseOffset, impedanceABS)
        impedanceComplex =  P.Calc_Impedanz_Complex(resistance, blind)
        H =                 P.Calc_Transferfunction_1(voltageUA, voltageUE)
        Hdb =               P.Calc_Transferfunction_db(voltageUA, voltageUE)

        # Rounded Values for seperate Excel
        rounded_voltageUE =     P.Round_Sig(voltageUE, S.Rounded)
        rounded_voltageUA =     P.Round_Sig(voltageUA, S.Rounded)
        rounded_currentI =      P.Round_Sig(currentI, S.Rounded)
        rounded_frequency =     P.Round_Sig(frequency, S.Rounded)
        rounded_phaseOffset =   P.Round_Sig(phaseOffset, S.Rounded)
        rounded_impedanceABS =  P.Round_Sig(impedanceABS, S.Rounded)
        rounded_resistance =    P.Round_Sig(resistance, S.Rounded)
        rounded_blind =         P.Round_Sig(blind, S.Rounded)
        rounded_impedanceComplex = rounded_resistance + 1j * rounded_blind
        rounded_phaseOffsetH =  P.Round_Sig(phaseOffsetH, S.Rounded)
        rounded_H =             P.Round_Sig(H, S.Rounded)
        rounded_Hdb =           P.Round_Sig(Hdb, S.Rounded)

        # 20260311, MODIFICATION, V0.1.2, LZerres: For the pretty txt file
        dfCalculationsPretty.iloc[Y, X    ] = str(f"{P.select_number_format(rounded_voltageUE)}V")
        dfCalculationsPretty.iloc[Y, X + 1] = str(f"{P.select_number_format(rounded_voltageUA)}V")
        dfCalculationsPretty.iloc[Y, X + 2] = str(f"{P.select_number_format(rounded_currentI)}A")
        dfCalculationsPretty.iloc[Y, X + 3] = str(f"{P.select_number_format(rounded_frequency)}Hz")
        dfCalculationsPretty.iloc[Y, X + 4] = str(f"{P.select_number_format(rounded_phaseOffset)}°")
        dfCalculationsPretty.iloc[Y, X + 5] = str(f"{P.select_number_format(rounded_impedanceABS)}Ω")
        dfCalculationsPretty.iloc[Y, X + 6] = str(f"{P.select_number_format(rounded_impedanceComplex)}Ω")
        dfCalculationsPretty.iloc[Y, X + 7] = str(f"{P.select_number_format(rounded_resistance)}Ω") 
        dfCalculationsPretty.iloc[Y, X + 8] = str(f"{P.select_number_format(rounded_blind)}Ω")
        dfCalculationsPretty.iloc[Y, X + 9] = str(f"{P.select_number_format(rounded_phaseOffsetH)}°")
        dfCalculationsPretty.iloc[Y, X + 10] = str(f"{P.select_number_format(rounded_H)}")
        dfCalculationsPretty.iloc[Y, X + 11] = str(f"{P.select_number_format(rounded_Hdb)}dB")

        # Saving all the Data into the dataframe
        dfCalculations, dfCalculationsRounded = P.Save_Voltage_Ue           (dfCalculations, dfCalculationsRounded, X, Y, voltageUE, rounded_voltageUE)
        dfCalculations, dfCalculationsRounded = P.Save_Voltage_Ua           (dfCalculations, dfCalculationsRounded, X, Y, voltageUA, rounded_voltageUA)
        dfCalculations, dfCalculationsRounded = P.Save_Current              (dfCalculations, dfCalculationsRounded, X, Y, currentI, rounded_currentI)
        dfCalculations, dfCalculationsRounded = P.Save_Frequenzy            (dfCalculations, dfCalculationsRounded, X, Y, frequency, rounded_frequency)
        dfCalculations, dfCalculationsRounded = P.Save_PhaseOffset          (dfCalculations, dfCalculationsRounded, X, Y, phaseOffset, rounded_phaseOffset)
        dfCalculations, dfCalculationsRounded = P.Save_Impedance            (dfCalculations, dfCalculationsRounded, X, Y, impedanceABS, rounded_impedanceABS)
        dfCalculations, dfCalculationsRounded = P.Save_Impedanz_Complex     (dfCalculations, dfCalculationsRounded, X, Y, impedanceComplex, rounded_impedanceComplex)
        dfCalculations, dfCalculationsRounded = P.Save_Resistance           (dfCalculations, dfCalculationsRounded, X, Y, resistance, rounded_resistance)
        dfCalculations, dfCalculationsRounded = P.Save_Blind                (dfCalculations, dfCalculationsRounded, X, Y, blind, rounded_blind)
        dfCalculations, dfCalculationsRounded = P.Save_Phase_Offset_H       (dfCalculations, dfCalculationsRounded, X, Y, phaseOffsetH, rounded_phaseOffsetH)
        dfCalculations, dfCalculationsRounded = P.Save_Transferfunction_1   (dfCalculations, dfCalculationsRounded, X, Y, H, rounded_H)
        dfCalculations, dfCalculationsRounded = P.Save_Transferfunction_db  (dfCalculations, dfCalculationsRounded, X, Y, Hdb, rounded_Hdb)

        # 20260222, MODIFICATION, V0.0.1, LZerres: Added Debug Messages for Calculations, so you can see what is calculated in each step
        if (S.Debug == "yes") and (S.Debug_Calc == "yes"):
            D.printCalc(
                X,
                Y,
                rounded_voltageUE,
                rounded_voltageUA,
                rounded_currentI,
                rounded_frequency,
                rounded_phaseOffset,
                rounded_impedanceABS,
                rounded_resistance,
                rounded_blind,
                rounded_impedanceComplex,
                rounded_H,
                rounded_Hdb,
            )

        Y += 1

    O.Export_CSV(Data_Path, "Clean_Calc.csv", dfCalculations)
    O.Export_CSV(Data_Path, "Clean_Calc_Rounded.csv", dfCalculationsRounded)
    O.Export_Pretty_txt(Data_Path, "Clean_Calc.txt", dfCalculationsPretty)

# endregion Functions Layer 1

# -------------------------------------------------- Layer 2

# Functions Layer 2
# region Functions Layer 2
def TEMP_graphAll(): # 20260318, MODIFICATION, V0.2.0, LZerres: Temporary to test graphing
    Data_Path = os.path.join(Base_Dir, "Data")
    dfData = I.Import_CSV(Data_Path, "Clean_Calc.csv")

    fig, ax = plt.subplots()             # Create a figure containing a single Axes.
    X = GC.FREQUENCY
    Y = GC.RESISTANCE
    XAxisName, YAxisName = P.selectGraphSettings(X, Y)
    fig.canvas.manager.set_window_title(f"{YAxisName} over {XAxisName}")
    ax.grid()
    ax.set_xscale("log")
    ax.set_xlabel(XAxisName)
    ax.set_ylabel(YAxisName)    
    ax.set_title(f"{YAxisName} over {XAxisName}")
    Xval = dfData.iloc[:, X]
    Yval = dfData.iloc[:, Y]
    plt.plot(Xval, Yval, color="Black")
                        

    fig, ax = plt.subplots()             # Create a figure containing a single Axes.
    X = GC.FREQUENCY
    Y = GC.BLIND
    XAxisName, YAxisName = P.selectGraphSettings(X, Y)
    fig.canvas.manager.set_window_title(f"{YAxisName} over {XAxisName}")
    ax.grid()
    ax.set_xscale("log")
    ax.set_xlabel(XAxisName)
    ax.set_ylabel(YAxisName)    
    ax.set_title(f"{YAxisName} over {XAxisName}")
    Xval = dfData.iloc[:, X]
    Yval = dfData.iloc[:, Y]
    plt.plot(Xval, Yval, color="green")
                        

    fig, ax = plt.subplots()             # Create a figure containing a single Axes.
    X = GC.FREQUENCY
    Y = GC.IMPEDANCE_ABS
    XAxisName, YAxisName = P.selectGraphSettings(X, Y)
    fig.canvas.manager.set_window_title(f"{YAxisName} over {XAxisName}")
    ax.grid()
    ax.set_xscale("log")
    ax.set_xlabel(XAxisName)
    ax.set_ylabel(YAxisName)    
    ax.set_title(f"{YAxisName} over {XAxisName}")
    Xval = dfData.iloc[:, X]
    Yval = dfData.iloc[:, Y]
    plt.plot(Xval, Yval, color="blue")
                        

    fig, ax = plt.subplots()             # Create a figure containing a single Axes.
    X = GC.FREQUENCY
    Y = GC.IMPEDANCE_ABS
    Y2= GC.PHASE_OFFSET_TOT
    XAxisName, YAxisName = P.selectGraphSettings(X, Y)
    fig.canvas.manager.set_window_title(f"{YAxisName} over {XAxisName}")
    ax.grid(color="blue")
    ax.set_xscale("log")
    ax.set_xlabel(XAxisName)
    ax.set_ylabel(YAxisName)    
    ax.set_title(f"{YAxisName} over {XAxisName}")
    Xval = dfData.iloc[:, X]
    Yval = dfData.iloc[:, Y]
    ax.plot(Xval, Yval, color="blue")
    ax2 = ax.twinx()  # instantiate a second axes that shares the same x-axis
    XAxisName, YAxisName = P.selectGraphSettings(X, Y)
    fig.canvas.manager.set_window_title(f"{YAxisName} over {XAxisName}")
    ax2.grid()
    ax2.set_xscale("log")
    ax2.set_xlabel(XAxisName)
    ax2.set_ylabel(YAxisName)    
    ax2.set_title(f"{YAxisName} over {XAxisName}")
    Xval = dfData.iloc[:, X]
    Yval = dfData.iloc[:, Y2]
    ax2.plot(Xval, Yval, color="black", linestyle="--")


    fig, ax = plt.subplots()             # Create a figure containing a single Axes.
    X = GC.FREQUENCY
    Y = GC.TRANSFER_FUNCTION
    XAxisName, YAxisName = P.selectGraphSettings(X, Y)
    fig.canvas.manager.set_window_title(f"{YAxisName} over {XAxisName}")
    ax.grid()
    ax.set_xscale("log")
    ax.set_xlabel(XAxisName)
    ax.set_ylabel(YAxisName)    
    ax.set_title(f"{YAxisName} over {XAxisName}")
    Xval = dfData.iloc[:, X]
    Yval = dfData.iloc[:, Y]
    plt.plot(Xval, Yval, color="orange")


    fig, ax = plt.subplots()             # Create a figure containing a single Axes.
    X = GC.FREQUENCY
    Y = GC.TRANSFER_FUNCTION_LOG
    Y2= GC.PHASE_OFFSET_H
    XAxisName, YAxisName = P.selectGraphSettings(X, Y)
    fig.canvas.manager.set_window_title(f"{YAxisName} over {XAxisName}")
    ax.grid(color="orange")
    ax.set_xscale("log")
    ax.set_xlabel(XAxisName)
    ax.set_ylabel(YAxisName)    
    ax.set_title(f"{YAxisName} over {XAxisName}")
    Xval = dfData.iloc[:, X]
    Yval = dfData.iloc[:, Y]
    ax.plot(Xval, Yval, color="orange")
    ax2 = ax.twinx()  # instantiate a second axes that shares the same x-axis
    XAxisName, YAxisName = P.selectGraphSettings(X, Y)
    fig.canvas.manager.set_window_title(f"{YAxisName} over {XAxisName}")
    ax2.grid()
    ax2.set_xscale("log")
    ax2.set_xlabel(XAxisName)
    ax2.set_ylabel(YAxisName)    
    ax2.set_title(f"{YAxisName} over {XAxisName}")
    Xval = dfData.iloc[:, X]
    Yval = dfData.iloc[:, Y2]
    ax2.plot(Xval, Yval, color="black", linestyle="--")

    plt.show()


# Code for Functions Layer 2

# endregion Functions Layer 2

# -------------------------------------------------- Layer 3

# Functions Layer 3
# region Functions Layer 3

# Code for Functions Layer 3

# endregion Functions Layer 3

# endregion Functions
# --------------------------------------------------------------------------- End Calculations
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

# --------------------------------------------------------------------------- Main Loop

while True:  # Main Loop
    O.Clear_CLI()
    O.TXT_Dialog(enum.START_TEXT)  # Starting Text
    O.TXT_Dialog(enum.PICK_TEXT1)  # pick from list text

    n = input("Your Input: ")  # User Input

    match n:
        case "1":  # Measure LCR Component (WIP)
            O.Clear_CLI()
            print("Measure LCR Component")

            repeat1 = 1

            # while repeat1 == 1:
            #     O.Clear_CLI()
            #     O.TXT_Dialog()

        case "2":  # Analyze / Calculate existing Measurement
            O.Clear_CLI()
            print("Analyze / Calculate existing Measurement")

            repeat1 = 1

            while repeat1 == 1:
                O.Clear_CLI()
                O.TXT_Dialog(enum.PICK_TEXT2)
                User_Input = input("Your Input: ")  # User Input

                # 20260225, MODIFICATION, V0.0.3, LZerres: Added this to Validate User Input (when wrong it returns "FALSE")
                processedInput = P.userInputValidation(User_Input, "number")

                match processedInput:

                    case "1":  # Calculate Data and export as Excel Files
                        O.Clear_CLI()
                        print("Calculate Data and export as Excel Files")

                        Calculate_All()

                    case "2":  # Plot Data (WIP)
                        O.Clear_CLI()
                        print("Plot Data")

                        TEMP_graphAll()

                    case "3":  # Both Calculate and Plot Data (WIP)
                        O.Clear_CLI()
                        print("Both Calculate and Plot Data")

                        Calculate_All()
                        TEMP_graphAll()

                    case "99": # Go back
                        O.Clear_CLI()
                        repeat1 = 0
                        print("Exit to Main Menu")
                        time.sleep(S.Time_Delay)

                    case "FALSE": # 20260225, MODIFICATION, V0.0.3, LZerres: Added for input Validation
                        O.Wrong_Input(User_Input)

        case "3":  # Settings
            O.Clear_CLI()

            repeat1 = 1

            while repeat1 == 1:
                O.Clear_CLI()
                O.TXT_Dialog(enum.PICK_TEXT3)
                User_Input = input("Your Input: ") # User Input

                # 20260225, MODIFICATION, V0.0.3, LZerres: Added this to Validate User Input (when wrong it returns "FALSE")
                processedInput = P.userInputValidation(User_Input, "number")

                match processedInput:
                    case "1":  # Load Default Settings
                        O.Clear_CLI()
                        print("Loaded Default Settings")

                        S.Settings("Default", "Load", 0)

                        time.sleep(S.Time_Delay)

                    case "2":  # Load Custom Settings
                        O.Clear_CLI()
                        print("Loaded Custom Settings")

                        S.Settings("Custom", "Load", 0)

                        time.sleep(S.Time_Delay)

                    case "3":  # Show Current Settings
                        O.Clear_CLI()
                        print("Current Settings:\n\n")

                        S.Settings("Current", "Show", 0)

                        O.waitForKeypress()

                    case "4":  # Change Settings
                        file_path = os.path.join(Settings_Path, "Settings_Current.csv")
                        dfData = pd.read_csv(file_path, header=None, index_col=None)

                        S.Settings_Change(dfData)
                        S.Settings("Current", "Save", dfData)

                    case "5":  # Save Current Settings as Custom Settings
                        O.Clear_CLI()
                        print("Save Current Settings as Custom Settings")
                        file_path = os.path.join(Settings_Path, "Settings_Current.csv")
                        dfData = pd.read_csv(file_path, header=None, index_col=None)

                        S.Settings("Custom", "Save", dfData)

                        print("\nCurrent Settings saved as Custom Settings")
                        time.sleep(S.Time_Delay)

                    case "99": # Go back
                        O.Clear_CLI()
                        repeat1 = 0
                        print("Exit to Main Menu")
                        time.sleep(S.Time_Delay)

                    case "FALSE": # 20260225, MODIFICATION, V0.0.3, LZerres: Added for input Validation
                        O.Wrong_Input(User_Input)

        case "4":  # Connect to Oscilloscope (WIP)
            # 20260301, MODIFICATION, V0.1.0, LZerres: Added this case for connection stuff
            O.Clear_CLI()
            print("Connect to Oscilloscope")

        case "98": # About
            # 20260301, MODIFICATION, V0.1.0, LZerres: Added this case for About Text (this will be updated in the future with more info about the project)
            O.Clear_CLI()
            O.TXT_Dialog(enum.ABOUT_TEXT)
            O.waitForKeypress()

        case "99": # Exit Program
            O.Clear_CLI()
            print("Program about to DIE")
            time.sleep(S.Time_Delay)  # Short Delay for better UX
            sys.exit()