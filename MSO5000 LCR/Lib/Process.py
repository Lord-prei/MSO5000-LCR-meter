# Lib for all the Process stuff

from    curses.ascii import isdigit
import re
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
from    enum        import IntEnum
import  pandas      as pd
import  matplotlib.pyplot as plt
import  numpy       as np
import  Lib.Debug   as D
import  Lib.Settings as S
from    Lib.Output  import enum


# --------------------------------------------------------------------------- Variables

class GC(IntEnum): #Graphing Constants
    # For Graphing
    VOLTAGE_UE =            0   # Voltage for Graphing
    VOLTAGE_UA =            1   # Voltage for Graphing
    CURRENT_IE =            2   # Current for Graphing
    FREQUENCY =             3   # Frequency for Graphing
    PHASE_OFFSET_TOT =      4   # Phase Offset for Graphing
    IMPEDANCE_ABS =         5   # Impedance for Graphing
    IMPEDANCE =             6   # Complex Impedance for Graphing
    RESISTANCE =            7   # Resistance for Graphing
    BLIND =                 8   # Blindwiderstand for Graphing
    PHASE_OFFSET_H =        9   # Phase Offset H for Graphing
    TRANSFER_FUNCTION =     10  # Transfer Function for Graphing
    TRANSFER_FUNCTION_LOG = 11  # Transfer Function in dB for Graphing

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

# --------------------------------------------------------------------------- Init

# Init
# region Init

file_path =     os.path.join(Settings_Path, "Settings_Default.CSV")

# Reading SI Prefixes from Excel File and preparing variables
filepath = os.path.join(Settings_Path, "SI_Prefixes.CSV")
dfPrefix = pd.read_csv(filepath, header=None, index_col=None)

# endregion Init

# --------------------------------------------------------------------------- Math
# Here Come all of the Functions
# region Math

# -------------------------------------------------- Layer 1

# Functions Layer 1
# region Functions Layer 1

# Functions for Reading Values from Dataframe and Calculating stuff

def Calc_Impedance(Voltage_Ue, Current):
    Impedance_abs = Voltage_Ue / Current  # Calculating Impedance in Ohm
    return Impedance_abs

def Calc_Resistance(PhaseOffset, Impedance_abs):
    Resistance = (math.cos(math.radians(PhaseOffset)) * Impedance_abs)  # Calculating Resistance in Ohm
    return Resistance

def Calc_Blind(PhaseOffset, Impedance_abs):
    Blind = (math.sin(math.radians(PhaseOffset)) * Impedance_abs)  # Calculating Blindwiderstand in Ohm
    return Blind

def Calc_Impedanz_Complex(Resistance, Blind):
    Impedance = complex(Resistance, Blind)
    return Impedance

def Calc_Transferfunction_1(Voltage_Ua, Voltage_Ue):
    H = Voltage_Ua / Voltage_Ue
    return H

def Calc_Transferfunction_db(Voltage_Ua, Voltage_Ue):
    H = Voltage_Ua / Voltage_Ue
    H_db = 20 * math.log10(abs(H))
    return H_db

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

def Save_Phase_Offset_H(dfCal, dfCalRounded, X, Y, Phase_Offset_H, Rounded_Phase_Offset_H):
    dfCal.iloc[Y, X + 9] = Phase_Offset_H
    dfCalRounded.iloc[Y, X + 8] = Rounded_Phase_Offset_H
    return dfCal, dfCalRounded

def Save_Transferfunction_1(dfCal, dfCalRounded, X, Y, H, Rounded_H):
    dfCal.iloc[Y, X + 10] = H
    dfCalRounded.iloc[Y, X + 9] = Rounded_H
    return dfCal, dfCalRounded

def Save_Transferfunction_db(dfCal, dfCalRounded, X, Y, H_db, Rounded_H_db):
    dfCal.iloc[Y, X + 11] = H_db
    dfCalRounded.iloc[Y, X + 10] = Rounded_H_db
    return dfCal, dfCalRounded

# endregion Functions Layer 1

# -------------------------------------------------- Layer 2

# Functions Layer 2
# region Functions Layer 2

def select_number_format(x):
    match S.Number_Display:
        case "normal":
            return Round_Sig(x, S.Rounded)
        case "eng":
            return eng(x)
        case "si":
            return si_prefix(x)

# endregion Functions Layer 2

# -------------------------------------------------- Layer 3

# Functions Layer 3
# region Functions Layer 3

def Round_Sig(x, Rounded):
    if x == 0:
        return 0
    return round(x, Rounded - 1 - int(math.floor(math.log10(abs(x)))))

