import time
import pandas as pd
import numpy as np
import calendar

CITY_DATA = {"chicago": "chicago.csv", "new york city": "new_york_city.csv", "washington": "washington.csv"}

def get_filters():
    print("Hello let's explore some US bike share data!")
    while True:
        cities = ["chicago", "new york city", "washington"]
        city = input("Please choose a city from chicago, new york city, washington to analyze: ").lower()
        if city not in cities:
            print("please re-enter a correct name of the city!")
        else:
            break
    while True:
        month = input('Please enter a month from january to june to filter by, or "all" to apply no month filter: ').lower()
        months = ["january", "february", "march", "april", "may", "june", "july"]
        if month != "all" and month not in months:
            print("please re-enter a correct name of the month!")
        else:
            break
    while True:
        day = input('Please enter a day of the week to filter by, or  "all" to apply no day filter: ').lower()
        days = ['saturday', "sunday", "monday", "tuesday", "wednesday", "thursday", "friday"]
        if day != "all" and day not in days:
            print("please re-enter a correct name of the day!")
        else:
            break
    print('-'*60)
    return city, month, day


def load_data(city, month, day):
    df = pd.read_csv(CITY_DATA[city])
    df["Start Time"] = pd.to_datetime(df["Start Time"])
    df["month"] = df["Start Time"].dt.month
    df["day_of_week"] = df["Start Time"].dt.day_name()
    if month != "all":
        months = ["january", "february", "march", "april", "may", "june", "july"]
        month = months.index(month)+1
        df = df[df["month"] == month]
    if day != "all":
        df = df[df["day_of_week"] == day.title()]
    return df

def display_raw_data(df):
    i = 0
    answer = input("DO you want to display the first 5 rows of data? yes or no: ").lower()
    pd.set_option("display.max_columns", None)
    while True:
        if answer == "no":
            break
        print(df[i:i+5])
        answer = input("DO you want to display the next 5 rows of data? yes or no: ").lower()
        i += 5

def time_stats(df):
    print("Displaying statistics on the most frequent times of travel...")
    start_time = time.time()
    most_common_month = df["month"].mode()[0]
    print("The most common month is ", calendar.month_name[most_common_month])
    most_common_day = df["day_of_week"].mode()[0]
    print("The most common day of week is ", most_common_day)
    df["hour"] = df["Start Time"].dt.hour
    common_hour = df["hour"].mode()[0]
    print("The most common start hour is ", common_hour)
    print("This took %s seconds." % (time.time() - start_time))
    print('-'*60)

def station_stats(df):
    print("Displaying statistics on the most popular stations and trip...")
    start_time = time.time()
    common_start_station = df["Start Station"].mode()[0]
    print("The most commonly used start station is ", common_start_station)
    common_end_station = df["End Station"].mode()[0]
    print("The most commonly used end station is ", common_end_station)
    common_start_end = (df["End Station"] + "-" + df["End Station"]).mode()[0]
    print("The most frequent combination of start and end stations trip is ", common_start_end)
    print("This took %s seconds." % (time.time() - start_time))
    print('-' * 60)

def trip_duration_stats(df):
    print("Displaying statistics on the total and average trip duration...")
    start_time = time.time()
    total_time = df["Trip Duration"].sum()
    print("The total travel time is ", total_time, "seconds,or", total_time/3600, "hours")
    avg_time = df["Trip Duration"].mean()
    print("The average travel time is ", avg_time, "seconds,or", avg_time / 3600, "hours")
    print("This took %s seconds." % (time.time() - start_time))
    print('-' * 60)

def user_stats(df):
    print("Displaying statistics on bike share users...")
    start_time = time.time()
    print("Counts of user types:", df["User Type"].value_counts())
    if "Gender" in df:
        print("Counts of gender:", df["Gender"].value_counts())
        if "Birth Year" in df:
            earliest_birth_year = int(df["Birth Year"].min())
            print("Earliest year of birth: ", earliest_birth_year)
            recent_birth_year = int(df["Birth Year"].max())
            print("Most recent  year of birth: ", recent_birth_year)
            common_birth_year = int(df["Birth Year"].mode()[0])
            print("Most common year of birth: ", common_birth_year)

        print("This took %s seconds." % (time.time() - start_time))
        print('-' * 60)

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        display_raw_data(df)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input("Would you like to restart? Enter yes or no. ")
        if restart.lower() != "yes":
            break

if __name__ == "__main__":
    main()
