import graphene

from graphene_django.types import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField

from core.models import Company

class CompanyType(DjangoObjectType):
    class Meta:
        model = Company
        filter_fields = ["shortname", "name"]
        interfaces = (graphene.relay.Node,)

class Query(object):
    companies = DjangoFilterConnectionField(CompanyType)
    # companies = graphene.List(CompanyType)
    company = graphene.Field(CompanyType, id=graphene.String())

    def resolve_companies(self, info, **kwargs):
        return Company.objects.all()

    def resolve_company(self, info, **kwargs):
        id = kwargs.get('id')

        if id is not None:
            return Company.objects.get(pk=id)

        return None
