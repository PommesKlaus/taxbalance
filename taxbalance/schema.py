import graphene
from graphene_django.debug import DjangoDebug

from core.schema import Query as core_query
from core.schema import Mutation as core_mutation
from localgaap.schema import Query as localgaap_query
from localgaap.schema import Mutation as localgaap_mutation


class Mutation(core_mutation, localgaap_mutation, graphene.ObjectType):
    pass

class Query(core_query, localgaap_query, graphene.ObjectType):
    debug = graphene.Field(DjangoDebug, name='__debug')

schema = graphene.Schema(query=Query, mutation=Mutation)
