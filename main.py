from backtest import Backtest
from dotenv import load_dotenv
import os
load_dotenv()

ALPHA_VANTAGE_API_KEY = os.getenv('ALPHA_VANTAGE_API_KEY')

class Algorithm():
  def __init__(self):
    self.openValue = None
    self.highValue = None
    self.lowValue = None
    self.closeValue = None

  def runAlgorithm(self, data):
    print(data)

if __name__ == '__main__':
  algorithm = Algorithm()
  backtest = Backtest(ALPHA_VANTAGE_API_KEY, symbol='SPY', interval='5min')
  backtest.runBacktest(algorithm=algorithm.runAlgorithm, startDate='2024-2-1', endDate='2024-2-27', afterHoursTrading=False)