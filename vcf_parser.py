#!/usr/bin/env python3
"""
VCARD 3.0 Parser CLI
Usage:
    python vcf_parser.py input1.vcf [input2.vcf ...] --output-dir ./csv_output
    python vcf_parser.py contacts1.vcf contacts2.vcf --output-dir ./csv_out
"""

import re
import os
import argparse
import pandas as pd
from collections import defaultdict

def parse_vcards(vcard_text):
    vcards = re.findall(r"BEGIN:VCARD(.*?)END:VCARD", vcard_text, re.DOTALL)

    standard_fields = ["N", "FN", "ORG", "TITLE", "BDAY"]
    type_sensitive_fields = ["TEL", "EMAIL", "ADR", "URL", "IMPP"]
    all_fields = standard_fields + ["RelatedNames", "CustomDates"]

    type_field_patterns = {
        field: re.compile(rf'{field}(?:;[^:]+)*:(.+)', re.IGNORECASE)
        for field in type_sensitive_fields
    }
    type_extract_pattern = re.compile(r';type=([^:;]+)', re.IGNORECASE)
    apple_related_pattern = re.compile(r"item(\d+)\.X-ABRELATEDNAMES(?::|;type=[^:]*:)(.+)")
    apple_label_pattern = re.compile(r"item(\d+)\.X-ABLabel(?::|;type=[^:]*:)(.+)")
    apple_date_pattern = re.compile(r"item(\d+)\.X-ABDATE(?::|;type=[^:]*:)(.+)")

    parsed_data = []
    all_type_columns = set()

    for block in vcards:
        entry = defaultdict(list)
        related_map = {}
        label_map = {}
        date_map = {}
        field_type_map = defaultdict(list)

        for line in block.strip().splitlines():
            # Apple-related
            if "X-ABRELATEDNAMES" in line:
                match = apple_related_pattern.match(line)
                if match:
                    idx, value = match.groups()
                    related_map[idx] = value.strip()
                continue
            if "X-ABLabel" in line:
                match = apple_label_pattern.match(line)
                if match:
                    idx, label = match.groups()
                    label_map[idx] = label.strip()
                continue
            if "X-ABDATE" in line:
                match = apple_date_pattern.match(line)
                if match:
                    idx, date = match.groups()
                    date_map[idx] = date.strip()
                continue

            for field in type_sensitive_fields:
                if line.startswith(field):
                    match = type_field_patterns[field].search(line)
                    if match:
                        value = match.group(1).strip()
                        if field == "URL" and value.lower().startswith("ms-outlook://"):
                            continue
                        types = type_extract_pattern.findall(line)
                        if not types:
                            types = ["GENERIC"]
                        for t in types:
                            col = f"{field.upper()}-{t.upper()}"
                            field_type_map[col].append(value)
                            all_type_columns.add(col)
                    break
            else:
                for field in standard_fields:
                    if line.startswith(field):
                        try:
                            _, value = line.split(":", 1)
                            entry[field].append(value.strip())
                        except ValueError:
                            pass

        # Apple: RelatedNames
        relationships = []
        for idx, name in related_map.items():
            label = label_map.get(idx, "Related")
            label_clean = re.sub(r"_\$!<(.*?)>!\$_", r"\1", label)
            relationships.append(f"{label_clean}: {name}")
        if relationships:
            entry["RelatedNames"] = [" | ".join(relationships)]

        # Apple: CustomDates
        dates = []
        for idx, date in date_map.items():
            label = label_map.get(idx, "CustomDate")
            label_clean = re.sub(r"_\$!<(.*?)>!\$_", r"\1", label)
            dates.append(f"{label_clean}: {date}")
        if dates:
            entry["CustomDates"] = [" | ".join(dates)]

        # Clean semicolons
        if "N" in entry:
            entry["N"] = [re.sub(r';{2,}', ';', n) for n in entry["N"]]

        # Clean backslashes in ADR
        for col in list(field_type_map.keys()):
            if col.startswith("ADR-"):
                field_type_map[col] = [re.sub(r'\\{2,}', r'\\', a) for a in field_type_map[col]]

        # Merge everything
        for col, values in field_type_map.items():
            entry[col] = [" | ".join(values)]

        parsed_data.append(entry)

    rows = []
    for entry in parsed_data:
        flat = {}
        for field in all_fields:
            flat[field] = " | ".join(entry.get(field, []))
        for col in all_type_columns:
            flat[col] = " | ".join(entry.get(col, []))
        rows.append(flat)

    return pd.DataFrame(rows)

def main():
    parser = argparse.ArgumentParser(description="VCARD 3.0 to CSV Parser")
    parser.add_argument("input", nargs="+", help="Path(s) to .vcf file(s)")
    parser.add_argument("--output-dir", "-o", required=True, help="Directory to save CSV files")
    args = parser.parse_args()

    os.makedirs(args.output_dir, exist_ok=True)

    for input_path in args.input:
        try:
            with open(input_path, "r", encoding="utf-8", errors="ignore") as f:
                text = f.read()
            df = parse_vcards(text)
            base_name = os.path.splitext(os.path.basename(input_path))[0]
            output_path = os.path.join(args.output_dir, f"{base_name}.csv")
            df.to_csv(output_path, index=False)
            print(f"✅ Parsed: {input_path} → {output_path}")
        except Exception as e:
            print(f"❌ Failed to parse {input_path}: {e}")

if __name__ == "__main__":
    main()
