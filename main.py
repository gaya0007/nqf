from datetime  import date
from Queue import Queue
from price_handler import HistoricalPriceHandler
from threading import Thread, Event

def main():
	queue = Queue()
	strt_date = date(2017, 11, 5)
	end_date = date(2017, 11, 15)
	cv = Event()
	phd = HistoricalPriceHandler('EUR_USD', strt_date, end_date, queue, cv)
	phd.start()
	
	while True:
		obj = queue.get()
		if obj.type == 'Done':
			break
		else:
			print obj
		
		cv.clear()
	phd.stop()	
if __name__ == '__main__':
	main()