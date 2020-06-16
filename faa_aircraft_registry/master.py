import csv

from typing import Optional

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


def read(csvfile, aircraft: Optional[dict] = None, engines: Optional[dict] = None) -> dict:
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
        other_names = []
        for key in set(row.keys()):
            if 'OTHER NAMES' in key:
                value = row.pop(key).strip()
                if value:
                    other_names.append(value)
        row['other_names'] = other_names or None

        # Transform row values into record dictionary
        record = transform(row,
                           RecordDictType,
                           [{
                               'field': 'registrant',
                               'substring': 'REGISTRANT_',
                               'type': RegistrantDictType
                           }]
                           )

        # Set source to FAA
        record['source'] = 'FAA'

        # Set aircraft from mfg code only if all aircraft are provided
        if aircraft:
            aircraft_code = record.pop('aircraft_manufacturer_code', None)
            record['aircraft'] = aircraft.get(aircraft_code, None)

        # Set engine from mfg code only if all engines are provided
        if engines:
            engine_code = record.pop('engine_manufacturer_code', None)
            record['engine'] = engines.get(engine_code, None)

        # Save engine to output dictionary by unique ID as key
        registrations[record['unique_regulatory_id']] = record

    return registrations
