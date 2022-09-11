from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model
from ordering.models import Profile


User = get_user_model()



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


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
        for field in self.fields:
            if str(field) == 'password1' or str(field) == 'password2':
                self.fields[str(field)].widget.attrs.update({
                    'class': 'block w-full px-2 py-1 mb-4 border border-2 border-transparent border-gray-200 rounded-lg focus:ring focus:ring-j6primary focus:outline-none',
                    'placeholder': 'Password',
                })
                print(self.fields[field],"true")
            else:
                self.fields[str(field)].widget.attrs.update({
                    'class': 'block w-full px-2 py-1 mb-4 border border-2 border-transparent border-gray-200 rounded-lg focus:ring focus:ring-j6primary focus:outline-none',
                    'placeholder': str(field).replace('_', ' ').capitalize(),
                })


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


class ProfileForm(forms.ModelForm):
    first_name = forms.CharField(required=True, widget=forms.TextInput(attrs={
        'class': 'block w-full px-2 py-1 mb-4 border border-2 border-transparent border-gray-200 rounded-lg focus:ring focus:ring-j6primary focus:outline-none',
        'placeholder': 'First name'
    }))
    middle_initial = forms.CharField(max_length=1, required=True, widget=forms.TextInput(attrs={
        'class': 'block w-full px-2 py-1 mb-4 border border-2 border-transparent border-gray-200 rounded-lg focus:ring focus:ring-j6primary focus:outline-none',
        'placeholder': 'Middle Initial'
    }))
    last_name = forms.CharField(required=True, widget=forms.TextInput(attrs={
        'class': 'block w-full px-2 py-1 mb-4 border border-2 border-transparent border-gray-200 rounded-lg focus:ring focus:ring-j6primary focus:outline-none',
        'placeholder': 'Last name'
    }))
    address = forms.CharField(required=True, widget=forms.Textarea(attrs={
        'class': 'block w-full px-2 py-1 mb-4 border border-2 border-transparent border-gray-200 rounded-lg focus:ring focus:ring-j6primary focus:outline-none',
        'placeholder': 'Address',
        'rows': 4
    }))
    cellphone_number = forms.CharField(max_length=14, required=True, widget=forms.NumberInput(attrs={
        'class': 'block w-full px-2 py-1 mb-4 border border-2 border-transparent border-gray-200 rounded-lg focus:ring focus:ring-j6primary focus:outline-none',
        'placeholder': 'Cellphone number'
    }))
    email_address = forms.CharField(required=True, widget=forms.TextInput(attrs={
        'class': 'block w-full px-2 py-1 mb-4 border border-2 border-transparent border-gray-200 rounded-lg focus:ring focus:ring-j6primary focus:outline-none',
        'placeholder': 'Email Address'
    }))
    
    class Meta:
        model = Profile
        fields = [
            'first_name',
            'middle_initial',
            'last_name',
            'address',
            'cellphone_number',
            'email_address'
            ]

            
                
           
    
        