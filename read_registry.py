import io
from aircraft import read as read_aircraft
from engines import read as read_engines
from master import read as read_master

url = 'http://registry.faa.gov/database/ReleasableAircraft.zip'

# r = requests.get(url, stream=True)
# if r.ok:
#     with zipfile.ZipFile(io.BytesIO(r.content)) as z:
#         registrations = read(z)


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

    return registrations
