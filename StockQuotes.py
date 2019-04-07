from iexfinance import get_historical_data #change this to backtrader and use that library instead for mining data
from datetime import datetime, timedelta
import pandas as pd
import math
import numpy as np
from sklearn import preprocessing, model_selection, svm
from sklearn.linear_model import LinearRegression
import backtrader as bt
import os
import csv
import matplotlib.pyplot as plt, matplotlib
from matplotlib import style
import random
pd.options.mode.chained_assignment = None
style.use('ggplot')


class TradingStrategy(bt.Strategy):
	period = 15
	smaArr = []
	rsiArr = []
	avgRangeArr = []
	def __init__(self):
		self.Bsma = True
		self.Brsi = True
		self.BaverageRange = True
		self.BlastHigh = True
		self.BlastLow = True
		if self.Bsma:
			self.sma = bt.indicators.MovingAverageSimple(period=self.period)
		if self.Brsi:
			self.rsi = bt.indicators.RelativeStrengthIndex(period=self.period)
		if self.BaverageRange:
			self.avgRange = bt.indicators.AverageTrueRange(period=self.period)
		if self.BlastHigh:
			self.lastHigh = bt.indicators.FindLastIndexHighest(period=self.period)
		if self.BlastLow:
			self.lastLow = bt.indicators.FindLastIndexLowest(period=self.period)

	def next(self):
		global global_Strength_buy
		if self.Bsma:  # if the user choses to do a simple moving average then do some calculations with it
			self.smaArr.append(self.sma[0])
			if self.sma > self.data.close:
				global_Strength_buy += 1
			else:
				global_Strength_buy -= 1

		if self.Brsi:
			self.rsiArr.append(self.rsi[0])
			if self.rsi < 30 and self.lastHigh > self.lastHigh[-1]:
				global_Strength_buy += 1

			if self.rsi < 30:
				global_Strength_buy += 3
			if self.rsi > 70:
				global_Strength_buy -= 3

		if self.BaverageRange:
			self.avgRangeArr.append(self.avgRange[0])
			if self.avgRange > 3:
				global_Strength_buy += 3
			if self.avgRange < 3:
				global_Strength_buy -=3

