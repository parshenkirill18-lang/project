from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm

class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput, label='Подтвердите пароль')

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Пароли не совпадают!')
        return cd['password2']

class LoginForm(AuthenticationForm):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
from django import forms
from .models import Order

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['full_name', 'address', 'phone']
        widgets = {
            'full_name': forms.TextInput(attrs={'placeholder':'Ваше имя', 'class':'input-field'}),
            'address': forms.Textarea(attrs={'placeholder':'Адрес доставки', 'class':'input-field', 'rows':3}),
            'phone': forms.TextInput(attrs={'placeholder':'Телефон', 'class':'input-field'}),
        }
