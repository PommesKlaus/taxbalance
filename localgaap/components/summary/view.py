from django.db.models import Sum, F
from rest_framework.views import APIView
from rest_framework.response import Response
from core.models import Version
from localgaap.models import Transaction
from localgaap.serializers import SummarySerializer


class SummaryView(APIView):

    def get(self, request, version_id):
        version = Version.objects.select_related(
            "compare_version",
            "matching_version",
            "localgaap_setting").get(pk=version_id)
        compare = version.compare_version
        matching = version.matching_version

        summary = {}

        # TODO: Substract neutral permanent movement from permanent_difference__sum
        version_sums = Transaction.objects.filter(version=version).aggregate(
            Sum('difference'),
            Sum('neutral_movement'),
            permanent_difference__sum=Sum(F('difference')*F('permanent_quota'))
            )

        if compare:
            compare_sums = Transaction.objects.filter(version=compare).aggregate(
                Sum('difference'),
                Sum('neutral_movement'),
                permanent_difference__sum=Sum(F('difference')*F('permanent_quota'))
                )
        else:
            compare_sums = {
                "difference__sum": 0,
                "neutral_movement__sum": 0,
                "permanent_difference__sum": 0
            }

        if matching:
            matching_sums = Transaction.objects.filter(version=matching).aggregate(
                Sum('difference'),
                Sum('neutral_movement'),
                permanent_difference__sum=Sum(F('difference')*F('permanent_quota'))
                )
        else:
            matching_sums = {
                "difference__sum": 0,
                "neutral_movement__sum": 0,
                "permanent_difference__sum": 0
            }

        summary = {
            "deferred_tax_rate": version.localgaap_setting.deferred_tax_rate,

            "difference_cy": version_sums["difference__sum"],
            "difference_py": compare_sums["difference__sum"],
            "difference_tu": matching_sums["difference__sum"],

            "movement_pl": version_sums["difference__sum"] - matching_sums["difference__sum"] - version_sums["neutral_movement__sum"],
            "movement_permanent_difference_pl": version_sums["permanent_difference_pl__sum"] - matching_sums["permanent_difference_pl__sum"],
            "movement_neutral": version_sums["neutral_movement__sum"],
            "movement_true_up": matching_sums["difference__sum"] - matching_sums["neutral_movement__sum"] - (compare_sums["difference__sum"] - compare_sums["neutral_movement__sum"])
        }


        serializer = SummarySerializer(summary)

        return Response(serializer.data)
