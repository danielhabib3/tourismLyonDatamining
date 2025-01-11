# import the csv file
import csv
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


# Function to read the csv file
def read_csv_file(file):
    with open(file, 'r') as f:
        reader = csv.reader(f)
        data = list(reader)
    return data

data = read_csv_file('./data/flickr_data2.csv')

# Data frame with the data
raw_data = pd.DataFrame(data[1:], columns=[col.strip() for col in data[0]])

# # Dropping unuseful columns
# print(raw_data.columns) # The 3 last columns are unnamed
# # Drop the three last columns
# raw_data = raw_data.drop(raw_data.columns[-3:], axis=1)
# # print(raw_data.columns)

print(len(raw_data)) # 420240

# lets delete the duplicates in the data based on all columns
raw_data_without_duplicates = raw_data.drop_duplicates(keep='first').copy().reset_index(drop=True) 
print(len(raw_data_without_duplicates)) # 168110

# export the data to a new csv file
raw_data_without_duplicates.to_csv('./data/data-no-duplicates.csv', index=False)


# we want to put constraints on the data values in columns
# 1. The values in the column 'lat' should be between -90 and 90
# 2. The values in the column 'long' should be between -180 and 180
# 3. the values in the column 'date_taken_minute' should be between 0 and 59
# 4. the values in the column 'date_taken_hour' should be between 0 and 23
# 5. the values in the column 'date_taken_day' should be between 1 and 31
# 6. the values in the column 'date_taken_month' should be between 1 and 12
# 7. the values in the column 'date_taken_year' should be between 1900 and present year
# 8. the values in the column 'date_uploaded_minute' should be between 0 and 59
# 9. the values in the column 'date_uploaded_hour' should be between 0 and 23
# 10. the values in the column 'date_uploaded_day' should be between 1 and 31
# 11. the values in the column 'date_uploaded_month' should be between 1 and 12
# 12. the values in the column 'date_uploaded_year' should be between 1900 and present year

# Use the dropna() function to remove rows with missing values from th 12 columns
cleaned_data = raw_data_without_duplicates.dropna()
# export the data to a new csv file
cleaned_data.to_csv('./data/clean-data.csv', index=False)
print(len(cleaned_data)) 



for index, data_row in cleaned_data.iterrows():
    # print(data_row['id'], index)
    if (float(data_row['lat']) < -90 or float(data_row['lat']) > 90 or
        float(data_row['long']) < -180 or float(data_row['long']) > 180 or
        int(data_row['date_taken_minute']) < 0 or int(data_row['date_taken_minute']) > 59 or
        int(data_row['date_taken_hour']) < 0 or int(data_row['date_taken_hour']) > 23 or
        int(data_row['date_taken_day']) < 1 or int(data_row['date_taken_day']) > 31 or
        int(data_row['date_taken_month']) < 1 or int(data_row['date_taken_month']) > 12 or
        int(data_row['date_taken_year']) < 1900 or int(data_row['date_taken_year']) > 2021 or
        int(data_row['date_upload_minute']) < 0 or int(data_row['date_upload_minute']) > 59 or
        int(data_row['date_upload_hour']) < 0 or int(data_row['date_upload_hour']) > 23 or
        int(data_row['date_upload_day']) < 1 or int(data_row['date_upload_day']) > 31 or
        int(data_row['date_upload_month']) < 1 or int(data_row['date_upload_month']) > 12 or
        int(data_row['date_upload_year']) < 1900 or int(data_row['date_upload_year']) > 2021):
        raw_data.drop(index, inplace=True)

print(len(cleaned_data)) 










