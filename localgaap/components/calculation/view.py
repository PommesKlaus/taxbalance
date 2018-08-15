import pandas as pd
from rest_framework.views import APIView
from rest_framework.response import Response
from core.models import Version
from localgaap.models import Transaction
from localgaap.serializers import CalculationSerializer


def calculation(version_id):
    version = Version.objects.select_related("compare_version", "matching_version").get(pk=version_id)
    compare = version.compare_version
    matching = version.matching_version

    current_values = version.transactions.values()
    if current_values.count() == 0:
        df_current = pd.DataFrame(columns=[f.name for f in Transaction._meta.get_fields()]).set_index("oar")
    else:
        df_current = pd.DataFrame(list(current_values)).set_index("oar")
    cy_taxrate = version.localgaap_settings.deferred_tax_rate / 100

    if compare is None:
        df_compare = pd.DataFrame(columns=[f.name for f in Transaction._meta.get_fields()]).set_index("oar")
        py_taxrate = 0
    else:
        df_compare = pd.DataFrame(list(compare.transactions.values())).set_index("oar")
        py_taxrate = compare.localgaap_settings.deferred_tax_rate / 100

    if matching is None:
        df_matching = pd.DataFrame(columns=[f.name for f in Transaction._meta.get_fields()]).set_index("oar")
        tu_taxrate = 0
    else:
        df_matching = pd.DataFrame(list(matching.transactions.values())).set_index("oar")
        tu_taxrate = matching.localgaap_settings.deferred_tax_rate / 100


    # Create "Lookup Table" for Transaction Meta-Data
    df_meta = pd.concat([
        df_current[["name", "category"]],
        df_matching[["name", "category"]],
        df_compare[["name", "category"]]
    ], axis=0)
    df_meta = df_meta[~df_meta.index.duplicated(keep="first")]

    # Create Dataframe for response
    df_res = pd.concat([
        df_meta[["name", "category"]],
        df_current[["id", "local", "difference", "neutral_movement", "permanent_quota"]].add_prefix("cy_"),
        df_matching[["id", "local", "difference", "neutral_movement", "permanent_quota"]].add_prefix("tu_"),
        df_compare[["id", "local", "difference", "neutral_movement", "permanent_quota"]].add_prefix("py_")
    ], axis=1).fillna(0)

    # Add calculated columns to Dataframe
    df_res["cy_tax"] = df_res["cy_local"] + df_res["cy_difference"]
    df_res["tu_tax"] = df_res["tu_local"] + df_res["tu_difference"]
    df_res["py_tax"] = df_res["py_local"] + df_res["py_difference"]

    df_res["cy_deferred_tax"] = df_res["cy_difference"] * (1 - df_res["cy_permanent_quota"]) * cy_taxrate
    df_res["py_deferred_tax"] = df_res["py_difference"] * (1 - df_res["py_permanent_quota"]) * py_taxrate

    df_res["cy_movement"] = (
        (df_res["cy_difference"] - df_res["cy_neutral_movement"])
        - (df_res["tu_difference"] - df_res["tu_neutral_movement"])
        )

    df_res["cy_movement_deferred_tax"] = (
        (df_res["cy_difference"] - df_res["cy_neutral_movement"])
        * (1 - df_res["cy_permanent_quota"]) * cy_taxrate
        - (df_res["tu_difference"] - df_res["tu_neutral_movement"])
        * (1 - df_res["tu_permanent_quota"]) * tu_taxrate
        )

    df_res["tu_movement"] = (
        (df_res["tu_difference"] - df_res["tu_neutral_movement"])
        - (df_res["py_difference"] - df_res["py_neutral_movement"])
        )

    df_res["tu_movement_deferred_tax"] = (
        (df_res["tu_difference"] - df_res["tu_neutral_movement"])
        * (1 - df_res["tu_permanent_quota"]) * tu_taxrate
        - (df_res["py_difference"] - df_res["py_neutral_movement"])
        * (1 - df_res["py_permanent_quota"]) * py_taxrate
        )

    # Pass Dictionary through serializer
    df_res.reset_index(inplace=True)
    df_res.rename(columns={"index": "oar"}, inplace=True)
    return df_res.to_dict(orient="records")


