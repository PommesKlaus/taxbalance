import graphene


class ErrorType(graphene.ObjectType):
    field = graphene.String()
    messages = graphene.List(graphene.String)


def graphene_django_filter(model_fields, filter_types=None):
    if filter_types is None:
        filter_types = ("exact", "icontains", "gt", "gte", "lt", "lte", "istartswith", "iendswith",)
    return { f.name: list(filter_types) for f in model_fields }

def filter_fields_args(filters):
    """
    Returns a dict with Django filter descriptions as keys and graphene_types as values,
    based on the provided information in param filters.

    Expected input:
    filters = {
        "field_name_1": {
            "field_type": graphene.String(),
            "filter": ["icontains", "istartswith", "iendswith"]
        },
        "field_name_2": {
            "field_type": graphene.Int(),
            "filter": ["gt", "gte"]
        }
    }

    Output:
    {
        "field_name_1__icontains": graphene.String(),
        "field_name_1__istartswith": graphene.String(),
        "field_name_1__iendswith": graphene.String(),
        "field_name_2__gt": graphene.Int(),
        "field_name_2__gte": graphene.Int()
    }
    """
    out = {}
    for field_name, v in filters.items():
        for filter_name in v["filter"]:
            out[field_name + "__" + filter_name] = v["field_type"]
    return out
