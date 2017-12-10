
from .event import TickEvent, AdminEvent
from .backtest import DownloadMgr
import pandas as pd

class HistoricalPriceHandler(Thread):
	def __init__(self, pair, start_date, end_date, queue):
		Thread.__init__(self)
		slef.queue = queue
		self.condition = threading.Condition()
		self.start_date = start_date
		self.end_date = end_date
		self.pair = pair
		self.dmgr = DownloadMgr()
		
	def run():	
		while True:
			files = self.dmgr.download_historical_data(self.pair, self.start_date, self.end_date)
			for file in files:
				df = pd.read_pickle(file)
				for index, row in df.iterrows():
					self.condition.wait()
					event = TickEvent()
					queue.put(event)
		
	def stream_df(self, ):

		for file in files:
			df = pd.read_pickle(file)
			
	def get_next():
		self.condition.notifyAll()