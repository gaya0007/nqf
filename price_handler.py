
from event import event
from downloader import DownloadMgr
import pandas as pd
from threading import Thread, Event

class HistoricalPriceHandler(Thread):
	def __init__(self, pair, start_date, end_date, queue, wait):
		Thread.__init__(self)
		self.queue = queue
		self.wait_ev = wait
		self.start_date = start_date
		self.end_date = end_date
		self.pair = pair
		self.dmgr = DownloadMgr()

		
	def run(self):	
		while True:
			files = self.dmgr.download_historical_data(self.pair, self.start_date, self.end_date)
			print files
			for file in files:
				df = pd.read_pickle(file)
				for index, row in df.iterrows():
					ev = event.TickEvent(self.pair, index, row[0], row[1])
					self.queue.put(ev)
					self.wait_ev.set()
					self.wait_ev.wait()
			ev = event.AdminEvent("Done", self.pair)
			self.queue.put(ev)
			
