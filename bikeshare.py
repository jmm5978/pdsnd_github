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

    # Gets user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input('Select one of the following cities: Chicago, New York City, Washington\n').lower()
        if city not in ['chicago','new york city','washington']:
            print('Invalid city entered.')
        else:
            break

    # Gets user input for month (all, january, february, ... , june)
    while True:
        month = input('Select one of the following months: January, February, March, April, May, or June--or all\n').lower()
        if month not in ['january','february','march','april','may','june','all']:
            print('Invalid month entered.')
        else:
            break

    # Gets user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input('Select one of the following days: Monday, Tuesday, Wednesday, etc.--or all\n').lower()
        if day not in ['monday','tuesday','wednesday','thursday','friday','saturday','sunday','all']:
            print('Invalid day entered.')
        else:
            break

    print('-'*40)
    print('\nRetrieving data for the following:\nCity: {}\nMonth(s): {}\nDay(s): {}\n'.format(city.title(), month.title(), day.title()))
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
    # loads data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # converts the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extracts month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # filters by month if applicable
    if month != 'all':
        # uses the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filters by month to create the new dataframe
        df = df[df['month'] == month]

    # filters by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # Displays the most common month
    common_month = df['month'].mode()[0]

    if common_month == 1:
        common_month = 'January'
    elif common_month == 2:
        common_month = 'February'
    elif common_month == 3:
        common_month = 'March'
    elif common_month == 4:
        common_month = 'April'
    elif common_month == 5:
        common_month = 'May'
    else:
        common_month = 'June'

    print('\nMost Common Month: {}'.format(common_month))

    # Displays the most common day of week
    print('\nMost Common Day Of The Week: {}'.format(df['day_of_week'].mode()[0]))

    # Displays the most common start hour
    print('\nMost Common Start Hour: {}'.format(df['Start Time'].dt.hour.mode()[0]))

    print("\nThis took %s seconds." % round(time.time() - start_time, 5))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # Displays most commonly used start station
    print('\nMost Common Start Station: {}'.format(df['Start Station'].mode()[0]))

    # Displays most commonly used end station
    print('\nMost Common End Station: {}'.format(df['End Station'].mode()[0]))

    # Displays most frequent combination of start station and end station trip
    print('\nMost Common Start/End Station Combination: ')
    print(df[['Start Station','End Station']].groupby(['Start Station','End Station'])['Start Station'].count().sort_values(ascending=False).index[0])

    print("\nThis took %s seconds." % round(time.time() - start_time, 5))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # Displays total travel time
    print('\nTotal Travel Time: {} seconds'.format(df['Trip Duration'].sum()))

    # Displays mean travel time
    print('\nMean Travel Time: {} seconds'.format(round(df['Trip Duration'].mean(), 1)))

    print("\nThis took %s seconds." % round(time.time() - start_time, 5))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Displays counts of user types
    print('\nSubscribers: {}\nCustomers: {}'.format(df['User Type'].value_counts()[0], df['User Type'].value_counts()[1]))

    # Displays counts of gender and handles empty gender field
    try:
        print('\nMale: {}\nFemale: {}'.format(df['Gender'].value_counts()[0], df['Gender'].value_counts()[1]))
    except KeyError:
        print('\nNo user gender data available.')

    # Displays earliest, most recent, and most common year of birth
    try:
        print('\nEarliest Birth Year: {}\nMost Recent Birth Year: {}\nMost Common Birth Year: {}'.format(str(int(df['Birth Year'].min())), str(int(df['Birth Year'].max())), str(int(df['Birth Year'].mode()[0]))))
    except KeyError:
        print('\nNo user birth data available.')

    print("\nThis took %s seconds." % round(time.time() - start_time, 5))
    print('-'*40)


def display_data(df, city):
    """Displays lines of raw data on request."""

    if city != 'washington':
        df['Gender'].fillna('N/A', inplace=True)
        df['Birth Year'].fillna('N/A', inplace=True)

    # Builds list of indices
    index_list = list(df.index.values)

    # Prints rows of raw data corresponding to the index_list elements
    line = 0

    while line < len(index_list):
        response = input('Would you like to view trip data? Enter yes or no.\n').lower()
        if response == 'yes':
            if line == len(index_list) - 1:
                print(df.loc[index_list[line],:])
                print('\n')
                line += 5
            elif line == len(index_list) - 2:
                print(df.loc[[index_list[line], index_list[line+1]],:])
                print('\n')
                line += 5
            elif line == len(index_list) - 3:
                print(df.loc[[index_list[line], index_list[line+1], index_list[line+2]],:])
                print('\n')
                line += 5
            elif line == len(index_list) - 4:
                print(df.loc[[index_list[line], index_list[line+1], index_list[line+2], index_list[line+3]],:])
                print('\n')
                line += 5
            else:
                print(df.loc[[index_list[line], index_list[line+1], index_list[line+2], index_list[line+3], index_list[line+4]],:])
                print('\n')
                line += 5
        elif response == 'no':
            break
        else:
            print('Invalid response.')


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_data(df, city)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
