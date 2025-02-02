import calendar
import pandas as pd
from fillpdf import fillpdfs as fp
from datetime import datetime, timedelta
from pytz import timezone
import os
import shutil

field_keys = {
  'employee': {
    'first_name': 'FEFF00660031005F0031005B0030005D',
    'middle_name': 'FEFF00660031005F0032005B0030005D',
    'last_name': 'FEFF00660031005F0033005B0030005D',

    'ssn': 'FEFF00660031005F0034005B0030005D',
    'address': 'FEFF00660031005F0035005B0030005D',
    'city': 'FEFF00660031005F0036005B0030005D',
    'state': 'FEFF00660031005F0037005B0030005D',
    'zip': 'FEFF00660031005F0038005B0030005D',

    # 'jan_1_age': '',
  },
  'employer': {
    'name': 'FEFF00660031005F0039005B0030005D',
    'ein': 'FEFF00660031005F00310030005B0030005D',
    'phone': 'FEFF00660031005F00310032005B0030005D',
    'address': 'FEFF00660031005F00310031005B0030005D',
    'city': 'FEFF00660031005F00310033005B0030005D',
    'state': 'FEFF00660031005F00310034005B0030005D',
    'zip': 'FEFF00660031005F00310035005B0030005D',
  },
  'plan': {
    'start_month': 'FEFF00660031005F00310036005B0030005D',
  },
  # keys correspond to months (1 = January, 2 = February, etc.)
  # subkeys correspond to rows (1 = first row, 2 = second row, 3 = third row)
  'months': {
    1: {
      1: 'FEFF00660031005F00310038005B0030005D',
      2: 'FEFF00660031005F00330031005B0030005D',
      3: 'FEFF00660031005F00340034005B0030005D',
    },
    2: {
      1: 'FEFF00660031005F00310039005B0030005D',
      2: 'FEFF00660031005F00330032005B0030005D',
      3: 'FEFF00660031005F00340035005B0030005D',
    },
    3: {
      1: 'FEFF00660031005F00320030005B0030005D',
      2: 'FEFF00660031005F00330033005B0030005D',
      3: 'FEFF00660031005F00340036005B0030005D',
    },
    4: {
      1: 'FEFF00660031005F00320031005B0030005D',
      2: 'FEFF00660031005F00330034005B0030005D',
      3: 'FEFF00660031005F00340037005B0030005D',
    },
    5: {
      1: 'FEFF00660031005F00320032005B0030005D',
      2: 'FEFF00660031005F00330035005B0030005D',
      3: 'FEFF00660031005F00340038005B0030005D',
    },
    6: {
      1: 'FEFF00660031005F00320033005B0030005D',
      2: 'FEFF00660031005F00330036005B0030005D',
      3: 'FEFF00660031005F00340039005B0030005D',
    },
    7: {
      1: 'FEFF00660031005F00320034005B0030005D',
      2: 'FEFF00660031005F00330037005B0030005D',
      3: 'FEFF00660031005F00350030005B0030005D',
    },
    8: {
      1: 'FEFF00660031005F00320035005B0030005D',
      2: 'FEFF00660031005F00330038005B0030005D',
      3: 'FEFF00660031005F00350031005B0030005D',
    },
    9: {
      1: 'FEFF00660031005F00320036005B0030005D',
      2: 'FEFF00660031005F00330039005B0030005D',
      3: 'FEFF00660031005F00350032005B0030005D',
    },
    10: {
      1: 'FEFF00660031005F00320037005B0030005D',
      2: 'FEFF00660031005F00340030005B0030005D',
      3: 'FEFF00660031005F00350033005B0030005D',
    },
    11: {
      1: 'FEFF00660031005F00320038005B0030005D',
      2: 'FEFF00660031005F00340031005B0030005D',
      3: 'FEFF00660031005F00350034005B0030005D',
    },
    12: {
      1: 'FEFF00660031005F00320039005B0030005D',
      2: 'FEFF00660031005F00340032005B0030005D',
      3: 'FEFF00660031005F00350035005B0030005D',
    }
  }
}


# the year for which we are generating forms
year = datetime.now(tz=timezone('US/Eastern')).year - 1
dir = f'{year}/{year}_1095-C_forms'
employee_required_contribution = 55.57
EMPLOYER_NAME = 'Indigo Management Inc'
EMPLOYER_EIN = '81-3791264'
EMPLOYER_PHONE = '(718) 843-1333'
EMPLOYER_ADDRESS = '103-15 101st Street'
EMPLOYER_CITY = 'Ozone Park'
EMPLOYER_STATE = 'NY'
EMPLOYER_ZIP = 'United States 11417'

PLAN_START_MONTH = '01'

