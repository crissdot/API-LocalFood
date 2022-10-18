from django.db import models
from simple_history.models import HistoricalRecords

from ..base.models import BaseModel

# Create your models here.
class Category(BaseModel):
  description = models.TextField()

  def __str__(self):
    return self.description


class Product(BaseModel):
  name = models.CharField(max_length=100)
  description = models.TextField(null=True)
  image = models.ImageField(upload_to='products/', null=True)
  category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
  historical = HistoricalRecords()

  def __str__(self):
    return f'{self.name}: {self.description}'
