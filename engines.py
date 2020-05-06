import csv

ENGINE_TYPES = {
    '0': 'None',
    '1': 'Reciprocating',
    '2': 'Turbo-prop',
    '3': 'Turbo-shaft',
    '4': 'Turbo-jet',
    '5': 'Turbo-fan',
    '6': 'Ramjet',
    '7': '2 Cycle',
    '8': '4 Cycle',
    '9': 'Unknown',
    '10': 'Electric',
    '11': 'Rotary',
}


def read(csvfile):
    """
    This function will read the ENGINE.txt csv file passed as a handle and return a list of engine models.
    """

    engines = {}

    reader = csv.DictReader(csvfile)
    for row in reader:
        code = row.get('CODE', None).strip()
        engine = {
            'code': code,
            'manufacturer': row.get('MFR', '').strip(),
            'model': row.get('MODEL', '').strip(),
            'type': ENGINE_TYPES.get(row.get('TYPE', '9').strip(), ''),
            'horsepower': int(row.get('HORSEPOWER', '0')),
            'thrust': int(row.get('THRUST', '0'))
        }
        engines[code] = engine

    return engines
