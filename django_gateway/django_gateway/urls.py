from django.conf.urls import patterns, include, url
from django.contrib import admin
from app.views import (IndexView, LoginView, PaymentFormView, PaymentListView,
    PaymentDetailView, DashboardListView)

urlpatterns = patterns('',
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}, name='logout'),
    
    url(r'^$', IndexView.as_view(), name='home'),
    url(r'^dashboard/$', DashboardListView.as_view(), name='dashboard'),
    url(r'^payment/$', PaymentFormView.as_view(), name='payment'),
    url(r'^payments/$', PaymentListView.as_view(), name='payments'),
    url(r'^payment/(?P<merchant_id>\w+)$', PaymentDetailView.as_view(), name='payment_detail'),
    
    # Examples:
    # url(r'^$', 'django_gateway.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
)
