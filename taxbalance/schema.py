import graphene
from graphene_django.debug import DjangoDebug

from core.schema import Query as core_query
from localgaap.schema import Query as localgaap_query


class Query(core_query, localgaap_query, graphene.ObjectType):
    debug = graphene.Field(DjangoDebug, name='__debug')

schema = graphene.Schema(query=Query)
