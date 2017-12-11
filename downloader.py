'''
Created on 29 Apr 2017

@author: Gayan
'''
import pandas as pd
import urllib
import re
import os
import pickle
import logging
import settings
import datetime
from requests import get
from datetime import timedelta, date
from threading import Thread
from Queue import Queue
import calendar

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


from requests import get
from io import BytesIO
from zipfile import ZipFile

class FCalandar:
	def __init__(self):
		pass
	def week_of_month(self, tgtdate):
		days_this_month = calendar.mdays[tgtdate.month]
		for i in range(1, days_this_month):
			d = datetime.date(tgtdate.year, tgtdate.month, i)
			if d.day - d.weekday() > 0:
				startdate = d
				break
		return (tgtdate - startdate).days //7 + 1
	
	def date_range(self, start_date, end_date):
		for n in range(int ((end_date - start_date).days)):
			yield start_date + timedelta(n)	
			
class FileHandler:
	def __init__(self):
		pass
				
	def get_pkl_files(self, dir):
		file_list = []
		for file in os.listdir(dir):
			if file.endswith('.pkl'):
				file_list.append(file)
		return 	file_list
	
	def stream_pkl(self, files):
		for file in files:
			df = pd.read_pickle(file)
			
		
class Downloader(Thread):
	def __init__(self, queue, ret):
		Thread.__init__(self)
		self.queue = queue
		self.ret = ret
	def run(self):
		try:
			while True:
				extract_ok = False
				directory, link = self.queue.get()
				
				request = get(link)
				if request.status_code != 200:
					logger.warn("Zip file get error for link %s", link)
					logger.info("Signalling Task Done.")
					self.queue.task_done()
				else:
					zip_file = ZipFile(BytesIO(request.content))
					logger.info("Extracting files %s", zip_file.namelist())
					try:
						zip_file.extractall(directory)
						extract_ok = True
					except Exception as e:	
						logger.error("Zip file extract error: %s",zip_file.getinfo(filename))
					if extract_ok:
						for f in zip_file.namelist():
							file = directory + f
							if os.path.isfile(file):
								logger.info("Extracting files %s", file)
								self.read_csv_and_pickle(file)
								self.ret.append(file)
								logger.info("Signalling Task Done.")
								self.queue.task_done()
							else:
								logger.warning("file %s not found.", file)
								
					else:
						self.queue.task_done()
		except Exception as e:
			logger.error("Downloader error %s.", e)
			logger.info("Signalling Task Done.")
			self.queue.task_done()
			
	def gain_parser(self, dt_str):
		try:
			return datetime.datetime.strptime(dt_str[:-3],'%Y-%m-%d %H:%M:%S.%f')
		except Exception as e:
			return datetime.datetime.strptime(dt_str,'%Y-%m-%d %H:%M:%S')
			
	def read_csv_and_pickle(self, path):
		logger.info("Pickling files %s", path)
		eu = pd.read_csv(path,index_col=3,date_parser=self.gain_parser)
		del eu['lTid'] 
		del eu['cDealable']
		del eu['CurrencyPair']
		grouped_data = eu.dropna()
		#grouped_data = eu.resample('1Min').ohlc()
		grouped_data.to_pickle(path.replace('.csv', '.pkl'))		
		os.remove(path)		
			
class DownloadMgr:
	def __init__(self):
		self.cal = FCalandar()
		
	def prepare_download_urls(self, pair, from_date, to_date):
		urls = []
		wmp = self.cal.week_of_month(from_date)
		if wmp != 0:
			url = settings.HIST_DATA_SITE + from_date.strftime('%Y') + '/' + from_date.strftime('%m') + ' ' + from_date.strftime("%B") + '/' + pair + '_Week' + '{}'.format(wmp) + '.zip'
			urls.append(url)
		for single_date in self.cal.date_range(from_date, to_date):
			wm = self.cal.week_of_month(single_date)
			if wm != wmp and wm != 0:
				wmp = wm
				url = settings.HIST_DATA_SITE + single_date.strftime('%Y') + '/' + single_date.strftime('%m') + ' ' + single_date.strftime("%B") + '/' + pair + '_Week' + '{}'.format(wmp) + '.zip'
				urls.append(url)
		return urls		

	def download_historical_data(self, pair, from_date, to_date):
		urls = self.prepare_download_urls(pair, from_date, to_date)
		n_urls =  len(urls)
		n_threads = min(4, n_urls)
		queue = Queue()
		ret = []
		
		for thrd in range(n_threads):
			logger.info("creading download thread %d", thrd) 
			worker = Downloader(queue, ret)
			# Setting daemon to True will let the main thread exit even though the workers are blocking
			worker.daemon = True
			worker.start()
		
		for url in urls:
			ids = url.split('/')
			path = '{}/{}/{}/{}/'.format(settings.CSV_DATA_DIR, pair, ids[3] , re.sub(r'\D', '',ids[4]) + '_' +  ids[5].translate(None, '.zip'))
			file = path + ids[5].translate(None, '.zip') + '.pkl'
			#TODO : check if the path exisists, if not download
			if os.path.isfile(file):
				logger.info("Data file %s exisists, download skipped.", file)
				ret.append(file)
			else:
				logger.info("Adding url %s to download queue", url)
				queue.put((path, url))
			
		queue.join()
		return ret

		

'''
	Define the test functional tests below
'''
	
if __name__ == '__main__':
	dmgr = DownloadMgr()
	strt_date = date(2017, 11, 5)
	end_date = date(2017, 11, 15)
	dmgr.download_historical_data('EUR_USD', strt_date, end_date)
	
