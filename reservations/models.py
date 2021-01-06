from django.db import models
from django.urls import reverse
from datetime import datetime, timedelta
from django.utils import timezone
from django.contrib.auth.models import User
from services.models import Department

event_status = (
	('PENDING', 'PENDING'),
	('ACCEPTED', 'ACCEPTED'),
	('DENIED', 'DENIED'),
	('CANCELED', 'CANCELED')
)

Hours_Choices = (
	('08:00', '08:00' ), ('08:15', '08:15'), ('08:30', '08:30'), ('08:45', '08:45'),
	('09:00', '09:00' ), ('09:15', '09:15'), ('09:30', '09:30'), ('09:45', '09:45'),
	('10:00', '10:00' ), ('10:15', '10:15'), ('10:30', '10:30'), ('10:45', '10:45'),
	('11:00', '11:00' ), ('11:15', '11:15'), ('11:30', '11:30'), ('11:45', '11:45'),
	('12:00', '12:00' ), ('12:15', '12:15'), ('12:30', '12:30'), ('12:45', '12:45'),
	('13:00', '13:00' ), ('13:15', '13:15'), ('13:30', '13:30'), ('13:45', '13:45'),
	('14:00', '14:00' ), ('14:15', '14:15'), ('14:30', '14:30'), ('14:45', '14:45'),
	('15:00', '15:00' ), ('15:15', '15:15'), ('15:30', '15:30'), ('15:45', '15:45'),
	('16:00', '16:00' ), ('16:15', '16:15'), ('16:30', '16:30'), ('16:45', '16:45'),
	('17:00', '17:00' ), ('17:15', '17:15'), ('17:30', '17:30'), ('17:45', '17:45'),
	('18:00', '18:00' ), ('18:15', '18:15'), ('18:30', '18:30'), ('18:45', '18:45'),
	('19:00', '19:00' ), ('19:15', '19:15'), ('19:30', '19:30'), ('19:45', '19:45'),
	('20:00', '20:00' ), ('20:15', '20:15'), ('20:30', '20:30'), ('20:45', '20:45'),
	('21:00', '21:00' ), ('21:15', '21:15'), ('21:30', '21:30'), ('21:45', '21:45'),
	('22:00', '22:00' ),
)

# Create your models here.
class Reservation(models.Model):
	# patient = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name = u'Μάθημα')
	patient = models.CharField(max_length=100, verbose_name = u'Όνομα')
	department = models.ForeignKey(Department, on_delete=models.CASCADE, verbose_name = u'Τμήμα')
	eventdate = models.DateField(default='2020-01-01', verbose_name = u'Ημερομηνία')
	start_time = models.CharField(max_length=5, choices=Hours_Choices, default='08:00', verbose_name = u'Ώρα Έναρξης')
	timestamp = models.DateTimeField(default=timezone.now)
	author = models.ForeignKey(User, on_delete=models.CASCADE)
	status = models.CharField(max_length=8, choices=event_status, default='PENDING', verbose_name = u'Κατάσταση')
	description = models.TextField(null=True, blank=True, verbose_name = u'Περιγραφή')

	@property
	def get_html_url(self):
		url = reverse('reservation:reservation_edit', args=(self.id,))
		# cs_room = ' - ' + str(self.department)
		# return '<a> %s%s%s </a>' % (cal_time,  'title', cs_room)
		# if self.lab_room=='206':
		return '<a class="info %sc" href="#" > %s - %s - %s - %s <span class="text-left p-2"> Όνομα: %s<br/>Τμήμα: %s<br/>Ώρα: %s </span></a>' % ('six', str(self.patient), str(self.department), str(self.eventdate), str(self.start_time), str(self.patient), str(self.department), str(self.start_time))

		# elif self.lab_room=='210':
		# 	return '<a class="info %sc" href="#" > %s - %s - %s - %s <span class="text-left p-2"> Αίθουσα: %s<br/>Mάθημα: %s<br/>Ώρες: %s - %s </span></a>' % ('ten', self.lab_room, self.course.title, self.start_time, self.end_time, self.lab_room, self.course.title, self.start_time, self.end_time)
		# else:
		# 	return '<a class="info %sc" href="#" > %s - %s - %s - %s <span class="text-left p-2"> Αίθουσα: %s<br/>Mάθημα: %s<br/>Ώρες: %s - %s </span></a>' % ('eleven', self.lab_room, self.course.title, self.start_time, self.end_time, self.lab_room, self.course.title, self.start_time, self.end_time)

	def get_absolute_url(self):
		return reverse('reservations:reservations')
	#
	def get_event_title(self):
		return '<a> %s </a>' % 'patient'

	def __str__(self):
		admin_show = self.patient + " - " + str(self.department)
		return admin_show
