from django.db import models

class DBModelBase(models.Model):

    class Meta:
        abstract = True
        
    id = models.AutoField(primary_key=True)
    datetime = models.DateTimeField(auto_now_add=True,)


class Transaction(DBModelBase):

    method = [
        ('GET', 'GET'),
        ('POST', 'POST'),
        ('PUT', 'PUT'),
        ('DELETE', 'DELETE'),
    ]

    method = models.CharField(max_length=10, choices=method)
    path = models.CharField(max_length=100)
    params = models.CharField(max_length=100)
    status_code = models.IntegerField()
    ip = models.CharField(max_length=15, default='', null=False)
    device = models.CharField(max_length=100, default='', null=False)