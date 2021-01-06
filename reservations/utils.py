#cal/utils

from calendar import HTMLCalendar
from datetime import datetime as dtime, date, time
import datetime
from .models import Reservation
from services.models import Department


class Calendar(HTMLCalendar):
	def __init__(self, year=None, month=None):
		super(Calendar, self).__init__()
		self.theyear = year
		self.themonth = month


	def formatday(self, day, weekday, events):
		"""
		Return a day as a table cell.
		"""
		events_from_day = events.filter(eventdate__day=day, status='ACCEPTED')
		events_html = "<ul class='events'>"
		for event in events_from_day:
			events_html += "<li>%s</li>" % (event.get_html_url)
		events_html += "</ul>"
		if day == 0:
			return '<td></td>'  # day outside month
		else:
			return '<td> <span class="date"> %d </span> <ul> %s </ul> </td>' % (day, events_html )

	def formatweek(self, theweek, events):
		"""
		Return a complete week as a table row.
		"""
		s = ''.join(self.formatday(d, wd, events) for (d, wd) in theweek)
		return '<tr>%s</tr>' % s

	def formatmonth(self, reservations, withyear = True):

		"""
		Return a formatted month as a table.
		"""
		reservations = reservations.filter(eventdate__month = self.themonth)

		v = []
		a = v.append
		a('<table border="0" cellpadding="0" cellspacing="0" class="calendar">')
		a('\n')
		a(self.formatmonthname(self.theyear, self.themonth, withyear=withyear))
		a('\n')
		a(self.formatweekheader())
		a('\n')
		for week in self.monthdays2calendar(self.theyear, self.themonth):
			a(self.formatweek(week, reservations))
			a('\n')
		a('</table>')
		a('\n')
		return ''.join(v)
