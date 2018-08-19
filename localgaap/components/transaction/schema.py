import graphene
from graphene_django.types import DjangoObjectType
from django.forms import ModelForm
from django.forms.models import model_to_dict
from django.shortcuts import get_object_or_404
from localgaap.models import Transaction
from localgaap.components.calculation.schema import CalculationType, GenericCalculationModel
from core.models import Version
from taxbalance.types import ErrorType


class TransactionType(DjangoObjectType):
    tax = graphene.Float()

    class Meta:
        model = Transaction


class TransactionForm(ModelForm):
    class Meta:
        model = Transaction
        fields = ('id', 'oar', 'name', 'category', 'version', 'local', 'difference', 'permanent_quota', 'neutral_movement',)


class CreateTransaction(graphene.Mutation):
    class Arguments:
        id = graphene.Int()
        oar = graphene.String()
        name = graphene.String()
        category = graphene.String()
        version = graphene.Int()
        local = graphene.Float()
        difference = graphene.Float()
        permanent_quota = graphene.Float()
        neutral_movement = graphene.Float()

    calculation = graphene.Field(CalculationType)
    errors = graphene.List(ErrorType)

    def mutate(self, info, **kwargs):
        # Get version and raise error if locked
        version = Version.objects.select_related("compare_version", "matching_version").get(pk=kwargs["version"])
        if version.locked:
            raise Exception("Provided Version is locked.")
        cy_taxrate = version.localgaap_settings.deferred_tax_rate

        if "id" in kwargs:
            # Try to retrieve an existing instance from the DB to update values
            existing_transaction = get_object_or_404(Transaction, pk=kwargs.pop("id"))
            transaction_form = TransactionForm(kwargs, instance=existing_transaction)
        else:
            transaction_form = TransactionForm(kwargs)

        if not transaction_form.is_valid():
            errors = [
                ErrorType(field=key, messages=value)
                for key, value in transaction_form.errors.items()
            ]
            return CreateTransaction(errors=errors)

        # Current year transaction values
        cy_transaction = transaction_form.save()
        calc = GenericCalculationModel(
            oar=cy_transaction.oar,
            name=cy_transaction.name,
            category=cy_transaction.category)

        # Prior year transaction values
        py_version_id = version.compare_version_id
        py_transaction = Transaction.objects.filter(oar=cy_transaction.oar, version_id=py_version_id)
        py_transaction = None if not py_transaction else py_transaction[0]
        py_taxrate = 0 if not py_version_id else version.compare_version.localgaap_settings.deferred_tax_rate

        # Matching year transaction values
        tu_version_id = version.compare_version_id
        tu_transaction = Transaction.objects.filter(oar=cy_transaction.oar, version_id=tu_version_id)
        tu_transaction = None if not tu_transaction else tu_transaction[0]
        tu_taxrate = 0 if not tu_version_id else version.matching_version.localgaap_settings.deferred_tax_rate

        # Loop through current-, prior year- and matching transactions and update GenericCalculationModel
        fields_to_update = ('id', 'local', 'difference', 'tax', 'permanent_quota', 'neutral_movement',)
        for field in fields_to_update:
            setattr(calc, "cy_"+field, getattr(cy_transaction, field))
            if py_transaction:
                setattr(calc, "py_"+field, getattr(py_transaction, field))
            if tu_transaction:
                setattr(calc, "tu_"+field, getattr(tu_transaction, field))

        calc.cy_deferred_tax = calc.cy_difference * (1 - calc.cy_permanent_quota) * cy_taxrate

        calc.py_deferred_tax = calc.py_difference * (1 - calc.py_permanent_quota) * py_taxrate

        calc.cy_movement = (calc.cy_difference - calc.cy_neutral_movement) - (calc.tu_difference - calc.tu_neutral_movement)

        calc.cy_movement_deferred_tax = (
            (calc.cy_difference - calc.cy_neutral_movement)
            * (1 - calc.cy_permanent_quota) * cy_taxrate
            - (calc.tu_difference - calc.tu_neutral_movement)
            * (1 - calc.tu_permanent_quota) * tu_taxrate
            )

        calc.tu_movement = (calc.tu_difference - calc.tu_neutral_movement) - (calc.py_difference - calc.py_neutral_movement)

        calc.tu_movement_deferred_tax = (
            (calc.tu_difference - calc.tu_neutral_movement)
            * (1 - calc.tu_permanent_quota) * tu_taxrate
            - (calc.py_difference - calc.py_neutral_movement)
            * (1 - calc.py_permanent_quota) * py_taxrate
            )

        calculation = CalculationType(**model_to_dict(calc))
        return CreateTransaction(calculation=calculation)


class Mutation(graphene.ObjectType):
    createTransaction = CreateTransaction.Field()


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