employer_field_keys = field_keys['employer']
plan_field_keys = field_keys['plan']
data_dict_defaults = {
  employer_field_keys['name']: EMPLOYER_NAME,
  employer_field_keys['ein']: EMPLOYER_EIN,
  employer_field_keys['phone']: EMPLOYER_PHONE,
  employer_field_keys['address']: EMPLOYER_ADDRESS,
  employer_field_keys['city']: EMPLOYER_CITY,
  employer_field_keys['state']: EMPLOYER_STATE,
  employer_field_keys['zip']: EMPLOYER_ZIP,

  plan_field_keys['start_month']: PLAN_START_MONTH,
}

def load_data():
  df = pd.DataFrame(pd.read_excel(f'{year}/{year}_data.xlsx'))
  # rename all columns that have Box in any capitalization to BOX
  df = df.rename(columns=lambda x: x.replace('Box', 'BOX'))
  renames = {
    'BOX 1': 'First Name',
    'BOX 1.1': 'Last Name',
    'BOX 2': 'SSN',
    'BOX 3': 'Address',
    'BOX 4': 'City',
    'BOX 5': 'State',
    'BOX 6': 'Zip Code',
  }
  df['Middle Initial'] = ''
  df['Country'] = 'United States'
  df = df.rename(columns=renames)
  df = df[['First Name', 'Middle Initial', 'Last Name', 'SSN', 'Address', 'City', 'State', 'Country', 'Zip Code', 'Hire Date', 'Final Pay Date', 'Enrolled For Insurance']]
  return df

def populate_dict(row):
  data_dict = data_dict_defaults.copy()
  employee_field_keys = field_keys['employee']

  data_dict[employee_field_keys['first_name']] = row['First Name']
  data_dict[employee_field_keys['middle_name']] = row['Middle Initial']
  data_dict[employee_field_keys['last_name']] = row['Last Name']
  data_dict[employee_field_keys['ssn']] = row['SSN']
  data_dict[employee_field_keys['address']] = row['Address']
  data_dict[employee_field_keys['city']] = row['City']
  data_dict[employee_field_keys['state']] = row['State']
  data_dict[employee_field_keys['zip']] = row['Country'] + ' ' + row['Zip Code']

  hire_date: datetime = row['Hire Date']
  first_of_month_hire_date = datetime(hire_date.year, hire_date.month, 1)
  end_of_ninety_days = hire_date + timedelta(days=90)
  final_pay_date: datetime = row['Final Pay Date']

  for month in range(1, 13):
    is_before_hire = (hire_date.year == year and month < hire_date.month)
    last_date_of_month = calendar.monthrange(year, month)[1]
    first_of_month = datetime(year, month, 1)
    last_of_month = datetime(year, month, last_date_of_month)
    is_within_90_days = (first_of_month >= first_of_month_hire_date and last_of_month < end_of_ninety_days)
    is_termination_month = (final_pay_date.year == year and month == final_pay_date.month)
    is_after_termination = (final_pay_date.year == year and month > final_pay_date.month)

    if is_before_hire or is_after_termination:
      first_row_code = '1H'
      second_row_code = ''
      third_row_code = '2A'
    elif is_within_90_days:
      first_row_code = '1H'
      second_row_code = ''
      third_row_code = '2D'
    elif is_termination_month:
      first_row_code = '1H'
      second_row_code = ''
      third_row_code = '2B'
    else:
      first_row_code = '1E'
      second_row_code = str(employee_required_contribution)
      third_row_code = '2C' if row['Enrolled For Insurance'] else '2H'

    month_field_keys = field_keys['months'][month]

    data_dict[month_field_keys[1]] = first_row_code
    data_dict[month_field_keys[2]] = second_row_code
    data_dict[month_field_keys[3]] = third_row_code

  return data_dict

def generate_form(row):
  data_dict = populate_dict(row)
  last_name = row['Last Name']
  first_name = row['First Name']

  file_name = f'{year}-{last_name}-{first_name}-1095-C.pdf'

  # make the dir if it doesn't exist
  if not os.path.exists(dir):
      os.makedirs(dir)

  # NOTE: For the fd.write_fillable_pdf function, comment out the following code in the package
  #   while target_aux['/Parent']:
  #     key = target['/Parent'][ANNOT_FIELD_KEY][1:-1] + '.' + key
  #     target_aux = target_aux['/Parent']
  fp.write_fillable_pdf(f'1095-C-{year}.pdf', f'{dir}/{file_name}', data_dict, flatten = False)

def generate_forms():
  df = load_data()
  # drop all employees who were hired after the year for which we are generating forms
  df = df[df['Hire Date'].dt.year <= year]

  # generate form for each employee
  for _, row in df.iterrows():
    generate_form(row)

  # make a zip from the dir
  shutil.make_archive(dir, 'zip', dir)
  # delete the dir
  shutil.rmtree(dir)

# NOTE - IMPORTANT: To get the values of the different form field keys to be used in `field_keys` fill out a sample form and run the following code
# form_fields = fp.get_form_fields(f'1095-C-{year}.pdf')
# print(form_fields)

# generate_forms()