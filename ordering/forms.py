from django import forms
from ordering.models import Checkout

class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Checkout
        fields = ['address', 'cellphone', 'email', 'full_name', 'payment_method']

    
        