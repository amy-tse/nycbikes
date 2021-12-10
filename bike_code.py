"""
Name: Amy Tse
Resources: https://data.cityofnewyork.us/Transportation/Bicycle-Counts https://s3.amazonaws.com/tripdata/index.html
Title: NYC Bike Trends : Are Bike Lane Expansions Necessary?
URL: https://nyc-bike-trends.glitch.me/

Note: Other portions should be commented out when testing each portion.
"""

import pandas as pd

"""
Creating citibike_counts.csv:
This portion of code will parse through 100+ citiBike csv files to scrape data and clean the dataframe in order to
extract the number of riders each month from 2013-2017.
It will then create a new csv file containing the counts by month and year, as well as calculate the total and average.
"""
# Make an empty dataframe to store citibike_counts
citibike_counts = pd.DataFrame(columns = ['01','02','03','04','05','06','07','08','09','10','11','12'],
index = ['2013','2014','2015','2016','2017','2018','2019','2020','2021','Monthly Average'])

#Given a dataframe, return the number of rows, aka number of riders.
def get_num_riders(df):
    return df.shape[0];

filenames=[]
#The datasets for citiBike data begin in 7/2013 and end in 10/2021
starting_year=2013
starting_month=6
#There are 108 files to process.
for i in range(108):
    if (starting_month==12):
        starting_month=0
        starting_year+=1
    else:
        starting_month+=1
        if starting_month<10:
            file = 'citibike_data/' + f'{starting_year}' +'0'+f'{starting_month}' +'.csv'
        else:
            file = 'citibike_data/' + f'{starting_year}' +f'{starting_month}' +'.csv'
    filenames.append(file)

#For each file, extract the number of riders that month and add it to its respective spot in the citibike_counts dataframe
for file in filenames:
    date=file.replace('citibike_data/','') .replace('.csv','')
    year=str(date[:4])
    month=str(date[4:])
    num_riders=get_num_riders(pd.read_csv(file, low_memory=False))
    citibike_counts[f'{month}'][f'{year}']=num_riders

#Get the total and average of each year
yearly_total = citibike_counts.sum(axis = 1)
yearly_avg = citibike_counts.mean(axis = 1)

citibike_counts['Yearly Total'] = yearly_total
citibike_counts['Yearly Average']= yearly_avg

monthly_avg=citibike_counts.mean(axis=0)
citibike_counts.at['Monthly Average']=monthly_avg
citibike_counts['Yearly Total']['Monthly Average']='NaN'
citibike_counts['Yearly Average']['Monthly Average']='NaN'

citibike_counts.to_csv('citibike_counts.csv')



"""
Creating citibike_monthly_percentages.csv:
This portion of code will use the previously created csv file to get the percentage of each month's average citiBike riders,
to find what percentage of citiBike rides are taken each month on average. The goal is to see which months have the most citiBike bicyclists.
"""
citibike_counts=pd.read_csv('citibike_counts.csv')
#clean data
month_percentage =citibike_counts.drop(['Yearly Total','Yearly Average'],axis=1).loc[9]
total=0
a_list=[]
month_percentage_csv = pd.DataFrame(columns = ['01','02','03','04','05','06','07','08','09','10','11','12'],
index = ['Percentage'])

# Get the total number of monthly averages. This will be the denominator.
for i in month_percentage:
    if (i!="Monthly Average"):
        total+=int(i)

# Divide each monthly average by the total and fill up the new dataframe.
for i in month_percentage:
    if (i!="Monthly Average"):
        to_add= int(i) / total *100
        a_list.append(to_add)
month_percentage_csv.at['Percentage']=a_list
month_percentage_csv.to_csv('citibike_monthly_percentages.csv')




"""
Creating nyc_yearly_counts.csv:
This portion of code will use openNYC dataset. The file will be cleaned and processed in order to get the sums for each year.
"""
nyc_yearly_counts = pd.DataFrame(columns = ['01','02','03','04','05','06','07','08','09','10','11','12'],
index = ['2013','2014','2015','2016','2017','2018','2019','2020','2021','Monthly Average'])

# Read in OpenNYC dataset
nyc_counts=pd.read_csv('Bicycle_Counts.csv').drop(['status','site','id'],axis=1,)
# Convert to date time objects
nyc_counts['date'] = pd.to_datetime(nyc_counts['date'])
nyc_counts['date'] = nyc_counts['date'].dt.strftime('%Y-%m')
nyc_counts=nyc_counts.groupby("date",sort=True,as_index=False).sum()

#Extract date and month to fill up new dataframe
for i in range(len(nyc_counts['counts'])):
    year=nyc_counts['date'][i][:4]
    month=nyc_counts['date'][i][5:]
    if(nyc_counts['counts'][i]==0):
        nyc_yearly_counts[f'{month}'][f'{year}']='NaN'
    else:
        nyc_yearly_counts[f'{month}'][f'{year}']=nyc_counts['counts'][i]


#Get the total and average of each year
yearly_total = nyc_yearly_counts.sum(axis = 1)
yearly_avg = nyc_yearly_counts.mean(axis = 1)

nyc_yearly_counts['Yearly Total'] = yearly_total
nyc_yearly_counts['Yearly Average']= yearly_avg

monthly_avg=nyc_yearly_counts.mean(axis=0)
nyc_yearly_counts.at['Monthly Average']=monthly_avg

nyc_yearly_counts.to_csv('nyc_yearly_counts.csv')

nyc_yearly_counts=pd.read_csv('nyc_yearly_count.csv')
iterator=0
for month in nyc_yearly_counts:
    if(iterator!=0):
        nyc_yearly_counts[month][9]=v[month].mean()
    iterator+=1

nyc_yearly_counts['Yearly Total'][9]='NaN'
nyc_yearly_counts['Yearly Average'][9]='NaN'
nyc_yearly_counts.to_csv('nyc_yearly_counts.csv')


"""
Creating nyc_monthly_percentages.csv:
This portion of code will use the previously created csv file to get the percentage of each month's average riders,
to find what percentage of rides are taken each month on average. The goal is to see which months have the most bicyclists.
"""
nyc_bike_counts=pd.read_csv('nyc_yearly_counts.csv')

#clean data
month_percentage =nyc_bike_counts.drop(['Yearly Total','Yearly Average'],axis=1).loc[9]
total=0
a_list=[]
month_percentage_csv = pd.DataFrame(columns = ['01','02','03','04','05','06','07','08','09','10','11','12'],
index = ['Percentage'])

# Get the total number of monthly averages. This will be the denominator.
for i in month_percentage:
    if (i!="Monthly Average"):
        total+=int(i)

# Divide each monthly average by the total and fill up the new dataframe.
iterator=0
for i in month_percentage:
    if (i!="Monthly Average" and iterator!=0):
        to_add= int(i) / total *100
        a_list.append(to_add)
    iterator+=1

month_percentage_csv.at['Percentage']=a_list
month_percentage_csv.to_csv('nyc_monthly_percentages.csv')
