import csv
from datetime import datetime
from .aircraft import AIRCRAFT_TYPES
from .engines import ENGINE_TYPES

REGISTRANT_TYPE = {
    '1': 'Individual',
    '2': 'Partnership',
    '3': 'Corporation',
    '4': 'Co-Owned',
    '5': 'Government',
    '7': 'LLC',
    '8': 'Non Citizen Corporation',
    '9': 'Non Citizen Co-Owned',
}

REGISTRANT_REGIONS = {
    '1': 'Eastern',
    '2': 'Southwestern',
    '3': 'Central',
    '4': 'Western-Pacific',
    '5': 'Alaskan',
    '7': 'Southern',
    '8': 'European',
    'C': 'Great Lakes',
    'E': 'New England',
    'S': 'Northwest Mountain',
}

STATUS_CODES = {
    'A': 'The Triennial Aircraft Registration form was mailed and has not been returned by the Post Office',
    'D': 'Expired Dealer',
    'E': 'The Certificate of Aircraft Registration was revoked by enforcement action',
    'M': 'Aircraft registered to the manufacturer under their Dealer Certificate',
    'N': 'Non-citizen Corporations which have not returned their flight hour reports',
    'R': 'Registration pending',
    'S': 'Second Triennial Aircraft Registration Form has been mailed and has not been returned by the Post Office',
    'T': 'Valid Registration from a Trainee',
    'V': 'Valid Registration',
    'W': 'Certificate of Registration has been deemed Ineffective or Invalid',
    'X': 'Enforcement Letter',
    'Z': 'Permanent Reserved',
    '1': 'Triennial Aircraft Registration form was returned by the Post Office as undeliverable',
    '2': 'N-Number Assigned – but has notyet been registered',
    '3': 'N-Number assigned as a Non Type   Certificated aircraft - but has not yet been registered',
    '4': 'N-Number assigned as import - but has not yet been registered',
    '5': 'Reserved N-Number',
    '6': 'Administratively canceled',
    '7': 'Sale reported',
    '8': 'A second attempt has been made at mailing a Triennial Aircraft Registration form to the owner with no response',
    '9': 'Certificate of Registration has been revoked',
    '10': 'N-Number assigned, has not been registered and is pending cancellation',
    '11': 'N-Number assigned as a Non Type Certificated (Amateur) but has not been registered that is pending cancellation',
    '12': 'N-Number assigned as import but has not been registered that is pending cancellation',
    '13': 'Registration Expired',
    '14': 'First Notice for Re-Registration/Renewal',
    '15': 'SecondNotice for Re-Registration/Renewal',
    '16': 'Registration Expired – Pending Cancellation',
    '17': 'Sale Reported – Pending Cancellation',
    '18': 'Sale Reported – Canceled',
    '19': 'Registration Pending – Pending Cancellation',
    '20': 'Registration Pending –C anceled',
    '21': 'Revoked – Pending Cancellation',
    '22': 'Revoked – Canceled',
    '23': 'Expired Dealer (Pending Cancellation)',
    '24': 'Third Notice for Re-Registration/Renewal',
    '25': 'First Notice for Registration Renewal',
    '26': 'Second Notice for Registration Renewal',
    '27': 'Registration Expired',
    '28': 'Third Notice for Registration Renewal',
    '29': 'Registration Expired – Pending Cancellation',
}


def get_zip_code(zip_code):

    if len(zip_code) == 9:
        return zip_code[:5]+'-'+zip_code[5:]
    return zip_code


def convert_date(datestr):

    if datestr:
        try:
            return datetime.strptime(datestr, '%Y%m%d').date()
        except:
            pass
    return None


def get_other_names(row):
    others = []
    for key in row.keys():
        if 'OTHER' in key:
            if row[key].strip():
                others.append(row[key].strip())
    return others


def read(csvfile):
    """
    This function will read the MASTER.txt csv file passed as a handle and return a list of registrations.
    """

    registrations = {}

    reader = csv.DictReader(csvfile)
    for row in reader:
        pk = row.get('UNIQUE ID', '')

        registrant = {
            'type': REGISTRANT_TYPE.get(row.get('TYPE REGISTRANT', ''), ''),
            'name': row.get('NAME', '').strip(),
            'street_1': row.get('STREET', '').strip(),
            'street_2': row.get('STREET 2', '').strip(),
            'city': row.get('CITY', '').strip(),
            'state': row.get('STATE', '').strip(),
            'zip_code': get_zip_code(row.get('ZIP CODE', '').strip()),
            'region': REGISTRANT_REGIONS.get(row.get('REGION', ''), ''),
            'county': row.get('COUNTY', '').strip(),
            'country': row.get('COUNTRY', '').strip(),
        }
        certification = {
            'class': None,
            'operations': None,
        }
        record = {
            'registration_number': 'N' + row.get('N-NUMBER', '').strip(),
            'serial_number': row.get('SERIAL NUMBER', '').strip(),
            'aircraft_manufacturer_code': row.get('MFR MDL CODE', '').strip(),
            'engine_manufacturer_code': row.get('ENG MFR MDL', '').strip(),
            'manufacturing_year': row.get('YEAR MFR', None).strip() or None,
            'registrant': registrant,
            'last_action_date': convert_date(row.get('LAST ACTION DATE', None)),
            'certificate_issue_date': convert_date(row.get('CERT ISSUE DATE', None)),
            'certification': certification,
            'aircraft_type': AIRCRAFT_TYPES.get(row.get('TYPE AIRCRAFT', '').strip(), None),
            'engine_type': ENGINE_TYPES.get(row.get('TYPE ENGINE', '9').strip(), None),
            'status': STATUS_CODES.get(row.get('STATUS CODE', '').strip(), ''),
            'transponder_code': row.get('MODE S CODE', None),
            'transponder_code_hex': row.get('MODE S CODE HEX', None),
            'fractional_ownership': True if row.get('FRACT OWNERSHIP', '').strip().upper() == 'Y' else False,
            'airworthiness_date': convert_date(row.get('AIR WORTH DATE', None)),
            'other_names': get_other_names(row),
            'expiration_date': convert_date(row.get('EXPIRATION DATE', None)),
            'id': pk,
            'kit_manufacturer': row.get('KIT MFR', '').strip(),
            'kit_model': row.get('KIT MODEL', '').strip(),
        }

        registrations[pk] = record

    return registrations
