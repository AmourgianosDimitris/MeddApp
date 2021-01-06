from django import forms
from datetime import datetime, timedelta, date
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponse, HttpResponseRedirect
from django.utils.datastructures import MultiValueDictKeyError #####
from django.views import generic
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.forms.utils import ErrorList
import calendar
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)

from .models import Reservation
from .utils import Calendar
from .forms import ReservationForm
from services.models import Department
from tempus_dominus.widgets import DateTimePicker

# Create your views here.
class CalendarView(generic.ListView):
    model = Reservation
    template_name = 'reservations/calendar.html'
    fields = ('department')

    def get_context_data(self, **kwargs):

        user = self.request.user
        if user.is_superuser:
            reservations = Reservation.objects.all().order_by('-timestamp')
        elif user.is_staff:
            dep = Department.objects.filter(title=user.username)[0]
            print("`````````````", dep)
            reservations = Reservation.objects.filter(department=dep).order_by('timestamp')
        else:
            reservations = Reservation.objects.filter(author=user).order_by('-timestamp')

        context = super().get_context_data(**kwargs)
        d = get_date(self.request.GET.get('month', None))
        cal = Calendar(d.year, d.month)
        department = self.request.POST.get('department')

        html_cal = cal.formatmonth(reservations, withyear=True)
        context['calendar'] = mark_safe(html_cal)
        context['prev_month'] = prev_month(d)
        context['next_month'] = next_month(d)
        # context['get_department'] = get_department(department)
        #
        print("Lab Rooms: ")
        print(department)
        # print (context)
        return context


def get_date(req_month):
    if req_month:
        year, month = (int(x) for x in req_month.split('-'))
        return date(year, month, day=1)
    return datetime.today()

def prev_month(d):
    first = d.replace(day=1)
    prev_month = first - timedelta(days=1)
    month = 'month=' + str(prev_month.year) + '-' + str(prev_month.month)
    return month

def next_month(d):
    days_in_month = calendar.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    next_month = last + timedelta(days=1)
    month = 'month=' + str(next_month.year) + '-' + str(next_month.month)
    return month

def get_department(request):
    cs_lab = request.POST.get('department')
    return cs_lab

def event(request, reservation_id=None):
    instance = Reservation()
    if reservation_id:
        instance = get_object_or_404(Reservation, pk=reservation_id)
    else:
        instance = Reservation()

    form = ReservationForm(request.POST or None, instance=instance)
    if request.POST and form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse('reservation:calendar'))
    return render(request, 'reservation/reservation.html', {'form': form})

class ReservationListView(LoginRequiredMixin, ListView):
    model = Reservation
    template_name = 'reservations/reservations.html'
    context_object_name = 'reservations'
    paginate_by = 25

    def get_queryset(self):
        user = self.request.user
        reservations = Reservation.objects
        if user.is_superuser:
            reservations = Reservation.objects.all().order_by('-timestamp')
        elif user.is_staff:
            dep = Department.objects.filter(title=user.username)[0]
            print("`````````````", dep)
            reservations = Reservation.objects.filter(department=dep).order_by('timestamp')
        else:
            reservations = Reservation.objects.filter(author=user).order_by('-timestamp')
        return reservations

    # def get_context_data(self, *args, **kwargs):
    #     context = super(ReservationListView, self).get_context_data(*args, **kwargs)
    #     if 'status' in self.request.GET:
    #         context['status'] = self.request.GET['status']
    #     if 'department' in self.request.GET:
    #         context['department'] = self.request.GET['department']
    #     return context

def time_to_int(time):
    time = time.split(':')
    return int(time[0]) * 60 + int(time[1])

