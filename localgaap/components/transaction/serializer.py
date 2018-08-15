from rest_framework import serializers
from localgaap.models import Transaction


class TransactionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Transaction
        fields = (
            'id',
            'oar',
            'name',
            'category',
            'version',
            'local',
            'tax',
            'difference',
            'permanent_quota',
            'neutral_movement'
            )
