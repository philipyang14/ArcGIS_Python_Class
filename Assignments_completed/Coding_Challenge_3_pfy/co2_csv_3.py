# Philip Yang
# NRS 528
# Coding Challenge 3

import pandas as pd
import io
import requests
import matplotlib.pyplot as plt
# from tabulate import tabulate
import seaborn as sns

# URL of the CSV file
csv_url = "https://raw.githubusercontent.com/datasets/co2-ppm-daily/master/data/co2-ppm-daily.csv"

# Fetch the CSV content from the URL
response = requests.get(csv_url)
csv_content = response.content

# Create a DataFrame from the CSV content
co2df = pd.read_csv(io.StringIO(csv_content.decode('utf-8')))

print(co2df.head(-10))


# Get a summary of the data 

# co2df.info() 
#### Pasted output ####
# <class 'pandas.core.frame.DataFrame'>
# RangeIndex: 18764 entries, 0 to 18763
# Data columns (total 2 columns):
#  #   Column  Non-Null Count  Dtype  
# ---  ------  --------------  -----  
#  0   date    18764 non-null  object 
#  1   value   18764 non-null  float64
# dtypes: float64(1), object(1)
# memory usage: 293.3+ KB

# Check for stats of numerical columns ******* ANSWER #2 *******

# co2df.describe() to satisfy as Answer #2 for min, max, avg (mean) 
#### Pasted output ####
# value
# count	18764.000000
# mean	354.855353
# std	26.207265
# min	312.330000
# 25%	331.730000
# 50%	353.525000
# 75%	375.382500
# max	412.660000

# Convert date to datetime
co2df['date'] = pd.to_datetime(co2df['date'], format='%Y-%m-%d')
# co2df.info()

# Rename value to co2_ppm_daily
co2df = co2df.rename(columns={'value':'co2_ppm'})
# co2df.head()


# Answering #1 

# Create a new column with the year
co2df['year'] = co2df['date'].dt.year 
# co2df.head()

# Group by 'year' and calculate average 
avg_co2_yr = co2df.groupby('year')['co2_ppm'].mean() 

# Yr avg plot
plt.figure(figsize=(5, 4))
plt.plot(avg_co2_yr, color ='red', marker='o')
plt.title('Average CO2 (ppm yr$^{-1}$) from 1958 to 2017')
plt.xlabel('Year')
plt.ylabel('Daily average CO2 (ppm)')
plt.grid(True)
plt.show()


# Make a nice table of CO2 values using Tabulate

# Convert the Series to a DataFrame for tabulation
co2_table_df = avg_co2_yr.reset_index().rename(columns={'co2_ppm': 'Average CO2 (ppm)'})

# Convert DataFrame to LaTeX format
# table_latex = tabulate(co2_table_df, tablefmt='latex_raw', headers='keys', showindex=False)
#
# print(table_latex)


# Answering #3

# Make a new column from the months converted to season
co2df['date'] = pd.to_datetime(co2df['date'])
co2df['season'] = co2df['date'].dt.month.map({1: 'Winter', 2: 'Winter', 3: 'Spring', 4: 'Spring', 5: 'Spring',
                                              6: 'Summer', 7: 'Summer', 8: 'Summer', 9: 'Autumn', 10: 'Autumn', 
                                              11: 'Autumn', 12: 'Winter'})

# Display the DataFrame with the new 'season' column
# print(co2df.head(-10))

# Group by 'season' and calculate average 
avg_co2_season = co2df.groupby('season')['co2_ppm'].mean() 

# Season boxplot
plt.figure(figsize=(5, 4))
sns.boxplot(x='season', y='co2_ppm', data=co2df, palette='viridis')
plt.title('CO2 (ppm) by Season from 1958 to 2017')
plt.xlabel('Season')
plt.ylabel('CO2 (ppm) ')
plt.show()


# Answering # 4

# Assuming 'co2_ppm' is the column containing CO2 ppm values
co2df['anomaly'] = co2df['co2_ppm'] - 354.855353 # mean taken from the df describe earlier

# print(co2df.head(-10))

# Anomaly plot
plt.figure(figsize=(5, 4))
plt.plot(co2df['date'], co2df['anomaly'], marker='o', markersize = 1)
plt.title('CO2 anomaly to the mean from 1958 to 2017')
plt.xlabel('Date')
plt.ylabel('CO2 anomaly')
plt.grid(True)
plt.show()

