import csv

from faa_aircraft_registry.types import EngineDictType
from faa_aircraft_registry.utils import transform

fieldnames = ['code', 'manufacturer',
              'model', 'type', 'power_hp', 'thrust_lbf']


def read(csvfile):
    """
    This function will read the ENGINE.txt csv file passed as a handle and return a list of engine models.
    """

    # Initialize output dictionary
    all_engines = {}

    # Create the CSV file reader
    reader = csv.DictReader(csvfile, fieldnames=fieldnames,
                            restkey='extra', restval=None)

    # Skip the header row
    next(reader, None)

    # Loop through rows and create dictionary
    for row in reader:

        # Transform row values into engine dictionary
        engine = transform(row, EngineDictType)

        # Save engine to output dictionary by FAA code as key
        all_engines[engine['code']] = engine

    return all_engines
