"""
Utility functions that support modules within faa_aircraft_registry.
"""

from typing import List, Text, Optional


CERTIFICATION_AND_OPERATION_CODES = {
    '1': {
        'classification': 'Standard',
        'operations': {
            'N': 'Normal',
            'U': 'Utility',
            'A': 'Acrobatic',
            'T': 'Transport',
            'G': 'Glider',
            'B': 'Balloon',
            'C': 'Commuter'
        }
    },
    '2': {
        'classification': 'Limited'
    },
    '3': {
        'classification': 'Restricted',
        'operations': {
            '0': 'Other',
            '1': 'Agriculture and Pest Control',
            '2': 'Aerial Surveying',
            '3': 'Aerial Advertising',
            '4': 'Forest',
            '5': 'Patrolling',
            '6': 'Weather Control',
            '7': 'Carriage of Cargo'
        }
    },
    '4': {
        'classification': 'Experimental',
        'operations': {
            '0': 'To show compliance with FAR',
            '1': 'Research and Development',
            '2': 'Amateur Built',
            '3': 'Exhibition',
            '4': 'Racing',
            '5': 'Crew Training',
            '6': 'Market Survey',
            '7': 'Operating Kit Built Aircraft',
            '8A': 'Reg. Prior to 01/31/08',
            '8B': 'Operating Light-Sport Kit-Built',
            '8C': 'Operating Light-Sport Previously issued cert under 21.190',
            '9A': 'Unmanned Aircraft - Research and Development',
            '9B': 'Unmanned Aircraft - Market Survey',
            '9C': 'Unmanned Aircraft - Crew Training',
            '9D': 'Unmanned Aircraft - Exhibition',
            '9E': 'Unmanned Aircraft – Compliance With CFR'
        }
    },
    '5': {
        'classification': 'Provisional',
        'operations': {
            '1': 'Class I',
            '2': 'Class II'
        }
    },
    '6': {
        'classification': 'Multiple',
        'subclassifications': {
            '1': 'Standard',
            '2': 'Limited',
            '3': 'Restricted'
        },
        'operations': {
            '0': 'Other',
            '1': 'Agriculture and Pest Control',
            '2': 'Aerial Surveying',
            '3': 'Aerial Advertising',
            '4': 'Forest',
            '5': 'Patrolling',
            '6': 'Weather Control',
            '7': 'Carriage of Cargo'
        }
    },
    '7': {
        'classification': 'Primary'
    },
    '8': {
        'classification': 'Special Flight Permit',
        'operations': {
            '1': 'Ferry flight for repairs, alterations, maintenance or storage',
            '2': 'Evacuate from area of impending danger',
            '3': 'Operation in excess of maximum certificated',
            '4': 'Delivery or export',
            '5': 'Production flight testing',
            '6': 'Customer Demo'
        }
    },
    '9': {
        'classification': 'Light Sport',
        'operations': {
            'A': 'Airplane',
            'G': 'Glider',
            'L': 'Lighter than Air',
            'P': 'Power-Parachute',
            'W': 'Weight-Shift-Control'
        }
    }
}


def parse_certification_codes(certification: Text) -> Optional[dict]:
    """
    Parses a single string for airworthiness classification code and operation codes.
    """
    value = certification.strip()
    if not value:
        return None

    cert = CERTIFICATION_AND_OPERATION_CODES.get(value[0], {})
    classification = cert.get('classification')

    if not classification:
        return None

    if classification == 'Multiple':
        index = 3
        subclassifications = [
            cert['subclassifications'].get(code)
            for code in value[1:3]
        ]
    else:
        index = 1
        subclassifications = None

    if len(value) > index and 'operations' in cert:
        operations = [
            cert['operations'].get(key)
            for key in set(cert.get('operations').keys()) if key in value[index:]
        ]
    else:
        operations = None

    return {
        'classification': classification,
        'subclassifications': subclassifications,
        'operations': operations
    }


def transform(dict_: dict, typed_dict: dict, substring_to_type: Optional[List] = None) -> dict:
    """
    Convert values in input dictionary to typed values in object.

    Allows for recursive populating of dictionary types if provided in substring_to_type kwarg. The
    format is as follows:

    substring_to_type
        substring: Text     - The prepended string to filter parameter names by
        field: Text         - The field that will be filled in dict_
        type: TypedDict     - The typeddict that will be created as field
    """

    if substring_to_type:
        for item in substring_to_type:
            # Initialize substring values to convert into dictionary type
            substring = item['substring']
            field = item['field']
            type_ = item['type']

            # Find keys that match the substring and pull them into a new dictionary
            sub_dict = dict((key.strip(substring), dict_.pop(key))
                            for key in set(dict_.keys()) if substring in key)

            # Transform the dictionary into the dictionary type provided
            dict_[field] = transform(sub_dict, type_)

    fields = typed_dict.__annotations__
    return {name: fields[name](value) for name, value in dict_.items() if name in fields.keys()}
