# -*- coding: utf-8 -*-
"""
QFIScope

A Module to let users drag a line on a pcolormesh plot & plot the data values along that line on a separate axis.
See `help(LineSlice)` for examples on usage.

"""
__version = "v2.0"
__author = "Demis D. John"

####################################################
# Module setup etc.

import numpy as np  # NumPy (multidimensional arrays, linear algebra, ...)
import matplotlib.pyplot as plt  # Matplotlib's pyplot: MATLAB-like syntax

####################################################


# Handle mouse clicks on the plot:
class LineSlice:
    '''Allow user to drag a line on a pcolormesh plot, and plot the Z values from that line on a separate axis.
    
    Example Usage
    -------------
    fig, (ax1, ax2) = pyplot.subplots( nrows=2 )    # one figure, two axes
    img = ax1.pcolormesh( x, y, Z )                 # pcolormesh on the 1st axis
    lntr = LineSlice( img, ax2 )                    # Connect the LineSlice object
    
    Arguments
    ---------
    img: the pcolor/pcolormesh plot to extract data from and that the User's clicks will be recorded for.  Should be a `QuadMesh` object, as returned by `matplotlib/pcolormesh()`.
    
    ax2: the axis on which to plot the data values along the dragged line.  You should create this axis before instantiating this class/object.

    hold : { True | False }, optional
        Clear a previously plotted LineSlice on `ax2` before plotting a new one?  `hold=True` will retain the previously plotted lines. Defaults to False.
        
    img_kwargs : dictionary of optional arguments to pass to the marker plots on the pcolormesh plot. (Eg. `markerstyle` etc.)
    
    ax_kwargs : dictionary of optional arguments to pass to the LineSlice plot on ax2. (Eg. `linewidth` etc.)
    
    '''
    def __init__(self, img, ax, hold=False, img_kwargs={}, ax_kwargs={}):
        '''
        img: the pcolormesh instance to get data from/that user should click on
        ax: the axis to plot the line trace on
        '''
        self.img = img
        self.ax = ax
        self.data = img.get_array().reshape(img._meshWidth, img._meshHeight)

        # register the event handlers:
        self.cidclick = img.figure.canvas.mpl_connect('button_press_event', self)
        self.cidrelease = img.figure.canvas.mpl_connect('button_release_event', self)
        
        self.markers, self.arrow = None, None   # the lineslice indicators on the pcolormesh plot
        self.line = None    # the lineslice values plotted in a line
        
        self.hold = hold
        self.img_kwargs = img_kwargs
        self.ax_kwargs = ax_kwargs
    #end __init__

    def __call__(self, event):
        '''Matplotlib will run this function whenever the user triggers an event on our figure'''
        #print( 'Event Name:', event.name )
        if event.inaxes != self.img.axes: return     # exit if clicks weren't within the axes
        
        if event.name == 'button_press_event':
            self.p1 = (event.xdata, event.ydata)    # save 1st point
        elif event.name == 'button_release_event':
            self.p2 = (event.xdata, event.ydata)    # save 2nd point
            self.drawLineSlice()    # draw the line trace position
    #end __call__
    
    def drawLineSlice( self):
        ''' Draw the region along which the Line Slice will be extracted, onto the original pcolor plot.'''
        '''Uses code from these hints:
        http://stackoverflow.com/questions/7878398/how-to-extract-an-arbitrary-line-of-values-from-a-numpy-array
        http://stackoverflow.com/questions/34840366/matplotlib-pcolor-get-array-returns-flattened-array-how-to-get-2d-data-ba
        '''
        
        x0,y0 = self.p1[0], self.p1[1]  # get user's selected coordinates
        x1,y1 = self.p2[0], self.p2[1]
        length = int( np.hypot(x1-x0, y1-y0) )
        x, y = np.linspace(x0, x1, length),   np.linspace(y0, y1, length)
        
        # Extract the values along the line with nearest-neighbor pixel value:
        #D = img.get_array().reshape(img._meshWidth, img._meshHeight)    # get temp. data from the pcolor plot
        zi = self.data[x.astype(np.int), y.astype(np.int)]
        # Extract the values along the line, using cubic interpolation:
        #import scipy.ndimage
        #zi = scipy.ndimage.map_coordinates(z, np.vstack((x,y)))
        
        # if plots exist, delete them:
        if self.markers != None and not self.hold:
            if isinstance(self.markers, list):
                self.markers[0].remove()
            else:
                self.markers.remove()
        if self.arrow != None:
            self.arrow.remove()
        
        # plot the endpoints
        if self.img_kwargs != None:
            self.markers = self.img.axes.plot([x0, x1], [y0, y1], 'wo', **self.img_kwargs)   
        else:
            self.markers = self.img.axes.plot([x0, x1], [y0, y1], 'wo')   
        # plot an arrow:
        self.arrow = self.img.axes.annotate("",
                    xy=(x0, y0),    # start point
                    xycoords='data',
                    xytext=(x1, y1),    # end point
                    textcoords='data',
                    arrowprops=dict(
                        arrowstyle="<-",
                        connectionstyle="arc3", 
                        color='white',
                        alpha=0.7,
                        linewidth=3
                        ),
                    
                    )
        
        # plot the data along the line:
        if self.line != None and not self.hold:
            self.line[0].remove()   # delete the plot
        
        if self.ax_kwargs != None:
            self.line = self.ax.plot(zi, **self.ax_kwargs)
        else:
            self.line = self.ax.plot(zi)
        
        # autoscale the axes:
        self.ax.relim()
        self.ax.autoscale_view(True,True,True)
    #end drawLineSlice()
    
