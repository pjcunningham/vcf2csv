# coding: utf-8
__author__ = 'Paul Cunningham'
__copyright = 'Copyright 2025, Paul Cunningham'

#!/usr/bin/env python3
import os
import sys
import subprocess
import shutil

def main():
    print("Building vcf2csv executable with Nuitka...")

    # Ensure we're in the project root directory
    if not os.path.exists("vcf_parser.py"):
        print("Error: vcf_parser.py not found. Make sure you're running this script from the project root.")
        sys.exit(1)

    # Create a build directory if it doesn't exist
    if not os.path.exists("build"):
        os.makedirs("build")

    # Define Windows metadata properties
    company_name = "Borsuk Software Engineering Ltd"
    product_name = "VCF to CSV"
    file_version = "1.0.0.0"
    product_version = "1.0.0.0"
    file_description = "Tool to convert VCF to CSV"
    copyright = "J. Rodger Koopman, Agilitatum LLC"


    # Build command for Nuitka
    nuitka_cmd = [
        sys.executable,  # Use the current Python interpreter
        "-m", "nuitka",
        "--output-filename=vcf2csv",  # Override output filename
        "--onefile",  # Create a standalone executable with all dependencies
        "--include-package=pandas",  # Explicitly include the pandas package
        "--output-dir=build",  # Output to the build directory
        "--remove-output",  # Clean previous build files
        "--assume-yes-for-downloads",  # Automatically download dependencies
        "--show-progress",  # Show build progress
        "--show-memory",  # Show memory usage during compilation
        "--windows-company-name=" + company_name,  # Company name for executable metadata
        "--windows-product-name=" + product_name,  # Product name for executable metadata
        "--windows-file-version=" + file_version,  # File version for executable metadata
        "--windows-product-version=" + product_version,  # Product version for executable metadata
        "--windows-file-description=" + file_description,  # File description for executable metadata
        "--copyright=" + copyright,
        "vcf_parser.py"  # The script to compile
    ]

    # Execute the Nuitka build command
    try:
        subprocess.run(nuitka_cmd, check=True)
        print("Build completed successfully!")

        # Copy the executable to the project root for easy access
        if os.path.exists("build"):
            exe_path = "build\\vcf2csv.exe"
            if os.path.exists(exe_path):
                shutil.copy(exe_path, "vcf2csv.exe")
                print(f"Executable copied to {os.path.abspath('vcf2csv.exe')}")
            else:
                print(f"Warning: Expected executable not found at {exe_path}")
        else:
            print("Warning: Build directory structure not as expected")

    except subprocess.CalledProcessError as e:
        print(f"Error during build: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

