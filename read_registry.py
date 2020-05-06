import requests
import zipfile
import io
from aircraft import read as read_aircraft
from engines import read as read_engines
from master import read as read_master

url = 'http://registry.faa.gov/database/ReleasableAircraft.zip'


def read(url):
    """
    Documentation
    """

    registrations = []

    r = requests.get(url, stream=True)
    if r.ok:
        with zipfile.ZipFile(io.BytesIO(r.content)) as z:

            # Read ACFTREF.txt csv file
            with z.open('ACFTREF.txt', 'r') as f:
                csvfile = io.TextIOWrapper(f, 'utf-8-sig')
                aircraft_dict = read_aircraft(csvfile)

            # Read DEALER.txt csv file
            # with z.open('DEALER.txt', 'r') as f:
            #     dealer_df = pd.read_csv(f, dtype='object')

            # Read DEREG.txt csv file
            # with z.open('DEREG.txt', 'r') as f:
            #     dereg_df = pd.read_csv(f, dtype='object')

            # Read DOCINDEX.txt csv file
            # with z.open('DOCINDEX.txt', 'r') as f:
            #     docindex_df = pd.read_csv(f, dtype='object')

            # Read ENGINE.txt csv file
            with z.open('ENGINE.txt', 'r') as f:
                csvfile = io.TextIOWrapper(f, 'utf-8-sig')
                engine_dict = read_engines(csvfile)

            # Read MASTER.txt csv file
            with z.open('MASTER.txt', 'r') as f:
                csvfile = io.TextIOWrapper(f, 'utf-8-sig')
                master_dict = read_master(csvfile)

            # Read RESERVED.txt csv file
            # with z.open('RESERVED.txt', 'r') as f:
            #     reserved_df = pd.read_csv(f, dtype='object')

        return {
            'aircraft': aircraft_dict,
            'engines': engine_dict,
            'master': master_dict,
        }