#end class LineTrace



####################################################


def Plot(DataFilePath, LineSlicePlot=True, hold=False, img_kwargs={}, ax_kwargs={}):
    '''Plot temperature or other 3D data from the QFI scope.
    
    Example Usage
    -------------
    >>> import QFIScope as qfi
    >>> FigHandles = qfi.Plot( '/Data/TempData.txt' )
        #   FigHandles = fig, (ax1, ax2), img
    >>>lntr = LineSlice( FigHandles )          # Take a LineSlice plot of the data
    
    Arguments
    ---------
    DataFilePath : str, path to the text data file.
    
    LineSlice : { True | False }, plot as a LineSlice plot (to plot data along a line)? Defaults to True.
    
    hold : { True | False }, optional
        Clear a previously plotted LineSlice on `ax2` before plotting a new one?  `hold=True` will retain the previously plotted lines. Defaults to False.
        
    img_kwargs : dictionary of optional arguments to pass to the marker plots on the pcolormesh plot. (Eg. `markerstyle` etc.)
    
    ax_kwargs : dictionary of optional arguments to pass to the LineSlice plot on ax2. (Eg. `linewidth` etc.)
    
    
    Returns
    -------
    Returns the handles (objects) for various figure elements.  
    
    fig : matplotlib Figure object for the plot window.
    
    ax1 : axis with the 3D temperature data.
    
    img : the pcolormesh object (actually a QuadMesh object) of the temperature data
    
    ax2 : axis with the 2D LineSlice plot, only returned if `LineSlice=True`
    
    LineTraceObj : the LineTrace Object, see `help(QFIScope.LineSlice)`, which also includes figure objects
    
    '''
    
    D = np.genfromtxt(DataFilePath, skip_header=4, delimiter=',', unpack=True)
    # remove NANs
    D = D[0:-1,:]
    #print( D.shape )

    # rotate the data
    D = np.rot90(D, 1)



    # plot the data:
    nplots = 2 if LineSlicePlot else 1
    fig, ax = plt.subplots(nrows=nplots, ncols=1)
    if not LineSlicePlot:   ax=[ax]     # make it indexable

    # contourf, pcolormesh, imshow
    import matplotlib.cm as cm      # colormaps
    #print( ax  )
    img = ax[0].pcolormesh( np.arange( len(D[0,:]) ), np.arange(len(D[:,0])), D  , cmap=cm.spectral)
    fig.colorbar(img, ax=ax[0])	# print the colorbar for this subplot/axis


    # format the plot
    ax[0].set_ylabel('pixels')
    ax[0].axis('image')    # square scaling
    img.colorbar.set_label(u"Temperature, °C")

    if LineSlicePlot:
        # format the 2nd plot
        ax[1].set_ylabel(u"Temperature, °C")
        ax[1].set_xlabel("Pixel Position along Line")
        
        # Enable click/drag to draw line-trace:
        LnTr = LineSlice(img, ax[1], hold=hold, img_kwargs=img_kwargs, ax_kwargs=ax_kwargs)    
        # args: the pcolor plot (img) & the axis to plot the values on (ax[1])
    
    fig.show()
    
    
    out = [fig, ax[0], img]
    if LineSlicePlot: out.extend(  [ax[1], LnTr]  )
    return  out
    
#end Plot()