class ReservationCreateView(LoginRequiredMixin, CreateView):
    model = Reservation
    fields = ['patient', 'department', 'eventdate', 'start_time', 'description']
    def form_valid(self, form):
        start_time = self.request.POST['start_time']
        # end_time = self.request.POST['end_time']
        # if time_to_int(start_time) >= time_to_int(end_time):
        #     #form._errors[forms.forms.NON_FIELD_ERRORS] = ErrorList([u''])
        #     form.add_error('end_time', 'Η ώρα λήξης πρέπει να είναι μεγαλύτερη από την ώρα έναρξης.')
        #     return super().form_invalid(form)
        reservations = Reservation.objects.filter(department=form.instance.department, eventdate=form.instance.eventdate, status='ACCEPTED')
        formstart = time_to_int(form.instance.start_time)
        # formend = time_to_int(form.instance.end_time)
        for reservation in reservations:
            if not(time_to_int(reservation.start_time) == formstart) :
                form._errors[forms.forms.NON_FIELD_ERRORS] = ErrorList([u'Το εργαστήριο μας δεν είναι διαθέσιμο για την ώρα και την ημερομηνία που επιλέξατε.'])
                return super().form_invalid(form)
        form.instance.author = self.request.user

        # from_email = settings.EMAIL_HOST_USER
        # recipient_list = ['amoyrgianos@windowslive.com']
        # #if name and email and courses and prof_assistants:
        #
        # subject = "Αίτηση Κράτησης από το Labtutor"
        # text = "Στοιχεία Κράτησης:\n"
        # now = datetime.now()
        # now_format = now.strftime("%d/%m/%Y %H:%M")
        # text_2 = "Καθηγητής: " + self.request.user.first_name + " " + self.request.user.last_name + "\nΗμέρα και Ώρα Υποβολής: " + str(now_format)
        # message = text + text_2 + "\nΜάθημα: " + str(form.instance.course) + ", Αίθουσα: " + str(form.instance.lab_room) + "\nΗμέρα Κράτησης: " + str(form.instance.eventdate) + ", Ώρα Έναρξης: " + str(form.instance.start_time) + ", Ώρα Λήξης: " + str(form.instance.end_time)
        #     # print ('Subject: ', subject, '\nMessage: ', message)
        # send_mail(subject, message, from_email, recipient_list)

        return super().form_valid(form)
    #
    # def get_form(self, form_class=None):
    #     form = super(ReservationCreateView, self).get_form(form_class)
    #     if self.request.user.is_staff:
    #         form.fields['course'].widget = forms.Select(choices=Course.objects.all().values_list("id", "title"))
    #     else:
    #         form.fields['course'].widget = forms.Select(choices=Course.objects.filter(professor__username=self.request.user.username).values_list("id", "title"))
    #     form.fields['eventdate'].widget = widget=DateTimePicker(
    #         options={
    #             'locale':'el',
    #             'format':'DD/MM/YYYY',
    #         },
    #     )
    #     form.fields['eventdate'].input_formats = ('%d/%m/%Y',)
    #     return form
# {% url 'cal:event-update' event.id %}
class ReservationUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Reservation
    fields = ['patient', 'department', 'eventdate', 'start_time', 'description']

    def form_valid(self, form, **kwargs):
        start_time = self.request.POST['start_time']
        # end_time = self.request.POST['end_time']
        # if time_to_int(start_time) >= time_to_int(end_time):
        #     #form._errors[forms.forms.NON_FIELD_ERRORS] = ErrorList([u''])
        #     form.add_error('end_time', 'Η ώρα λήξης πρέπει να είναι μεγαλύτερη από την ώρα έναρξης.')
        #     return super().form_invalid(form)
        if 'status' in self.request.POST:
            if self.request.POST['status'] == '1':
                reservations = Reservation.objects.filter(department=form.instance.department, eventdate=form.instance.eventdate, status='ACCEPTED')
                formstart = time_to_int(form.instance.start_time)
                # formend = time_to_int(form.instance.end_time)
                for reservation in reservations:
                    if not(time_to_int(reservation.start_time) == formstart) :
                        form._errors[forms.forms.NON_FIELD_ERRORS] = ErrorList([u'Το εργαστήριο μας δεν είναι διαθέσιμο για την ώρα και την ημερομηνία που επιλέξατε.'])
                        return super().form_invalid(form)
        if 'status' in self.request.POST:
            status = self.request.POST['status']
            if status == '0':
                form.instance.status = 'DENIED'
            elif status == '1':
                form.instance.status = 'ACCEPTED'
            elif status == '2':
                form.instance.status = 'CANCELED'
        return super().form_valid(form)

    def test_func(self):
        reservation = self.get_object()
        if self.request.user.is_staff or self.request.user == reservation.author:
            return True
        return False

    def get_context_data(self, *args, **kwargs):
        context = super(ReservationUpdateView, self).get_context_data(*args, **kwargs)
        context['edit'] = True
        return context

class ReservationDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Reservation
    success_url = '/reservations/'

    def test_func(self):
        reservation = self.get_object()
        if self.request.user.is_staff or self.request.user == reservation.author:
            return True
        return False
