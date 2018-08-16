import graphene

from localgaap.components.setting.schema import Query as setting_query
from localgaap.components.transaction.schema import Query as transaction_query
from localgaap.components.transaction.schema import Mutation as transaction_mutation
from localgaap.components.calculation.schema import Query as calculation_query


class Mutation(transaction_mutation, graphene.ObjectType):
    pass


class Query(setting_query, transaction_query, calculation_query, graphene.ObjectType):
    pass
