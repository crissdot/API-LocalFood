from django.db import models

# Create your models here.
class LocalFood(models.Model):
  name = models.CharField(max_length=50)
  description = models.TextField()
  registered_at = models.DateTimeField(auto_now_add=True)
