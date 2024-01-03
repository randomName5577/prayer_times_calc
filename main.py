import pandas as pd
from datetime import timedelta

# Load the dataset
file_path = "yearly.csv"
data = pd.read_csv(file_path)


# Function to add minutes to a time string without timezone
def add_minutes_to_series(time_series, minutes):
    return (
        pd.to_datetime(time_series, format="%H:%M").add(
            pd.to_timedelta(minutes, unit="m")
        )
    ).dt.strftime("%I:%M %p")


# Convert times in the dataset to 12-hour format using dt accessor
data["Fajr_12hr"] = pd.to_datetime(
    data["timings.Fajr"].str.extract(r"(\d{2}:\d{2})")[0], format="%H:%M"
).dt.strftime("%I:%M %p")
data["Dhuhr_12hr"] = pd.to_datetime(
    data["timings.Dhuhr"].str.extract(r"(\d{2}:\d{2})")[0], format="%H:%M"
).dt.strftime("%I:%M %p")
data["Asr_12hr"] = pd.to_datetime(
    data["timings.Asr"].str.extract(r"(\d{2}:\d{2})")[0], format="%H:%M"
).dt.strftime("%I:%M %p")
data["Maghrib_12hr"] = pd.to_datetime(
    data["timings.Maghrib"].str.extract(r"(\d{2}:\d{2})")[0], format="%H:%M"
).dt.strftime("%I:%M %p")
data["Isha_12hr"] = pd.to_datetime(
    data["timings.Isha"].str.extract(r"(\d{2}:\d{2})")[0], format="%H:%M"
).dt.strftime("%I:%M %p")

# Create a new date column
data["Date"] = pd.date_range(start="2024-01-01", periods=data.shape[0]).strftime(
    "%b %d"
)

# Calculate Maghrib plus 10 minutes for additional_times
maghrib_plus_10 = add_minutes_to_series(
    data["timings.Maghrib"].str.extract(r"(\d{2}:\d{2})")[0], 10
)

# Concatenate times with the 'Date' column
additional_times = "6:45 AM--1:00 PM--4:00 PM--{}--7:15 PM".format(
    maghrib_plus_10.iloc[0]
)
data["Date"] = (
    data["Date"]
    + "--"
    + data["Fajr_12hr"]
    + "--"
    + data["Dhuhr_12hr"]
    + "--"
    + data["Asr_12hr"]
    + "--"
    + data["Maghrib_12hr"]
    + "--"
    + data["Isha_12hr"]
    + "--"
    + additional_times
)

# save the updated dataframe
data[["Date"]].to_csv("output.csv", index=False)
