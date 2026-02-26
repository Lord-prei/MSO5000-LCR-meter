# Lib for all the Process stuff

from curses.ascii import isdigit
import  sys
import  os
import  time
import  subprocess
import  math
import  pyvisa
import  msvcrt
from    hmac        import new
from    types       import new_class
from    calendar    import c
from    re          import DEBUG
from    turtle      import clear
from    enum        import Enum
import  pandas      as pd
import  matplotlib.pyplot as plt
import  numpy       as np
import  Lib.Input   as I
import  Lib.Output  as O
from    Lib.Output  import S

# --------------------------------------------------------------------------- Variables

# -------------------------------------------------- Settings Variables
Rounded =           0  # Decimal places for rounding
Time_Delay =        0  # Time Delay for better UX
Debug =             0  # Debug Variable
Debug_Calc =        0  # Debug Variable for Calculations
Number_Display =    0  # Variable for Displaying Numbers in different formats (Normal, Eng, SI)

# --------------------------------------------------------------------------- define Paths

# define Paths
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

# --------------------------------------------------------------------------- Init

file_path =     os.path.join(Settings_Path, "Settings_Default.xlsx")
dfSettings =    pd.read_excel(file_path, header=None, index_col=None)

# --------------------------------------------------------------------------- Math
# Here Come all of the Functions

# -------------------------------------------------- Layer 1

# Functions Layer 1

def Impedance_Calculation(Rounded):  # Main Function for Calculating Everything

    # Reading Data from Excel File and preparing variables
    file_path = os.path.join(Data_Path, "Clean.xlsx")   # Cleaned data from MSO5000
    dfCal = pd.read_excel(file_path)                    # Cleaned data from MSO5000
    dfCalRounded = dfCal.copy()                         # Copy of dataframe for rounded values
    Xmax = dfCal.shape[1]                               # Number of columns
    Ymax = dfCal.shape[0] - 1                           # Number of rows
    X = 0
    Y = 0

    # Debug Messages
    if Debug == "yes":
        print("Xmax =", Xmax)
        print("Ymax =", Ymax)

    print("\nCalculating...")

    # Remove the old float64 column
    dfCal.drop(dfCal.columns[X + 6], axis=1, inplace=True)
    dfCalRounded.drop(dfCalRounded.columns[X + 6], axis=1, inplace=True)

    # Insert a new complex column at the same position as a Complex number
    dfCal.insert(
        X + 6,
        f"Z_[Ω]",
        pd.Series(np.zeros(len(dfCal), dtype=np.complex128), index=dfCal.index),
    )
    dfCalRounded.insert(
        X + 6,
        f"Z_[Ω]",
        pd.Series(
            np.zeros(len(dfCalRounded), dtype=np.complex128),
            index=dfCalRounded.index,
        ),
    )

    while Y <= Ymax:
        (
            Voltage_Ue,
            Rounded_Voltage_Ue,
            Voltage_Ua,
            Rounded_Voltage_Ua,
            Current,
            Rounded_Current,
            Frequenzy,
            Rounded_Frequeny,
            PhaseOffset,
            Rounded_PhaseOffset,
            Impedance_abs,
            Rounded_Impedance_abs,
            Resistance,
            Rounded_Resistance,
            Blind,
            Rounded_Blind,
            Impedance,
            Rounded_Impedance,
            H,
            Rounded_H,
            H_db,
            Rounded_H_db,
        ) = Calc_All(
            Rounded, dfCal, Y, X
        )  # Calculate everything

        # 20260222, MODIFICATION, V0.0.1, LZerres: Added Debug Messages for Calculations, so you can see what is calculated in each step
        if (Debug == "yes") and (Debug_Calc == "yes"):
            O.dprintCalc(
                X,
                Y,
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
            )

        Save_All(
            dfCal,
            dfCalRounded,
            X,
            Y,
            Voltage_Ue,
            Rounded_Voltage_Ue,
            Voltage_Ua,
            Rounded_Voltage_Ua,
            Current,
            Rounded_Current,
            Frequenzy,
            Rounded_Frequeny,
            PhaseOffset,
            Rounded_PhaseOffset,
            Impedance_abs,
            Rounded_Impedance_abs,
            Resistance,
            Rounded_Resistance,
            Blind,
            Rounded_Blind,
            Impedance,
            Rounded_Impedance,
            H,
            Rounded_H,
            H_db,
            Rounded_H_db,
        )  # Save everything

        Y += 1  # Next Row

    # Creating Excel File with Calculated Data

    # Exporting calculated data to Excel File
    file_path = os.path.join(Data_Path, "Clean_Calc.xlsx")
    dfCal.to_excel(file_path, index=False)

    # Exporting calculated data to Excel File
    file_path = os.path.join(Data_Path, "Clean_Calc_Rounded.xlsx")
    dfCalRounded.to_excel(file_path, index=False)


