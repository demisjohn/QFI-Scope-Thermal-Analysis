# README #

## Project Purpose ##

A Module to let users drag a line on a pcolormesh plot & plot the data values along that line on a separate axis.
See `help(LineSlice)` for examples on usage.

### Examples ###

The following script pops up a plot of the thermal image, with interactive dragging to show a line-slice along the dragged line:

```
#!python

import QFIScope as qfi     # module for QFI Thermal Imaging Microscope data analysis

DataFilePath = '2016-03-02 - QFI thermal image data - 1.5mA med temp.txt'

qfi.Plot(DataFilePath, LineSlicePlot=True, hold=True)
```

The resulting interactive plot, with data plotted along the dragged line:
![Screen Shot 2016-03-29 at 3.27.25 PM.png](https://bitbucket.org/repo/j86bp8/images/784973820-Screen%20Shot%202016-03-29%20at%203.27.25%20PM.png)