# 20260222, MODIFICATION, V0.0.2, LZerres: Added convert a number to engineering notation
def eng(x):  # Normal to Engineering Notation Converter
    precision = S.Rounded

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

    global dfPrefix
    Xmax = dfPrefix.shape[1]  # Number of columns
    Ymax = dfPrefix.shape[0] - 1  # Number of rows
    X = 0
    Y = 1

    precision = S.Rounded

    # Handle zero as a special case to avoid log10 issues
    if x == 0:
        return f"{0:.{precision}f}"

    # Calculate exponent and mantissa for engineering notation
    exp = int(math.floor(math.log10(abs(x)) / 3) * 3)   # Round exponent to nearest multiple of 3
    mantissa = x / (10**exp)                            # Calculate mantissa

    # Find the SI prefix for the exponent from the Excel file
    while Y <= Ymax:
        factor = int(dfPrefix.iloc[Y, 2])
        if factor == exp:
            prefix = dfPrefix.iloc[Y, 1]
            if prefix == "none":
                prefix = ""
            break
        Y += 1

    # limit to ±999.precision mantissa
    return f"{mantissa:.{precision}f} {prefix}"

# endregion Functions Layer 3

# endregion Math
# --------------------------------------------------------------------------- End Math
# ----------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------- Process
# Here Come all of the Functions
# region Process

# -------------------------------------------------- Layer 1

# Functions Layer 1
# region Functions Layer 1

# 20260225, MODIFICATION, V0.0.3, LZerres: Added this function to validate user input, so you can prevent errors if the user enters a wrong input
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

# endregion Functions Layer 1

# -------------------------------------------------- Layer 2

# Functions Layer 2
# region Functions Layer 2

# 20260225, MODIFICATION, V0.0.3, LZerres: Added this function to check user input for being a number, so you can prevent errors if the user enters a wrong input
def checkUserInputNumber(input):
    if input.isdigit(): # Check if input is a number (excluds floating and negative numbers)
        if S.Debug == "yes":
            print(f"good boy ;) {input}")
        return "TRUE"
    if S.Debug == "yes":
        print(f"bad boy {input}")
    return "FALSE"

def checkUserInputFloat(input):
    try:
        float(input)
        return "TRUE"
    except ValueError:
        return "FALSE"

# endregion Functions Layer 2

# -------------------------------------------------- Layer 3

# Functions Layer 3
# region Functions Layer 3

# Code for Functions Layer 3

# endregion Functions Layer 3

# endregion Process
# --------------------------------------------------------------------------- End Process
# ----------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------- Graphing
# Here Come all of the Functions
# region Functions

# -------------------------------------------------- Layer 1

# Functions Layer 1
# region Functions Layer 1

# 20260318, MODIFICATION, V0.1.3, LZerres: Added to select the axis name for the graph
def selectGraphSettings(X, Y):

    #selecting the X axis
    match X:
        case GC.VOLTAGE_UE:
            axisNameX = "Voltage Ue in [V]"

        case GC.VOLTAGE_UA:
            axisNameX = "Voltage Ua in [V]"

        case GC.CURRENT_IE:
            axisNameX = "Current Ie in [A]"

        case GC.FREQUENCY:
            axisNameX = "Frequency in [Hz]"

        case GC.PHASE_OFFSET_TOT:
            axisNameX = "Phase Offset Total in [°]"

        case GC.IMPEDANCE_ABS:
            axisNameX = "Impedance Absolute in [Ω]"

        case GC.IMPEDANCE:
            axisNameX = "Impedance Complex in [Ω]"

        case GC.RESISTANCE:
            axisNameX = "Resistance in [Ω]"

        case GC.BLIND:
            axisNameX = "Blindwiderstand in [Ω]"

        case GC.PHASE_OFFSET_H:
            axisNameX = "Phase Offset H in [°]"

        case GC.TRANSFER_FUNCTION:
            axisNameX = "Transfer Function H"

        case GC.TRANSFER_FUNCTION_LOG:
            axisNameX = "Transfer Function H in dB"

    #selecting the Y axis
    match Y:
        case GC.VOLTAGE_UE:
            axisNameY = "Voltage Ue in [V]"

        case GC.VOLTAGE_UA:
            axisNameY = "Voltage Ua in [V]"

        case GC.CURRENT_IE:
            axisNameY = "Current Ie in [A]"

        case GC.FREQUENCY:
            axisNameY = "Frequency in [Hz]"

        case GC.PHASE_OFFSET_TOT:
            axisNameY = "Phase Offset Total in [°]"

        case GC.IMPEDANCE_ABS:
            axisNameY = "Impedance Absolute in [Ω]"

        case GC.IMPEDANCE:
            axisNameY = "Impedance Complex in [Ω]"

        case GC.RESISTANCE:
            axisNameY = "Resistance in [Ω]"

        case GC.BLIND:
            axisNameY = "Blindwiderstand in [Ω]"

        case GC.PHASE_OFFSET_H:
            axisNameY = "Phase Offset H in [°]"

        case GC.TRANSFER_FUNCTION:
            axisNameY = "Transfer Function H"

        case GC.TRANSFER_FUNCTION_LOG:
            axisNameY = "Transfer Function H in dB"

    return axisNameX, axisNameY


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
# --------------------------------------------------------------------------- End Graphing
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