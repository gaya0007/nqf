import datetime
import calendar
from datetime import timedelta, date

def date_range(start_date, end_date):
	for n in range(int ((end_date - start_date).days)):
		yield start_date + timedelta(n)
		
def week_of_month(tgtdate):
	days_this_month = calendar.mdays[tgtdate.month]
	for i in range(1, days_this_month):
		d = datetime.date(tgtdate.year, tgtdate.month, i)
		if d.day - d.weekday() > 0:
			startdate = d
			break
	return (tgtdate - startdate).days //7 + 1