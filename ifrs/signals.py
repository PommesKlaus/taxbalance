from django.db.models.signals import post_save
from django.dispatch import receiver
from core.models import Version
from ifrs.models import Transaction
from ifrs.models import Setting


@receiver(post_save, sender=Version, dispatch_uid="copy_values_from_version")
def copy_values_from_version(sender, **kwargs):
    """
    Signal Handler to be triggered if new Version Object is created
    AND created instance's copy_version property is not None
    Copying values from
        - Transactions
        - Settings (or create default)
    """
    version = kwargs["instance"]
    if kwargs["created"]:
        if version.copy_version:
            # Copy Transactions
            values = Transaction.objects.filter(version_id=version.copy_version)
            for transaction in values:
                transaction.id = None
                transaction.version_id = version.id
            Transaction.objects.bulk_create(values)

            # Copy Settings
            setting = Setting.objects.filter(version_id=version.copy_version)[0]
            setting.id = None
            setting.version_id = version.id
            setting.save()
        else:
            # Store default Setting
            setting = Setting(version_id = version.id)
            setting.save()
