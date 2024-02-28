import requests, json, os
from datetime import datetime
from dotenv import load_dotenv
load_dotenv()

ALPHA_VANTAGE_API_KEY = os.getenv('ALPHA_VANTAGE_API_KEY')

class Backtest():

  def __init__(self, alphaVantageAPIKEY: str, symbol: str, interval: str):
    self.openValue: float = None
    self.highValue: float = None
    self.lowValue: float = None
    self.closeValue: float = None
    self.volumeValue: float = None
    self.alphaVantageAPIKEY: str = alphaVantageAPIKEY
    self.symbol: str = symbol
    self.interval: str = interval

  def loadData(self):
    if os.path.exists(f'Data/{self.symbol}-{self.interval}.json'):
      print(f'Data file already exists...')

      try:
        with open(f'Data/{self.symbol}-{self.interval}.json', 'r') as file:
          tradingData: dict = json.load(file)
      except Exception as e:
        raise Exception(f'Error accessing file data:', e)
    else:
      response = requests.get(f'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={self.symbol}&interval={self.interval}&outputsize=full&apikey={self.alphaVantageAPIKEY}')

      if response.status_code == 200:
        tradingData: dict = response.json()
      else:
        raise Exception('Failed to fetch data')

    return tradingData

  def filterDataByDateRange(self, tradingData:dict, startDate: str, endDate: str, afterHoursTrading: bool):
      if afterHoursTrading == True:
        startDate: datetime = datetime.strptime(startDate + ' 04:00:00', '%Y-%m-%d %H:%M:%S')
        endDate: datetime = datetime.strptime(endDate + ' 20:00:00', '%Y-%m-%d %H:%M:%S')
      elif afterHoursTrading == False:
        startDate: datetime = datetime.strptime(startDate + ' 09:30:00', '%Y-%m-%d %H:%M:%S')
        endDate: datetime = datetime.strptime(endDate + ' 15:55:00', '%Y-%m-%d %H:%M:%S')

      tradingDataJson: dict = tradingData[f'Time Series ({self.interval})']

      filteredDict = {}

      for timestamp, value in tradingDataJson.items():
        datetimeTimestamp = datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S')
        if startDate <= datetimeTimestamp <= endDate:
                filteredDict[datetimeTimestamp] = value

      sortedDict = dict(sorted(filteredDict.items(), key=lambda item: item[0]))

      return sortedDict

  def processData(self, timestamp, data):
     self.openValue = data['1. open']
     self.highValue = data['2. high']
     self.lowValue = data['3. low']
     self.closeValue = data['4. close']
     self.volumeValue = data['5. volume']
     self.date, self.time = str(timestamp).split(' ')

     formattedData = {
      'T': 'b',
      'S': f'{self.symbol}',
      'o': self.openValue,
      'h': self.highValue,
      'l': self.lowValue,
      'c': self.closeValue,
      'v': self.volumeValue,
      't': self.date + 'T' + self.time + 'Z',
     }

     return formattedData

  def runBacktest(self, algorithm, startDate: str, endDate: str, afterHoursTrading: bool):
     data = self.loadData()
     filterData = self.filterDataByDateRange(data, startDate, endDate, afterHoursTrading)

     for timestamp, data in filterData.items():
        formattedData = self.processData(timestamp, data)
        algorithm(formattedData)

# if __name__ == '__main__':
#   bck = Backtest(ALPHA_VANTAGE_API_KEY, symbol='SPY', interval='5min')
#   bck.runBacktest(algorithm=algorithm, startDate='2024-2-1', endDate='2024-2-27', afterHoursTrading=False)
