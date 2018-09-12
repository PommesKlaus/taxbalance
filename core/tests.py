from datetime import date
from helpers.tst_helper import GraphQLTestCase
from core.models import Company, Version
from localgaap.models import Transaction


class CompanyTest(GraphQLTestCase):

    @classmethod
    def setUpTestData(cls):
        Company.objects.create(shortname="X", name="X-Company")
        Company.objects.create(shortname="Y", name="Y-Company")
        v_1 = Version.objects.create(company_id="X", shortname="V1", reporting_date=date(2010, 12, 31))
        v_2 = Version.objects.create(company_id="X", shortname="V2", reporting_date=date(2011, 12, 31))
        Version.objects.create(
            company_id="X",
            shortname="V3",
            reporting_date=date(2012, 12, 31),
            compare_version=v_1,
            matching_version=v_2
            )
        Version.objects.create(company_id="Y", shortname="dummy", reporting_date=date(2011, 12, 31))
        super().setUpTestData()

    def test_company_model_string_repr(self):
        print(""" - Company object instances should be represented with shortname """)
        company = Company.objects.get(pk="Y")
        self.assertEqual(str(company), "Y")

    def test_get_all_companies(self):
        print(""" - Return a list of all companies in the database """)
        qry = ("""
            {
                companies {
                    shortname
                    name
                }
            }
        """)
        expected = {
            "companies": [
                {
                    "shortname": "X",
                    "name": "X-Company"
                },
                {
                    "shortname": "Y",
                    "name": "Y-Company"
                }
            ]
        }
        self.assertResponseNoErrors(self.query(qry), expected)

    def test_get_filtered_companies(self):
        print(""" - Return a list of filtered companies """)
        qry = ("""
            {
                companies(shortname_Icontains:"x") {
                    shortname
                    name
                }
            }
        """)
        expected = {
            "companies": [
                {
                    "shortname": "X",
                    "name": "X-Company"
                }
            ]
        }
        self.assertResponseNoErrors(self.query(qry), expected)

    def test_get_single_company(self):
        print(""" - Return a Company with all related versions """)
        qry = ("""
            {
                company(id:"X") {
                    shortname
                    name
                    versions {
                        shortname
                    }
                }
            }
        """)
        expected = {
            "company": {
                "shortname": "X",
                "name": "X-Company",
                "versions": [
                    { "shortname": "V3" },
                    { "shortname": "V2" },
                    { "shortname": "V1" }
                ]
            }
        }
        self.assertResponseNoErrors(self.query(qry), expected)

    def test_get_none_company(self):
        print(""" - Return None if no company-ID is provided """)
        qry = ("""
            {
                company {
                    shortname
                    name
                    versions {
                        shortname
                    }
                }
            }
        """)
        expected = {
            "company": None
        }
        self.assertResponseNoErrors(self.query(qry), expected)


class VersionTest(GraphQLTestCase):

    @classmethod
    def setUpTestData(cls):
        Company.objects.create(shortname="X", name="X-Company")
        Company.objects.create(shortname="Y", name="Y-Company")
        v_1 = Version.objects.create(company_id="X", shortname="V1", reporting_date=date(2010, 12, 31))

        v_2 = Version.objects.create(company_id="X", shortname="V2", reporting_date=date(2011, 12, 31))
        Version.objects.create(
            company_id="X",
            shortname="V3",
            reporting_date=date(2012, 12, 31),
            compare_version=v_1,
            matching_version=v_2
            )
        Version.objects.create(company_id="Y", shortname="dummy", reporting_date=date(2011, 12, 31))
        super().setUpTestData()

    def test_get_all_companies(self):
        print(""" - Return a list of all companies in the database """)
        qry = ("""
            {
                companies {
                    shortname
                    name
                }
            }
        """)
        expected = {
            "companies": [
                {
                    "shortname": "X",
                    "name": "X-Company"
                },
                {
                    "shortname": "Y",
                    "name": "Y-Company"
                }
            ]
        }
        self.assertResponseNoErrors(self.query(qry), expected)

    """ To-Do: Open Test-Cases """
    # def test_get_all_companies (Existing is a dummy)
    # def test_version_model_string_repr
    # def test_get_filtered_versions
    # def test_get_single_version
    # def test_get_none_version
    # Create Version (incl. signal)
    # Mutate Version