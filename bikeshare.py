import pandas as pd
import os
import numpy as np

#import files and label them
chg = pd.read_csv('chicago.csv')
chg['city'] = 'Chicago'

wdc = pd.read_csv('washington.csv')
wdc['city'] = 'Washington'

nyc = pd.read_csv('new_york_city.csv')
nyc['city'] = 'New York'

#combine files into one dataset
df = chg.append(wdc, ignore_index = True).append(nyc, ignore_index = True)

#remove NaN's from Birth Year and change to integer to eliminate trailing 0's
df['Birth Year'] = df['Birth Year'].fillna(0)
df['Birth Year'] = df['Birth Year'].astype(int)

#select city
available_cities =  ['Chicago', 'Washington', 'New York']
available_cities.extend(['All'])
city_list = input('\nEnter City- "Chicago", "Washington", or "New York" or \n "all" for all cities: ')
sel_city = city_list.split(',')
#error correction
while True:
    if city_list.title() in available_cities:
        break
    else:
        city_list = input('\nInvalid City. Check spelling and \n reenter ')
sel_city = city_list.split(',')
sel_city = [city.title() for city in sel_city]; sel_city #adapted from https://chrisalbon.com/python/basics/applying_functions_to_list_items/
for city in sel_city:
    if city_list.title() == 'All':
       df
       break
    else:
       df = df.loc[df['city'].isin(sel_city)]

# extract hour, month, and day of week from Start Time to create new columns
df['Start Time'] = pd.to_datetime(df['Start Time'])
df['hour'] =  df['Start Time'].dt.hour
df['month'] = df['Start Time'].dt.month_name()
df['day_of_week'] = df['Start Time'].dt.weekday_name
#select month
available_months = ['January','February','March','April','May','June']
available_months.extend(['All'])
month_list = input('\nmonth of travel by fullname of month (i.e. "January")) \n or "all" for all months: ')
month_list.title()
sel_month = month_list.split(',')
#error correction
while True:
    if month_list.title() in available_months:
        break
    else:
        month_list = input('\nInvalid month- verify spelling and reenter: ')

sel_month =  month_list.split(',')
sel_month = [month.title() for month in sel_month];sel_month #see sel_city comment
for month in sel_month:
    if month_list.title() == 'All':
        df
        break
    else:
        df =  df.loc[df['month'].isin(sel_month)]
#select day
available_days =  ['Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
available_days.extend(['All'])
day_list = input('\nday of travel by name of day (i.e. "Sunday")) \n or "all" for all days. \n(USER WARNING: due to system limitations and processing time, \nentering "all" for all three questions is not recommended.): ')
day_list.title()
sel_day = day_list.split(',')
#error correction
while True:
    if day_list.title() in available_days:
        break
    else:
        day_list = input('\nInvalid day- verify spelling and reenter: ')
sel_day = day_list.split(',')
sel_day = [day.title() for day in sel_day];sel_day #see sel_city comment
for day in sel_day:
    if day_list.title() == 'All':
        df
        break
    else:
        df = df.loc[df['day_of_week'].isin(sel_day)]

#request data
#http://introtopython.org/while_input.html gave me the idea for the and while loop
print('\nchoose data')
print('-type "raw data" for the first 5 rows of data')
print('-type "stats" for stats')
print('-type "quit" to quit')
ch = input('selection: ')
choice = str(ch)
#print(choice)
st = 0
sp = 0
while choice != 'quit':
    if choice == 'raw data':
        sp += 5
        start = int(st)
        stop = int(sp)
        rd = df[start:stop]
        print(rd)
        choice = input('\n type "raw data" for 5 more lines of raw data, \n "stats" for statiscs, or "quit": ')
    elif choice == 'stats':
        #travel day and time info
        mcm = df.mode()['month'][0]
        mcd = df.mode()['day_of_week'][0]
        mch = df.mode()['hour'][0]
        print('\nPopular times of travel')
        print('Most common month: ',mcm)
        print('Most common day of week: ',mcd)
        print('Most common hour of day: ',mch)
        #stations and trips info
        df['trip'] = df['Start Station']+df['End Station']
        css = df.mode()['Start Station'][0]
        cdw = df.mode()['End Station'][0]
        mct = df.mode()['trip'][0]
        print(" ")
        print('Popular stations and trip')
        print('Most common start station: ',css)
        print('Most common end station: ',cdw)
        print('Most common trip from start to end: ',mct)
        #trip duration info
        df['dummy'] = 'Trip Duration'
        t_dur = df.groupby(['dummy'])['Trip Duration'].sum()
        t_dur = dict(t_dur)
        t_mean= df.groupby(['dummy'])['Trip Duration'].mean()
        t_mean = dict(t_mean)
        for key, value in t_dur.items():
        print("{}: {}".format(key, value))
        for key, value in t_mean.items():
        print("{}: {}".format(key, value))

        print(" ")
        print('Trip duration')
        print('Total travel time (in minutes): ',round(tot,2))
        print('Average travel time (in minutes): ',round(avg,2))
        #birth year info
        eby = df.min()['Birth Year']
        rby = df.max()['Birth Year']
        cby = df.mode()['Birth Year'][0]
        if sel_city == ['Washington']:
            print('\nAge demographics not available for Washington')
        else:
            print('\nAge demographics')
            print('Earliest year of birth: ',eby)
            print('Most recent birth: ',rby)
            print('Most common year of birth: ',cby)
        #usergroup info
        user_group = df.groupby(['User Type'])['Birth Year'].count()
        user_type = dict(user_group)
        print(" ")
        print('User type info')
        for key, value in user_type.items():
            print("{}: {}".format(key, value)) #stack overflow assisted
            break
        #gender info
        gender_group = df.groupby(['Gender'])['Gender'].count()
        gender = dict(gender_group)
        if sel_city == ['Washington']:
            print('\nGender info not available for Washington')
        else:
            print('\nUsage by Gender')
            for key, value in gender.items():
                print("{}: {}".format(key, value))
        choice = input('\ntype "raw data" for raw data or "quit" to quit ')
    #exit the program
    elif choice == 'quit':
        print('good bye')
    #error correction
    else:
        choice = input('verify typing and reenter ' )
