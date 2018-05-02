# -*- coding: utf-8 -*-
"""
Created on Wed Apr  5 14:38:45 2017

@author: huerjua
"""

import os
import sys
#import numpy as np
#import datetime
#import itertools
sys.path.append('C:\\Program Files\\Continuum\\Anaconda3\\Lib\\site-packages')
sys.path.append('C:\\Program Files\\Anaconda3\\Lib\\site-packages')
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.pylab as py
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from matplotlib.collections import EllipseCollection

def plot_corr(df,size=10):
    '''Function plots a graphical correlation matrix for each pair of columns in the dataframe.

    Input:
        df: pandas DataFrame
        size: vertical and horizontal size of the plot'''

    corr = df.corr()
    fig, ax = plt.subplots(figsize=(size, size))
    ax.matshow(corr)
    plt.xticks(range(len(corr.columns)), corr.columns);
    plt.yticks(range(len(corr.columns)), corr.columns);
    return

def plot_corr_ellipses(data, ax=None, **kwargs):

    M = np.array(data)
    if not M.ndim == 2:
        raise ValueError('data must be a 2D array')
    if ax is None:
        fig, ax = plt.subplots(1, 1, subplot_kw={'aspect':'equal'})
        ax.set_xlim(-0.5, M.shape[1] - 0.5)
        ax.set_ylim(-0.5, M.shape[0] - 0.5)

    # xy locations of each ellipse center
    xy = np.indices(M.shape)[::-1].reshape(2, -1).T

    # set the relative sizes of the major/minor axes according to the strength of
    # the positive/negative correlation
    w = np.ones_like(M).ravel()
    h = 1 - np.abs(M).ravel()
    a = 45 * np.sign(M).ravel()

    ec = EllipseCollection(widths=w, heights=h, angles=a, units='x', offsets=xy,
                           transOffset=ax.transData, array=M.ravel(), **kwargs)
    ax.add_collection(ec)

    # if data is a DataFrame, use the row/column names as tick labels
    if isinstance(data, pd.DataFrame):
        ax.set_xticks(np.arange(M.shape[1]))
        ax.set_xticklabels(data.columns, rotation=90)
        ax.set_yticks(np.arange(M.shape[0]))
        ax.set_yticklabels(data.index)

    return ec



path = os.path.dirname(os.path.realpath(__file__))
		
file_path = path +  "\\raw_data\\" + "prices_adjusted_rolling" + ".xlsx"

df = pd.read_excel(open(file_path,'rb'), sheetname='rolling')
mylist=df.columns.values.tolist()

#plot_corr(df)
#py.savefig('correlation.png')

#pd.scatter_matrix(df, alpha = 0.3, figsize = (10,10), diagonal = 'kde');
#py.savefig('correlation_2.png')

data = df.corr()
matrix=data.as_matrix()
cho=pd.DataFrame(np.linalg.cholesky(matrix))
print(cho)
total_file = os.path.dirname(os.path.realpath(__file__)) + "\\raw_data\\Cholesky_EWA_avg_all.xlsx"
writer = pd.ExcelWriter(total_file)

cho.to_excel(writer,"Cholesky")
writer.save()

fig, ax = plt.subplots(1, 1, figsize=(10, 10))
m = plot_corr_ellipses(data, ax=ax, cmap='Greens')
cb = fig.colorbar(m)
cb.set_label('Correlation coefficient EWA')
ax.margins(0.1)

py.savefig('EWA_all.png')