import sys
from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit, QFormLayout, QPushButton, QCompleter, QPlainTextEdit, QLabel
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIcon
import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import QPixmap
from PyQt5 import QtGui
import pandas as pd
from NewsBackend import GetArticles
from textBoxData import generateSimulator
from StockQuotes import StockQuotes

blimit = 30
slimit = 100

class inputdialog(QWidget):
   def __init__(self, parent = None):
      super(inputdialog, self).__init__(parent)

      layout = QFormLayout()

      self.chart = QLabel(self)

      self.sim = None

      self.stock_name = QLineEdit()
      self.stock_name.setPlaceholderText("Press Button")
      self.btn = QPushButton("Pick a Stock")
      self.btn.clicked.connect(self.getStocks)
      layout.addRow(self.btn,self.stock_name)
		
      self.starting_amount = QLineEdit()
      self.starting_amount.setPlaceholderText("10000")
      self.btn1 = QPushButton("Starting Amount")
      self.btn1.clicked.connect(self.getAmount)
      layout.addRow(self.btn1,self.starting_amount)

      self.cash_limit = QLineEdit()
      self.cash_limit.setPlaceholderText("2000")
      self.btn2 = QPushButton("Cash Limit")
      self.btn2.clicked.connect(self.getLimit)
      layout.addRow(self.btn2,self.cash_limit)

      self.start_date = QLineEdit()
      self.start_date.setPlaceholderText("6/7/2018")
      self.btn3 = QPushButton("Start Date")
      self.btn3.clicked.connect(self.getStart)
      layout.addRow(self.btn3,self.start_date)

      self.end_date = QLineEdit()
      self.end_date .setPlaceholderText("11/7/2018")
      self.btn4 = QPushButton("End Date")
      self.btn4.clicked.connect(self.getEnd)
      layout.addRow(self.btn4,self.end_date)

      self.algorithm = QLineEdit()
      self.algorithm.setPlaceholderText("Press Button")
      self.btn5 = QPushButton("Pick an Algorithm")
      self.btn5.clicked.connect(self.getAlgorithm)
      layout.addRow(self.btn5,self.algorithm)

      self.execute = QPushButton("Execute")
      self.execute.clicked.connect(self.ExecuteAlgo)

      self.log = QPlainTextEdit(self)

      layout.addRow(self.log)

      self.news = QPlainTextEdit(self)

      self.end_value = QLineEdit()

      self.newslabel = QLabel(self)
      self.loglabel = QLabel(self)

      layout.addRow(self.newslabel)
      layout.addRow(self.news)
      layout.addRow(self.execute)
      layout.addRow(self.chart)
      layout.addRow(self.end_value)
		
      # self.le2 = QLineEdit()
      # layout.addRow(self.btn2,self.le2)

      self.setLayout(layout)
      self.setWindowTitle("PyFutures")

   def getStrings(self):
      names = pd.read_csv('nasdaq.csv')
      items = [ str(x[0]) for x in names.values]
      return items
		
   def getStocks(self):
      # items = ("C", "C++", "Java", "Python")
      names = pd.read_csv('nasdaq.csv')
      items = [ str(x[0]) for x in names.values]
		
      item, ok = QInputDialog.getItem(self, "Company's",
         "Stock Tickers", items, 0, False)
			
      if ok and item:
         self.stock_name.setText(item)

   def getAlgorithm(self):
      items = ("SMA", "Average Range", "High statistics", "Low statistics", "RSI")
      
      item, ok = QInputDialog.getItem(self, "ALGOS", 
         "Trading Algorithms", items, 0, False)
         
      if ok and item:
         self.algorithm.setText(item)
			
   def getStart(self):
      text, ok = QInputDialog.getText(self, 'Text Input Dialog', 'Enter Date')
		
      if ok:
         self.start_date.setText(str(text))

   def getEnd(self):
      text, ok = QInputDialog.getText(self, 'Text Input Dialog', 'Enter Date')
      
      if ok:
         self.end_date.setText(str(text))
			
   def getAmount(self):
      num,ok = QInputDialog.getInt(self,"integer input dualog","enter a number")
		
      if ok:
         self.starting_amount.setText(str(num))

   def getLimit(self):
      num,ok = QInputDialog.getInt(self,"integer input dualog","enter a number")
      
      if ok:
         self.cash_limit.setText(str(num))

   def ExecuteAlgo(self):

      self.resize(1000, 600)

      sdate = self.start_date.text().split("/")
      edate = self.end_date.text().split("/")

      sdate = list(map(int, sdate))
      edate = list(map(int, edate))

      self.newslabel.setText(self.stock_name.text() + " NEWS")

      print(str(self.stock_name.text()).strip())
      #[2017,12,1], [2018,10,1]
      StockQuotes(self.stock_name.text().upper(), int(self.starting_amount.text()), int(self.cash_limit.text()), sdate, edate, self.algorithm.text())
      endvals, self.sim = generateSimulator(str(self.stock_name.text()).strip(),blimit, slimit, int(self.starting_amount.text()), sdate, edate)

      self.end_value.setText(str(endvals))
      self.sim.plot()
      with open('output.csv') as df:
         for line in df:
            self.log.insertPlainText(line)

      articles = GetArticles(self.stock_name.text())
      self.news.insertPlainText(articles)

      pixmap = QPixmap('StockQuotes.png')
      self.chart.setPixmap(pixmap)


			
def main(): 
   app = QApplication(sys.argv)
   ex = inputdialog()
   ex.show()
   sys.exit(app.exec_())
	
if __name__ == '__main__':
   main()