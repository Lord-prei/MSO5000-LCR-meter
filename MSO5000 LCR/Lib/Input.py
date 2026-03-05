# Lib for all the Input stuff

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
import  Lib.Process as P
import  Lib.Output  as O
from    Lib.Output  import enum

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

# --------------------------------------------------------------------------- Excel
# Here Come all of the Functions
# region Functions

# -------------------------------------------------- Layer 1

# Functions Layer 1
# region Functions Layer 1

# 20260301, MODIFICATION, V0.1.1, LZerres: Function to import Excel file, returns a DataFrame
def Import_Excel(fileFolderPath, fileName):
    filePath = os.path.join(fileFolderPath, fileName)
    dfExcel = pd.read_excel(filePath)
    return dfExcel

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
# --------------------------------------------------------------------------- Excel
# ----------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------- Calculations
# Here Come all of the Functions
# region Functions

# -------------------------------------------------- Layer 1

# Functions Layer 1
# region Functions Layer 1

def Read_Voltage_Ue(dfCal, X, Y):
    Voltage_Ue = dfCal.iloc[Y, X]  # reading Voltage Ue

    return Voltage_Ue

def Read_Voltage_Ua(dfCal, X, Y):
    Voltage_Ua = dfCal.iloc[Y, X + 1]  # reading Voltage UA

    return Voltage_Ua

def Read_Current(dfCal, X, Y):
    Current = dfCal.iloc[Y, X + 2]  # reading Current

    return Current

def Read_Frequenzy(dfCal, X, Y):
    Frequenzy = dfCal.iloc[Y, X + 3]  # reading Frequency

    return Frequenzy

def Read_PhaseOffset(dfCal, X, Y):
    PhaseOffset = dfCal.iloc[Y, X + 4]  # reading Phase Offset

    return PhaseOffset

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