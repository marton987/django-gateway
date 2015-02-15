from django.conf.urls import patterns, include, url
from django.contrib import admin
from app.views import IndexView

urlpatterns = patterns('',
    url(r'^$', IndexView.as_view(), name='home'),
    
    # Examples:
    # url(r'^$', 'django_gateway.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
)
