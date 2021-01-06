from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.utils.crypto import get_random_string
from django.http import HttpRequest
from django.contrib.auth.forms import PasswordResetForm

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField(max_length=200)
    last_name = forms.CharField(max_length=200)
    birthdate = forms.DateField()
    password1 = None
    password2 = None

    class Meta:
        model = User
        #fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
        fields = ['first_name', 'last_name', 'email']

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(get_random_string())
        user.save()
        '''reset_form = PasswordResetForm({'email': user.email})
        assert reset_form.is_valid()
        reset_form.save(
            request=request,
            use_https=request.is_secure(),
            subject_template_name='registration/account_creation_subject.txt',
            email_template_name='registration/account_creation_email.html',
        )'''
        form = PasswordResetForm({'email': user.email})
        assert form.is_valid()
        request = HttpRequest()
        request.META['SERVER_NAME'] = '192.168.1.15'
        request.META['SERVER_PORT'] = '8000'
        form.save(
            request= request,
            use_https=False,
            from_email="smirartdigitalarts@gmail.com"
        )
        return user

    '''def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        self.fields['password1'].required = False
        self.fields['password2'].required = False
        # If one field gets autocompleted but not the other, our 'neither
        # password or both password' validation will be triggered.
        self.fields['password1'].widget.attrs['autocomplete'] = 'off'
        self.fields['password2'].widget.attrs['autocomplete'] = 'off'

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = super(UserCreationForm, self).clean_password2()
        if bool(password1) ^ bool(password2):
            raise forms.ValidationError("Fill out both fields")
        return password2'''

class SignUpForm(forms.Form):
    first_name = forms.CharField(max_length=200)
    last_name = forms.CharField(max_length=200)
    email = forms.EmailField(max_length=254)
    phone = forms.CharField(max_length=200)
    address = forms.CharField(max_length=200)
    birthdate = forms.DateField()
    password1 = forms.CharField(max_length=200, widget=forms.PasswordInput)
    password2 = forms.CharField(max_length=200, widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super(SignUpForm, self).clean()
        first_name = cleaned_data.get('first_name')
        last_name = cleaned_data.get('last_name')
        email = cleaned_data.get('email')
        phone = cleaned_data.get('phone')
        address = cleaned_data.get('address')
        birthdate = cleaned_data.get('birthdate')
        #if not first_name and not last_name and not email and not courses and not prof_assisstans:
        if not first_name and not last_name and not email and not password1 and not password2 and not birthdate:
            raise forms.ValidationError('You have to write something!')

class PasswordForm(forms.Form):
    class Meta:
        model = UserRegisterForm
        fields = ['password1', 'password2']
