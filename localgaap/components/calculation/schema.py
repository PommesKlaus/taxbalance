from django.db import models

import graphene
from graphene_django.types import DjangoObjectType
from graphene_django.rest_framework.mutation import SerializerMutation

from localgaap.components.calculation.view import calculation

"""
Graphene Django requires a Django Model for the creation of a DjangoObjectType.
Create a "fake/generic" model that never gets saved to the database. This model
is then used to create a List of Django Models based on the calculation results
performed in the calculation function.
"""

class GenericCalculationModel(models.Model):
    oar = models.CharField(max_length=32)
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=20)

    cy_id = models.IntegerField()
    cy_local = models.DecimalField(max_digits=16, decimal_places=2)
    cy_difference = models.DecimalField(max_digits=16, decimal_places=2)
    cy_permanent_quota = models.DecimalField(max_digits=7, decimal_places=4)
    cy_tax = models.DecimalField(max_digits=16, decimal_places=2)
    cy_deferred_tax = models.DecimalField(max_digits=16, decimal_places=2)
    cy_neutral_movement = models.DecimalField(max_digits=16, decimal_places=2)

    tu_id = models.IntegerField()
    tu_local = models.DecimalField(max_digits=16, decimal_places=2)
    tu_difference = models.DecimalField(max_digits=16, decimal_places=2)
    tu_permanent_quota = models.DecimalField(max_digits=7, decimal_places=4)
    tu_tax = models.DecimalField(max_digits=16, decimal_places=2)
    tu_neutral_movement = models.DecimalField(max_digits=16, decimal_places=2)

    py_id = models.IntegerField()
    py_local = models.DecimalField(max_digits=16, decimal_places=2)
    py_difference = models.DecimalField(max_digits=16, decimal_places=2)
    py_permanent_quota = models.DecimalField(max_digits=7, decimal_places=4)
    py_tax = models.DecimalField(max_digits=16, decimal_places=2)
    py_deferred_tax = models.DecimalField(max_digits=16, decimal_places=2)
    py_neutral_movement = models.DecimalField(max_digits=16, decimal_places=2)

    cy_movement = models.DecimalField(max_digits=16, decimal_places=2)
    cy_movement_deferred_tax = models.DecimalField(max_digits=16, decimal_places=2)
    tu_movement = models.DecimalField(max_digits=16, decimal_places=2)
    tu_movement_deferred_tax = models.DecimalField(max_digits=16, decimal_places=2)



class CalculationType(DjangoObjectType):
    class Meta:
        model = GenericCalculationModel


class Query(object):
    calculation = graphene.List(CalculationType, version_id=graphene.Int())

    def resolve_calculation(self, info, **kwargs):
        id = kwargs.get('version_id')

        if id is not None:
            calculation_dict = calculation(id)
            return [GenericCalculationModel(**item) for item in calculation_dict]

        return None
