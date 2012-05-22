from django import forms
from db.models import PlanningFeedModel

class PlanningFeedForm (forms.ModelForm):
    class Meta:
        model = PlanningFeedModel
