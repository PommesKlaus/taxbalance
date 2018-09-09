import graphene
from graphene_django.types import DjangoObjectType
from django.shortcuts import get_object_or_404
from django.forms import ModelForm

from helpers.graphene import ErrorType
from core.models import Version
from localgaap.models import Transaction
from localgaap.components.transaction.calculation import GenericCalculationModel, calculate_version


class CalculationType(DjangoObjectType):
    cy_tax = graphene.Float()
    tu_tax = graphene.Float()
    py_tax = graphene.Float()
    cy_deferred_tax = graphene.Float()
    py_deferred_tax = graphene.Float()
    cy_movement = graphene.Float()
    cy_movement_deferred_tax = graphene.Float()
    tu_movement = graphene.Float()
    tu_movement_deferred_tax = graphene.Float()

    class Meta:
        model = GenericCalculationModel


class Query(object):
    calculation = graphene.List(CalculationType, version_id=graphene.Int())

    def resolve_calculation(self, info, **kwargs):
        version_id = kwargs.get('version_id')

        if version_id is not None:
            cy_version = Version.objects.select_related(
                "compare_version", "matching_version"
                ).get(pk=version_id)
            py_version, tu_version = cy_version.compare_version, cy_version.matching_version
            return calculate_version(
                cy_version=cy_version,
                py_version=py_version,
                tu_version=tu_version
                )

        return None


class TransactionForm(ModelForm):
    class Meta:
        model = Transaction
        fields = ('id', 'oar', 'name', 'category', 'version', 'local', 'difference', 'permanent_quota', 'neutral_movement',)


class MutateTransaction(graphene.Mutation):
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
        version = Version.objects.select_related(
            "compare_version", "matching_version", "localgaap_settings"
            ).get(pk=kwargs["version"])
        if version.locked:
            raise Exception("Provided Version is locked.")
        cy_taxrate = version.localgaap_settings.deferred_tax_rate

        if "id" in kwargs:
            # Try to retrieve an existing instance from the DB to update values
            existing_transaction = get_object_or_404(Transaction, pk=kwargs.pop("id"))
            # Override/Add Transaction "Name" and "Category" in kwargs with values from existing transaction
            kwargs["name"] = existing_transaction.name
            kwargs["category"] = existing_transaction.category
            kwargs["oar"] = existing_transaction.oar
            transaction_form = TransactionForm(kwargs, instance=existing_transaction)
        else:
            transaction_form = TransactionForm(kwargs)

        if not transaction_form.is_valid():
            errors = [
                ErrorType(field=key, messages=value)
                for key, value in transaction_form.errors.items()
            ]
            return MutateTransaction(errors=errors)

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
        fields_to_update = ('id', 'local', 'difference', 'permanent_quota', 'neutral_movement',)
        for field in fields_to_update:
            setattr(calc, "cy_"+field, getattr(cy_transaction, field))
            setattr(calc, "cy_taxrate", cy_taxrate)
            if py_transaction:
                setattr(calc, "py_"+field, getattr(py_transaction, field))
                setattr(calc, "py_taxrate", py_taxrate)
            if tu_transaction:
                setattr(calc, "tu_"+field, getattr(tu_transaction, field))
                setattr(calc, "tu_taxrate", tu_taxrate)

        return MutateTransaction(calculation=calc)


class Mutation(graphene.ObjectType):
    mutateTransaction = MutateTransaction.Field()
