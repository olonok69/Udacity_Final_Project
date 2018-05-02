import os
import sys
import numpy as np
import datetime
import itertools
sys.path.append('C:\\Program Files\\Anaconda3\\Lib\\site-packages')
sys.path.append('C:\\Program Files\\Continuum\\Anaconda3\\Lib\\site-packages')
#C:\Program Files\Anaconda3\Lib\site-packages\sklearn\neighbors
import matplotlib.pyplot as plt
import pandas as pd
import library as mio
from sklearn.metrics import classification_report



def write_Excel(__df_r1, filename, title):
	print ("Printing Report..."+ str(title))
	total_file = os.path.dirname(os.path.realpath(__file__)) + "\\raw_data\\" + filename
	writer = pd.ExcelWriter(total_file)

	__df_r1.to_excel(writer,title)
	writer.save()

def correlations(df):

	df_correlation=df.corr() # create correlation matrix

	#write_Excel(df_correlation, "Correlation Matrix.xlsx"," Correlation Matrix" )
	return

#NASDAQ Composite (^IXIC Yahoo Finance)
#Dow Jones Industrial Average (^DJI Quandl)
#Frankfurt DAX (^GDAXI Yahoo Finance)
#London FTSE-100 (^FTSE Yahoo Finance)
#Paris CAC 40 (^FCHI Yahoo Finance)
#Tokyo Nikkei-225 (^N225 Yahoo Finance)
#Hong Kong Hang Seng (^HSI Yahoo Finance)
#Australia ASX-200 (^AXJO Yahoo Finance)
	


def main():

	indices_list_Complete = ["^GSPC","SPY","^IXIC", "^DJI", "^GDAXI", "^FTSE","^FCHI", "^N225","^HSI", "^AXJO","ORB", "EUR","AUD","GBP","JPY", "SILVER", "GOLD", "PLAT","WT1010"] # reduced list only the most correlated
	indices_list_reduced = ["^GSPC","^IXIC", "^DJI", "^GDAXI", "^FTSE","^N225","^HSI", "^AXJO", "EUR","JPY"] # Indexes correlated >.5
	indices_list_ultra = ["^GSPC","^IXIC", "^DJI", "^GDAXI", "^FTSE","^N225"] # Indexes correlated >.7
	indices_day_after=["^GSPC", "^N225","^HSI", "^AXJO","ORB", "AUD","JPY", "GOLD", "PLAT"] # this index have closing price before NY stock exchange opens
	#index_list=["^GSPC"]
	#algorithm=["KNN","RFC","SVM","ADA Bost","GTB","LDA", "SGD","LRC", "VOT", "DTC"] # Optimizers
	#algorithm=["MLC"]
	#algorithm=["LDA", "KNN"]
	#optimiza=0 # 0= Normal processing, 1= CVGridSearch, 2 Stacking and Blending
	#TEST=6		#1= Standard Rolling Awerage Series of Daily Returns 5 Days Windows
				#2=Standard Rolling Awerage Series of Momemtum 5 Days Windows
				#3=Standard Rolling Awerage Series of Volatility 5 Days Windows
				#4=Exponential Rolling awerage Series of Daily Returns 5 Days 
				#6= Standard Rolling Awerage Series of Daily Returns 5 Days Windows + Standard Rolling Awerage Series of Momemtum 21 Days Windows +
				# Standard Rolling Awerage Series of Volatility 2 Days Windows+ Exponential Rolling awerage Series of Daily Returns 21 Days Windows
	#numDaysArray = [1] # day, week, month, quarter, year
	#numDays = [5,21,42]

	start_date = "2003-01-01" # Start day of Series
	end_date = "2018-01-01"	  # Final day of series
	dates = pd.date_range(start_date, end_date)  # date range as index
	#df_accu = mio.Load_DataFrames()

	indices_list = indices_list_Complete
	path = os.path.dirname(os.path.realpath(__file__))



	df_index = mio.get_data(indices_list, dates) # get data from index and return a dataframe with all prices , but adjusted to the days we have prices of SP500
	#df_index=mio.shit_day(df_index,indices_list,indices_day_after)	# Move the closing price 1 day before if needed
	df_index.fillna(method='ffill', inplace=True)# fill Nan with previos value as order is ascending date 
	df_index.fillna(method='bfill', inplace=True)# fill NaN first day
	file_path = path +  "\\prices_shift.xlsx"
	print(file_path)
	#write_Excel(df_index, file_path, "prices_shift") 	
	#Normalize data as have diferent dimension
	#correlations(df_index_normalized) ##CORRELATIONS#


                

main()
