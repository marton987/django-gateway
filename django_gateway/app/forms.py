from django import forms
from django.contrib.auth.models import User


class PaymentForm(forms.Form):

    """ Form that process the payment of the user """
    cardholder_name = forms.CharField(label="Cardholder Name", max_length=100)
    amount = forms.DecimalField(label="Amount")
    number = forms.IntegerField(label="Credit Card Number")
    month = forms.IntegerField(label="Month")
    year = forms.IntegerField(label="Year")
    cvv = forms.IntegerField(widget=forms.PasswordInput())


class UserForm(forms.ModelForm):   
  def __init__(self, *args, **kwargs):
    super(UserForm, self).__init__(*args, **kwargs)
    self.fields['first_name'].required = True
    self.fields['last_name'].required = True
    self.fields['email'].required = True
    self.fields['username'].required = True
  class Meta:
    model = User
    fields = ('username','first_name','last_name','email')
    widgets = {
      'username': forms.TextInput(attrs={'readonly':'readonly'}),
      'email': forms.TextInput(attrs={'type':'email'}),
    }
