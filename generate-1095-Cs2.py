import pandas as pd
from fillpdf import fillpdfs as fp
import os
from dicts import *
import os
from pypdf import PdfReader, PdfWriter
from util import Util

def load_data():
  df = pd.DataFrame(pd.read_csv('csv2.csv'))
  # convert SSN to string and take the last 4 digits
  df['SSN'] = '***-**-' + df['SSN'].astype(str).apply(lambda x: x[-4:])
  # convert Zip_Code to string and add leading 0s if they're less than 5 digits and remove decimal
  df['ZipCode'] = df['ZipCode'].astype(str).apply(lambda x: x.split('.')[0].zfill(5))
  return df

def populate_dict(row):
  data_dict = data_dict_defaults.copy()
  employee_field_keys = field_keys['employee']

  data_dict[employee_field_keys['first_name']] = row['First_Name']
  data_dict[employee_field_keys['middle_name']] = ''
  data_dict[employee_field_keys['last_name']] = row['Last_Name']
  data_dict[employee_field_keys['ssn']] = row['SSN']
  data_dict[employee_field_keys['address']] = row['Address_1']
  data_dict[employee_field_keys['city']] = row['City']
  data_dict[employee_field_keys['state']] = row['State']
  data_dict[employee_field_keys['zip']] = 'US' + ' ' + row['ZipCode']

  # iterate over ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
  for i, month in enumerate(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']):
    month_field_keys: dict[int, str] = field_keys['months'][i + 1]
    data_dict[month_field_keys[1]] = row[f'14_{month}']
    data_dict[month_field_keys[2]] = row[f'15_{month}'] if not pd.isna(row[f'15_{month}']) else ''
    data_dict[month_field_keys[3]] = row[f'16_{month}'] if not pd.isna(row[f'16_{month}']) else ''

  return data_dict

def generate_form(row):
  data_dict = populate_dict(row)
  last_name = row['Last_Name']
  first_name = row['First_Name']

  file_name = f'{YEAR}-{last_name}-{first_name}-1095-C.pdf'

  # make the dir if it doesn't exist
  if not os.path.exists(DIR):
      os.makedirs(DIR)

  # NOTE: Commented out bug from fp.write_fillable_pdf function:
  #   while target_aux['/Parent']:
  #     key = target['/Parent'][ANNOT_FIELD_KEY][1:-1] + '.' + key
  #     target_aux = target_aux['/Parent']
  fp.write_fillable_pdf(f'1095-C-{YEAR}.pdf', f'{DIR}/{file_name}', data_dict, flatten = False)

def generate_forms():
  df = load_data()

  # generate form for each employee
  generated_forms = 0
  total_forms = len(df)
  for _, row in df.iterrows():
    generate_form(row)
    generated_forms += 1
    if generated_forms % 5 == 0:
      print(f'Generated {generated_forms}/{total_forms} forms')


generate_forms()

# merge the forms into one pdf selecting only the first page
# Util.merge_pdfs(DIR, f'{DIR}/1095-Cs-{YEAR}.pdf')

# NOTE - IMPORTANT: open the merged form on a Mac and in the print dialog select the arrow on bottom left and save it as a PDF to make it uneditable and a normal PDF file type