# -------------------------------------------------- Layer 2

# Functions Layer 2

def Calc_All(Rounded, dfCal, Y, X):
    Voltage_Ue, Rounded_Voltage_Ue = Read_Voltage_Ue(
    Rounded, dfCal, Y, X
    )  # reading Voltage Ue

    Voltage_Ua, Rounded_Voltage_Ua = Read_Voltage_Ua(
        Rounded, dfCal, Y, X
    )  # reading Voltage Ua

    Current, Rounded_Current = Read_Current(Rounded, dfCal, Y, X)  # reading Current
    Frequenzy, Rounded_Frequeny = Read_Frequenzy(
        Rounded, dfCal, Y, X
    )  # reading Frequenzy

    PhaseOffset, Rounded_PhaseOffset = Read_PhaseOffset(
        Rounded, dfCal, Y, X
    )  # reading Phaseoffset

    Impedance_abs, Rounded_Impedance_abs = Calc_Impedance(
        Rounded, dfCal, Y, X
    )  # calculating impedanc

    Resistance, Rounded_Resistance = Calc_Resistance(
        Rounded, dfCal, Y, X
    )  # calculating resistance

    Blind, Rounded_Blind = Calc_Blind(
        Rounded, dfCal, Y, X
    )  # calculating blindwiderstand

    Impedance, Rounded_Impedance = Calc_Impedanz_Complex(
        Rounded, dfCal, Y, X
    )  # calculating complex impedance

    H, Rounded_H = Calc_Transferfunction_1(
        Rounded, dfCal, Y, X
    )  # calculating transferfunction 1

    H_db, Rounded_H_db = Calc_Transferfunction_db(
        Rounded, dfCal, Y, X
    )  # calculating transferfunction db

    return (
        Voltage_Ue,
        Rounded_Voltage_Ue,
        Voltage_Ua,
        Rounded_Voltage_Ua,
        Current,
        Rounded_Current,
        Frequenzy,
        Rounded_Frequeny,
        PhaseOffset,
        Rounded_PhaseOffset,
        Impedance_abs,
        Rounded_Impedance_abs,
        Resistance,
        Rounded_Resistance,
        Blind,
        Rounded_Blind,
        Impedance,
        Rounded_Impedance,
        H,
        Rounded_H,
        H_db,
        Rounded_H_db,
    )

