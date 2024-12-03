import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
from datetime import datetime
import unittest
import seaborn as sns

input_file = 'no_missing.csv'
output_file = 'normalized.csv'

data = pd.read_csv(input_file)

# Convert date function
def convert_date(this_date):
    try:
        return datetime.strptime(this_date, '%B %d %Y').strftime('%m-%d-%Y')
    except ValueError:
        return this_date

data['incident_date'] = data['incident_date'].apply(convert_date)
data.to_csv(output_file, index=False)

print("Date normalization complete")

# Reload the dataset
normalized_data = pd.read_csv('normalized.csv')

normalized_data['killed'] = pd.to_numeric(normalized_data['killed'], errors='coerce').fillna(0)
normalized_data['injured'] = pd.to_numeric(normalized_data['injured'], errors='coerce').fillna(0)

# Filter rows where 'killed' or 'injured' are greater than 50
normalized_data = normalized_data[(normalized_data['killed'] <= 50) & (normalized_data['injured'] <= 50)]

# Calculate statistics for 'killed' and 'injured'
mean_killed = normalized_data['killed'].mean()
median_killed = normalized_data['killed'].median()
mode_killed = stats.mode(normalized_data['killed'], keepdims=True).mode[0]
std_killed = normalized_data['killed'].std()
max_killed = normalized_data['killed'].max()
min_killed = normalized_data['killed'].min()

mean_injured = normalized_data['injured'].mean()
median_injured = normalized_data['injured'].median()
mode_injured = stats.mode(normalized_data['injured'], keepdims=True).mode[0]
std_injured = normalized_data['injured'].std()
max_injured = normalized_data['injured'].max()
min_injured = normalized_data['injured'].min()


print("\nStatistics for 'killed':")
print(f"Mean: {mean_killed: .5f}")
print(f"Median: {median_killed: .5f}")
print(f"Mode: {mode_killed}")
print(f"Standard Deviation: {std_killed: .5f}")
print(f"Highest: {max_killed}")
print(f"Lowest: {min_killed}")

print("\nStatistics for 'injured':")
print(f"Mean: {mean_injured: .5f}")
print(f"Median: {median_injured: .5f}")
print(f"Mode: {mode_injured}")
print(f"Standard Deviation: {std_injured: .5f}")
print(f"Highest: {max_injured}")
print(f"Lowest: {min_injured}")

print("\n")

normalized_data = pd.read_csv('normalized.csv')

#Outliers...
# Identify rows where 'killed' or 'injured' are greater than 50
outliers = normalized_data[(normalized_data['killed'] > 50) | (normalized_data['injured'] > 50)]

# Print the outliers
if not outliers.empty:
    print("Outliers (killings or injuries above 50):")
    print(outliers)
else:
    print("No outliers found (no killings or injuries above 50).")


plt.figure(figsize=(8, 6))
correlation_matrix = normalized_data[['injured', 'killed']].corr()
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt='.2f')
plt.title('Heatmap between Injured and Killed')
plt.show()


#line graph with #injured and killed overlay. Close the first graph window to reveal this...
normalized_data['incident_date'] = pd.to_datetime(normalized_data['incident_date'])
normalized_data['year'] = normalized_data['incident_date'].dt.year
yearly_data = normalized_data.groupby('year')[['killed', 'injured']].sum().reset_index()

# Plot the line graph
plt.figure(figsize=(10, 6))
plt.plot(yearly_data['year'], yearly_data['killed'], label='Killed', marker='o')
plt.plot(yearly_data['year'], yearly_data['injured'], label='Injured', marker='o', color='red')
plt.title('Yearly Trends of Killed and Injured')
plt.xlabel('Year')
plt.ylabel('Count')
plt.legend()
plt.grid(True)
plt.show()
