[![PyPI version](https://badge.fury.io/py/vcf2csv.svg)](https://pypi.org/project/vcf2csv/)
[![Python](https://img.shields.io/badge/python-3.6+-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

<p align="center">
  <img src="https://raw.githubusercontent.com/jrkoop/vcf2csv/main/logo.jpg" alt="Agilitatum logo" width="300"/>
</p>

# vcf2csv

Convert VCARD 3.0 `.vcf` files into clean `.csv` format. Handles Apple/iCloud-specific fields, related names, dates, etc.

## Usage
```bash
vcf2csv my_contacts.vcf -o ./csv_output
```