def Save_All(
    dfCal,
    dfCalRounded,
    X,
    Y,
    Voltage_Ue,
    Rounded_Voltage_Ue,
    Voltage_Ua,
    Rounded_Voltage_Ua,
    Current,
    Rounded_Current,
    Frequenzy,
    Rounded_Frequeny,
    PhaseOffset,
    Rounded_PhaseOffset,
    Impedance_abs,
    Rounded_Impedance_abs,
    Resistance,
    Rounded_Resistance,
    Blind,
    Rounded_Blind,
    Impedance,
    Rounded_Impedance,
    H,
    Rounded_H,
    H_db,
    Rounded_H_db,
):

    dfCal, dfCalRounded = Save_Voltage_Ue(
        dfCal, dfCalRounded, X, Y, Voltage_Ue, Rounded_Voltage_Ue
    ) # Saving Voltage Ue

    dfCal, dfCalRounded = Save_Voltage_Ua(
        dfCal, dfCalRounded, X, Y, Voltage_Ua, Rounded_Voltage_Ua
    ) # Saving Voltage Ua

    dfCal, dfCalRounded = Save_Current(
        dfCal, dfCalRounded, X, Y, Current, Rounded_Current
    ) # Saving Current

    dfCal, dfCalRounded = Save_Frequenzy(
        dfCal, dfCalRounded, X, Y, Frequenzy, Rounded_Frequeny
    ) # Saving Frequenzy

    dfCal, dfCalRounded = Save_PhaseOffset(
        dfCal, dfCalRounded, X, Y, PhaseOffset, Rounded_PhaseOffset
    ) # Saving Phase Offset

    dfCal, dfCalRounded = Save_Impedance(
        dfCal, dfCalRounded, X, Y, Impedance_abs, Rounded_Impedance_abs
    ) # Saving Impedance

    dfCal, dfCalRounded = Save_Resistance(
        dfCal, dfCalRounded, X, Y, Resistance, Rounded_Resistance
    ) # Saving Resistance

    dfCal, dfCalRounded = Save_Blind(
        dfCal, dfCalRounded, X, Y, Blind, Rounded_Blind
    ) # Saving Blindwiderstand

    dfCal, dfCalRounded = Save_Impedanz_Complex(
        dfCal, dfCalRounded, X, Y, Impedance, Rounded_Impedance
    ) # Saving Complex Impedance

    dfCal, dfCalRounded = Save_Transferfunction_1(
        dfCal, dfCalRounded, X, Y, H, Rounded_H
    ) # Saving Transferfunction 1

    dfCal, dfCalRounded = Save_Transferfunction_db(
        dfCal, dfCalRounded, X, Y, H_db, Rounded_H_db
    )# Saving Transferfunction db

    return dfCal, dfCalRounded

# -------------------------------------------------- Layer 3

# Functions Layer 3

# Functions for Reading Values from Dataframe and Calculating stuff
def Read_Voltage_Ue(Rounded, dfCal, Y, X):
    Voltage_Ue = dfCal.iloc[Y, X]  # reading Voltage Ue
    Rounded_Voltage_Ue = Round_Sig(Voltage_Ue, Rounded)
    return Voltage_Ue, Rounded_Voltage_Ue

def Read_Voltage_Ua(Rounded, dfCal, Y, X):
    Voltage_Ua = dfCal.iloc[Y, X + 1]  # reading Voltage UA
    Rounded_Voltage_Ua = Round_Sig(Voltage_Ua, Rounded)
    return Voltage_Ua, Rounded_Voltage_Ua

def Read_Current(Rounded, dfCal, Y, X):
    Current = dfCal.iloc[Y, X + 2]  # reading Current
    Rounded_Current = Round_Sig(Current, Rounded)
    return Current, Rounded_Current

def Read_Frequenzy(Rounded, dfCal, Y, X):
    Frequenzy = dfCal.iloc[Y, X + 3]  # reading Frequency
    Rounded_Frequeny = Round_Sig(Frequenzy, Rounded)
    return Frequenzy, Rounded_Frequeny

def Read_PhaseOffset(Rounded, dfCal, Y, X):
    PhaseOffset = dfCal.iloc[Y, X + 4]  # reading Phase Offset
    Rounded_PhaseOffset = Round_Sig(PhaseOffset, Rounded)
    return PhaseOffset, Rounded_PhaseOffset

def Calc_Impedance(Rounded, dfCal, Y, X):
    Voltage_Ue, Rounded_Voltage_Ue = Read_Voltage_Ue(
        Rounded, dfCal, Y, X
    )  # reading Voltage
    Current, Rounded_Current = Read_Current(Rounded, dfCal, Y, X)  # reading Current

    Impedance_abs = Voltage_Ue / Current  # Calculating Impedance in Ohm
    Rounded_Impedance_abs = Round_Sig(Impedance_abs, Rounded)
    return Impedance_abs, Rounded_Impedance_abs

def Calc_Resistance(Rounded, dfCal, Y, X):
    PhaseOffset, Rounded_PhaseOffset = Read_PhaseOffset(
        Rounded, dfCal, Y, X
    )  # reading Phaseoffset
    Impedance_abs, Rounded_Impedance_abs = Calc_Impedance(
        Rounded, dfCal, Y, X
    )  # calculating impedanc

    Resistance = (
        math.cos(math.radians(PhaseOffset)) * Impedance_abs
    )  # Calculating Resistance in Ohm
    Rounded_Resistance = Round_Sig(Resistance, Rounded)
    return Resistance, Rounded_Resistance

