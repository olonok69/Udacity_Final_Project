import os
import sys
import numpy as np
import datetime
import itertools
import matplotlib.pyplot as plt
import pandas as pd
#import library as mio




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

def get_data(symbols, dates):
    #"""Read stock data (adjusted close) for given symbols from CSV files."""
	df_final = pd.DataFrame(index=dates)
	i=0
	for symbol in symbols:
		path = os.path.dirname(os.path.realpath(__file__))
		
		file_path = path +  "\\raw_data\\" + symbol + ".csv"
		
		#print ("Loading csv..." + str(file_path))
		if symbol=="ORB"or symbol=="WT1010":#OIL
			df_temp = pd.read_csv(file_path, parse_dates=True, index_col="Date",usecols=["Date", "Value"], na_values=["nan"])
			df_temp = df_temp.rename(columns={"Value": symbol})
		elif symbol=="EUR" or symbol=="GBP" or symbol=="AUD" or symbol=="JPY":
			df_temp = pd.read_csv(file_path, parse_dates=True, index_col="DATE",usecols=["DATE", "RATE"], na_values=["nan"])
			df_temp = df_temp.rename(columns={"RATE": symbol})
		elif symbol=="PLAT":
			df_temp = pd.read_csv(file_path, parse_dates=True, index_col="Date",usecols=["Date", "London 08:00"], na_values=["nan"])
			df_temp = df_temp.rename(columns={"London 08:00": symbol})
		elif symbol=="GOLD":
			df_temp = pd.read_csv(file_path, parse_dates=True, index_col="Date",usecols=["Date", "USD (AM)"], na_values=["nan"])
			df_temp = df_temp.rename(columns={"USD (AM)": symbol})
		elif symbol=="SILVER":
			df_temp = pd.read_csv(file_path, parse_dates=True, index_col="Date",usecols=["Date", "USD"], na_values=["nan"])
			df_temp = df_temp.rename(columns={"USD": symbol})
		else:
			df_temp = pd.read_csv(file_path, parse_dates=True, index_col="Date",usecols=["Date", "Adj Close"], na_values=["nan"])
			df_temp = df_temp.rename(columns={"Adj Close": symbol})
		
		#df_temp = df_temp.rename(columns={"Adj Close": symbol})
		df_final = df_final.join(df_temp)
		i+=1
		if i == 1:  # drop dates SPY did not trade
			df_final = df_final.dropna(subset=[symbol])

	return df_final
	
def normalize(df, symbols):
	result = df.copy()
	for symbol in df.columns:
		max_value = df[symbol].max()
		min_value = df[symbol].min()
		
		result[symbol] = (df[symbol] - min_value) / (max_value - min_value)
	return result
	


def main():

	indices_list_Complete = ["^GSPC","SPY","^IXIC", "^DJI", "^GDAXI", "^FTSE","^FCHI", "^N225","^HSI", "^AXJO","ORB", "EUR","AUD","GBP","JPY", "SILVER", "GOLD", "PLAT","WT1010"] # reduced list only the most correlated
	indices_list_reduced = ["^GSPC","^IXIC", "^DJI", "^GDAXI", "^FTSE","^N225","^HSI", "^AXJO", "EUR","JPY"] # Indexes correlated >.5
	indices_list_ultra = ["^GSPC","^IXIC", "^DJI", "^GDAXI", "^FTSE","^N225"] # Indexes correlated >.7
	indices_day_after=["^GSPC", "^N225","^HSI", "^AXJO","ORB", "AUD","JPY", "GOLD", "PLAT"] # this index have closing price before NY stock exchange opens
	#index_list=["^GSPC"]
	#algorithm=["KNN","RFC","SVM","ADA Bost","GTB","LDA", "SGD","LRC", "VOT", "DTC"]
	algorithm=["SVM"]
	#algorithm=["LDA", "KNN"]
	optimiza=3 # Control to optize Algorithms or to Produce outcomes
	TEST=1# Tipo Ge feautures
	numDaysArray = [1] # day, week, month, quarter, year
	numDays = [5,21,63]
	param='Default'
	version='Completed'

	start_date = "2003-01-01"
	end_date = "2017-01-01"
	dates = pd.date_range(start_date, end_date)  # date range as index
	#df_accu = mio.Load_DataFrames()

	indices_list = indices_list_Complete

	df_index = get_data(indices_list, dates) # get data from index and return a dataframe with all prices , but adjusted to the days we have prices of SP500
	#df_index=mio.shit_day(df_index,indices_list,indices_day_after)	# Move the closing price 1 day before if needed
	df_index.fillna(method='ffill', inplace=True)# fill Nan with previos value as order is ascending date 
	df_index.fillna(method='bfill', inplace=True)# fill NaN first day
	#write_Excel(df_index, "prices.xlsx", "prices") 	
	#print(df_index.mean())
	pie1=df_index.plot(figsize=(15,12))
	pie1.legend(bbox_to_anchor=(1.05, 1), loc=1, borderaxespad=0.)
	fig = pie1.get_figure()
	fig.savefig("myplot.jpg")
	pie =df_index.plot(figsize=(15,20), subplots=True)
	fig = pie[0].get_figure()
	fig.savefig("myplot1.jpg") #print(df_index.max())
	#print(df_index.std())
	#Normalize data as have diferent dimension
	df_index_normalized=normalize(df_index,indices_list)

	correlations(df_index_normalized) ##CORRELATIONS#
	#write_Excel(df_index_normalized, "prices_normalized.xlsx", "Normalized") 
		
	df_adjusted=df_index_normalized.copy()
	

	#pie2 =df_adjusted.plot(figsize=(15,15), subplots=False)
	pie2=df_adjusted.plot(figsize=(15,12))
	pie2.legend(bbox_to_anchor=(1.05, 1), loc=1, borderaxespad=0.)
	fig = pie2.get_figure()
	fig.savefig("myplot2.jpg")
	pie =df_adjusted.plot(figsize=(15,20), subplots=True)
	fig = pie[0].get_figure()
	fig.savefig("myplot3.jpg") #print(df_index.max())
	#print(df_index.std())
 
	return


	
	

main()
