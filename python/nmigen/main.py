import sys
import os 

cwd = os.getcwd()
sys.path.append(cwd)


from muxes.muxes import *
from decoder.decoder import *
from registerfile.registerfile import *

if __name__ == "__main__":
    # main_muxs()
    # main_decoders()
    main_regfile()