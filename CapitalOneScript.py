# Matt Grant
# 9/28/2105
# Data Analysis: Capital One, Use transaction data to categorize clients

import pandas as pd
import numpy as np
from datetime import datetime
from pylab import *
#get_ipython().magic(u'matplotlib inline')
style.use('ggplot')

#Using the transactions data attached below, write a script in 
#Python,that outputs a list of subscription IDs,their subscription 
#type (daily, monthly, yearly, one-off), and the duration of their 
#subscription.
# Subscription ID, Type , Duration 
#    3159        , Monthly, 900 days 

#Bounus
#1. Give annual revenue numbers for all years between 1966 and 2014. 
#Which years had the highest revenue growth, and highest revenue loss?

#2. Predict annual revenue for year 2015 (based on historical retention and new subscribers)

#Import data into pandas dataframe
data = pd.read_csv('../Data Science/CapitalOneScript/subscription_report.csv')

# Explore data
#data.head()
#data.shape

# Set Transaction Date as time data type
# YYYY - MM - DD
data['Transaction Date'] = pd.to_datetime(data['Transaction Date'])

# Verify correct data type 
data['Transaction Date'].dtype

# Look for any null values
data.isnull().sum()

#Distribution of Subscriber for # of transactions(min:1 (one-off), max 91)
data['Subscription ID'].value_counts().plot(kind='hist', bins=20, )
ylabel('Subscribers')
xlabel('Number of Transactions')
title('Distribution of Subscriber per # of transactions')

# Sort data by 'Subscription ID' and date & re-index 
data.sort(['Subscription ID','Transaction Date'], inplace=True)
data.index = range(1,len(data) + 1)

#Create a column for the year in which the transaction occured 
data['Year'] = [datetime.year for datetime in data['Transaction Date']]


#Create a list of Subscription IDs  27,609 Unique IDs
IDs = [data['Subscription ID'].unique()]
#print IDs, len(IDs[0])

#Create dataframe for results
results = pd.DataFrame(columns =['Subscription ID','Duration','Type',])

# Initailize arrays to store data
IDCol = [0]*27609
nrowCol = [0]*27609
deltaTcol=[0]*27609
durationCol=[0]*27609
TypeCol=[0]*27609

# loop through all subscription IDs and pull out ID,#transactions,Duration(max-min),Type(monthly..)
for item in range(27609): #27609 elements
    
    IDdata = data[data['Subscription ID'] == IDs[0][item]]
    ID = IDdata['Subscription ID'].iloc[0]#IDs[0][item] 
    nrow = IDdata.shape[0]
    
    if nrow > 1:  
        deltaT = IDdata['Transaction Date'].iloc[nrow-1] - IDdata['Transaction Date'].iloc[0]
        duration = deltaT/nrow
    else:
        deltaT = pd.to_timedelta('0 days')
        duration = pd.to_timedelta('0 days')
        tType = 'One Off'
        
    if duration > pd.to_timedelta('250 days'):
        tType = 'Yearly'
        
    elif duration >= pd.to_timedelta('27 days') and duration <= pd.to_timedelta('32 days'):
        tType = 'Monthly'                      
        
    elif duration > pd.to_timedelta('0 days') and  duration < pd.to_timedelta('2 days'):
        tType = 'Daily'

    
# Save data to lists
    IDCol[item] = ID
    nrowCol[item] = nrow
    deltaTcol[item]= deltaT
    durationCol[item]= duration
    TypeCol[item]= tType
    #print ID, nrow, deltaT, duration, tType     
    

print 'complete'

#Save data to dataframe
results['Subscription ID'] = IDCol
results['Duration'] = deltaTcol
results['Type'] = TypeCol

#Output to csv file
results.to_csv("CapitalOneTransactions.csv", index=False, cols=('ID','Type','Duration(Days)'))


# Total revenue by year in $ 
revenue_by_year = data['Amount (USD)'].groupby(data['Year']).sum()#
print 'Revenue by year',revenue_by_year


#plot revenue over time
revenue_by_year.plot(title='Revenue Over Time ($100 Million)')
rcParams['figure.figsize'] = (10, 6)

# Bar chart of revenue change per year
revenue_by_year.pct_change().plot(kind='bar',title='Percent Revenue Change Per Year')
rcParams['figure.figsize'] = (10, 6)

# generates percent change and orders series from highest revenue loss to highest revenue growth
# 2014 - greatest revenue loss (-58.0%)
# 1967 - greatest revenue growth (51.5%)
print 'Greatest Revenue Growth:',revenue_by_year.pct_change().idxmax()
print 'Greatest Revenue Loss:', revenue_by_year.pct_change().idxmin()
revenue_by_year.pct_change().order()

# Total Number of Subscribers per year
data['Subscription ID'].groupby(data['Year']).nunique()

# Total number of transactions per year
data['Subscription ID'].groupby(data['Year']).count()