def Calc_Blind(Rounded, dfCal, Y, X):
    PhaseOffset, Rounded_PhaseOffset = Read_PhaseOffset(
        Rounded, dfCal, Y, X
    )  # reading Phaseoffset
    Impedance_abs, Rounded_Impedance_abs = Calc_Impedance(
        Rounded, dfCal, Y, X
    )  # calculating impedanc

    Blind = (
        math.sin(math.radians(PhaseOffset)) * Impedance_abs
    )  # Calculating Blindwiderstand in Ohm
    Rounded_Blind = Round_Sig(Blind, Rounded)
    return Blind, Rounded_Blind

def Calc_Impedanz_Complex(Rounded, dfCal, Y, X):
    Resistance, Rounded_Resistance = Calc_Resistance(Rounded, dfCal, Y, X)
    Blind, Rounded_Blind = Calc_Blind(Rounded, dfCal, Y, X)

    Impedance = complex(Resistance, Blind)
    Rounded_Impedance = Rounded_Resistance + Rounded_Blind * 1j
    return Impedance, Rounded_Impedance

def Calc_Transferfunction_1(Rounded, dfCal, Y, X):
    Voltage_Ue, Rounded_Voltage_Ue = Read_Voltage_Ue(Rounded, dfCal, Y, X)
    Voltage_Ua, Rounded_Voltage_Ua = Read_Voltage_Ua(Rounded, dfCal, Y, X)

    H = Voltage_Ua / Voltage_Ue
    Rounded_H = Round_Sig(Voltage_Ua / Voltage_Ue, Rounded)
    return H, Rounded_H

def Calc_Transferfunction_db(Rounded, dfCal, Y, X):
    Voltage_Ue, Rounded_Voltage_Ue = Read_Voltage_Ue(Rounded, dfCal, Y, X)
    Voltage_Ua, Rounded_Voltage_Ua = Read_Voltage_Ua(Rounded, dfCal, Y, X)

    H = Voltage_Ua / Voltage_Ue
    Rounded_H = Round_Sig(Voltage_Ua / Voltage_Ue, Rounded)

    H_db = 20 * math.log10(abs(H))
    Rounded_H_db = Round_Sig(H_db, Rounded)
    return H_db, Rounded_H_db

# Functions for Saving Values to Dataframe
def Save_Voltage_Ue(dfCal, dfCalRounded, X, Y, Voltage_Ue, Rounded_Voltage_Ue):
    dfCal.iloc[Y, X] = Voltage_Ue  # Storing Voltage Ue in V
    dfCalRounded.iloc[Y, X] = Rounded_Voltage_Ue
    return dfCal, dfCalRounded

def Save_Voltage_Ua(dfCal, dfCalRounded, X, Y, Voltage_Ua, Rounded_Voltage_Ua):
    dfCal.iloc[Y, X + 1] = Voltage_Ua  # Storing Voltage Ua in V
    dfCalRounded.iloc[Y, X + 1] = Rounded_Voltage_Ua
    return dfCal, dfCalRounded

def Save_Current(dfCal, dfCalRounded, X, Y, Current, Rounded_Current):
    dfCal.iloc[Y, X + 2] = Current  # Storing Current in A
    dfCalRounded.iloc[Y, X + 2] = Rounded_Current
    return dfCal, dfCalRounded

def Save_Frequenzy(dfCal, dfCalRounded, X, Y, Frequenzy, Rounded_Frequeny):
    dfCal.iloc[Y, X + 3] = Frequenzy
    dfCalRounded.iloc[Y, X + 3] = Rounded_Frequeny
    return dfCal, dfCalRounded

def Save_PhaseOffset(dfCal, dfCalRounded, X, Y, PhaseOffset, Rounded_PhaseOffset):
    dfCal.iloc[Y, X + 4] = PhaseOffset
    dfCalRounded.iloc[Y, X + 4] = Rounded_PhaseOffset
    return dfCal, dfCalRounded

def Save_Impedance(dfCal, dfCalRounded, X, Y, Impedance, Rounded_Impedance):
    dfCal.iloc[Y, X + 5] = Impedance
    dfCalRounded.iloc[Y, X + 5] = Rounded_Impedance
    return dfCal, dfCalRounded

