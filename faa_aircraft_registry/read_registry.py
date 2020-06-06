import io

from faa_aircraft_registry.aircraft import read as read_aircraft
from faa_aircraft_registry.engines import read as read_engines
from faa_aircraft_registry.master import read as read_master


def read(zipped_file):
    """
    This function reads a zipped folder and parses aircraft, engine, and registration data from their respective files.
    """

    registrations = {}

    # Read ACFTREF.txt csv file
    with zipped_file.open('ACFTREF.txt', 'r') as f:
        csvfile = io.TextIOWrapper(f, 'utf-8-sig')
        aircraft = read_aircraft(csvfile)

    # Read ENGINE.txt csv file
    with zipped_file.open('ENGINE.txt', 'r') as f:
        csvfile = io.TextIOWrapper(f, 'utf-8-sig')
        engines = read_engines(csvfile)

    # Read MASTER.txt csv file
    with zipped_file.open('MASTER.txt', 'r') as f:
        csvfile = io.TextIOWrapper(f, 'utf-8-sig')
        records = read_master(csvfile)

    for _pk, record in records.items():
        # Add source
        record['source'] = 'FAA'

        # Find engine from engine code in master list
        engine_code = record.pop('engine_manufacturer_code')
        record['engine'] = engines.get(engine_code)

        # Find airframe from airframe code in master list
        aircraft_code = record.pop('aircraft_manufacturer_code')
        record['aircraft'] = aircraft.get(aircraft_code)

    registrations = {
        'aircraft': aircraft,
        'engines': engines,
        'master': records,
    }

    return registrations
