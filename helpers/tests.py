import graphene
from datetime import date
from core.models import Company, Version
from helpers.tst_helper import GraphQLTestCase
from helpers.functions import to_dict
from helpers.graphene import filter_fields_args


class HelperFunctionsTest(GraphQLTestCase):

    @classmethod
    def setUpTestData(cls):
        company = Company.objects.create(shortname="X", name="X-Company")
        Version.objects.create(company=company, shortname="V1", reporting_date=date(2010, 12, 31))
        super().setUpTestData()

    def test_toDict_with_existing_instance(self):
        print(""" - to_dict() works as expected with existing model instance """)
        version = Version.objects.all()[0]
        expected = {
            "pk": version.id,
            "id": version.id,
            "shortname": "V1",
            "reporting_date": version.reporting_date,
            "company": version.company,
            "compare_version": None,
            "matching_version": None,
            "copy_version": None,
            "description": "",
            "archived": False,
            "locked": False,
            "created_at": version.created_at,
            "updated_at": version.updated_at
        }
        self.assertEqual(to_dict(version), expected)


class HelperGrapheneTest(GraphQLTestCase):

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()

    def test_filterFieldsArgs(self):
        print(""" - filter_fields_args() works as expected """)
        filter_fields = {
            "company": {
                "field_type": graphene.String(),
                "filter": ["exact"]
            },
            "reporting_date__year": {
                "field_type": graphene.Int(),
                "filter": ["gt", "gte"]
            },
            "shortname": {
                "field_type": graphene.String(),
                "filter": ["icontains"]
            }
        }
        expected = {
            "company__exact": graphene.String(),
            "shortname__icontains": graphene.String(),
            "reporting_date__year__gt": graphene.Int(),
            "reporting_date__year__gte": graphene.Int()
        }
        self.assertEqual(filter_fields_args(filter_fields), expected)