def Save_Resistance(dfCal, dfCalRounded, X, Y, Resistance, Rounded_Resistance):
    dfCal.iloc[Y, X + 7] = Resistance
    dfCalRounded.iloc[Y, X + 7] = Rounded_Resistance
    return dfCal, dfCalRounded

def Save_Blind(dfCal, dfCalRounded, X, Y, Blind, Rounded_Blind):
    dfCal.iloc[Y, X + 8] = Blind
    dfCalRounded.iloc[Y, X + 8] = Rounded_Blind
    return dfCal, dfCalRounded

def Save_Impedanz_Complex(dfCal, dfCalRounded, X, Y, Impedance, Rounded_Impedance):
    dfCal.iloc[Y, X + 6] = Impedance
    dfCalRounded.iloc[Y, X + 6] = Rounded_Impedance
    return dfCal, dfCalRounded

def Save_Transferfunction_1(dfCal, dfCalRounded, X, Y, H, Rounded_H):
    dfCal.iloc[Y, X + 9] = H
    dfCalRounded.iloc[Y, X + 9] = Rounded_H
    return dfCal, dfCalRounded

def Save_Transferfunction_db(dfCal, dfCalRounded, X, Y, H_db, Rounded_H_db):
    dfCal.iloc[Y, X + 10] = H_db
    dfCalRounded.iloc[Y, X + 10] = Rounded_H_db
    return dfCal, dfCalRounded

# -------------------------------------------------- Layer 4

# Functions Layer 4

def select_number_format(x):
    match Number_Display:
        case "normal":
            return Round_Sig(x, Rounded)
        case "eng":
            return eng(x)
        case "si":
            return si_prefix(x)

# -------------------------------------------------- Layer 5

# Functions Layer 5

def Round_Sig(x, Rounded):
    if x == 0:
        return 0
    return round(x, Rounded - 1 - int(math.floor(math.log10(abs(x)))))

# 20260222, MODIFICATION, V0.0.2, LZerres: Added convert a number to engineering notation
def eng(x):  # Normal to Engineering Notation Converter
    precision = Rounded

    # Handle zero as a special case to avoid log10 issues
    if x == 0:
        return f"{0:.{precision}f}"

    # Calculate exponent and mantissa for engineering notation
    exp = int(math.floor(math.log10(abs(x)) / 3) * 3)   # Round exponent to nearest multiple of 3
    mantissa = x / (10**exp)                            # Calculate mantissa

    # limit to ±999.999 mantissa
    return f"{mantissa:.{precision}f}e{exp:+03d} "

# 20260222, MODIFICATION, V0.0.2, LZerres: Added a converter for normal to si prefixes
def si_prefix(x):  # Normal to SI Prefix Converter

    # Reading SI Prefixes from Excel File and preparing variables
    filepath = os.path.join(Settings_Path, "SI_Prefixes.xlsx")
    dfPrefix = pd.read_excel(filepath, header=None, index_col=None)
    Xmax = dfPrefix.shape[1]  # Number of columns
    Ymax = dfPrefix.shape[0] - 1  # Number of rows
    X = 0
    Y = 0

    precision = Rounded

    # Handle zero as a special case to avoid log10 issues
    if x == 0:
        return f"{0:.{precision}f}"

    # Calculate exponent and mantissa for engineering notation
    exp = int(math.floor(math.log10(abs(x)) / 3) * 3)   # Round exponent to nearest multiple of 3
    mantissa = x / (10**exp)                            # Calculate mantissa

    # Find the SI prefix for the exponent from the Excel file
    while Y <= Ymax:
        if dfPrefix.iloc[Y, 2] == exp:
            prefix = dfPrefix.iloc[Y, 1]
            if prefix == "none":
                prefix = ""
            break
        Y += 1

    # limit to ±999.precision mantissa
    return f"{mantissa:.{precision}f} {prefix}"

# --------------------------------------------------------------------------- End Math
# ----------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------- Settings
# Here Come all of the Functions

# -------------------------------------------------- Layer 1

# Functions Layer 1

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


# -------------------------------------------------- Layer 2

