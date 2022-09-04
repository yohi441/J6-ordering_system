from django import forms
from ordering.models import Checkout

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
    
        