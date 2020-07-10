# faa-aircraft-registry
This Python package formats the multiple CSV files provided from the [FAA Aircraft Registry](https://registry.faa.gov/aircraftinquiry/) and reformats them into a single list of Python dictionaries allowing for easier use for programmatic usage.

## Data Information
The downloaded data is read from multiple comma-delimited files contained within one zipped file. The expected structure is:
- `ReleasableAircraft.zip`
  - `ACFTREF.txt`: aircraft reference file by make/model/series sequence
  - `ardata.pdf`: documentation for file content and configuration
  - `DEALER.txt`: aircraft dealer applicant file
  - `DEREG.txt`: deregistered aircraft file
  - `DOCINDEX.txt`: aircraft document index file
  - `ENGINE.txt`: engine reference file
  - `MASTER.txt`: aircraft registration master file

## Installation
```
pip install faa_aircraft_registry
```

## Example Usage
```python
import io
import zipfile
import requests
from faa_aircraft_registry import read

registry_zipped_file = 'ReleasableAircraft.zip'
with zipfile.ZipFile(registry_zipped_file) as z:
    registrations = read(z)
```
