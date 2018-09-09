import graphene

from graphene_django.types import DjangoObjectType

from core.models import Company
from helpers.graphene import filter_fields_args


class CompanyType(DjangoObjectType):
    class Meta:
        model = Company
        filter_fields = {
            "shortname": {
                "field_type": graphene.String(),
                "filter": ["icontains", "istartswith", "iendswith"]
            },
            "name": {
                "field_type": graphene.String(),
                "filter": ["icontains", "istartswith", "iendswith"]
            }
        }


class Query(object):
    companies = graphene.List(CompanyType, **filter_fields_args(CompanyType._meta.filter_fields))
    company = graphene.Field(CompanyType, id=graphene.String())

    def resolve_companies(self, info, **kwargs):
        return Company.objects.filter(**kwargs)

    def resolve_company(self, info, **kwargs):
        id = kwargs.get('id')

        if id is not None:
            return Company.objects.get(pk=id)

        return None
