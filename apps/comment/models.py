from django.db import models

from ..base.models import BaseModel
from ..user.models import User
from ..localfood.models import LocalFood

# Create your models here.
class Comment(BaseModel):
  text = models.TextField(null=False, blank=False)
  user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False, related_name='user')
  localfood = models.ForeignKey(LocalFood, on_delete=models.CASCADE, null=False, blank=False, related_name='localfood')

  def __str__(self):
    return f'{self.text}'

  class Meta:
    db_table = 'comentarios'
