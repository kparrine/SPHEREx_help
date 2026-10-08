#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct  5 18:32:11 2026

@author: kaitlynparrinello
"""

import os, argparse
from astropy.table import Table

#available inputs for data
input_formats = {
    ".fits": "fits",
    ".fit": "fits",
    ".csv": "ascii.csv",
    ".tsv": "ascii.tab",
    ".tbl": "ascii.ipac",
    ".xml": "votable",
    ".parquet": "parquet"
}

#Formats used to determine output file
output_formats = {
    "csv": "ascii.csv",
    "tsv": "ascii.tab",
    "ipac": "ascii.ipac",
    "votable": "votable",
    "fits": "fits",
    "parquet": "parquet"
}

#These help with getting the correct extensions later for the table
output_extensions = {
    "csv": ".csv",
    "tsv": ".tsv",
    "ipac": ".tbl",
    "votable": ".xml",
    "fits": ".fits",
    "parquet": ".parquet"
}

def main():
    parser = argparse.ArgumentParser(description="Split a catalog into SPHEREx-compatible groups of 20 objects.")

    parser.add_argument("input_file", help = "Data file that has RA, Dec coordinates. Available formats: fits, csv, tsv, ipac, votable, parquet.")
    parser.add_argument("ra_colname", help = "RA column name")
    parser.add_argument("dec_colname", help = "Dec column name")
    parser.add_argument("object_colname", help = "Object column name")
    parser.add_argument("output_format", help = "String of output format for file. Choices: IPAC, CSV, TSV, VOTABLE, Parquet, or FITS.")
    
    args = parser.parse_args()
    
    #Get input format from the file extension
    input_extension = os.path.splitext(args.input_file)[1].lower()

    if input_extension not in input_formats:
        print("Input file format is not supported. Choices: FITS, CSV, TSV, IPAC, VOTABLE, and Parquet.")
        return

    data = Table.read(args.input_file, format=input_formats[input_extension]) #read as astropy table - easier to write to different file formats

    #Check that the requested columns exist
    required_columns = [args.ra_colname, args.dec_colname, args.object_colname]

    for column in required_columns:
        if column not in data.colnames:
            print(f"Column '{column}' was not found in the input catalog.")
            return

    n_groups = (len(data) + 19) // 20 #amount of files generated - ensures always make the extra needed so get all objects

    print(f"Input catalog contains {len(data)} objects.")
    print(f"Creating {n_groups} output file(s).")

    #Astropy output format and file extension
    output_astropy_format = output_formats[args.output_format]
    output_extension = output_extensions[args.output_format]

    #Split the catalog into groups of 20 since spherex only allows 20 objects per file
    for i in range(n_groups):
        idx_start = i * 20
        idx_end = idx_start + 20

        #Select only the columns needed by SPHEREx
        r_new = data[idx_start:idx_end][[args.object_colname,args.ra_colname,
                                         args.dec_colname]]

        output_filename = f"spherex_R{i}{output_extension}"
        r_new.write(output_filename, format=output_astropy_format, overwrite=True)
        
        print(f"Wrote {output_filename} ({len(r_new)} objects)")

if __name__ == "__main__":
    main()


        