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
import  Lib.Input   as I
import  Lib.Process as P
import  Lib.Output  as O
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

# ----------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------- Debug
# Here Come all of the Functions
# region Debug
# -------------------------------------------------- Layer 1

# Functions Layer 1
# region Functions Layer 1

def printDir():  # printing debug for paths
    if S.Debug == "yes":
        O.linePrint()
        print("All of the important Paths:\n")
        print("Base Dir = \t\t", Base_Dir)
        print("Lib Dir = \t\t", Lib_Dir)
        print("Settings Path = \t", Settings_Path)
        print("Data Path = \t\t", Data_Path)
        print("\b")
        print("End of Debug Paths")
        O.linePrint()
        O.waitForKeypress()

# 20260222, MODIFICATION, V0.0.2, LZerres: Debug messages for Calculations
def printCalc(
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
):
    if S.Debug == "yes":
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

# endregion Debug
# --------------------------------------------------------------------------- End Debug
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