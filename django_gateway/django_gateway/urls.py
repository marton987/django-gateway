from django.conf.urls import patterns, include, url
from django.contrib import admin
from app.views import IndexView, LoginView

urlpatterns = patterns('',
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}, name='logout'),
    
    url(r'^$', IndexView.as_view(), name='home'),
    
    # Examples:
    # url(r'^$', 'django_gateway.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
)
