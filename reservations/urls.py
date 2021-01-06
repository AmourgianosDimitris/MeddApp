
from django.conf.urls import url
from django.urls import path, include
from django.views.generic.base import TemplateView # new
from . import views
from .views import ReservationListView, ReservationCreateView , ReservationUpdateView, ReservationDeleteView#, event_download

app_name = 'reservation'
urlpatterns = [
    #url(r'^index/$', views.index, name='index'),
    #path('accounts/', include('django.contrib.auth.urls'), name='login'), # new
    #url(r'^profil/', TemplateView.as_view(template_name='cal/profil.html'), name='profil'), #
    #path('event/new/', views.event, name='event_new'),

    path('reservations/', ReservationListView.as_view(), name='reservations'),
    path('reservations/new/', ReservationCreateView.as_view(), name='reservation-create'),
    path('reservations/<int:pk>/update/', ReservationUpdateView.as_view(), name='reservation-update'),
    path('reservations/<int:pk>/delete/', ReservationDeleteView.as_view(), name='reservation-delete'),
    # path('reservations/download/', event_download, name='event-download'),
    #
    url(r'^reservations/edit/(?P<reservations_id>\d+)/$', views.event, name='reservation_edit'),
    path('calendar/', views.CalendarView.as_view(), name='calendar'),
]