def editDataFrame(df, simpleAverageArr, rsiArr, avgRangeArr, period = 1):
	df = df[['open','high','low','close','volume']]
	df['high_low%'] = ((df['high'] - df['low'])/df['low']) * 100
	df['%change'] = ((df['open'] - df['close']) / df['open']) * 100

	if rsiArr and simpleAverageArr and avgRangeArr: #all three true
		df['SMA'] = pd.Series(simpleAverageArr)
		count = 0
		for val in range(len(df.index)):
			if (count < len(simpleAverageArr)):
				df['SMA'][val] = simpleAverageArr[count]
				if (val % period == 0):
					count += 1

		count = 0
		df['RSI'] = pd.Series(rsiArr)
		for val in range(len(df.index)):
			if (count < len(rsiArr)):
				df['RSI'][val] = rsiArr[count]
				if (val % period == 0):
					count += 1

		df['avgRange'] = pd.Series(avgRangeArr)
		count = 0
		for val in range(len(df.index)):
			if (count < len(avgRangeArr)):
				df['avgRange'][val] = avgRangeArr[count]
				if (val % period == 0):
					count += 1

		df = df[['close', 'volume', 'high_low%', '%change', 'SMA', 'RSI', 'avgRange']]

	if rsiArr and simpleAverageArr and not avgRangeArr: #just rsi and simple avg
		df['SMA'] = pd.Series(simpleAverageArr)
		count = 0
		for val in range(len(df.index)):
			if (count < len(simpleAverageArr)):
				df['SMA'][val] = simpleAverageArr[count]
				if (val % period == 0):
					count += 1

		df['RSI'] = pd.Series(rsiArr)
		count = 0
		for val in range(len(df.index)):
			if (count < len(rsiArr)):
				df['RSI'][val] = rsiArr[count]
				if (val % period == 0):
					count += 1

		df = df[['close', 'volume', 'high_low%', '%change', 'SMA', 'RSI']]

	if rsiArr and not simpleAverageArr and avgRangeArr: #just rsi and avg range
		df['RSI'] = np.none
		count = 0
		for val in range(len(df.index)):
			if (count < len(rsiArr)):
				df['RSI'][val] = rsiArr[count]
				if (val % period == 0):
					count += 1

		count = 0
		df['avgRange'] = np.none
		for val in range(len(df.index)):
			if (count < len(avgRangeArr)):
				df['avgRange'][val] = avgRangeArr[count]
				if (val % period == 0):
					count += 1

		df = df[['close', 'volume', 'high_low%', '%change', 'RSI', 'avgRange']]

	if not rsiArr and simpleAverageArr and avgRangeArr: #just simpleavg and avg range
		df['SMA'] = np.nan
		count = 0
		for val in range(len(df.index)):
			if (count < len(simpleAverageArr)):
				df['SMA'][val] = simpleAverageArr[count]
				if (val % period == 0):
					count += 1

		count = 0
		df['avgRange'] = np.nan
		for val in range(len(df.index)):
			if (count < len(avgRangeArr)):
				df['avgRange'][val] = avgRangeArr[count]
				if (val % period == 0):
					count += 1

		df = df[['close', 'volume', 'high_low%', '%change', 'SMA', 'avgRange']]

	if rsiArr and not simpleAverageArr and not avgRangeArr: #just rsiarr
		df['RSI'] = np.nan
		# for value column in df:
		count = 0
		for val in range(len(df.index)):
			if (count < len(rsiArr)):
				df['RSI'][val] = rsiArr[count]
				if (val % period == 0):
					count += 1
		df = df[['close', 'volume', 'high_low%', '%change', 'RSI']]

	if not rsiArr and simpleAverageArr and not avgRangeArr: #just simpleavg
		df['SMA'] = np.nan
		#for value column in df:
		count = 0
		for val in range(len(df.index)):
			if(count < len(simpleAverageArr)):
				df['SMA'][val] = simpleAverageArr[count]
				if((val + 1) % period == 0):
					count += 1

		df = df[['close', 'volume', 'high_low%', '%change', 'SMA']]

	if not rsiArr and not simpleAverageArr and avgRangeArr: #just avgrange
		df['avgRange'] = np.nan
		# for value column in df:
		count = 0
		for val in range(len(df.index)):
			if (count < len(avgRangeArr)):
				df['avgRange'][val] = avgRangeArr[count]
				if (val % period == 0):
					count += 1
		df = df[['close', 'volume', 'high_low%', '%change', 'avgRange']]

	if not rsiArr and not simpleAverageArr and avgRangeArr:  #All disabled
		df = df[['close', 'volume', 'high_low%', '%change']]

	return df

def forecast(df, forecast_out, forecast_col):
	forecast_out = 2
	#df_clone = df.copy()

	df['label'] = df[forecast_col].shift(-forecast_out)

	X = np.array(df.drop(['label'],1))
	X = preprocessing.scale(X)

	X_data = X[-forecast_out:]
	X = X[:-forecast_out]

	df.dropna(inplace=True)
	#print('BEFORE', len(df), (df.tail()))
	y = np.array(df['label'])
	y = np.array(df['label'])

	X_train, X_test, y_train, y_test = model_selection.train_test_split(X,y,test_size=0.25)
	clf = LinearRegression()
	clf.fit(X_train, y_train)
	percent_confidence = clf.score(X_test,y_test)
	#print(percent_confidence)

	#print(len(df),df.tail())
	#exit(1)
	forcast_data = clf.predict(X_data)

	df['Prediction'] = np.nan
	dayBefore = df.iloc[-1].name
	dayBefore = datetime.strptime(dayBefore,'%m/%d/%y' )

	for predictedVal in forcast_data:
		#tmr = datetime.fromtimestamp(nextDay)
		#nextDay += 86400
		dayBefore += timedelta(days=1)

		for val in range(len(df.columns)+1):
			#if val < len(df.columns):
			df.loc[dayBefore] = np.nan
			if val == len(df.columns):
				df.loc[dayBefore]['Prediction'] = predictedVal

	return df

