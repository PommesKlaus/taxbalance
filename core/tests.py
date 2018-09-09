from datetime import date
from helpers.test_helper import GraphQLTestCase
from core.models import Company, Version


class CompanyTest(GraphQLTestCase):

    def setUpTestData(self):
        Company.objects.create(shortname="X", name="X-Company")
        Company.objects.create(shortname="Y", name="Y-Company")
        Version.objects.create(company_id="X", shortname="V1", reporting_date=date(2010, 12, 31))
        Version.objects.create(company_id="X", shortname="V2", reporting_date=date(2011, 12, 31))
        Version.objects.create(company_id="X", shortname="V2", reporting_date=date(2012, 12, 31))
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

    def test_get_filtered_companies(self):
        print(""" - Return a Company with all versions """)
        qry = ("""
            {
                company(id:"X" {
                    shortname
                    name
                    versions
                }
            }
        """)
        expected = {
            "company": [
                {
                    "shortname": "X",
                    "name": "X-Company"
                }
            ]
        }
        self.assertResponseNoErrors(self.query(qry), expected)