# Functions Layer 2

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
        O.TXT_Dialog(S.PICK_TEXT_SETTINGS)
        User_Input = input("Your Input: ")

        match User_Input:
            case "1":  # Change Decimal Places
                O.Clear_CLI()
                print("Change Decimal Places")
                New_Value = input("Enter new value (Current: " + str(Rounded) + "): ")
                Rounded = int(New_Value)
                dfData.iloc[0, 1] = Rounded
                print("Decimal Places changed to: ", Rounded)
                print("\n\ndo you wana change more settings?")
                again = int(input("2 = yes / 1 = no: ")) - 1

            case "2":  # Change Time Delay
                O.Clear_CLI()
                print("Change Time Delay")
                New_Value = input("Enter new value (Current: " + str(Time_Delay) + "s): ")
                Time_Delay = float(New_Value)
                dfData.iloc[1, 1] = Time_Delay
                print("Time Delay changed to: ", Time_Delay, "s")
                print("\n\ndo you wana change more settings?")
                again = int(input("2 = yes / 1 = no: ")) - 1

            case "3":  # Debug Messages
                O.Clear_CLI()
                print("Do u want Debug Messages")
                New_Value = input("Enter new value (Current: " + str(Debug) + ") (2 = Yes/ 1 = No): ")

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
                again = int(input("2 = yes / 1 = no: ")) - 1

            # 20260222, MODIFICATION, V0.0.2, LZerres: Added new setting for Debug Messages for Calculations
            case "4":  # Debug Calc Messages
                O.Clear_CLI()
                print("Do u want Debug Messages")
                New_Value = input("Enter new value (Current: " + str(Debug_Calc) + ") (2 = Yes / 1 = No): ")

                if New_Value == "1":
                    New_Value = "no"
                elif New_Value == "2":
                    New_Value = "yes"

                if (New_Value == "yes") or (New_Value == "no"):
                    Debug_Calc = str(New_Value)
                    dfData.iloc[3, 1] = Debug_Calc
                    print("Debug Messages changed to: ", Debug_Calc)
                print("\n\ndo you wana change more Settings?")
                again = int(input("2 = yes / 1 = no: ")) - 1

            # 20260222, MODIFICATION, V0.0.2, LZerres: Added new Setting for Number Display Format (Normal, Eng, SI) and added this to the settings menu
            case "5":  # Number Display Format
                O.Clear_CLI()
                print("Do u want Debug Messages")
                New_Value = input("Enter new value (Current: " + str(Number_Display) + ") (3 = SI / 2 = ENG / 1 = NORMAL): ")

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
                again = int(input("2 = yes / 1 = no: ")) - 1

            case "99":  # Go back
                O.Clear_CLI()
                again = 0
                print("Go back")
                time.sleep(Time_Delay)

# -------------------------------------------------- Layer 3

# Functions Layer 3



# --------------------------------------------------------------------------- End Settings
# ----------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------- Excel
# Here Come all of the Functions

# -------------------------------------------------- Layer 1

# Functions Layer 1

def createExcel(type, lenght, name):
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

# -------------------------------------------------- Layer 2

# Functions Layer 2



# -------------------------------------------------- Layer 3

# Functions Layer 3



# --------------------------------------------------------------------------- End Excel
# ----------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------- Process
# Here Come all of the Functions

# -------------------------------------------------- Layer 1

# Functions Layer 1

# 20260225, MODIFICATION, V0.0.3, LZerres: 
def userInputValidation(input, type):
    match type:
        case "number":

            check = checkUserInputNumber(input)

            if check == "TRUE":
                return input
            elif check == "FALSE":
                return check

# -------------------------------------------------- Layer 2

# Functions Layer 2

# 20260225, MODIFICATION, V0.0.3, LZerres: Added this function to check user input for being a number, so you can prevent errors if the user enters a wrong input
def checkUserInputNumber(input):
    if input.isdigit(): # Check if input is a number (excluds floating and negative numbers)
        if Debug == "yes":
            print(f"good boy ;) {input}")
        return "TRUE"
    if Debug == "yes":
        print(f"bad boy {input}")
    return "FALSE"

# -------------------------------------------------- Layer 3

# Functions Layer 3



# --------------------------------------------------------------------------- End Process
# ----------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------
# Here Come all of the Functions

# -------------------------------------------------- Layer 1

# Functions Layer 1



# -------------------------------------------------- Layer 2

# Functions Layer 2



# -------------------------------------------------- Layer 3

# Functions Layer 3



# ---------------------------------------------------------------------------