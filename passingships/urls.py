from django.conf.urls import url, include
from django.contrib import admin
from . import views

admin.autodiscover()

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^admin/', include(admin.site.urls)),
    url('', include('django.contrib.auth.urls', namespace='auth')),
    url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),
    url(r'^profileupdate.html', views.editprofile, name='editprofile'),
    url(r'^newitinerary.html', views.newitinerary, name='newitinerary'),
    url(r'^(?P<pk>[0-9]+)/edititinerary.html', views.edititinerary, name='edititinerary'),
]
