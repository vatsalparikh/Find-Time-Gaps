# load modules
import pandas as pd
import time

# log start time
start_time = time.time()

# load input data set (Python pickle file)
df = pd.read_pickle(r'px.xz') # replace <path> with proper file path

# USER CODE

# convert dt column data to datetime format for processing
df['dt'] = pd.to_datetime(df['dt'], format='%Y-%m-%d', errors='coerce')

# sort dataframe by bbgid and by date to get all records for single bbgid sequentially
df.sort_values(['bbgid', 'dt'])

# group dataframe by bbgids and get pandas series of dates.
# compute difference between dates for each group and store result in pandas series
# reason for subtracting 1 at the very end is explained with example below
# example: start - 2018-05-11, end - 2018-05-10, here the answer produced is 1
# since there is 'no gap' in data from one day to next the expected answer is 0
# subtracting 1 from result for every row takes care of this
df['length'] = df.groupby('bbgid')['dt'].diff().dt.days - 1

# create new series for all columns needed in output: start, end, bbgid, length (next 4 lines of uncommented code)

# to create a series of start dates, take all rows except last row from 'dt' column
start = pd.Series(df.iloc[:-1, 0])

# to create a series of end dates, take all rows except first row from 'dt' column and reset indices to start from 0
end = pd.Series(df.iloc[1:, 0]).reset_index(drop = True)

# to create a series of bbgids, take all rows except first from 'bbgid' column and reset indices to start from 0
bbgid = pd.Series(df.iloc[1:, 1]).reset_index(drop = True)

# to create a series of lengths, take all rows except first row from 'length' column and reset indices to start from 0
length = pd.Series(df.iloc[1:, 2]).reset_index(drop = True)

# create a dictionary of pandas series with column name as key and series as value
d = {'start' : start, 'end' : end, 'bbgid' : bbgid, 'length' : length}

# create new dataframe and sort it by length, bbgid, start in descending, ascending, ascending order respectively
stats = pd.DataFrame(d).sort_values(['length', 'bbgid', 'start'], ascending = [False, True, True])

# export result to Excel
stats.iloc[0:1000].to_excel(r'solution.xlsx', index = False) # replace <path> with proper file path

# show execution time
print("--- %s seconds ---" % (time.time() - start_time))