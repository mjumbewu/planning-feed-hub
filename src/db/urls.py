from django.conf.urls.defaults import patterns, url

from djangorestframework.views import ListOrCreateModelView, InstanceModelView
from .views import PlanningFeedListView, PlanningFeedInstanceView

urlpatterns = patterns('',
    url(r'^feeds/$',
        PlanningFeedListView.as_view(),
        name='feed-resources'),
    url(r'^feeds/(?P<pk>[0-9]+)/$',
        PlanningFeedInstanceView.as_view(),
        name='feed-resource'),
)
