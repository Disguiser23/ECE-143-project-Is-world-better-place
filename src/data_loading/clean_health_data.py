import pandas as pd
import numpy as np
import csv

# format 1
data_health = '../../data/health'
data_list = ['/Adolescent birth rate (births per 1,000 women ages 15-19).csv',
            '/Life expectancy at birth.csv',
            '/Maternal mortality ratio (deaths per 100,000 live births).csv',
            '/Mortality rate, infant (per 1,000 live births).csv',
            '/Mortality rate, under-five (per 1,000 live births).csv',
            '/Proportion of births attended by skilled health personnel (%).csv',
            '/Share of seats in parliament (% held by women).csv']
# data_list = ['/Adolescent birth rate (births per 1,000 women ages 15-19).csv']
# country count in each list
country = [20, 19, 19, 18, 18, 18, 24]
output = dict()
for c, d in zip(country, data_list):
    df = pd.read_csv(data_health + d,skiprows=1)

    df.drop(columns=['HDI Rank (2018)'], inplace = True)
    df.drop(df.columns[df.columns.str.contains('unnamed',case = False)],axis = 1, inplace = True)

    # Keep only the country data
    df.drop(df.tail(c).index,inplace=True)
    df.replace('..', np.nan,inplace=True)
    
    df.set_index("Country", inplace = True)
    df.astype('float64').dtypes
    df = df.apply(pd.to_numeric, errors='ignore')

    min_year = int(min(df.columns))
    max_year = int(max(df.columns))

    df = df.reindex(columns=map(str, range(min_year, max_year)))
    df = df.interpolate(method='linear', limit_direction='both', axis=1)
    
    output[d] = df
    df.to_csv(data_health +'/cleaned_data/cleaned_'+ d[1:])

# format 2
df = pd.read_csv(data_health + '/seats_held_by_women_in_parliaments.csv')

cols = [0, 1] + list(range(3,41))
df.drop(df.columns[cols],axis=1,inplace=True)
df.drop(df.tail(5).index,inplace=True)
df.set_index("Country Name", inplace = True)
df.rename(columns=lambda s: s[:4], inplace = True)
df.replace('..', np.nan,inplace=True)
df.astype('float64').dtypes
df = df.apply(pd.to_numeric, errors='ignore')

# Merge 'seats_held_by_women_in_parliaments.csv' and 'Share of seats in parliament (% held by women).csv'
merge = pd.concat([output['/Share of seats in parliament (% held by women).csv'], df], sort=False)
output['/Share of seats in parliament (% held by women).csv'] = merge.groupby(merge.index).mean()
output['/Share of seats in parliament (% held by women).csv'].to_csv(data_health +'/cleaned_data/cleaned_Share of seats in parliament (% held by women).csv')

# format 3
year = list(range(2015,2020))
country_str = ['Country', 'Country', 'Country', 'Country or region', 'Country or region']
score_str = ['Happiness Score', 'Happiness Score','Happiness.Score','Score','Score']

for y, c, s in zip(year, country_str, score_str):
    df = pd.read_csv(data_health + '/World_Happiness_Report'+str(y)+'.csv')
    if y == 2015:
        tmp = pd.DataFrame(data = df[s])
        tmp.set_index(df[c], inplace=True)
        tmp = tmp.rename(index={'Somaliland region': 'Somaliland Region'})
    else:
        tmp2 = pd.DataFrame(data = df[s])
        tmp2.set_index(df[c], inplace=True)
        tmp2 = tmp2.rename(index={'Hong Kong S.A.R., China': 'Hong Kong','Taiwan Province of China':'Taiwan','Trinidad & Tobago':'Trinidad and Tobago'})
        tmp = pd.concat([tmp, tmp2], axis = 1, sort=True)

tmp.columns = year
output['world_happiness'] = tmp
tmp.to_csv(data_health + '/cleaned_data/cleaned_world_happiness.csv')


