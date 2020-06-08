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
            {'classification': 'Standard'}
        )

    def test_standard_normal(self):
        self.assertDictEqual(
            parse_certification_codes('1N'),
            {'classification': 'Standard', 'operations': ['Normal', ]}
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
                'operations': ['Unmanned Aircraft - Research and Development']
            }
        )
