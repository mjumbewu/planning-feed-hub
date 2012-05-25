from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from . import views

# Find admin modules in apps
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', views.HomeView.as_view(), name='home'),
    url(r'^feeds/$', views.PlanningFeedApiView.as_view(), name='feeds'),
    url(r'^api/', include('db.urls')),
    url(r'^admin/', include(admin.site.urls)),
)

# Serve static files
urlpatterns += staticfiles_urlpatterns()
