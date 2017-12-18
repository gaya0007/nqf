from datetime  import date, datetime
from Queue import Queue
from price_handler import HistoricalPriceHandler
from threading import Thread, Lock
import socket
import sys
import json

HOST, PORT = "127.0.0.1", 6969

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def run_bt(start, end):
	queue = Queue()
	strt_date = (datetime.strptime(start, '%d/%m/%Y')).date()
	end_date = (datetime.strptime(end, '%d/%m/%Y')).date()
	print "start {}".format(strt_date)
	print "end {}".format(end_date)
	cv = Lock()
	phd = HistoricalPriceHandler('EUR_USD', strt_date, end_date, queue, cv)
	phd.start()
	sock.connect((HOST, PORT))
	
	while True:
		obj = queue.get()
		if obj.type == 'Done':
			break
		else:
			sock.sendall(str(obj))
		cv.release()	
		
	phd.join()	
	sock.close()
	
	
if __name__ == '__main__':
	print "arguments " + sys.argv[1]
	run_bt(sys.argv[1], sys.argv[2])