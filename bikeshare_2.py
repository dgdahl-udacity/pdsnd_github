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
    city, month, day = None, None, None

    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    # Make a dict of likely inputs for cities; map it to a consistent name in cases like New York vs. New York City, etc.
    cities = {'chicago':'chicago', 'new york':'new york city', 'new york city':'new york city', 'washington':'washington', 'washington, d.c.':'washington'}
    while not city:
        city = input('Please enter a city to examine: Chicago, New York or Washington, D.C.\n')
        city = city.lower()
        if city not in cities:
            city = None

    # get user input for month (all, january, february, ... , june)
    # Allow users to enter either an abbreviation for the month or the full name; map it to the full name no matter what they enter.
    months = {'all':'all', 'january':'january', 'february':'february', 'march':'march', 'april':'april', 'may':'may', 'june':'june', 'jan':'january', 'feb':'february', 'mar':'march', 'apr':'april', 'jun':'june' }
    while not month:
        month = input('Please enter the month, from january to june, \nwhose data you would like to see, or enter \'all\'.\n')
        month = month.lower()
        if month not in months:
            month = None

    # get user input for day of week (all, monday, tuesday, ... sunday)
    # Allow users to enter an abbreviated name for the day or the full day; map it to the full day's name.
    days = {'all':'all', 'sunday':'sunday', 'sun':'sunday', 'monday':'monday', 'mon':'monday', 'tuesday':'tuesday', 'tue':'tuesday', 'wednesday':'wednesday', 'wed':'wednesday', 'thursday':'thursday', 'thu':'thursday', 'friday':'friday', 'fri':'friday', 'saturday':'saturday', 'sat':'saturday' }
    while not day:
        day = input('Please enter a day of the week whose data you would \nlike to see, or enter \'all\'.\n')
        day = day.lower()
        if day not in days:
            day = None

    print('-'*40)
    #Choose the value from the city/month/day keys.
    return cities[city], months[month], days[day]


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
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month_name'] = df['Start Time'].dt.month_name()
    df['day_of_week'] = df['Start Time'].dt.day_name()
    df['hour'] = df['Start Time'].dt.hour

    if month != 'all':
        df = df[df['month_name'] == month.title()]

    if day != 'all':
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df, is_all_months, is_all_days):
    """Displays statistics on the most frequent times of travel, based on the user choices for city, month and day."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # DataFrame.mode()[0] gives us the most common occurrence in a particular column.
    month_mode = df['month_name'].mode()[0]
    day_mode = df['day_of_week'].mode()[0]
    hour_mode = df['hour'].mode()[0]
    # Ditch the military time notation for AM/PM
    if hour_mode > 12:
        hour_mode = str(hour_mode - 12) + 'PM'
    else:
        hour_mode = str(hour_mode) + 'AM'

    # display the most common month
    if is_all_months:
        print('The month with the most trips was {}.'.format(month_mode))
    else:
        print('You chose to view data from the month of {}.'.format(month_mode))

    # display the most common day of week
    if is_all_days:
        print('The day of the week with the most trips was {}.'.format(day_mode))
    else:
        print('You chose to view data only from {}.'.format(day_mode))

    # display the most common start hour
    print('The hour during which the most trips started was {}.'.format(hour_mode))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # Use DataFrame.mode(), as was done in time_stats, to get the most popular stations
    # display most commonly used start station
    print('The most popular station from which to start a ride was {}.'.format(df['Start Station'].mode()[0]))

    # display most commonly used end station
    print('The most popular station at which to end a ride was {}.'.format(df['End Station'].mode()[0]))

    # display most frequent combination of start station and end station trip
    # I could not figure out how to groupby and take a mode, so off to StackOverflow I went...
    # Suggested by https://stackoverflow.com/questions/53037698/how-can-i-find-the-most-frequent-two-column-combination-in-a-dataframe-in-python
    station_combo = df.groupby(['Start Station', 'End Station']).size().idxmax()
    print_string = ''
    
    if station_combo[0] == station_combo[1]:
        print_string = 'The most popular route was from {} to {}, which seems loopy (bad joke).'
    else:
        print_string = 'The most popular route was from {} to {}.'
    
    print(print_string.format(station_combo[0], station_combo[1]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print('The total travel time was {} minutes'.format(df['Trip Duration'].sum()))

    # display mean travel time
    print('The average travel time was {} minutes'.format(df['Trip Duration'].mean()))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_type_group = df.groupby(['User Type'])
    for name, group in user_type_group:
        print('There were {} users of type {}.'.format(group['User Type'].count(), name))

    print('\n')
    # Display counts of gender
    if 'Gender' in df.keys():
        gender_group = df.groupby(['Gender'])
        for name, group in gender_group:
            print('There were {} users of gender {}.'.format(group['Gender'].count(), name))

    print('\n')
    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.keys():
        print('The oldest renter was born in {}.'.format(int(group['Birth Year'].min())))
        print('The youngest renter was born in {}.'.format(int(group['Birth Year'].max())))
        print('The most common year in which renters were born is {}.'.format(int(group['Birth Year'].mode()[0])))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        is_all_months = month == 'all'
        is_all_days = day == 'all'

        time_stats(df, is_all_months, is_all_days)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        
        view_data = input("Would you like to view 5 rows of individual trip data? Enter yes or no?\n").lower()
        start_loc = 0
        while view_data == 'yes' and len(df) > start_loc:
            print(df.iloc[start_loc:start_loc + 5])
            start_loc += 5
            view_data = input("Do you wish to continue?(yes or no):\n").lower()

        restart = input('\nWould you like to restart? Enter yes or no.\n')        
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
