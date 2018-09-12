# pylint: disable=W0221
from uuid import uuid4
from django.db import models


class Transaction(models.Model):
    oar = models.CharField(max_length=32, verbose_name="Reference", blank=True)
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=20, default="Other")
    version = models.ForeignKey(
        "core.Version",
        related_name="ifrs_transactions",
        on_delete=models.CASCADE)
    difference = models.DecimalField(
        max_digits=16,
        decimal_places=2,
        default=0,
        blank=True,
        verbose_name="Local to IFRS difference")
    permanent_quota = models.DecimalField(max_digits=7, decimal_places=4, default=0, blank=True)
    oci_difference = models.DecimalField(max_digits=16, decimal_places=2, default=0, blank=True)

    class Meta:
        unique_together = (("version", "oar"),)

    def __str__(self):
        return "{0} ({1})".format(self.name, self.difference)

    def save(self, *args, **kwargs):
        # If "oar" is not present: Add unique key for new transaction
        if not self.oar or self.oar == "":
            self.oar = str(uuid4()).replace("-", "")
        super().save(*args, **kwargs)
