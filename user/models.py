from django.db import models


class Cash(models.Model):
    pid = models.AutoField(primary_key=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=100000)
    username = models.OneToOneField("auth.User", on_delete=models.CASCADE)
