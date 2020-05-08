import io
from .aircraft import read as read_aircraft
from .engines import read as read_engines
from .master import read as read_master


def read(zipped_file):
    """
    Documentation
    """

    registrations = {}

    # Read ACFTREF.txt csv file
    with zipped_file.open('ACFTREF.txt', 'r') as f:
        csvfile = io.TextIOWrapper(f, 'utf-8-sig')
        registrations['aircraft'] = read_aircraft(csvfile)

    # Read ENGINE.txt csv file
    with zipped_file.open('ENGINE.txt', 'r') as f:
        csvfile = io.TextIOWrapper(f, 'utf-8-sig')
        registrations['engines'] = read_engines(csvfile)

    # Read MASTER.txt csv file
    with zipped_file.open('MASTER.txt', 'r') as f:
        csvfile = io.TextIOWrapper(f, 'utf-8-sig')
        registrations['master'] = read_master(csvfile)

    for pk, registration in registrations['master'].items():
        # Find engine from engine code in master list
        engine_code = registration.get('engine_manufacturer_code', None)
        if engine_code and engine_code in registrations['engines']:
            registration['engine_details'] = registrations['engines'].get(
                engine_code)
        else:
            registration['engine_details'] = {}

        # Find airframe from airframe code in master list
        aircraft_code = registration.get('aircraft_manufacturer_code', None)
        if aircraft_code and aircraft_code in registrations['aircraft']:
            registration['aircraft_details'] = registrations['aircraft'].get(
                aircraft_code)
        else:
            registration['aircraft_details'] = {}

    return registrations
