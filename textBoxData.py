import backtrader as bt
import backtrader.feeds as btfeeds
import datetime
import sys
import os.path

# https://www.backtrader.com/docu/strategy.html
# strategy skeleton

# Default values for buying and selling indicators
globalSell = 30
globalBuy = 90
globalFile = open('output.csv','a')


class Sim():

	# Cerebro is the system that runs the strategy
	cerebro = bt.Cerebro()

	# This is the default data
	data = bt.feeds.YahooFinanceData(
		dataname= "MSFT" ,
		fromdate=datetime.datetime(2010,1,1),
		todate = datetime.datetime(2018,10,16),
		buffered=True
		)

	#################Functions#######################

	# Pass an array [2018, 10, 10]..this is 10/10/2018
	# Pass an stock too
	def setDateStock(self, dateBeg, dateEnd, stock ):
		
		self.data = bt.feeds.YahooFinanceData(
		dataname= stock ,
		fromdate=datetime.datetime(dateBeg[0], dateBeg[1], dateBeg[2]),
		todate = datetime.datetime(dateEnd[0], dateEnd[1], dateEnd[2]),
		buffered=True
		)

	#  INT only, setting the starting cash value
	def setCashStart(self, num):
		userCash = num
		self.cerebro.broker.setcash(userCash)

	# Prints all the beginning cash values that users starts with
	def getStartValues(self):
		startCash = self.cerebro.broker.getvalue();
		startCashStr = 'Starting Cash: {}'.format(startCash)
		
		return startCashStr


	# Prints all the remaining cash & stock values by running through cerebro
	def getEndValues(self):
		self.garbageCollector()
		self.cerebro.addstrategy(self.algStrategy)
		self.cerebro.adddata(self.data)
		self.cerebro.run()

		# Money Variables
		endTotalVal = self.cerebro.broker.getvalue()
		endCash = self.cerebro.broker.get_cash()
		endStock = (endTotalVal) - (endCash)

		# Strings Format
		endTotalValStr = 'Final Total Value (Cash + Stocks): {:0.2f}'.format(endTotalVal)
		endCashStr = 'Remaining Cash: {:0.2f}'.format(endCash)
		endStockStr = 'Final Total Stock Value: {:0.2f}'.format(endStock)
		
		# Final Values - (Things To Plot Later?)
		return endTotalValStr, endCashStr, endStockStr

	# Can only run after getEndValues
	def plot(self):
		self.cerebro.plot(style='candlestick')

	# global variables
	def setBuyLimit(self,num):
		global globalSell
		globalSell = num

	def setSellLimit(self,num):
		global globalBuy
		globalBuy = num

	# garbage collector - check if output.txt exists upon running
	def garbageCollector(self):
		if (os.path.isfile('output.csv')) == True:
			global globalFile
			globalFile.close()
			os.remove('output.csv')
			globalFile = open('output.csv','a')


	###############################################
	# This is the strategy that are being created and used
	class algStrategy(bt.Strategy):


		# this is where the indicators are created
		def __init__(self):

			# This is one indicator
			self.sma = bt.ind.SimpleMovingAverage(period=10)
			
			# Indicator Variables
			self.dataclose = self.datas[0].close
			self.date = '10-30-08'
			
			# These are the global variables that are setted by the user
			# Logic:
			# User uses setGlobalSell() or set setGlobalBuy()
			# Then globalSell is set to self here
			# Now we are able to use it in the indicators below
			global globalSell
			global globalBuy

			self.sellLimit = globalSell
			self.buyLimit = globalBuy

			# Cash Variables
			self.curCash = self.cerebro.broker.getvalue()
			self.orderNum = 0
			self.purList = list()
			self.netGain = '0'

		# Based on the indicator value that is produced, we then can make
		# purchases here
		# Backtrader documentation quickstart will explain this very well
		def next(self):

			global globalFile

			if not self.position:
				if self.sma > self.buyLimit and self.curCash > self.dataclose[0]:
					self.log('BUY ATTEMPT, %.2f' % self.dataclose[0])
					self.buy(size=1)

					""" Test this out """
					self.curCash -= self.dataclose[0]
					self.orderNum += 1

			else:
				if self.sma > self.sellLimit and self.orderNum > 0:
					self.log('SELL ATTEMPT, %.2f' % self.dataclose[0])
					
					""" Test this out """
					self.curCash += self.dataclose[0]
					self.sell(size=1)
					self.orderNum -= 1

		# This creates the output when orders are executed
		def notify_order(self,order):

			global globalFile

			if order.status in [bt.Order.Submitted, bt.Order.Accepted]:
				return

			if order.status == order.Completed:
			
				# Every order is added to the stack for net calculations
				# self.purList is a stack that holds all the executed prices
				# Then it it used in the netGainCal()
				
				if order.isbuy() == True:
					buyExecuted = 'BUY EXECUTED, %.2f' % order.executed.price
					self.purList.append(order.executed.price)				#Writes to stack
					self.log(buyExecuted)
					globalFile.write('\n' + self.date + ', ' + buyExecuted + '\n')		#Writes to file

				else:
					sellExecuted = 'SELL EXECUTED, %.2f' % order.executed.price
					self.log(sellExecuted)

					# This calculates the net gain/loss
					self.netGainCal(order.executed.price)
					netGainStr = (self.date + ', ' + 'NET, ' +  self.netGain + '\n')

					# Writes to file
					print(netGainStr)
					sys.stdout = open('output.csv', 'a')
					print('\n' + self.date + ', ' + sellExecuted)
					print('\n' + netGainStr)
					sys.stdout = sys.__stdout__

		# This calculates netGain
		def netGainCal(self,order):

			if (len(self.purList) != 0 ):
				
				self.netGain = (float(order) - self.purList.pop())

				#Postive & Negative Strings
				if self.netGain > 0:
					self.netGain = '+%.2f' % self.netGain
				else:
					self.netGain = '%.2f' % self.netGain
		
		# log - Creates the date correctly
		def log(self, txt, dt = None):
			sys.stdout = open('output.csv', 'a')
			dt = dt or self.datas[0].datetime.date(0)
			print('%s, %s' % (dt.isoformat(), txt))
			self.date = (dt.isoformat())
			sys.stdout = sys.__stdout__


def generateSimulator(ticker, blimit, slimit, startcash, s, e):
	# Testing the class and making it
	test = Sim()

	sys.stdout  = open("output.csv","w")
	print("")
	sys.stdout = sys.__stdout__


	###########################################################

	# Log has been completed. It is local directory when the program is ran

	# buyLimit && sellLimit
	# Determines when to purchase a stock
	# Example, if algorithm is greater than 30, buy a stock

	# getEndValues()
	# returns 3 strings 
	# endTotalValStr, endCashStr, endStockStr
	# endTotalValue = cash + stock

	# debugging functions
	# getStartValues() 
	# This gets the beginning cash of the program

	test.setBuyLimit(blimit)
	test.setSellLimit(slimit)
	test.setCashStart(startcash)
	test.setDateStock([s[2],s[0],s[1]], [e[2],e[0],e[1]], ticker)
	# print (test.getStartValues())
	# print (test.getEndValues())
	return test.getEndValues(), test
	