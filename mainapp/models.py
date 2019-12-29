from django.db import models

# Create your models here.
class Stock_Info(models.Model):
    objects = models.Manager()
    name = models.CharField(max_length=15,null=True)
    url = models.TextField(null=True)

    def __str__(self):
        return self.name
   