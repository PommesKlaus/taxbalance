import graphene

from core.components.company.schema import Query as company_query
from core.components.version.schema import Query as version_query


class Query(company_query, version_query, graphene.ObjectType):
    pass
