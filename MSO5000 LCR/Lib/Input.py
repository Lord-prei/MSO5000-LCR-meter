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
from    Lib.Output  import S

# --------------------------------------------------------------------------- define Paths

if True:  # define Paths
    if getattr(sys, "frozen", False):
        # Running as PyInstaller EXE
        Base_Dir = os.path.dirname(sys.executable)
        Lib_Dir = os.path.join(Base_Dir, "Lib")
    else:
        # Running as normal Python script
        Lib_Dir = os.path.dirname(os.path.abspath(__file__))
        Base_Dir = os.path.dirname(Lib_Dir)

    Settings_Path = os.path.join(Base_Dir, "Settings")
    Data_Path = os.path.join(Base_Dir, "Data")

# ---------------------------------------------------------------------------
# Here Come all of the Functions

# -------------------------------------------------- Layer 1

# Functions Layer 1

# if True:
#     print(1)

# -------------------------------------------------- Layer 2

# Functions Layer 2

# if True:
#     print(1)

# -------------------------------------------------- Layer 3

# Functions Layer 3

# if True:
#     print(1)

# ---------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------
# Here Come all of the Functions

# -------------------------------------------------- Layer 1

# Functions Layer 1

# if True:
#     print(1)

# -------------------------------------------------- Layer 2

# Functions Layer 2

# if True:
#     print(1)

# -------------------------------------------------- Layer 3

# Functions Layer 3

# if True:
#     print(1)

# ---------------------------------------------------------------------------