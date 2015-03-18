from app.forms import PaymentForm, UserForm
from app.models import MerchantTransaction
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import (
    TemplateView,
    FormView,
    ListView,
    DetailView,
    UpdateView
)
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


class EditUserView(SuccessMessageMixin, UpdateView):
    
    """ Form to edit the user """
    model = User
    form_class = UserForm
    template_name = "profile.html"
    success_url = '/'
    success_message = 'User updated'

    def get_object(self, queryset=None):
        return self.request.user


class DashboardListView(ListView):

    """ List of payments made by all the users """
    model = MerchantTransaction
    paginate_by = 10
    queryset = MerchantTransaction.objects.filter(status="success")
    template_name = 'dashboard.html'

    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()

        if self.request.is_ajax():
            return self.json_to_response()

        context = self.get_context_data()
        return self.render_to_response(context)

    def json_to_response(self):
        data = [{
            'transaction_id': payment.merchant_id,
            'user': payment.user.username,
            'amount': payment.amount,
            'status': payment.status,
            'timestamp': payment.timestamp.strftime('%Y-%m-%d'),
        } for payment in self.object_list]

        return JsonResponse(data, safe=False)


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
    success_url = '/payments'

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
