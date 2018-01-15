from event import event
from downloader import DownloadMgr
import pandas as pd
from util import node_send_event

class HistoricalPriceHandler():
	def __init__(self, pair, start_date, end_date):
		self.start_date = start_date
		self.end_date = end_date
		self.pair = pair
		self.dmgr = DownloadMgr()

	def stream_df(self):	
		files = self.dmgr.download_historical_data(self.pair, self.start_date, self.end_date)
		strat_date_ts = pd.Timestamp(self.start_date)
		end_date_ts = pd.Timestamp(self.end_date)
		node_send_event(end_date_tsend_date_ts)
		for file in files:
			df = pd.read_pickle(file)
			for index, row in df.iterrows():
				if index >= strat_date_ts and index <= end_date_ts:
					ev = event.TickEvent(self.pair, index, row[0], row[1])
					node_send_event(ev)
				else:
					if index > end_date_ts:
						break
					else:
						continue 					