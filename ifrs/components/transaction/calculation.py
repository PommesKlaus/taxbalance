from collections import defaultdict
from django.db import models
from django.db.models import Q
from ifrs.models import Setting, Transaction


class GenericCalculationModel(models.Model):
    oar = models.CharField(max_length=32, default="", primary_key=True)
    name = models.CharField(max_length=100, default="")
    category = models.CharField(max_length=20, default="")

    cy_id = models.IntegerField(default=0)
    cy_local = models.DecimalField(max_digits=16, decimal_places=2, default=0)
    cy_difference = models.DecimalField(max_digits=16, decimal_places=2, default=0)
    cy_permanent_quota = models.DecimalField(max_digits=7, decimal_places=4, default=0)
    cy_neutral_movement = models.DecimalField(max_digits=16, decimal_places=2, default=0)
    cy_taxrate = models.DecimalField(max_digits=7, decimal_places=6, default=0)

    tu_id = models.IntegerField(default=0)
    tu_local = models.DecimalField(max_digits=16, decimal_places=2, default=0)
    tu_difference = models.DecimalField(max_digits=16, decimal_places=2, default=0)
    tu_permanent_quota = models.DecimalField(max_digits=7, decimal_places=4, default=0)
    tu_neutral_movement = models.DecimalField(max_digits=16, decimal_places=2, default=0)
    tu_taxrate = models.DecimalField(max_digits=7, decimal_places=6, default=0)

    py_id = models.IntegerField(default=0)
    py_local = models.DecimalField(max_digits=16, decimal_places=2, default=0)
    py_difference = models.DecimalField(max_digits=16, decimal_places=2, default=0)
    py_permanent_quota = models.DecimalField(max_digits=7, decimal_places=4, default=0)
    py_neutral_movement = models.DecimalField(max_digits=16, decimal_places=2, default=0)
    py_taxrate = models.DecimalField(max_digits=7, decimal_places=6, default=0)

    @property
    def cy_tax(self):
        return self.cy_local + self.cy_difference

    @property
    def tu_tax(self):
        return self.tu_local + self.tu_difference

    @property
    def py_tax(self):
        return self.py_local + self.py_difference

    @property
    def cy_deferred_tax(self):
        return self.cy_difference * (1 - self.cy_permanent_quota) * self.cy_taxrate

    @property
    def py_deferred_tax(self):
        return self.py_difference * (1 - self.py_permanent_quota) * self.py_taxrate

    @property
    def cy_movement(self):
        return (
            (self.cy_difference - self.cy_neutral_movement)
            - (self.tu_difference - self.tu_neutral_movement)
        )

    @property
    def cy_movement_deferred_tax(self):
        return (
            (self.cy_difference - self.cy_neutral_movement)
            * (1 - self.cy_permanent_quota) * self.cy_taxrate
            - (self.tu_difference - self.tu_neutral_movement)
            * (1 - self.tu_permanent_quota) * self.tu_taxrate
        )

    @property
    def tu_movement(self):
        return (
            (self.tu_difference - self.tu_neutral_movement)
            - (self.py_difference - self.py_neutral_movement)
        )

    @property
    def tu_movement_deferred_tax(self):
        return (
            (self.tu_difference - self.tu_neutral_movement)
            * (1 - self.tu_permanent_quota) * self.tu_taxrate
            - (self.py_difference - self.py_neutral_movement)
            * (1 - self.py_permanent_quota) * self.py_taxrate
        )

    def __str__(self):
        return "{0} ({1})".format(self.oar, self.name)

    def update(self, **kwargs):
        for k, val in kwargs.items():
            setattr(self, k, val)


def calculate_version(cy_version, tu_version=None, py_version=None):
    """
    Aggregates data accross provided versions and calculates tax and movement
    """
    # Set default filter: Get values for all provided Versions
    for_all_versions = Q(Q(version=cy_version) | Q(version=tu_version) | Q(version=py_version))

    # Get Taxrates
    taxrates = {s.version_id: s.deferred_tax_rate for s in Setting.objects.filter(for_all_versions)}

    # Get all transactions
    transactions_query = Transaction.objects.filter(for_all_versions)

    # Loop through all transactions and generate/update GenericCalculationModels
    calculation_dict = defaultdict(GenericCalculationModel)
    relevant_fields = [
        "oar",
        "name",
        "category",
        "version_id",
        "id",
        "local",
        "difference",
        "permanent_quota",
        "neutral_movement",
    ]
    for t in transactions_query.values(*relevant_fields):
        # single queryset to dict with version_prefix
        prefix = "cy_"
        version_id = t.pop("version_id")
        if version_id == getattr(tu_version, "id", None):
            prefix = "tu_"
        elif version_id == getattr(py_version, "id", None):
            prefix = "py_"

        oar = t.pop("oar")
        update_values = (
            ("oar", oar),
            ("name", t.pop("name")),
            ("category", t.pop("category")),
            (prefix + "taxrate", taxrates.get(version_id, 0))
        )
        update_values += tuple((prefix + k, v) for (k, v) in t.items())
        calculation_dict[oar].update(**dict(update_values))

    return calculation_dict.values()
