import graphene

from graphene_django.types import DjangoObjectType

from localgaap.models import Setting


class SettingType(DjangoObjectType):

    class Meta:
        model = Setting


class Query(object):
    setting = graphene.Field(SettingType, id=graphene.Int())

    def resolve_setting(self, info, **kwargs):
        id = kwargs.get('id')

        if id is not None:
            return Setting.objects.get(pk=id)

        return None
