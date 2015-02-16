from django import forms


class PaymentForm(forms.Form):
    """ Form that process the payment of the user """
    cardholder_name = forms.CharField(label="Cardholder Name", max_length=100)
    amount = forms.DecimalField(label="Amount")
    number = forms.IntegerField(label="Credit Card Number")
    month = forms.IntegerField(label="Month")
    year = forms.IntegerField(label="Year")
    cvv = forms.IntegerField(widget=forms.PasswordInput())
