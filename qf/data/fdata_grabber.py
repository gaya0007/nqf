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
from datetime import datetime
from datetime import timedelta, date
from calander import 

logging.basicConfig()
logger = logging.getLogger(__name__)

download_site = 'http://ratedata.gaincapital.com/'
from requests import get
from io import BytesIO
from zipfile import ZipFile

__all__ = ['download_historical_data']


def download_unzip(url, path):
	request = get(url)
	if request.status_code != 200:
		logger.warn("Zip file get error for url %s", url)
		return
	zip_file = ZipFile(BytesIO(request.content))
	logger.info("Extracting files %s", zip_file.namelist())

	try:
		zip_file.extractall(path)
	except Exception as e:	
		logger.error("Zip file extract error: %s",zip_file.getinfo(filename))
		return
		
def prepare_download_urls(pair, from_date, to_date):
	urls = []
	wmp = week_of_month(from_date)
	if wmp != 0:
		urls.append(download_site + from_date.strftime('%Y') + '/' + from_date.strftime('%m') + ' ' + from_date.strftime("%B") + '/' + pair + '_Week' + '{}'.format(wmp) + '.zip')
	for single_date in date_range(from_date, to_date):
		wm = week_of_month(single_date)
		if wm != wmp and wm != 0:
			wmp = wm
			urls.append(download_site + single_date.strftime('%Y') + '/' + single_date.strftime('%m') + ' ' + single_date.strftime("%B") + '/' + pair + '_Week' + '{}'.format(wmp) + '.zip')
	return urls		

def download_historical_data(pair, from_date, to_date):
	urls = prepare_download_urls(pair, from_date, to_date)
	for url in urls:
		ids = url.split('/')
		path = settings.DATA_DIR + ids[3] + '_' + re.sub(r'\D', '',ids[4]) + '_' +  ids[5].translate(None, '.zip')
		if not os.path.isdir(path):
			logger.info("Downloading  url :%s to :%s", url, path)
			download_unzip(url, path)
			get_csv_files_and_resample()
		
def gain_parser(dt_str):
	try:
		return datetime.strptime(dt_str[:-3],'%Y-%m-%d %H:%M:%S.%f')
	except Exception as e:
		return datetime.strptime(dt_str,'%Y-%m-%d %H:%M:%S')
		
def read_save_pkl(dir):
	for file in os.listdir(dir):
		if file.endswith('csv'):
			filename = dir + file
			eu = pd.read_csv(filename,index_col=3,date_parser=gain_parser)
			del eu['lTid'] 
			del eu['cDealable']
			del eu['CurrencyPair']
			grouped_data = eu.dropna()
			#grouped_data = eu.resample('1Min').ohlc()
			grouped_data.to_pickle(filename + '.pkl')		
			os.remove(filename)
		
def get_csv_files_and_resample():
	for dir_name in os.listdir('./Data'):
		if os.path.isdir(os.path.join('./Data/', dir_name)):
			dir_name = './Data/'+ dir_name + '/'
			read_save_pkl(dir_name)
		
def get_pkl_files(dir):
	file_list = []
	for file in os.listdir(dir):
		if file.endswith('.pkl'):
			file_list.append(file)
	return 	file_list


	
#def read_sampled_files():
#	for dir_name in os.listdir('./Data'):
#		if os.path.isdir(os.path.join('./Data/', dir_name)):
#			dir_name = './Data/'+ dir_name + '/'
#			pkl_files = get_pkl_files(dir_name)
#			for file in pkl_files:
#				with open(dir_name + file, 'rb') as f:
#					data = pickle.load(f)
#				print "from file {}{}".format(dir_name,file)	
#				print data['RateBid'].head()
#				print data['RateBid'].tail()	