class CalculationView(APIView):

    def get(self, request, version_id):
        version = Version.objects.select_related("compare_version", "matching_version").get(pk=version_id)
        compare = version.compare_version
        matching = version.matching_version

        current_values = version.transactions.values()
        if current_values.count() == 0:
            df_current = pd.DataFrame(columns=[f.name for f in Transaction._meta.get_fields()]).set_index("oar")
        else:
            df_current = pd.DataFrame(list(current_values)).set_index("oar")
        cy_taxrate = version.localgaap_settings.deferred_tax_rate / 100

        if compare is None:
            df_compare = pd.DataFrame(columns=[f.name for f in Transaction._meta.get_fields()]).set_index("oar")
            py_taxrate = 0
        else:
            df_compare = pd.DataFrame(list(compare.transactions.values())).set_index("oar")
            py_taxrate = compare.localgaap_settings.deferred_tax_rate / 100

        if matching is None:
            df_matching = pd.DataFrame(columns=[f.name for f in Transaction._meta.get_fields()]).set_index("oar")
            tu_taxrate = 0
        else:
            df_matching = pd.DataFrame(list(matching.transactions.values())).set_index("oar")
            tu_taxrate = matching.localgaap_settings.deferred_tax_rate / 100


        # Create "Lookup Table" for Transaction Meta-Data
        df_meta = pd.concat([
            df_current[["name", "category"]],
            df_matching[["name", "category"]],
            df_compare[["name", "category"]]
        ], axis=0)
        df_meta = df_meta[~df_meta.index.duplicated(keep="first")]

        # Create Dataframe for response
        df_res = pd.concat([
            df_meta[["name", "category"]],
            df_current[["id", "local", "difference", "neutral_movement", "permanent_quota"]].add_prefix("cy_"),
            df_matching[["id", "local", "difference", "neutral_movement", "permanent_quota"]].add_prefix("tu_"),
            df_compare[["id", "local", "difference", "neutral_movement", "permanent_quota"]].add_prefix("py_")
        ], axis=1).fillna(0)

        # Add calculated columns to Dataframe
        df_res["cy_tax"] = df_res["cy_local"] + df_res["cy_difference"]
        df_res["tu_tax"] = df_res["tu_local"] + df_res["tu_difference"]
        df_res["py_tax"] = df_res["py_local"] + df_res["py_difference"]

        df_res["cy_deferred_tax"] = df_res["cy_difference"] * (1 - df_res["cy_permanent_quota"]) * cy_taxrate
        df_res["py_deferred_tax"] = df_res["py_difference"] * (1 - df_res["py_permanent_quota"]) * py_taxrate

        df_res["cy_movement"] = (
            (df_res["cy_difference"] - df_res["cy_neutral_movement"])
            - (df_res["tu_difference"] - df_res["tu_neutral_movement"])
            )

        df_res["cy_movement_deferred_tax"] = (
            (df_res["cy_difference"] - df_res["cy_neutral_movement"])
            * (1 - df_res["cy_permanent_quota"]) * cy_taxrate
            - (df_res["tu_difference"] - df_res["tu_neutral_movement"])
            * (1 - df_res["tu_permanent_quota"]) * tu_taxrate
            )

        df_res["tu_movement"] = (
            (df_res["tu_difference"] - df_res["tu_neutral_movement"])
            - (df_res["py_difference"] - df_res["py_neutral_movement"])
            )

        df_res["tu_movement_deferred_tax"] = (
            (df_res["tu_difference"] - df_res["tu_neutral_movement"])
            * (1 - df_res["tu_permanent_quota"]) * tu_taxrate
            - (df_res["py_difference"] - df_res["py_neutral_movement"])
            * (1 - df_res["py_permanent_quota"]) * py_taxrate
            )

        # Pass Dictionary through serializer
        df_res.reset_index(inplace=True)
        df_res.rename(columns={"index": "oar"}, inplace=True)
        serializer = CalculationSerializer(df_res.to_dict(orient="records"), many=True)

        return Response(serializer.data)
