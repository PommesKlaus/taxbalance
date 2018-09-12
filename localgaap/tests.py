from datetime import date
from helpers.tst_helper import GraphQLTestCase
from core.models import Company, Version
from localgaap.models import Transaction, Setting


class SettingTest(GraphQLTestCase):

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

    def test_setting_model_string_repr(self):
        print(""" - Setting object instances should be represented with readable string """)
        version = Version.objects.all()[0]
        setting = Setting.objects.filter(version=version)[0]
        self.assertEqual(
            str(setting), "Vers.ID {0}, {1}%".format(version.id, setting.deferred_tax_rate * 100))
