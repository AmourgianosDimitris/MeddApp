from django.shortcuts import render, redirect
from .forms import UserRegisterForm, SignUpForm
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import user_passes_test
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)

from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.forms import PasswordResetForm
from .models import *

def staff_check(user):
    return user.is_staff

def get_user(user):
    return user

def thanks(request):
    return redirect('/')

@user_passes_test(staff_check)
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.instance.username = form.cleaned_data.get('email').split('@')[0]
            form.save()
            return redirect('users:user-list')
    else:
        form = UserRegisterForm()
    return render(request, 'users/user_form.html', {'form':form})

def signup(request):

    if request.method == 'POST':

        form = SignUpForm(request.POST)
        if form.is_valid():

            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            email = form.cleaned_data.get('email')
            phone = form.cleaned_data.get('phone')
            address = form.cleaned_data.get('address')
            birthdate = form.cleaned_data.get('birthdate')
            password1 = form.cleaned_data.get('password1')
            password2 = form.cleaned_data.get('password2')
            print ("phone: ", phone)

            if not first_name or not last_name or not email or not phone or not address or not birthdate or not password1 or not password2:
                form = SignUpForm()
                return render(request, 'users/signup.html', {'form': form})

            if password1 == password2:
                username = first_name + " " + last_name
                user = User.objects.create_user(username, email, password1, is_staff=False, is_superuser=False)
                user.first_name = first_name
                user.last_name = last_name
                user.save()
                # print(user.password)
                print (phone)
                print(address)
                # profile = Profile(user=user, phone=phone, address=address, birthdate=birthdate)
                profile = Profile(user=user, phone=phone, address=address, birthdate=birthdate)
                profile.save()

                return redirect('/')

            else:
                form = SignUpForm()
                return render(request, 'users/signup.html', {'form': form})
            #else:
            #    print ('Wrong password!')
            #    form = SignUpForm()
    else:
        form = SignUpForm()
    return render(request, 'users/signup.html', {'form': form})

# def get_profile():
#     return Profile.odjects.all()

class Profile(LoginRequiredMixin, ListView):
    model = Profile
    template_name = 'users/users.html'
    context_object_name = 'profiles'


    def get_queryset(self):
        user = self.request.user

        profile = Profile.all().filter(user=self.request.user)
        # profile = get_profile()
        return profile



class UserListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = User
    template_name = 'users/userslist.html'
    context_object_name = 'users'
    paginate_by = 25

    def get_queryset(self):
        return User.objects.order_by('last_name')

    def test_func(self):
        if self.request.user.is_staff:
            return True
        return False

class UserUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = User
    template_name = 'users/user_form.html'
    fields = ['username', 'first_name', 'last_name', 'email']
    success_url = '/users'

    def form_valid(self, form):
        return super().form_valid(form)

    def test_func(self):
        if self.request.user.is_staff:
            return True
        return False

    def get_context_data(self, *args, **kwargs):
        context = super(UserUpdateView, self).get_context_data(*args, **kwargs)
        context['edit'] = True
        return context

class UserDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = User
    template_name = 'users/user_confirm_delete.html'
    success_url = '/users'

    def test_func(self):
        if self.request.user.is_staff:
            return True
        return False
