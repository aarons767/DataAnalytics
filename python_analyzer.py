import pandas as pd
from datetime import datetime

input_file = 'no_missing.csv'
output_file = 'normalized.csv'

data = pd.read_csv(input_file)

def convert_date(this_date):
    try:
        return datetime.strptime(this_date, '%B %d %Y').strftime('%m-%d-%Y')
    except ValueError:
        return this_date

data['incident_date'] = data['incident_date'].apply(convert_date)

data.to_csv(output_file, index=False)

print("Date normalization complete")

