from rest_framework import serializers


class CalculationSerializer(serializers.Serializer):
    oar = serializers.CharField(max_length=32)
    name = serializers.CharField(max_length=100)
    category = serializers.CharField(max_length=20)
    cy_id = serializers.IntegerField()
    cy_local = serializers.DecimalField(max_digits=16, decimal_places=2)
    cy_difference = serializers.DecimalField(max_digits=16, decimal_places=2)
    cy_permanent_quota = serializers.DecimalField(max_digits=7, decimal_places=4)
    cy_tax = serializers.DecimalField(max_digits=16, decimal_places=2)
    cy_deferred_tax = serializers.DecimalField(max_digits=16, decimal_places=2)
    cy_neutral_movement = serializers.DecimalField(max_digits=16, decimal_places=2)

    tu_id = serializers.IntegerField()
    tu_local = serializers.DecimalField(max_digits=16, decimal_places=2)
    tu_difference = serializers.DecimalField(max_digits=16, decimal_places=2)
    tu_permanent_quota = serializers.DecimalField(max_digits=7, decimal_places=4)
    tu_tax = serializers.DecimalField(max_digits=16, decimal_places=2)
    tu_neutral_movement = serializers.DecimalField(max_digits=16, decimal_places=2)

    py_id = serializers.IntegerField()
    py_local = serializers.DecimalField(max_digits=16, decimal_places=2)
    py_difference = serializers.DecimalField(max_digits=16, decimal_places=2)
    py_permanent_quota = serializers.DecimalField(max_digits=7, decimal_places=4)
    py_tax = serializers.DecimalField(max_digits=16, decimal_places=2)
    py_deferred_tax = serializers.DecimalField(max_digits=16, decimal_places=2)
    py_neutral_movement = serializers.DecimalField(max_digits=16, decimal_places=2)

    cy_movement = serializers.DecimalField(max_digits=16, decimal_places=2)
    cy_movement_deferred_tax = serializers.DecimalField(max_digits=16, decimal_places=2)
    tu_movement = serializers.DecimalField(max_digits=16, decimal_places=2)
    tu_movement_deferred_tax = serializers.DecimalField(max_digits=16, decimal_places=2)
