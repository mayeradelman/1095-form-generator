## Generating 1095-C Form PDFs
- dicts.py holds the mapping of form values to the PDF field keys that correspond to those values.
- dicts.py is also where the general shared information for the form values is populated.
- The generation scripts deal with dynamically generating forms for each employee.
- generate-1095-Cs.py is the original script which generates a separate file for each employee.
- generate-1095-Cs2.py is an alternative script that uses data from a different format and which also 

## E-filing
- efile/efile_1.py is a script that's used to transform the data into a format that's used for e-filing.
  - NOTE: This is an *alternative* to generating all the 1095 form PDFs