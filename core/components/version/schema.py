from datetime import date
import graphene
from graphene_django.types import DjangoObjectType
from django.forms import ModelForm
from django.forms.models import model_to_dict
from django.shortcuts import get_object_or_404
from core.models import Version
from taxbalance.types import ErrorType
from taxbalance.helper_functions import to_dict

from localgaap.models import Transaction


class VersionType(DjangoObjectType):
    pk = graphene.Int()

    class Meta:
        model = Version
        filter_fields = ["company", "reporting_date", "shortname"]


class VersionForm(ModelForm):
    class Meta:
        model = Version
        exclude = ()


class CreateVersion(graphene.Mutation):
    class Arguments:
        id = graphene.Int()
        shortname = graphene.String(required=True)
        reporting_date = graphene.Date(required=True)
        company = graphene.String(required=True)
        compare_version = graphene.Int()
        matching_version = graphene.Int()
        copy_version = graphene.Int()
        description = graphene.String()
        archived = graphene.Boolean()
        locked = graphene.Boolean()
        created_at = graphene.DateTime()
        updated_at = graphene.DateTime()

    version = graphene.Field(lambda: VersionType)
    errors = graphene.List(ErrorType)

    def mutate(self, info, **kwargs):
        if "id" in kwargs:
            # Version should already exist: UPDATE
            existing_version = get_object_or_404(Version, pk=kwargs["id"])
            version_form = VersionForm(kwargs, instance=existing_version)
        else:
            version_form = VersionForm(kwargs)

        if not version_form.is_valid():
            errors = [
                ErrorType(field=key, messages=value)
                for key, value in version_form.errors.items()
            ]
            return CreateVersion(errors=errors)

        vers = version_form.save()

        version = VersionType(**to_dict(vers))
        return CreateVersion(version=version)


class Mutation(graphene.ObjectType):
    createVersion = CreateVersion.Field()


class Query(object):
    all_versions = graphene.List(VersionType)
    all_versions_for_company_and_year_gt = graphene.List(VersionType, companyId=graphene.String(), year=graphene.Int())
    version = graphene.Field(VersionType, id=graphene.Int())

    def resolve_all_versions(self, info, **kwargs):
        return Version.objects.select_related('company').all()

    def resolve_all_versions_for_company_and_year_gt(self, info, **kwargs):
        company_id = kwargs.get('companyId')
        year = kwargs.get('year') or 2000
        if company_id is not None:
            return Version.objects.filter(company_id=company_id, reporting_date__gte=date(year, 1, 1))
        return None

    def resolve_version(self, info, **kwargs):
        id = kwargs.get('id')
        if id is not None:
            return Version.objects.get(pk=id)
        return None
