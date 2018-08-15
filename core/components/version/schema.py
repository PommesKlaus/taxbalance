import graphene

from graphene_django.types import DjangoObjectType

from core.models import Version


class VersionType(DjangoObjectType):

    class Meta:
        model = Version


class Query(object):
    all_versions = graphene.List(VersionType)
    version = graphene.Field(VersionType, id=graphene.Int())

    def resolve_all_versions(self, info, **kwargs):
        return Version.objects.select_related('company').all()

    def resolve_version(self, info, **kwargs):
        id = kwargs.get('id')

        if id is not None:
            return Version.objects.get(pk=id)

        return None
