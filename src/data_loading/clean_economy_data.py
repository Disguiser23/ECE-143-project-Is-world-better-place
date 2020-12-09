import pandas as pd
import numpy as np

# format 1 

# read csv as DataFrame data structure
df = pd.read_csv('../../data/economy/UNdata_GDP.csv')

# countries: an 1D np array of all the countries (str)
countries = df['Country or Area'].drop_duplicates().values

# years: an 1D np array of all the years (int)
years = np.flip(df['Year'].drop_duplicates().values)

# GDP: an 1D np array of GDP values (int) of each countries each year
GDP = df['Value'].values

# n_countries, n_years are the # of countries and years
n_co = countries.shape[0]
n_yr = years.shape[0]

# create a DataFrame with all values as nan
dummy = np.zeros([n_co, n_yr])
dummy = np.nan
gdp_df = pd.DataFrame(dummy, index = countries, columns=years)

# assigning the correct GDP values to the DF
for i in range(0, GDP.shape[0]):
    i_year = df['Year'].values[i]
    i_country = df['Country or Area'].values[i]
    gdp_df[i_year][i_country] = GDP[i]
    
#print(newdf.index)

gdp_df.to_csv('../../data/economy/cleaned_data/cleaned_GDP.csv', index = True)

# format 2
# read csv as DataFrame data structure
df = pd.read_csv('../../data/economy/annual-work-hours.csv')

# countries: an 1D np array of all the countries (str)
countries = df['Country'].drop_duplicates().values

# years: an 1D np array of all the years (int)
years = (df['Time'].drop_duplicates().values)

# GDP: an 1D np array of GDP values (int) of each countries each year
GDP = df['Value'].values

# n_countries, n_years are the # of countries and years
n_co = countries.shape[0]
n_yr = years.shape[0]

# create a DataFrame with all values as nan
dummy = np.zeros([n_co, n_yr])
dummy = np.nan
workhrs_df = pd.DataFrame(dummy, index = countries, columns=years)

# assigning the correct GDP values to the DF
for i in range(0, GDP.shape[0]):
    i_year = df['Time'].values[i]
    i_country = df['Country'].values[i]
    workhrs_df[i_year][i_country] = GDP[i]
    
workhrs_df.to_csv('../../data/economy/cleaned_data/cleaned_annual_work_hrs.csv', index = True)

# format 3
data_economy = '../../data/economy/'
data_list = ['Employment to population ratio (% ages 15 and older).csv',
            'Labour force participation rate (% ages 15 and older).csv',
            'Unemployment, total (% of labour force).csv'
            ]
# country count in each list
country = [19, 19, 19]
for c, d in zip(country, data_list):
    df = pd.read_csv(data_economy + d,skiprows=1)

    df.drop(columns=['HDI Rank (2018)'], inplace = True)
    df.drop(df.columns[df.columns.str.contains('unnamed',case = False)],axis = 1, inplace = True)

    # Keep only the country data
    df.drop(df.tail(c).index,inplace=True)
    df.replace('..', np.nan,inplace=True)

    df.set_index("Country", inplace = True)
    df.astype('float64').dtypes
    df = df.apply(pd.to_numeric, errors='ignore')
    
    # intepolate the data (missing data for some years)
    min_year = int(min(df.columns))
    max_year = int(max(df.columns))

    df = df.reindex(columns=map(str, range(min_year, max_year)))
    df = df.interpolate(method='linear', limit_direction='both', axis=1)
    df.to_csv('../../data/economy/cleaned_data/'+ 'cleaned_' + d, index=True)
    

