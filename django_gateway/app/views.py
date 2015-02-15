from django.views.generic import TemplateView


class IndexView(TemplateView):
    """ Index page of the application """
    template_name = 'index.html'

    # @method_decorator(ensure_csrf_cookie)
    # def dispatch(self, *args, **kwargs):
    #     return super(IndexView, self).dispatch(*args, **kwargs)