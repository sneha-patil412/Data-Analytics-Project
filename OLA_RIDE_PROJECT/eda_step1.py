import pandas as pd
import matplotlib.pyplot as plt

# File path
file_path = r"OLA_Cleaned.xlsx"

# Read only July sheet
df = pd.read_excel(file_path, sheet_name="July")

print("\n First 5 Rows:")
print(df.head())

print("\n Total Rows and Columns:")
print(df.shape)

print("\n Column Names:")
print(df.columns)

print("\n Data Types:")
print(df.dtypes)

print("\n Missing Values:")
print(df.isnull().sum())

# Convert Date column to datetime
df['Date'] = pd.to_datetime(df['Date'])

print("\nDate column after conversion:")
print(df['Date'].head())
print(df['Date'].dtype)

#coverting date which has time to hour
df['Hour'] = df['Date'].dt.hour

# Booking Status Count
print("\nBooking Status Count:")
print(df['Booking_Status'].value_counts())

# Booking Status Percentage
print("\nBooking Status Percentage:")
print(df['Booking_Status'].value_counts(normalize=True) * 100)

# Peak Demand Hours
print("\nRides per Hour:")
print(df['Hour'].value_counts().sort_index())

# removing space
df['Booking_Status'] = df['Booking_Status'].str.strip()

# 1️ Filter successful rides
success_df = df[df['Booking_Status'] == "Success"]

# 2️ Print peak hours
print("\nPeak Hours for Successful Rides:")
print(success_df['Hour'].value_counts().sort_index())

# Replace 'null', 'NULL', and blanks with np.nan
df.replace(['null', 'NULL', ''], pd.NA, inplace=True)

# 3 Plot graph : to identify peak hr for successfull rides


success_df['Hour'].value_counts().sort_index().plot(kind='bar')
plt.title("Peak Hours for Successful Rides")
plt.xlabel("Hour")
plt.ylabel("Number of Successful Rides")
plt.show()

# plot graph for successfull rides vs cancelled ones

df['Booking_Status'].value_counts().plot(kind='bar')
plt.title("Booking Status Count")
plt.xlabel("Status")
plt.ylabel("Number of Rides")
plt.show()

# plot grapg to identify vehicle type popularity

df['Vehicle_Type'].value_counts().plot(kind='bar')
plt.title("Vehicle Type Demand")
plt.xlabel("Vehicle Type")
plt.ylabel("Number of Rides")
plt.show()
