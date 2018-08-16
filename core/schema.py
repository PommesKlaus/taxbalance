import graphene

from core.components.company.schema import Query as company_query
from core.components.version.schema import Query as version_query
from core.components.version.schema import Mutation as version_mutation


class Mutation(version_mutation, graphene.ObjectType):
    pass


class Query(company_query, version_query, graphene.ObjectType):
    pass
