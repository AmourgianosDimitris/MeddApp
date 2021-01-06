from django.conf.urls import url
from django.urls import path, include
from django.views.generic.base import TemplateView # new
from . import views
from .views import *

app_name = 'services'
urlpatterns = [

    path('', views.index, name='index'),
    path('aboutus/', views.aboutus, name='about-us'),
    path('departments/', views.departments, name='departments'),
    path('departments/<str:department>', views.department, name='department'),
    # path('assistant/<int:pk>/delete/', AssistantDeleteView.as_view(), name='assistant-delete'),

]
