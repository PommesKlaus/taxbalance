from django.db import models


class Company(models.Model):
    shortname = models.CharField(max_length=10, primary_key=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.shortname
