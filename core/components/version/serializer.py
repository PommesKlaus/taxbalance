from rest_framework import serializers
from core.models import Version
from core.serializers import CompanySerializer

class VersionListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Version
        fields = (
            "id",
            "shortname",
            "reporting_date",
            "locked",
            "updated_at",
        )


class VersionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Version
        fields = (
            "shortname",
            "reporting_date",
            "company",
            "compare_version",
            "matching_version",
            "description",
            "copy_version"
        )


class VersionDetailSerializer(serializers.ModelSerializer):
    company = CompanySerializer(read_only=True)
    matching_version = VersionListSerializer(read_only=True)
    compare_version = VersionListSerializer(read_only=True)

    class Meta:
        model = Version
        fields = (
            "id",
            "shortname",
            "reporting_date",
            "company",
            "compare_version",
            "matching_version",
            "description",
            "archived",
            "locked",
            "created_at",
            "updated_at",
            "copy_version"
        )
