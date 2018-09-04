import graphene

from graphene_django.types import DjangoObjectType

from core.models import Company

class CompanyType(DjangoObjectType):
    class Meta:
        model = Company

class Query(object):
    companies = graphene.List(CompanyType)
    company = graphene.Field(CompanyType, id=graphene.String())

    def resolve_companies(self, **kwargs):
        return Company.objects.all()

    def resolve_company(self, **kwargs):
        id = kwargs.get('id')

        if id is not None:
            return Company.objects.get(pk=id)

        return None
