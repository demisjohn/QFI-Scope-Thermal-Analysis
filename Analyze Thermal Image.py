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


DataFilePath = 'media/2016-03-26 - DJ - 1mA thermal.txt'  # Can also use absolute path for ease

fig00, ax00, img00, ax01, line00  =  \
    qfi.Plot(DataFilePath, LineSlicePlot=True)      # LineSlicePlot will allow you to drag a line on the plot, and show data along that line.


# correct scale for saturated pixels:
if img00.get_clim()[1] > 1000:
    img00.set_clim( img00.get_clim()[0],  500 )


ax00.set_title(  DataFilePath.split('/')[-1]  , fontsize=8) # set plot title to datafile name
ax01.grid(True)
fig00.canvas.manager.window.raise_()    # bring window to front (for Python(X,Y).exe bug)

print('done.')




