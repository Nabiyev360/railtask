from django.contrib.auth.models import User
from django.db import models


class Role(models.Model):
    ROLE_CHOICES = (
        ('assigner', 'Buyuruvchi'),
        ('performer', 'Ijrochi'),
        ('dual', 'Buyuruvchi hamda ijrochi'),
    )
    name = models.CharField(max_length=50, choices=ROLE_CHOICES)

    def __str__(self):
        return self.name


class Department(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=50)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True, blank=True)
    position = models.CharField(max_length=150)
    roles = models.ManyToManyField(Role)
    tg_id = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.full_name
