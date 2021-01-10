from django.conf.urls import url
from django.urls import path, include
from django.views.generic.base import TemplateView # new
from . import views
from .views import UserListView, UserUpdateView, UserDeleteView, Profile
from django.contrib.auth import views as auth_views

app_name = 'users'
urlpatterns = [
    #url(r'^index/$', views.index, name='index'),
    #path('accounts/', include('django.contrib.auth.urls'), name='login'), # new
    #url(r'^profil/', TemplateView.as_view(template_name='cal/profil.html'), name='profil'), #
    path('thanks/', views.thanks , name='thanks'),
    path('signup/', views.signup, name='user-signup'),
    path('signin/', auth_views.LoginView.as_view(template_name='users/login.html'), name='signin'),
    path('signout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='signout'),
    path('profile/', Profile.as_view(), name='profile'),
    # path('user/new/', views.register, name='user-create'),
    path('user/<int:pk>/update/', UserUpdateView.as_view(), name='user-update'),
    path('user/<int:pk>/delete/', UserDeleteView.as_view(), name='user-delete'),
]
