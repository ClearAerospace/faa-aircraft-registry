import unittest

from faa_aircraft_registry.utils import parse_certification_codes


class CertificationCodeTests(unittest.TestCase):

    def test_empty_string(self):
        self.assertIsNone(parse_certification_codes(''))

    def test_zero_string(self):
        self.assertIsNone(parse_certification_codes('0'))

    def test_only_classification(self):
        self.assertDictEqual(
            parse_certification_codes('1'),
            {
                'classification': 'Standard',
                'subclassifications': None,
                'operations': None
            }
        )

    def test_standard_normal(self):
        self.assertDictEqual(
            parse_certification_codes('1N'),
            {
                'classification': 'Standard',
                'subclassifications': None,
                'operations': ['Normal', ]
            }
        )

    def test_multiple(self):
        self.assertDictEqual(
            parse_certification_codes('6131'),
            {
                'classification': 'Multiple',
                'subclassifications': ['Standard', 'Restricted'],
                'operations': ['Agriculture and Pest Control', ]
            }
        )

    def test_experimental_uas_rnd(self):
        self.assertDictEqual(
            parse_certification_codes('49A'),
            {
                'classification': 'Experimental',
                'subclassifications': None,
                'operations': ['Unmanned Aircraft - Research and Development']
            }
        )
