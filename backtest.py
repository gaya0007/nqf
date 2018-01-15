from datetime  import date, datetime
from Queue import Queue
from price_handler import HistoricalPriceHandler
from threading import Thread
import socket
import sys
import json
import io
from util import node_send_event


def read_in():
    lines = sys.stdin.readlines()
    #Since our input would only be having one line, parse our JSON data from that
    return json.loads(lines[0])

def run_bt(start, end):
	strt_date = (datetime.strptime(start, '%Y/%m/%d')).date()
	end_date = (datetime.strptime(end, '%Y/%m/%d')).date()
	phd = HistoricalPriceHandler('EUR_USD', strt_date, end_date)
	phd.stream_df()


	
	
if __name__ == '__main__':	
	while True:
		d = read_in()
		#str = '{ "msg": "start_bt", "start": "2017/11/09", "end": "2017/11/09" }'
		#d = json.loads(str)
		if d['msg'] == 'start_bt':
			node_send_event("start")
			run_bt(d['start'], d['end'])