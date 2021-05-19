import time
import pandas as pd
desired_width = 320
pd.set_option('display.width', desired_width)
pd.set_option('display.max_columns', 20)


CITY_DATA = {
    'chicago': 'E:/bikeshare/chicago.csv',
    'new york city': 'E:/bikeshare/new_york_city.csv',
    'washington': 'E:bikeshare/washington.csv'}

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
    city = input("\nKindly specify a city to analyze: chicago or new york city or washington.\n").lower()
    while city not in CITY_DATA.keys():
        city = input("\nKindly specify a city to analyze: chicago or new york city or washington.\n").lower()

    # get user input for month (all, january, february, ... , june)
    month = input("\nWould you like to filter with a certain month or all? type 'y' to filter or 'n' for no filter:\n"
                  ).lower()
    if month == 'y':
        month = input('Please specify a month (from january to june): \n').lower()
    elif month.lower() == 'n':
        month = 'all'

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = input("\nWould you like to filter with a certain day or all? type 'y' to filter or 'n' for no filter:\n")\
        .lower()
    if day == 'y':
        day = input('\nPlease specify a day (from sunday to friday):\n').title()
    elif day == 'n':
        day = 'all'

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
    df['Month'] = df['Start Time'].dt.month
    df['Day_of_Week'] = df['Start Time'].dt.day_name()
    df['Hour'] = df['Start Time'].dt.hour

    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        df = df[df['Month'] == month]
    if day != 'all':
        df = df[df['Day_of_Week'] == day]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    popular_month = df['Month'].mode()[0]
    print('The most common month is:\n{}\n'.format(popular_month))

    # display the most common day of week
    popular_day = df['Day_of_Week'].mode()[0]
    print('The most common day of week is:\n{}\n'.format(popular_day))

    # display the most common start hour
    popular_hour = df['Hour'].mode()[0]
    print('The most common start hour is:\n{}\n'.format(popular_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""
    print('\nCalculating The Most Popular Stations and Trip...\n')

    start_time = time.time()
    # display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    print('The most commonly used start station is:\n{}\n'.format(popular_start_station))

    # display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    print('The most commonly used end station is:\n{}\n'.format(popular_end_station))

    # display most frequent combination of start station and end station trip
    df['Route'] = df['Start Station'] + '-' + df['End Station']
    most_frequent = df['Route'].mode()[0]

    print('Most frequent combination of Start/End Station is:\n{}\n'.format(most_frequent))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print('Total travel time is:\n{}\n'.format(total_travel_time))

    # display mean travel time
    average_travel_time = df['Trip Duration'].mean()
    print('Average travel time is:\n{}\n'.format(average_travel_time))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = 'User types counts are: {}'.format(df.groupby(['User Type'])['User Type'].count())
    print('Gender counts are:\n{}\n'.format(user_types))

    # Display counts of gender
    if 'Gender' in df:
        gender = df.groupby(['Gender'])['Gender'].count()
        print('Gender counts are:\n{}\n'.format(gender))
    else:
        print("Gender stats cannot be calculated because it doesn't appear in dataframe")

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df:
        earliest_year_of_birth = df['Birth Year'].min()
        print('Earliest year of birth is:\n{}\n'.format(earliest_year_of_birth))
        most_recent_year_of_birth = df['Birth Year'].max()
        print('Most recent year of birth is:\n{}\n'.format(most_recent_year_of_birth))
        most_common_year_of_birth = df['Birth Year'].mode()[0]
        print('Most common year of birth is:\n{}\n'.format(most_common_year_of_birth))
    else:
        print("\n\nBirth Year stats cannot be calculated because it doesn't appear in dataframe\n\n")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def display_raw_data(df):
    """Displays raw data about Bikeshare project."""
    start_loc = 0
    # A 'prompt' that asks the user whether he/she wants to check raw data.
    display_raw = input('\nWould you like to check 5 rows of raw data? Enter yes or no:\n')
    # A 'while' loop that handles invalid inputs from the user.
    while display_raw.lower() not in ('yes', 'no'):
        print('\nInvalid input!, kindly re-enter your selection again.\n')
        display_raw = input('\nWould you like to check 5 rows of raw data? Enter yes or no:\n')
    if display_raw.lower() == 'no':
        print('\nThank You\n')
    # A 'while' loop that keeps displaying more raw data if the user wants to check more of it.
    while display_raw.lower() == 'yes':
        print(df.iloc[start_loc:start_loc+5])
        start_loc += 5
        display_raw = input('\nDo you want to check 5 more rows of raw data? Enter yes or no:\n')
        if display_raw.lower() == 'no':
            print('\nExiting raw data...\n')
            break
        # 'elif' statement to handle invalid inputs.
        elif display_raw.lower() != 'yes' and display_raw.lower() != 'no':
            print('\nInvalid Input, kindly re-enter your selection again.\n')
            display_raw = input('\nDo you want to check 5 more rows of raw data? Enter yes or no:\n')



def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
