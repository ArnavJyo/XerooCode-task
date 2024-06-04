from django.db import models

class Repository(models.Model):
    name = models.CharField(max_length=100)
    full_name = models.CharField(max_length=100)
    private = models.BooleanField()
    html_url = models.URLField()
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

