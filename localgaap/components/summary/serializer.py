from rest_framework import serializers


class SummarySerializer(serializers.Serializer):
    deferred_tax_rate = serializers.DecimalField(max_digits=7, decimal_places=4)
    difference_cy = serializers.DecimalField(max_digits=16, decimal_places=2)
    difference_py = serializers.DecimalField(max_digits=16, decimal_places=2)
    difference_tu = serializers.DecimalField(max_digits=16, decimal_places=2)
    movement_pl = serializers.DecimalField(max_digits=16, decimal_places=2)
    movement_permanent_difference_pl = serializers.DecimalField(max_digits=16, decimal_places=2)
    movement_neutral = serializers.DecimalField(max_digits=16, decimal_places=2)
    movement_true_up = serializers.DecimalField(max_digits=16, decimal_places=2)
