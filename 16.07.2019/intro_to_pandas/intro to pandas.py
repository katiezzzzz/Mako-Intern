import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
pd.set_option('max_columns', 50)


# create a series (similar to a column in a table) with an arbitrary list
# it will assign a labeled index to each item in the series, 0-N by default
s = pd.Series([7, 'Heisenberg', 3.14, -1789710578, 'Happy Eating!'])

s = pd.Series([7, 'Heisenberg', 3.14, -1789710578, 'Happy Eating!'],
              index=['A', 'Z', 'C', 'Y', 'E'])
# index can be specified

print(s)

# the series constructor can also convert a dictionary, using the keys of the dictionary as its index
d = {'Chicago': 1000, 'New York': 1300, 'Portland': 900, 'San Francisco': 1100,
     'Austin': 450, 'Boston': None}
cities = pd.Series(d)
print(d)

# index can be used to select specific items from the series
print(cities[['Chicago', 'Portland', 'San Francisco']])

# can use boolean indexing for selection - only responding true items
print(cities[cities < 1000])

# values in a series can be changed on the fly
print('\n')
cities['Chicago'] = 1400
print('New value:', cities['Chicago'])
print(cities[cities < 1000])
print('\n')
cities[cities < 1000] = 750

print (cities[cities < 1000])

# can check if an item is in the series
print('Seattle' in cities)
print('San Francisco' in cities)

# mathematical operations can be done using scalar
print(cities /3)
print(np.square(cities))

# two series can be added and a union of the two siries with addition occurring on the shared index values
# will be returned - values on either series that did not have a shared index will produce a NULL/NaN
# NULL checking can be performed with isnull and notnull
print(cities.notnull())
print(cities.isnull())

'''
DataFrame
- a tablular data structure comprised of rows and columns
- can be thought of as a group of Series objects that share an index (the column names)
- by default, the dataframe constructor will order the columns alphabetically
'''
data = {'year': [2010, 2011, 2012, 2011, 2012, 2010, 2011, 2012],
        'team': ['Bears', 'Bears', 'Bears', 'Packers', 'Packers', 'Lions', 'Lions', 'Lions'],
        'wins': [11, 8, 10, 15, 11, 6, 10, 4],
        'losses': [5, 8, 6, 1, 5, 10, 6, 12]}
football = pd.DataFrame(data, columns=['year', 'team', 'wins', 'losses'])
print(football)

# reading csv
from_csv = pd.read_csv('mariano-rivera.csv')
print(from_csv.head())

cols = ['num', 'game', 'date', 'team', 'home_away', 'opponent',
        'result', 'quarter', 'distance', 'receiver', 'score_before',
        'score_after']
no_headers = pd.read_csv('peyton-passing-TDs-2012.csv', sep=',', header=None,
                         names=cols)
print(no_headers.head())

print(football.head)

# delete the DataFrame
del football

# read from Excel
football = pd.read_excel('football.xlsx', 'Sheet1')
print(football)