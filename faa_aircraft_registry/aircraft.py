import csv
from .engines import ENGINE_TYPES

AIRCRAFT_TYPES = {
    '1': 'Glider',
    '2': 'Balloon',
    '3': 'Blimp/Dirigible',
    '4': 'Fixed wing single engine',
    '5': 'Fixed wing multi engine',
    '6': 'Rotorcraft',
    '7': 'Weight-shift-control',
    '8': 'Powered Parachute',
    '9': 'Gyroplane',
    'H': 'Hybrid Lift',
    'O': 'Other'
}

AIRCRAFT_CATEGORIES = {
    '1': 'Land',
    '2': 'Sea',
    '3': 'Amphibian'
}

CERTIFICATION_CODES = {
    '0': 'Type Certificated',
    '1': 'Not Type Certificated',
    '2': 'Light Sport'
}

AIRCRAFT_WEIGHTS = {
    '1': 'Up to 12,499',
    '2': '12,500 - 19,999',
    '3': '20,000 and over.',
    '4': 'UAV up to 55'
}


def read(csvfile):
    """
    This function will read the ACFTREF.txt csv file as a handle and return a list of aircraft models.
    """

    aircraft = {}

    reader = csv.DictReader(csvfile)
    for row in reader:
        code = row.get('CODE', None).strip()
        entry = {
            'code': code,
            'manufacturer': row.get('MFR', '').strip(),
            'model': row.get('MODEL', '').strip(),
            'type': AIRCRAFT_TYPES.get(row.get('TYPE-ACFT', ''), ''),
            'engine_type': ENGINE_TYPES.get(row.get('TYPE-ENG', '9').strip(), ''),
            'category': AIRCRAFT_CATEGORIES.get(row.get('AC-CAT', ''), ''),
            'certification': CERTIFICATION_CODES.get(row.get('BUILD-CERT-IND', ''), ''),
            'number_of_engines': int(row.get('NO-ENG', None)),
            'number_of_seats': int(row.get('NO-SEATS', None)),
            'weight_lbf': AIRCRAFT_WEIGHTS.get(row.get('AC-WEIGHT', '').strip('CLASS '), ''),
            'cruising_speed_mph': int(row.get('SPEED', None))
        }

        aircraft[code] = entry

    return aircraft