def getUserStrategy(algorithm, period =1):
	currentstrat = TradingStrategy
	currentstrat.Bsma = False
	currentstrat.BaverageRange = False
	currentstrat.BlastHigh = False
	currentstrat.BlastLow = False
	currentstrat.Brsi = False
	currentstrat.Bsma = bool(algorithm == "SMA")
	currentstrat.BaverageRange = bool(algorithm == "Average Range")
	currentstrat.BlastHigh = bool(algorithm == "High statistics")
	currentstrat.BlastLow = bool(algorithm == "Low statistics")
	currentstrat.Brsi = bool(algorithm == "RSI")
	currentstrat.period = period
	return currentstrat

global_Strength_buy = 0 # short term strategy

def StockQuotes(stock_name, starting_amount,cash_limit, s, e, algorithm):
	cerebro = bt.Cerebro()
	# cerebro.addstrategy(TradingStrategy)
	filepath = "StockInfo.csv"
	# start = datetime(2014, 1, 1) #allow the user to control
	# end = datetime(2018, 7, 25) #allow the user to control
	currentstrat = getUserStrategy(algorithm)
	cerebro.addstrategy(currentstrat)
	start = datetime(s[2],s[0],s[1]) #allow the user to control
	end = datetime(e[2],e[0],e[1]) #allow the user to control

	input_quote = stock_name

#First 5 parameters are expected to be boolean values, period is an integer, dateStart and dateEnd are datetime objects, stockticker is a string
# def StockQuotes(sma, averageRange, lastHigh, lastLow, rsi, period, dateStart, dateEnd, stockTicker):
# 	cerebro = bt.Cerebro()
# 	currentstrat = TradingStrategy
# 	#currentstrat = getUserStrategy()
# 	currentstrat.Bsma = sma
# 	currentstrat.BaverageRange = averageRange
# 	currentstrat.BlastHigh = lastHigh
# 	currentstrat.BlastLow = lastLow
# 	currentstrat.Brsi = rsi
# 	currentstrat.period = period

	cerebro.addstrategy(currentstrat)

	# filepath = os.path.join(os.environ["HOMEDRIVE"], os.environ["HOMEPATH"], "Desktop", "StockInfo.csv")
	# start = dateStart #datetime(2014, 1, 1) #allow the user to control
	# end = dateEnd     #datetime(2018, 11, 20) #allow the user to control
	# input_quote = stockTicker

	with open(filepath, 'w') as csv_file:
		data = pd.DataFrame(get_historical_data(
			input_quote,
			start=start,
			end=end,
			output_format='pandas'
		))

		#data = pdr.get_data_yahoo(symbols=input_quote, start=start,end=end)
		#print(data.tail())

		datesList = []
		for index in data.index:
			year,month,day = (index.split('-'))
			year = year[2] + year[3]
			datesList.append(month + '/' + day + '/' + year)

		# data["date"] = datesList
		data.index = datesList
		# print(data)

		data.to_csv("StockInfo.csv")

		# data.index.name = datesList

		datapath = input_quote + '.csv'
		btdata = bt.feeds.YahooFinanceData(dataname=input_quote,
		                                   fromdate=start,
		                                   todate=end,
		                                   reverse=True)

		cerebro.adddata(btdata)
		# cerebro.run()
		#cerebro.plot()

	df = editDataFrame(data, currentstrat.smaArr, currentstrat.rsiArr, currentstrat.avgRangeArr, currentstrat.period) #have to make sure this doesnt brick when user suggests a different strategy
	forecast_col = 'close'

	forecast_out = currentstrat.period #int(math.ceil(.01 * len(df)))

	prediction = forecast(df,forecast_out,forecast_col)

	prediction['close'].plot()
	prediction['Prediction'].plot()
	plt.title(stock_name)
	plt.legend(loc=4)
	plt.xlabel('Date')
	plt.ylabel('Price in Dollars')
	plt.savefig("stockquotes.png")
	plt.close()
	return global_Strength_buy #higher this number the better

