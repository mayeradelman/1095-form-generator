import pandas as pd
import numpy as np
from datetime import datetime

# NOTE - transforms data into format for efiling as templated in {year}/{year}_1095-C_eFile_Sample.xls

tax_year = 2023
date_format = '%m/%d/%Y'

# load cdpap.csv
file_name = 'cdpap'
df = pd.read_csv(f'{file_name}.csv')

column_mapping = {
  'Last Name': 'RecipientLastName',
  'First Name': 'RecipientFirstName',
  'SSN': 'RecipientTIN',
  'Address 1': 'RecipientAddress',
  'Address 2': 'RecipientAddress2',
  'City': 'RecipientCity',
  'State': 'RecipientState',
  'ZipCode': 'RecipientZip',

  'Offer Coverage Jan': 'JanOfferCoverage',
  'Offer Coverage Feb': 'FebOfferCoverage',
  'Offer Coverage Mar': 'MarOfferCoverage',
  'Offer Coverage Apr': 'AprOfferCoverage',
  'Offer Coverage May': 'MayOfferCoverage',
  'Offer Coverage Jun': 'JunOfferCoverage',
  'Offer Coverage Jul': 'JulOfferCoverage',
  'Offer Coverage Aug': 'AugOfferCoverage',
  'Offer Coverage Sep': 'SepOfferCoverage',
  'Offer Coverage Oct': 'OctOfferCoverage',
  'Offer Coverage Nov': 'NovOfferCoverage',
  'Offer Coverage Dec': 'DecOfferCoverage',

  'Monthly Premium Jan': 'JanMonthlyPremium',
  'Monthly Premium Feb': 'FebMonthlyPremium',
  'Monthly Premium Mar': 'MarMonthlyPremium',
  'Monthly Premium Apr': 'AprMonthlyPremium',
  'Monthly Premium May': 'MayMonthlyPremium',
  'Monthly Premium Jun': 'JunMonthlyPremium',
  'Monthly Premium Jul': 'JulMonthlyPremium',
  'Monthly Premium Aug': 'AugMonthlyPremium',
  'Monthly Premium Sep': 'SepMonthlyPremium',
  'Monthly Premium Oct': 'OctMonthlyPremium',
  'Monthly Premium Nov': 'NovMonthlyPremium',
  'Monthly Premium Dec': 'DecMonthlyPremium',

  'Safe Harbor Jan': 'JanSafeHarbor',
  'Safe Harbor Feb': 'FebSafeHarbor',
  'Safe Harbor Mar': 'MarSafeHarbor',
  'Safe Harbor Apr': 'AprSafeHarbor',
  'Safe Harbor May': 'MaySafeHarbor',
  'Safe Harbor Jun': 'JunSafeHarbor',
  'Safe Harbor Jul': 'JulSafeHarbor',
  'Safe Harbor Aug': 'AugSafeHarbor',
  'Safe Harbor Sep': 'SepSafeHarbor',
  'Safe Harbor Oct': 'OctSafeHarbor',
  'Safe Harbor Nov': 'NovSafeHarbor',
  'Safe Harbor Dec': 'DecSafeHarbor',

  # NOTE - COLUMNS THAT DON'T HAVE A CORRESPONDING COLUMN IN THE SOURCE DATA
  # '': 'JanZipCode',
  # '': 'FebZipCode',
  # '': 'MarZipCode',
  # '': 'AprZipCode',
  # '': 'MayZipCode',
  # '': 'JunZipCode',
  # '': 'JulZipCode',
  # '': 'AugZipCode',
  # '': 'SepZipCode',
  # '': 'OctZipCode',
  # '': 'NovZipCode',
  # '': 'DecZipCode',


  # '': 'RecepientMiddle',
  # '': 'RecipientSuffix',
  # '': 'RecepientAddressType',
  # '': 'RecepientCountryName',
  # '': 'EmployeeAge',
  # '': 'PlanStartMonth',
  # '': 'All12OfferCoverage',
  # '': 'All12MonthlyPremium',
  # '': 'All12SafeHarbor',
  # '': 'AllZipCode',
  # '': 'EmployerSelfCoverage',
}

empty_columns = [
  'JanZipCode',
  'FebZipCode',
  'MarZipCode',
  'AprZipCode',
  'MayZipCode',
  'JunZipCode',
  'JulZipCode',
  'AugZipCode',
  'SepZipCode',
  'OctZipCode',
  'NovZipCode',
  'DecZipCode',

  'RecepientMiddle',
  'RecipientSuffix',
  'RecepientAddressType',
  'RecepientCountryName',
  'EmployeeAge',
  'PlanStartMonth',
  'All12OfferCoverage',
  'All12MonthlyPremium',
  'All12SafeHarbor',
  'AllZipCode',
  'EmployerSelfCoverage',

  'CoveredIndividualFirst01',
  'CoveredIndividualMid01',
  'CoveredIndividualLast01',
  'CoveredIndividualSuffix01',
  'CoveredIndividual1SSN',
  'CoveredIndividual1DOB',
  'CoveredIndividual1All12',
  'CoveredIndividual1January',
  'CoveredIndividual1Feb',
  'CoveredIndividual1Mar',
  'CoveredIndividual1Apr',
  'CoveredIndividual1May',
  'CoveredIndividual1Jun',
  'CoveredIndividual1Jul',
  'CoveredIndividual1Aug',
  'CoveredIndividual1Sep',
  'CoveredIndividual1Oct',
  'CoveredIndividual1Nov',
  'CoveredIndividual1Dec',
]

PLAN_START_MONTH = '01'

new_data = []
for index, row in df.iterrows():
  # skip if DOT is prior to the year
  dot_str = row['DOT']
  dot_str = '' if pd.isna(dot_str) else dot_str
  if dot_str:
    # if month is missing leading zero, add it
    month = dot_str.split('/')[0]
    if len(month) == 1:
      dot_str = '0' + dot_str
    # if day is missing leading zero, add it
    day = dot_str.split('/')[1]
    if len(day) == 1:
      dot_str = dot_str[:3] + '0' + dot_str[3:]
    # if year is missing leading 20, add it
    year = dot_str.split('/')[2]
    if len(year) == 2:
      dot_str = dot_str[:6] + '20' + dot_str[6:]

    dot = datetime.strptime(dot_str, date_format)
    if dot.year < tax_year:
      continue

  new_row = {}

  for old_column, new_column in column_mapping.items():
    value = row[old_column]
    if pd.isna(value):
      value = ''
    value = str(value)

    # if the old column is SSN, make sure it's the right length of 9 digits, filling in leading zeros
    if old_column == 'SSN':
      value = value.zfill(9)
    # if the old column is ZIP, make sure it's the right length of 5 digits, filling in leading zeros
    if old_column == 'ZipCode':
      # remove trailing . and all digits after it
      value = value.split('.')[0]
      value = value.zfill(5)

    # have to get rid of dollar fomatting
    if 'Monthly Premium' in old_column:
      value = value.replace('$', '')

    new_row[new_column] = value

  for column in empty_columns:
    new_row[column] = ''

  new_row['EmployeeAge'] = '' # get the age
  new_row['PlanStartMonth'] = PLAN_START_MONTH
  new_row['EmployerSelfCoverage'] = '' # get the self coverage

  # append the new row
  new_data.append(new_row)

efile_df = pd.DataFrame(new_data)

# save as 
efile_df.to_csv(f'{file_name}_efile.csv', index=False)