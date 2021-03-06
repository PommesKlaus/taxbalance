from datetime import date
import graphene
from graphene_django.types import DjangoObjectType
from django.shortcuts import get_object_or_404
from core.models import Version
from helpers.functions import to_dict
from helpers.graphene import filter_fields_args


class VersionType(DjangoObjectType):
    pk = graphene.Int()

    class Meta:
        model = Version
        filter_fields = {
            "company": {
                "field_type": graphene.String(),
                "filter": ["exact"]
            },
            "reporting_date__year": {
                "field_type": graphene.Int(),
                "filter": ["gt", "gte", "lt", "lte"]
            },
            "shortname": {
                "field_type": graphene.String(),
                "filter": ["icontains", "istartswith", "iendswith"]
            }
        }


class MutateVersion(graphene.Mutation):

    Output = VersionType

    def mutate(self, **kwargs):
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
            version = Version(company_id=kwargs.pop("company"))

        version.partial_update(**kwargs)

        return VersionType(**to_dict(version))


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
    versions = graphene.List(VersionType, **filter_fields_args(VersionType._meta.filter_fields))
    version = graphene.Field(VersionType, id=graphene.Int())

    def resolve_versions(self, info, **kwargs):
        return Version.objects.select_related('company').filter(**kwargs)

    def resolve_version(self, info, **kwargs):
        id = kwargs.get('id')
        if id is not None:
            return Version.objects.get(pk=id)
        return None
