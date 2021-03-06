
from event import event
from downloader import DownloadMgr
import pandas as pd
from threading import Thread

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
			strat_date_ts = pd.Timestamp(self.start_date)
			end_date_ts = pd.Timestamp(self.end_date)
			for file in files:
				df = pd.read_pickle(file)
				for index, row in df.iterrows():
					if index >= strat_date_ts and index <= end_date_ts:
						ev = event.TickEvent(self.pair, index, row[0], row[1])
						self.wait_ev.acquire()
						self.queue.put(ev)
					else:
						if index > end_date_ts:
							break
						else:
							continue		
			ev = event.AdminEvent("Done", self.pair)
			self.queue.put(ev)
			break;
