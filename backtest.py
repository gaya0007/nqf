from datetime  import date, datetime
from Queue import Queue
from price_handler import HistoricalPriceHandler
from threading import Thread
import socket
import sys
import json
import io

def bt_print(data):
	print data
	sys.stdout.flush()

def read_in():
    lines = sys.stdin.readlines()
    #Since our input would only be having one line, parse our JSON data from that
    return json.loads(lines[0])

def run_bt(start, end):
	queue = Queue()
	strt_date = (datetime.strptime(start, '%d/%m/%Y')).date()
	end_date = (datetime.strptime(end, '%d/%m/%Y')).date()
	print "start {}".format(strt_date)
	print "end {}".format(end_date)
	phd = HistoricalPriceHandler('EUR_USD', strt_date, end_date, queue)
	phd.stream()
	
	
	while True:
		obj = queue.get()
		if obj.type == 'Done':
			break
		else:
			bt_print(obj)

		
	phd.join()	

	
	
if __name__ == '__main__':	
	while True:
		#input = read_in();
		input = "{u'msg': u'start_bt', u'start': u'2017/11/15', u'end': u'2017/11/15'}"
		d = json.loads(input)
		bt_print(d['msg'])

		bt_print(d)
		#if d.msg == 'start_bt':
		#	run_bt(d.start, d.end)