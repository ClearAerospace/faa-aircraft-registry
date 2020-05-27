import csv

from faa_aircraft_registry.utils import transform
from faa_aircraft_registry.types import RecordDictType, RegistrantDictType

fieldnames = ['registration_number', 'serial_number', 'aircraft_manufacturer_code', 'engine_manufacturer_code',
              'manufacturing_year', 'REGISTRANT_type', 'REGISTRANT_name', 'REGISTRANT_street_1', 'REGISTRANT_street_2',
              'REGISTRANT_city', 'REGISTRANT_state', 'REGISTRANT_zip_code', 'REGISTRANT_region',
              'REGISTRANT_county', 'REGISTRANT_country', 'last_action_date', 'certificate_issue_date',
              'certification', 'aircraft_type', 'engine_type', 'status',
              'transponder_code', 'fractional_ownership', 'airworthiness_date',
              'OTHER NAMES(1)', 'OTHER NAMES(2)', 'OTHER NAMES(3)', 'OTHER NAMES(4)', 'OTHER NAMES(5)',
              'expiration_date', 'unique_regulatory_id', 'kit_manufacturer', 'kit_model', 'transponder_code_hex',
              ]


def read(csvfile):
    """
    This function will read the MASTER.txt csv file passed as a handle and return a list of registrations.
    """

    # Initialize output dictionary
    registrations = {}

    # Create the CSV file reader
    reader = csv.DictReader(csvfile, fieldnames=fieldnames,
                            restkey='extra', restval=None)

    # Skip the header row
    next(reader, None)

    # Loop through rows and create dictionary
    for row in reader:

        # Concatenate other names
        others = {}
        other_names = []
        for key, value in row.items():
            if 'OTHER NAMES' in key:
                others[key] = value
        for key, value in others.items():
            del row[key]
            other_names.append(value.strip())
        row['other_names'] = ', '.join(filter(None, other_names))

        # Transform row values into record dictionary
        record = transform(row,
                           RecordDictType,
                           [{
                               'field': 'registrant',
                               'substring': 'REGISTRANT_',
                               'type': RegistrantDictType
                           }]
                           )

        # Save engine to output dictionary by unique ID as key
        registrations[record['unique_regulatory_id']] = record

    return registrations
