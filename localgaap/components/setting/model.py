from django.db import models


class Setting(models.Model):
    version = models.OneToOneField(
        "core.Version",
        on_delete=models.CASCADE,
        related_name='localgaap_settings'
        )
    deferred_tax_rate = models.DecimalField(
        max_digits=7,
        decimal_places=6,
        default=0.32
        )

    def __str__(self):
        return "Vers.ID {0}, {1}%".format(self.version_id, self.deferred_tax_rate * 100)
