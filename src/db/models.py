from django.db import models

class PlanningFeedModel (models.Model):
    publisher = models.CharField(max_length=256)
    source_url = models.URLField()
    description = models.TextField(null=True, blank=True)
