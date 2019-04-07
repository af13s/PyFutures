#Name: Alejandro Mateos
#FSUID: AM16AN

from tkinter import *
import cufflinks as cf
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as mticker
from mpl_finance import candlestick_ohlc
import numpy as np
import urllib
import datetime as dt           
from datetime import datetime
import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure

def graph_data(stock):

    names = ['date', 'open', 'high', 'low', 'close', 'volume']

    df = pd.read_csv('dataSet.csv', names=names)
   
   #print(df.head())
   #print(df.tail())
    
    # parses dates and converts to matplotlib numbers
    df['date'] = pd.to_datetime(df['date'], yearfirst=True, format='%m/%d/%y')
    df['date'] = df['date'].map(mdates.date2num)

    date, closep, highp, lowp, openp, volume = df.iteritems()


    fig = plt.figure()
    ax1 = plt.subplot2grid((1,1), (0,0))
    plt.xticks(rotation=45)
    
    ax1.xaxis.set_major_locator(mticker.MaxNLocator(10))
    ax1.grid(True)
    
    # converts number to date 
    ax1.xaxis_date()
    
    # index all but 'volume' column, remove headers
    candlestick_ohlc(ax1, df.iloc[:,:-1].values, width=0.4, colorup='#77d879', colordown='#db3f3f')

    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.title(stock)
    plt.legend()
    plt.subplots_adjust(left=0.09, bottom=0.20, right=0.94, top=0.90, wspace=0.2, hspace=0)
    return fig


def embed_in_window(root, f):
    canvas = FigureCanvasTkAgg(f, root)
    canvas.draw()
    canvas.get_tk_widget().pack(anchor='center')
    toolbar = NavigationToolbar2Tk(canvas, root)
    toolbar.update()
    canvas.get_tk_widget().pack(anchor='center')

def ShowGraph(company_name):
    root = Tk()		#creates blank window
    label = Label(root, text="PyFutures")		#create text on screen
    label.pack(side=TOP)
    root.overrideredirect(True)
    root.overrideredirect(False)
    root.attributes('-fullscreen',True)

	
    fig = graph_data('')
    embed_in_window(root, fig)
    root.mainloop()			#keep window open

ShowGraph("AAPL")

