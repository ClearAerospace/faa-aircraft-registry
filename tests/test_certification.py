import pytest

from faa_aircraft_registry.utils import parse_certification_codes


only_classification_dict = {
    'classification': 'Standard',
    'subclassifications': None,
    'operations': None
}

standard_normal_dict = {
    'classification': 'Standard',
    'subclassifications': None,
    'operations': ['Normal', ]
}

multiple_dict = {
    'classification': 'Multiple',
    'subclassifications': ['Standard', 'Restricted'],
    'operations': ['Agriculture and Pest Control', ]
}

uas_rnd_dict = {
    'classification': 'Experimental',
    'subclassifications': None,
    'operations': ['Unmanned Aircraft - Research and Development']
}


@pytest.mark.parametrize(['certification_code', 'result'], [
    pytest.param('', None, id='empty string'),
    pytest.param('0', None, id='zero string'),
    pytest.param('1', only_classification_dict, id='only classification'),
    pytest.param('1N', standard_normal_dict, id='only classification'),
    pytest.param('6131', multiple_dict, id='only classification'),
    pytest.param('49A', uas_rnd_dict, id='only classification'),
])
def test_certification_codes(certification_code, result):
    """Uses parse_certification_codes function to return the text values of the provided certficiation code."""
    assert parse_certification_codes(certification_code) == result
