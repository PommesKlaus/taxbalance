from django.db import models


class Version(models.Model):
    shortname = models.CharField(max_length=30)
    reporting_date = models.DateField()
    company = models.ForeignKey('Company', related_name='versions', on_delete=models.CASCADE)
    compare_version = models.ForeignKey(
        'self',
        blank=True,
        null=True,
        related_name="compared_in",
        on_delete=models.PROTECT
        )
    matching_version = models.ForeignKey(
        'self',
        blank=True,
        null=True,
        related_name="matching_in",
        on_delete=models.PROTECT
        )
    copy_version = models.ForeignKey(
        'self',
        blank=True,
        null=True,
        related_name="copied_in",
        on_delete=models.SET_NULL
        )
    description = models.CharField(max_length=150, blank=True, default="")
    archived = models.BooleanField(default=False)
    locked = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{0} > {1}".format(self.reporting_date, self.shortname)
