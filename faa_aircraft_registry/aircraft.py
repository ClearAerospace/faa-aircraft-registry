import csv

from faa_aircraft_registry.types import AircraftDictType
from faa_aircraft_registry.utils import transform

fieldnames = ['code', 'manufacturer', 'model',
              'type', 'engine_type', 'category', 'certification', 'number_of_engines',
              'number_of_seats', 'weight_category', 'cruising_speed_mph']


def read(csvfile):
    """
    This function will read the ACFTREF.txt csv file as a handle and return a list of aircraft models.
    """

    # Initialize output dictionary
    all_aircraft = {}

    # Create the CSV file reader
    reader = csv.DictReader(csvfile, fieldnames=fieldnames,
                            restkey='extra', restval=None)

    # Skip the header row
    next(reader, None)

    # Loop through rows and create dictionary
    for row in reader:

        # Transform row values into aircraft dictionary
        aircraft = transform(row, AircraftDictType)

        # Save aircraft to output dictionary by FAA code as key
        all_aircraft[aircraft['code']] = aircraft

    return all_aircraft
