import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

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
    while True:
        city = input("which city shall we analyze\n").lower()
        if city not in ('chicago', 'new york city', 'washington'):
            print("please enter either chicago, new york city or washington\n")
        else:
            break

    # get user input for month (all, january, february, ... , june)
    while True:
        month = input("which month shall we analyze? | (e.g. for january, please input [1])\n").lower()
        if month not in ('1','2','3','4','5','6'):
            print ("please enter the correct input. | (e.g. for january, please input [1])\n")
        else:
            break

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input("which day of week shall we analyze?\n").lower()
        if day not in ('monday','tuesday','wednesday','thursday','friday','saturday','sunday'):
            print ("please enter the correct input.\n")
        else:
            break


    print('-'*40)
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
   # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['1', '2', '3', '4', '5', '6']
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
    common_month = df['month'].mode()[0]
    print("the most common month:",common_month)

    # display the most common day of week
    common_day = df['day_of_week'].mode()[0]
    print("the most common day:",common_day)

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    common_hour = df['hour'].mode()[0]
    print("the most common hour:",common_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    common_start = df['Start Station'].mode()[0]
    print("the most commonly used start station:",common_start)

    # display most commonly used end station
    common_end = df['End Station'].mode()[0]
    print("the most commonly used end station:",common_end)

    # display most frequent combination of start station and end station trip
    common_trip = df.groupby(['Start Station','End Station']).size().idxmax()
    print("most frequent combination of start station and end station trip:",common_trip)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_duration = df['Trip Duration'].sum()
    print("total travel time:",total_duration)

    # display mean travel time
    average_duration = df['Trip Duration'].mean()
    print("average travel time:",average_duration)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print("counts of user types:\n",user_types)

    # Display counts of gender if available, else skip
    try:
        gender_types = df['Gender'].value_counts()
        print("counts of gender:\n",gender_types)
    except:
        print('Sorry, gender is not available.')

    # Display earliest, most recent, and most common year of birth if available, else skip
    try:
        birth_year_earliest = df['Birth Year'].min()
        birth_year_recent = df['Birth Year'].max()
        birth_year_common = df['Birth Year'].mode()[0]
    except:
        print('Sorry, year of birth data is not available.')
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        individual = input('\nWould you like to view individual trip data?\n').lower()
        if individual in ('yes','y'):
            i = 0
            while True:
                print(df.iloc[i:i+5])
                i += 5
                more_data = input('Would you like to see moredata?\n').lower()
                if more_data not in ('yes', 'y'):
                    break
                    
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
