# import modules
import time
import pandas as pd

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

# uses user's inputs to filter the data
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
        city = input("\nWhich city would you like to explore? Chicago, New York city, or Washington?\n").lower()
        if city not in ('chicago', 'new york city', 'washington'):
            print("Invalid city. Please try again")
            continue
        else:
            break

    # get user input for month (all, january, february, ... , june)
    while True:
        month = input("\nWhich month would you like to explore? January, February, March, April, May, June or type 'all' if you want to see data for all months. \n").lower()
        if month not in ('january', 'february', 'march', 'april', 'may', 'june', 'all'):
            print("Invalid month. Please try again")
            continue
        else:
            break

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input("\nWhich day would you like to explore? Monday? Tuesday? Wednesday? Thursday? Friday? Saturday? Sunday? or type 'all' if you want to see data for all days. \n").lower()
        if day not in ('monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all'):
            print("Invalid day. Please try again!")
            continue
        else:
            break


    # print separating line
    print('-'*40)
    return city, month, day

# load bikeshare data from csv to dataframe
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
    #load data into the dataframe
    df = pd.read_csv(CITY_DATA[city])

    #convert start time column to datetime
    df['Start Time'] = pd.to_datetime(arg = df ['Start Time'], format = '%Y-%m-%d %H:%M:%S')


    #filter by month if applicable
    if month != 'all':
        # Extract month
        df['month'] = df['Start Time'].dt.month

        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df.loc[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        #extract day of the week
        df['day_of_week'] = df['Start Time'].dt.weekday_name

        # filter by day of week to create the new dataframe
        df = df.loc[df['day_of_week'] == day.title()]


    return df

# compute statistics on bikeshare dataframe
def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    #Convert the start time column to datetime
    df['Start Time'] =  pd.to_datetime(arg = df['Start Time'], format = '%Y-%m-%d %H:%M:%S')

    # display the most common month
    df['month'] = df['Start Time'].dt.month
    popular_month = df['month'].mode()[0]
    print("Most popular month is: ", popular_month)

    # display the most common day of week
    df['day_of_week'] =  df['Start Time'].dt.weekday_name
    popular_day = df['day_of_week'].mode()[0]
    print("Most popular day: ", popular_day)

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print("Most popular hour: ", popular_hour)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

# gets statictics for stations
def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    start_station = df['Start Station'].value_counts().idxmax()
    print("The most commonly used start station is: ", start_station)

    # display most commonly used end station
    print("The most commnly used end station is: ", df['End Station'].value_counts().idxmax())

    # display most frequent combination of start station and end station trip
    stations_combined = df['Start Station'] + " * " + df['End Station']
    common_stations = stations_combined.value_counts().idxmax()
    print("The most frequent combinatioin of start station and end station are: ", common_stations)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

# computes trip duration
def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_trip_duration = df['Trip Duration'].sum()
    print('Total travel time: \n')
    print(total_trip_duration/60/60/24, 'days')

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print('\nMean travel time: {} seconds'.format(mean_travel_time))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

#computes user statictics
def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print("User types: \n", user_types)

    # Display counts of gender
    if 'Gender' in df.columns:
        gender_count = df['Gender'].value_counts()
        print("Gender: \n", gender_count)

    # Display earliest, most recent, and most common year of birth.
    if 'Birth Year' in df.columns:
        earliest_birth_year = df['Birth Year'].min()
        most_recent_birth_year = df['Birth Year'].max()
        most_common_birth_year = df['Birth Year'].mode()[0]

        print("\nEarliest birth year: " + str(earliest_birth_year))
        print("\nMost recent birth year: " + str(most_recent_birth_year))
        print("\nMost common birth year: " + str(most_common_birth_year))



    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


#prints raw data
def raw_data(df):
    #request user if they want to see raw data
    user_input = input("Do you want to see raw data? Enter yes or no. \n")
    lines = 0

    while True:
        if user_input.lower() != 'no':
            print(df.iloc[lines : lines + 5])
            lines += 5
            user_input = input("\n Do you want to see more raw data? Enter yes or no.\n")
        else:
            break

#main method
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
