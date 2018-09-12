import graphene

from ifrs.components.setting.schema import Query as setting_query
from ifrs.components.transaction.schema import Query as calculation_query
from ifrs.components.transaction.schema import Mutation as transaction_mutation


class Mutation(transaction_mutation, graphene.ObjectType):
    pass


class Query(setting_query, calculation_query, graphene.ObjectType):
    pass
