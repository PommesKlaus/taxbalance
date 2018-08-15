import graphene

from graphene_django.types import DjangoObjectType

from localgaap.models import Transaction


class TransactionType(DjangoObjectType):
    tax = graphene.Float()

    class Meta:
        model = Transaction


class Query(object):
    all_transactions = graphene.List(TransactionType)
    transaction = graphene.Field(TransactionType, id=graphene.Int())

    def resolve_version_transactions(self, info, **kwargs):
        return Transaction.objects.select_related('version').all()

    def resolve_transaction(self, info, **kwargs):
        id = kwargs.get('id')

        if id is not None:
            return Transaction.objects.get(pk=id)

        return None
