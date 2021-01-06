from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
from .models import *
import re


# Create your views here.

def index(request):
     return render(request, 'services/index.html')

def aboutus(request):
     return render(request, 'services/about.html')

def departments(request):

    depart = Department.objects.all()

    for d in depart:
        depart.introduction = d.introduction.split()[:20]

    return render(request,'services/departments_list.html',{'depart':depart})

def department(request, department):

    depart = Department.objects.filter(title=department)

    return render(request,'services/department.html',{'depart':depart})
