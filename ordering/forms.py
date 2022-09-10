from django import forms
from ordering.models import Checkout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model


User = get_user_model()

class CheckoutForm(forms.ModelForm):
    address = forms.CharField(widget=forms.Textarea)
    class Meta:
        model = Checkout
        fields = ['address', 'cellphone', 'email', 'full_name', 'payment_method']
        widgets = {
        'address': forms.Textarea(attrs={'cols': 30, 'rows': 10}),
        'cellphone': forms.TextInput()
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
        for field in self.fields:
                self.fields[str(field)].widget.attrs.update({
                    'class': 'block w-full px-4 py-2 text-gray-700 bg-white border rounded-md focus:border-blue-400 focus:ring-blue-300 focus:outline-none focus:ring focus:ring-opacity-40',
                    'placeholder': str(field).replace('_', ' ').capitalize(),
                })



class ContactForm(forms.Form):
    name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={
        'class':'block w-full px-4 py-2 text-gray-700 bg-white border rounded-md focus:border-blue-400 focus:ring-blue-300 focus:outline-none focus:ring focus:ring-opacity-40'
        }))
    message = forms.CharField(widget=forms.Textarea(attrs={
        'class':'block w-full px-4 py-2 text-gray-700 bg-white border rounded-md focus:border-blue-400 focus:ring-blue-300 focus:outline-none focus:ring focus:ring-opacity-40'
        }))
    email = forms.CharField(widget=forms.TextInput(attrs={
        'class':'block w-full px-4 py-2 text-gray-700 bg-white border rounded-md focus:border-blue-400 focus:ring-blue-300 focus:outline-none focus:ring focus:ring-opacity-40',
        'type':'email'
        }))



class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    username = forms.CharField(required=True, min_length=4, max_length=10)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        user.email = self.cleaned_data['email']

        if commit:
            user.save()
            
        return user

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'block w-full px-2 py-1 mb-4 border border-2 border-transparent border-gray-200 rounded-lg focus:ring focus:ring-j6primary focus:outline-none',
        'placeholder': 'Username'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'block w-full px-2 py-1 mb-4 border border-2 border-transparent border-gray-200 rounded-lg focus:ring focus:ring-j6primary focus:outline-none',
        'placeholder': 'Password'
    }))
    
        