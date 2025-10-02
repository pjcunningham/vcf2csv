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

This Python code is fast. It converted a single VCF file containing over 80K records into CSV format in just a few minutes.

---
## 🤖 Built With Help From ChatGPT

This project was created in collaboration with [ChatGPT Python GPT](https://openai.com/chatgpt), a customized AI assistant for advanced Python development.

*Special thanks to GPT for helping transform a messy vCard export into a clean, production-grade command-line tool.*

---

## Building a Standalone Executable

You can build a standalone executable using the included `build.py` script, which uses Nuitka to compile the Python code:

```
python build.py
```

This will create a self-contained executable in the project root directory. The executable includes all dependencies and can be distributed without requiring Python or any additional packages to be installed.

Requirements for building:
* Python 3.9+
* Nuitka (installed automatically via project dependencies)
* A C compiler (MinGW64 on Windows, which Nuitka can download automatically) 
