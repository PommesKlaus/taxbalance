from datetime import date
import graphene
from graphene_django.types import DjangoObjectType
from django.forms import ModelForm
from django.forms.models import model_to_dict
from django.shortcuts import get_object_or_404
from core.models import Version
from taxbalance.types import ErrorType
from taxbalance.utils import to_dict


class VersionType(DjangoObjectType):
    pk = graphene.Int()
    company_id = graphene.String()
    matching_version_id = graphene.Int()
    compare_version_id = graphene.Int()
    copy_version_id = graphene.Int()

    class Meta:
        model = Version
        # filter_fields = ["company", "reporting_date", "shortname"]


class MutateVersion(graphene.Mutation):
    version = graphene.Field(lambda: VersionType)
    errors = graphene.List(ErrorType)

    def mutate(self, info, **kwargs):
        # Graphene expects for foreign key fields an int() value.
        # However, Django model also allows None/null as value. These values
        # are sent as "-1" by the frontend and have to be converted to "None"
        for key in ('compare_version', 'matching_version', 'copy_version'):
            if key in kwargs:
                if kwargs[key] == -1:
                    kwargs[key] = None

        if "id" in kwargs:
            # Version should already exist: UPDATE
            version = get_object_or_404(
                Version.objects.select_related('compare_version', 'matching_version'),
                pk=kwargs["id"])

            # Don't allow changes if version is locked
            if version.locked:
                raise Exception("Provided Version is locked.")

            # Only allow a version to be set to locked if compare_version
            # and matching_version are also locked
            if (kwargs.get("locked", False)     # POST-request says: Lock version
                and not version.locked # Up to now, version isn't locked
                and (
                    not getattr(version.compare_version, "locked", True)     # One of the prior year
                    or not getattr(version.matching_version, "locked", True) # versions is not locked
                )):
                raise Exception("Cannot lock version if compare- or matching-version are unlocked.")
        else:
            # If new version is created: Make sure it is not locked
            kwargs["locked"] = False
            version = Version()

        version.partial_update(**kwargs)

        vers = VersionType(**to_dict(version))
        # vers = VersionType(**model_to_dict(version))
        return MutateVersion(version=vers)


class CreateVersion(MutateVersion):
    class Arguments:
        shortname = graphene.String(required=True)
        reporting_date = graphene.Date(required=True)
        company = graphene.String(required=True)
        compare_version = graphene.Int()
        matching_version = graphene.Int()
        copy_version = graphene.Int()
        description = graphene.String()


class UpdateVersion(MutateVersion):
    class Arguments:
        id = graphene.Int()
        compare_version = graphene.Int()
        matching_version = graphene.Int()
        description = graphene.String()
        archived = graphene.Boolean()
        locked = graphene.Boolean()


class Mutation(graphene.ObjectType):
    createVersion = CreateVersion.Field()
    updateVersion = UpdateVersion.Field()


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
