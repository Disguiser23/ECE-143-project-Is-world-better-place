import pandas as pd
import numpy as np


def read_co2_continent(year_start = 1900, year_end = 2018):
    '''
    This function reads the amounts of CO2 emission of the world and each
    continents from 1900 to 2018. The data was rearranged. with years as 
    index and types of disaster as colums
    :param year_start: The start year
    :type year_start: int
    :param year_end: The end year
    :type year_end: int
    :returns: pd.Dataframe
    '''
    assert isinstance(year_start, int)
    assert isinstance(year_end, int)
    assert 1900 <= year_start < year_end
    assert year_end <= 2018

    origin_data = pd.read_csv('./data/owid-co2-data.csv', usecols=[1, 2, 3])
    continents = [
        'World', 'Africa', 'Asia', 'Europe', 'Oceania', 'North America',
        'South America'
    ]

    origin_data = origin_data.drop(
        origin_data[origin_data['year'] < year_start].index)
    origin_data = origin_data.drop(
        origin_data[~origin_data['country'].isin(continents)].index)

    years = list(range(year_start, year_end + 1))
    temp = np.zeros([len(years), len(continents)])
    output_df = pd.DataFrame(temp,
                             columns=continents,
                             index=years,
                             dtype=float)

    for _, row in origin_data.iterrows():
        output_df[row['country']][row['year']] = row['co2']

    return output_df


def read_co2_trans():
    '''
    This function reads the amounts of CO2 emission of international.
    The data was rearranged with year as index
    :returns: pd.Dataframe
    '''
    origin_data = pd.read_csv('./data/owid-co2-data.csv', usecols=[1, 2, 3])
    origin_data = origin_data.drop(
        origin_data[~origin_data['country'].str.
                    contains('International transport')].index)
    origin_data = origin_data.drop(origin_data[origin_data['co2'] == 0].index)
    origin_data = origin_data.drop(labels='country', axis=1)
    origin_data = origin_data.set_index('year')

    return origin_data


def read_co2_country(year_start = 1990, year_end = 2018):
    '''
    This function reads the amounts of CO2 emission of each country.
    The data was rearranged with year as index and countries as columns.
    :param year_start: The start year
    :type year_start: int
    :param year_end: The end year
    :type year_end: int
    :returns: pd.Dataframe
    '''

    assert isinstance(year_start, int)
    assert isinstance(year_end, int)
    assert 1900 <= year_start < year_end
    assert year_end <= 2018

    origin_data = pd.read_csv('./data/owid-co2-data.csv', usecols=[0, 1, 2, 3])
    origin_data = origin_data.drop(
        origin_data[origin_data['year'] < year_start].index)
    origin_data = origin_data.drop(
        origin_data[origin_data['iso_code'].isin([np.nan, 'OWID_WRL'])].index)
    
    countries = origin_data['country'].drop_duplicates().values
    years = list(range(year_start, year_end + 1))

    temp = np.zeros([len(years), len(countries)])
    output_df = pd.DataFrame(temp,
                             columns=countries,
                             index=years,
                             dtype=int)

    temp = np.zeros([len(years), len(countries)])
    output_df = pd.DataFrame(temp,
                            columns=countries,
                            index=years,
                            dtype=float)

    for _, row in origin_data.iterrows():
        output_df[row['country']][row['year']] = row['co2']

    return output_df
