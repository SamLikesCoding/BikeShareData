import time
import pandas as pd
import numpy as np

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}
MONTHS = {1: "january", 2: "february", 3: "march", 4: "april", 5: "may", 6: "june"}
DAYS = {'monday': 0, 'tuesday': 1, 'wednesday': 2, 'thursday': 3, 'friday': 4, 'saturday': 5, 'sunday': 6}


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """

    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = input("Would you like to see data for Chicago, New York City or Washington? \n")
    city = city.lower()
    while True:
        if city in CITY_DATA.keys():
            break
        else:
            city = input("Give a valid city : Chicago, New York City, or Washington \n")

    option = input("Would you like to filter the data by month, day, both or none \n")
    option = option.lower()
    while True:

        # get user input for month (all, january, february, ... , june)
        if option == "month":
            month = input("Which month - January, February, March, April, May, or June \n")
            month = month.lower()
            print(month)
            day = 'all'
            while True:
                if month in MONTHS.values():
                    break
                else:
                    month = input("Give a valid month : January...July \n")
                    month = month.lower()
            break

        # get user input for day of week (all, monday, tuesday, ... sunday)
        elif option == 'day':
            day = input("Which day - Monday, Tuesday, Wednesday, Thursday, Friday, Saturday or Sunday \n")
            day = day.lower()
            month = 'all'
            while True:
                if day in DAYS.keys():
                    break
                else:
                    day = input(
                        "Give a valid day - Monday, Tuesday, Wednesday, Thursday, Friday, Saturday or Sunday \n")
                    day = day.lower()
            break

        # For both month and day filter
        elif option == "both":
            month = input("Which month - January, February, March, April, May, or June \n")
            month = month.lower()
            while True:
                if month in MONTHS.values():
                    break
                else:
                    month = input("Give a valid month : January...July\n")
                    month = month.lower()
            day = input("Which day - Monday, Tuesday, Wednesday, Thursday, Friday, Saturday or Sunday \n")
            day = day.lower()
            while True:
                if day in DAYS.keys():
                    break
                else:
                    day = input(
                        "Give a valid day - Monday, Tuesday, Wednesday, Thursday, Friday, Saturday or Sunday \n")
                    day = day.lower()
            break

        elif option == 'none':
            day = 'all'
            month = 'all'
            break

        else:
            option = input("Please enter an valid option - day, month or none \n")
            option = option.lower()

    print('-' * 40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    print("\nMost common month : \n", MONTHS[pd.to_datetime(df['Start Time']).dt.month.value_counts(sort=True).index[0]])
    # display the most common day of week
    print("Most common day : \n", pd.to_datetime(df['Start Time']).dt.weekday_name.value_counts(sort=True).index[0])
    # display the most common start hour
    print(" Most common Start Hours : \n", pd.to_datetime(df["Start Time"]).dt.hour.value_counts(sort=True).index[0])
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print("\n Most Commonly used Start Station : " + df["Start Station"].value_counts(sort=True).index[0])
    # display most commonly used end station
    print(" Most Commonly used End Station : " + df["End Station"].value_counts(sort=True).index[0])
    # display most frequent combination of start station and end station trip
    print(" Most Commonly used Combination of Start and End Stations : ")
    station_combo = df.groupby(["Start Station", "End Station"]).size().nlargest().keys().tolist()
    for start_stn, end_stn in station_combo:
        print("Start Station : {} \nEnd Station : {}\n".format(start_stn, end_stn))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print("\n Total Travel Time : {} mins".format(df["Trip Duration"].sum()))

    # display mean travel time
    print(" Mean Travel Time : {} mins".format(df["Trip Duration"].mean()))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def user_stats(df, w_flag):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print("\nUser Type Data : \n", df["User Type"].value_counts(sort=True))
    # Display counts of gender
    if w_flag:
        print("\n Gender Information : \n", df["Gender"].value_counts(sort=True))
        # Display earliest, most recent, and most common year of birth
        birth_year = df["Birth Year"].dropna().tolist()
        print("\n Earliest Birth Year : \n ", birth_year[0])
        print(" Most Recent Birth Year : \n ", birth_year[-1])
        print(" Most Common Birth Year : \n", df["Birth Year"].value_counts(sort=True).index[0])
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        # Since Washington data does not contain Gender and Birth Year information ,w_flag is used
        if city != 'washington':
            user_stats(df, True) # Other Cities
        else:
            user_stats(df, False) # For Washington

        n = 0
        stop_flag = False
        df = load_data(city, 'all', 'all')
        while n < len(df.index) and not stop_flag:
            print("\n==== User Data Index :: {} ====\n".format(n))
            print(df.loc[n])
            if n%10 == 0 and n != 0:
                while True:
                    set_stop = input("\n\n Would you like to see more data (yes or no) : ")
                    if set_stop.lower() == 'yes':
                        break
                    elif set_stop.lower() == 'no':
                        stop_flag = True
                        break
                    else:
                        print("\n Invalid Option!! \n")
            n += 1

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
