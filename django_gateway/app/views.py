from app.forms import PaymentForm
from app.models import MerchantTransaction
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import TemplateView, FormView, ListView, DetailView
from app.gateway import get_gateway, TransactionProblem


class IndexView(TemplateView):

    """ Index page of the application """
    template_name = 'index.html'


class LoginView(SuccessMessageMixin, FormView):

    """ Login of the application """
    form_class = AuthenticationForm
    template_name = 'login.html'
    success_url = '/'
    success_message = 'Welcome'

    def form_valid(self, form):
        login(self.request, form.get_user())

        return super(LoginView, self).form_valid(form)


class PaymentListView(ListView):

    """ List of payments made by the user """
    model = MerchantTransaction
    paginate_by = 10
    template_name = 'payments_list.html'


class PaymentDetailView(DetailView):

    """ List of payments made by the user """
    model = MerchantTransaction
    slug_field = 'merchant_id'
    slug_url_kwarg = 'merchant_id'
    template_name = 'payment_detail.html'
    
    def get_context_data(self, **kwargs):
        context = super(PaymentDetailView, self).get_context_data(**kwargs)

        merchant = get_gateway("braintree_payments")
        transaction = merchant.find_transaction(self.object.merchant_id)
        context['transaction'] = transaction

        return context


class PaymentFormView(FormView):

    """ Form to process the payment from the user """
    form_class = PaymentForm
    template_name = 'payment_form.html'
    success_url = '/'

    def form_valid(self, form):
        merchant = get_gateway("braintree_payments")
        
        # Form details
        cardholder_name = form.cleaned_data['cardholder_name']
        amount = form.cleaned_data['amount']
        number = form.cleaned_data['number']
        month = form.cleaned_data['month']
        year = form.cleaned_data['year']
        cvv = form.cleaned_data['cvv']

        # Create transaction
        try:
            transaction = merchant.create_transaction(
                user=self.request.user, cardholder_name=cardholder_name, 
                amount=amount, number=number, month=month, year=year, cvv=cvv)
            if transaction.status == "success":
                messages.success(self.request, 'Your purchase has been confirmed')
            else:
                messages.error(self.request, 'We had a problem with your transaction')
        except TransactionProblem:
            messages.error(self.request, 'We had a problem with your transaction')

        return super(PaymentFormView, self).form_valid(form)
