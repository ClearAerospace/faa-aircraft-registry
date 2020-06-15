from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional, Text, TypedDict
from .utils import parse_certification_codes

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


class StrippedText(Text):
    """This type will remove whitespace on left and right of provided text, "input_text"."""

    def __new__(self, input_text: Text) -> Text:
        value = input_text.strip()
        return value if value else ''


class ListOrNone():

    def __new__(self, value: List) -> Optional[List]:
        return value or None


class AircraftType(Text):

    def __new__(self, type_: Text) -> Text:
        return AIRCRAFT_TYPES.get(type_.strip(), '')


class AircraftCategory(Text):

    def __new__(self, category: Text) -> Text:
        return AIRCRAFT_CATEGORIES.get(category.strip(), '')


class AircraftCertification(Text):

    def __new__(self, certification: Text) -> Text:
        return CERTIFICATION_CODES.get(certification, '')


class AircraftWeightCategory(Text):

    def __new__(self, weight_category: Text) -> Text:
        return AIRCRAFT_WEIGHTS.get(weight_category.strip('CLASS '), '')


class NonZeroInt(int):

    def __new__(self, input_int: Text) -> Optional[int]:
        try:
            value = int(input_int)
            return value if value else None
        except ValueError:
            return None


class EngineType(Text):

    def __new__(self, engine_type: Text) -> Text:
        return ENGINE_TYPES.get(engine_type.strip(), '')


class ZipCode(Text):

    def __new__(self, zip_code: Text) -> Text:
        zip_code = zip_code.strip()
        if len(zip_code) == 9:
            return zip_code[:5]+'-'+zip_code[5:]
        return zip_code


class DateType(Text):

    def __new__(self, datestr: Text) -> Optional[Text]:
        try:
            return datetime.strptime(datestr.strip(), '%Y%m%d').strftime('%Y-%m-%d')
        except ValueError:
            return None


class RegistrantTypeType(Text):

    def __new__(self, registrant_type: Text) -> Text:
        return REGISTRANT_TYPE.get(registrant_type.strip(), '')


class RegistrantRegionType(Text):

    def __new__(self, region: Text) -> Text:
        return REGISTRANT_REGIONS.get(region.strip(), '')


class RegistrationNumberType(Text):

    def __new__(self, number: Text) -> Text:
        return f'N{number.strip()}'


class StatusType(Text):

    def __new__(self, status: Text) -> Text:
        return STATUS_CODES.get(status.strip(), None)


class CertificationType(Text):

    def __new__(self, certification: Text) -> Optional[dict]:
        return parse_certification_codes(certification)


class FractionalOwnershipType(Text):

    def __new__(self, ownership: Text) -> bool:
        if ownership.strip().upper() == 'Y':
            return True
        return False


@dataclass
class AircraftDictType(TypedDict):
    """Airplane dictionary with types."""
    code: StrippedText
    manufacturer: StrippedText
    model: StrippedText
    type: AircraftType
    engine_type: EngineType
    category: AircraftCategory
    certification: AircraftCertification
    weight_category: AircraftWeightCategory
    number_of_engines: NonZeroInt
    number_of_seats: NonZeroInt
    cruising_speed_mph: NonZeroInt


@dataclass
class EngineDictType(TypedDict):
    """Engine dictionary with types."""
    code: StrippedText
    manufacturer: StrippedText
    model: StrippedText
    type: EngineType
    power_hp: NonZeroInt
    thrust_lbf: NonZeroInt


@dataclass
class RegistrantDictType(TypedDict):
    """Registrant dictionary with types."""
    type: RegistrantTypeType
    name: StrippedText
    street_1: StrippedText
    street_2: StrippedText
    city: StrippedText
    state: StrippedText
    zip_code: ZipCode
    region: RegistrantRegionType
    county: StrippedText
    country: StrippedText


@dataclass
class RecordDictType(TypedDict):
    """Record dictionary with types."""
    registration_number: RegistrationNumberType
    serial_number: StrippedText
    aircraft_manufacturer_code: StrippedText
    engine_manufacturer_code: StrippedText
    manufacturing_year: NonZeroInt
    registrant: RegistrantDictType
    last_action_date: DateType
    certificate_issue_date: DateType
    certification: CertificationType
    aircraft_type: AircraftType
    engine_type: EngineType
    status: StatusType
    transponder_code: StrippedText
    transponder_code_hex: StrippedText
    fractional_ownership: FractionalOwnershipType
    airworthiness_date: DateType
    other_names: ListOrNone
    expiration_date: DateType
    unique_regulatory_id: StrippedText
    kit_manufacturer: StrippedText
    kit_model: StrippedText
