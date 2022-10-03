from django.db import models
from simple_history.models import HistoricalRecords

# Create your models here.
class LocalFood(models.Model):
  name = models.CharField(max_length=50)
  description = models.TextField()
  registered_at = models.DateTimeField(auto_now_add=True)
  historical = HistoricalRecords()

  def __str__(self):
    return f'{self.name}: {self.description}'
