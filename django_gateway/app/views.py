from app.forms import PaymentForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import TemplateView, FormView


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


class PaymentView(FormView):

    """ Form to process the payment from the user """
    form_class = PaymentForm
    template_name = 'payment_form.html'
    success_url = '/'
