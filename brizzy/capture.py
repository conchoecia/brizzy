import matplotlib
matplotlib.use('TkAgg')
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import seabreeze.spectrometers as sb
import seabreeze
from scipy import signal
import progressbar
import os
import atexit
import argparse
import csv

def exit_handler():
    print("You have closed the brizzy program.\nNow looking for spectra files.")
    filelist = []
    for filename in os.listdir(os.getcwd()):
        if filename.endswith(".csv"):
            filelist.append(filename)
    print("Found {} spectra, plotting".format(len(filelist)))
    bar = progressbar.ProgressBar()
    for i in bar(range(len(filelist))):
        df = pd.read_csv(filelist[i], comment = '#')
        x = df['wavelength']
        y = df['intensity']
        plot_spectrum(x, y, filelist[i], yhat=True)

def plot_spectrum(x, y, filename, yhat=False):
    figWidth = 5
    figHeight = 4
    fig = plt.figure(figsize=(figWidth,figHeight))
    #set the panel dimensions
    panelWidth = 4
    panelHeight = 3
    #find the margins to center the panel in figure
    leftMargin = (figWidth - panelWidth)/2
    bottomMargin = ((figHeight - panelHeight)/2) + 0.25
    panel0 =plt.axes([leftMargin/figWidth, #left
                     bottomMargin/figHeight,    #bottom
                     panelWidth/figWidth,   #width
                     panelHeight/figHeight])     #height
    panel0.tick_params(axis='both',which='both',\
                       bottom='on', labelbottom='on',\
                       left='off', labelleft='off', \
                       right='off', labelright='off',\
                       top='off', labeltop='off')
    #panel0.spines['top'].set_visible(False)
    #panel0.spines['right'].set_visible(False)
    #panel0.spines['left'].set_visible(False)
    panel0.set_xlabel("wavelength")

    mindone = False
    maxdone = False
    index_x_gt350 = -1
    index_x_gt730 = -1
    for i in range(len(x)):
        if x[i] >= 375 and not mindone:
            index_x_gt350 = i
            mindone = True
        if x[i] >= 730 and not maxdone:
            index_x_gt730 = i
            maxdone = True

    yhat = signal.savgol_filter(y[index_x_gt350: index_x_gt730], 31, 3) # window size 51, polynomial order 3
    panel0.plot(x,y, lw=0.50, alpha = 0.4 )
    panel0.plot(x[index_x_gt350: index_x_gt730],yhat, color='red', alpha = 0.5)
    newx = list(x[index_x_gt350: index_x_gt730])
    lambdamax = newx[list(yhat).index(max(yhat))]
    panel0.axvline(x=lambdamax, color='black', lw=1.0)
    panel0.set_title("Spectrum lambda max = {}".format(int(lambdamax)))

    panel0.set_xlim([min(x[index_x_gt350: index_x_gt730]),
                     max(x[index_x_gt350: index_x_gt730])])
    panel0.set_ylim([min(y[index_x_gt350: index_x_gt730]),
                     max(yhat)*1.05])


    plt.savefig("{}.png".format(filename), dpi=300)
    plt.close()

def animate(frameno, inttime, monitor, prefix):
    devices = sb.list_devices()
    spec = sb.Spectrometer(devices[0])

    spec.integration_time_micros(inttime)
    x = spec.wavelengths()
    y = spec.intensities()
    line.set_ydata(y)  # update the data
    ax.set_ylim([min(y[10:]), max(y)*1.1])
    spec.close()
    if not monitor:
        a = np.column_stack([x,y])
        #in np.savetext, using inttime/1000 since the USB2000 uses microseconds, not milliseconds. 
        if prefix:
            filepref = prefix
        else:
            filepref = "spectrum_data"
        np.savetxt("{}_{}.csv".format(filepref, frameno),
                   a, delimiter = ',',
                   header = "wavelength,intensity",
                   fmt = '%.14f',
                   comments="#integration time: {0} ms\n#{0}\n".format(inttime/1000))
    return line,

def run(args):
    # Change the directory if it is specified by the user
    print(args)
    if args.directory:
        if not os.path.exists(args.directory):
            os.makedirs(args.directory)
        os.chdir(args.directory)
    np.set_printoptions(suppress=True)
    atexit.register(exit_handler)
    global fig
    global ax
    fig, ax = plt.subplots()
    devices = sb.list_devices()
    if len(devices) == 0:
        raise IOError("""No Ocean Optics devices found. Try a combination
        of unplugging things and plugging them in again.""")
    print("Found this device: {}".format(devices[0]))
    spec = sb.Spectrometer(devices[0])
    spec.tec_set_enable(True)
    spec.tec_set_temperature_C(4)

    spec.integration_time_micros(int(args.integration_time * 1000))

    x = spec.wavelengths()
    y = spec.intensities()
    spec.close()
    global line
    line, = ax.plot(x, y, lw=1, alpha=0.5)
    ax.set_xlim([min(x), max(x)])
    ax.set_ylim([min(y[10:]), max(y)*1.1])

    if args.prefix is not None:
        prefix = args.prefix
    else:
        prefix = None

    ani = animation.FuncAnimation(fig, animate, blit=False,
                                  interval=args.integration_time,
                                  fargs = [int(args.integration_time*1000),
                                           args.monitor,
                                           prefix],
                                  repeat=True)
    plt.show()
