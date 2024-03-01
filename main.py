from backtest import Backtest
from dotenv import load_dotenv
import os
load_dotenv()

ALPHA_VANTAGE_API_KEY = os.getenv('ALPHA_VANTAGE_API_KEY')

class Algorithm():
  def __init__(self, backtest):
    self.backtest = backtest
    self.openValue = None
    self.highValue = None
    self.lowValue = None
    self.closeValue = None

  def runAlgorithm(self, data):
    print(data)

    if all([self.closeValue is not None, self.openValue is not None, self.lowValue is not None, self.highValue is not None]):
      if self.closeValue > self.openValue:
        self.backtest.marketBuyOrder(0.25, 0.005)

if __name__ == '__main__':
  backtest = Backtest(ALPHA_VANTAGE_API_KEY, symbol='TSLA', interval='5min', accountBalance=5000)
  algorithm = Algorithm(backtest=backtest)
  backtest.runBacktest(algorithm=algorithm.runAlgorithm, startDate='2024-2-1', endDate='2024-2-27', afterHoursTrading=False)