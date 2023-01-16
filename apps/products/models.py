from django.db import models

from ..base.models import BaseModel
from ..localfood.models import LocalFood

# Create your models here.
class Category(BaseModel):
  description = models.TextField()

  def __str__(self):
    return self.description

  class Meta:
    verbose_name_plural='Categories'
    db_table = 'categorias'


class Product(BaseModel):
  name = models.CharField(max_length=100)
  description = models.TextField(null=True, blank=True)
  price = models.FloatField(null=True, blank=True)
  image = models.ImageField(upload_to='images/products/', null=True, blank=True)
  category = models.ForeignKey(Category, on_delete=models.CASCADE, null=False, blank=False)
  localfood = models.ForeignKey(LocalFood, on_delete=models.CASCADE, null=False, blank=False)

  def __str__(self):
    return f'{self.name}: {self.description}'

  class Meta:
    verbose_name='Product (Platillo)'
    verbose_name_plural='Products (Platillos)'
    db_table = 'platillos'
