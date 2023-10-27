from django.db import models

# Create your models here.
class DBModelBase(models.Model):
    id = models.AutoField(primary_key=True)
    datetime = models.DateTimeField(auto_now_add=True,)


class RequestRecord(DBModelBase):

    EVENT = [
        ('GET', 'GET'),
        ('POST', 'POST'),
        ('PUT', 'PUT'),
        ('DELETE', 'DELETE'),
    ]

    event = models.CharField(max_length=10, choices=EVENT)
    path = models.CharField(max_length=100)
    params = models.CharField(max_length=100)
    status_code = models.IntegerField()