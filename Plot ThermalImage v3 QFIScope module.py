# -*- coding: utf-8 -*-
"""
Use QFIScope module to draw/plot arbitrary lineSlices of a saved thermal image.


Python/Spyder script
Run Configuration should either:
    Execute in Current Interpreter
        OR
    
    Execute in New Interpreter 
        AND
    Interact with shell rcompletion (for plt.show() to work)

@author: demis


"""
####################################################
# Module setup etc.
#   General Scientific Modules:
import numpy as np  # NumPy (multidimensional arrays, linear algebra, ...)
import scipy as sp  # SciPy (signal and image processing library)

import matplotlib as mpl         # Matplotlib (2D/3D plotting library)
import matplotlib.pyplot as plt  # Matplotlib's pyplot: MATLAB-like syntax
from pylab import *              # Matplotlib's pylab interface
plt.ion()                        # Turn on Matplotlib's interactive mode

####################################################

#   Other modules:
import QFIScope as qfi     # module for QFI Thermal Imaging Microscope data analysis

####################################################

print('Running...')


DataFilePath = '/Volumes/Macintosh HD/Dropbox (Praevium Research)/Cleanroom/Experiments/Active Experiments/Mid-IR (ARPA-E) Experiments/3300_metal_dot/2016-03-08 - 3300_metal_dot light-out testing_metal_only/2016-03-08 -3300_metal_dot - A65 - 12mA low temp.txt'

qfi.Plot(DataFilePath, LineSlicePlot=True)      # LineSlicePlot will allow you to drag a line on the plot, and show data along that line.


print('done.')




