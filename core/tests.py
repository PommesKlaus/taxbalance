from helpers.test_helper import GraphQLTestCase
from core.models import Company, Version


class CompanyTest(GraphQLTestCase):

    def setUp(self):
        Company.objects.create(shortname="X", name="X-Company")
        Company.objects.create(shortname="Y", name="Y-Company")
        super().setUp()

    def test_get_all_companies(self):
        print(""" - Return a list of all companies in the database """)
        qry = ("""
            {
                companies {
                    edges {
                        node {
                            shortname
                            name
                        }
                    }
                }
            }
        """)
        expected = {
            "companies": {
                "edges" :[
                    {
                        "node": {
                            "shortname": "X",
                            "name": "X-Company"
                        }
                    },
                    {
                        "node": {
                            "shortname": "Y",
                            "name": "Y-Company"
                        }
                    }
                ]
            }
        }
        self.assertResponseNoErrors(self.query(qry), expected)
