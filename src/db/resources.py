from djangorestframework import resources

from .models import PlanningFeedModel

class PlanningFeedResource (resources.ModelResource):
    model = PlanningFeedModel
