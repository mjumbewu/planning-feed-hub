from djangorestframework import views, mixins
from .resources import PlanningFeedResource

class PlanningFeedInstanceView (views.InstanceModelView):
    resource = PlanningFeedResource

class PlanningFeedListView (mixins.PaginatorMixin, views.ListOrCreateModelView):
    resource = PlanningFeedResource
