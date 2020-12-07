import pandas as pd
from utils import average_countries_to_continents
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Environment.read_co2 import read_co2_continent
from visualizations.world_map import create_world_bubble_map
from predictions.predictions import autoregressive_integrated_moving_average

def adaptDataForPCT(raw_data):
    '''this function performs the calculation of percentage change from the previous year
    :param raw_data: pandas.dataframe
    returns: pandas.dataframe
    columns should be years, rows continents'''
    assert(isinstance(raw_data, list))

    pct_data = []
    for data in raw_data:
        # pct change operates on cols, hence transposing
        data = data.T
        africa = data.iloc[0].pct_change()
        data = data.pct_change()
        data.iloc[0] = africa
        data = data.T
        pct_data.append(data)
    return pct_data

def filterDataFrameByYears(data_list, min_year, max_year):
    '''filters the given dataframes in data_list by parameters min_year and max_year. Columns should be years and rows continents
    :param data_list: list of pandas.dataframe
    :param min_year: int
    :param max_year: int
    :returns list of pandas.dataframe
    '''
    assert(isinstance(data_list, list))
    assert(isinstance(min_year, int))
    assert(isinstance(max_year, int))

    filtered_data = []
    for data in data_list:
        data_df = pd.read_csv(data, index_col=0)
        avg_df = average_countries_to_continents(data_df)
        columns_to_drop = []
        for column in avg_df.columns:
            if int(column) < min_year or int(column) > max_year:
                columns_to_drop.append(column)

        avg_df = avg_df.drop(columns=columns_to_drop)
        filtered_data.append(avg_df)
    return filtered_data

def prepareHealthDataFramesForPrediction(data_list_health, min_year, max_year):
    '''prepares the given health dataframes for prediction and filters by given years
    :param data_list_health: list of pandas.dataframe
    :param min_year: int
    :param max_year: int
    :returns pandas.dataframe'''
    assert (isinstance(data_list_health, list))
    assert (isinstance(min_year, int))
    assert (isinstance(max_year, int))

    health_data = filterDataFrameByYears(data_list_health, min_year, max_year)

    health_data = adaptDataForPCT(health_data)
    health_data[1] = - (health_data[1]) # inverse when the higher the better
    avg_health_df = pd.concat([health_data[0], health_data[1]], axis=1).groupby(axis=1, level=0).mean()
    return avg_health_df

def prepareEconomyDataForPrediction(data_list_economy, min_year, max_year):
    '''prepares the given economy dataframes for prediction and filters by given years
    :param data_list_economy: list of pandas.dataframe
    :param min_year: int
    :param max_year: int
    :returns pandas.dataframe'''
    assert (isinstance(data_list_economy, list))
    assert (isinstance(min_year, int))
    assert (isinstance(max_year, int))
    econ_data = filterDataFrameByYears(data_list_economy, min_year, max_year)
    econ_data = adaptDataForPCT(econ_data)
    econ_data[1] = - econ_data[1]  # inverse when the higher the better
    avg_economy_df = pd.concat([econ_data[0], econ_data[1]], axis=1).groupby(axis=1, level=0).mean()
    return avg_economy_df

def loadAndPrepareEnvironmentDataForPrediction(min_year, max_year):
    '''loads co2 and methane data with the environment load data function and prepares it for prediction
    :param min_year: int
    :param max_year: int
    :return: pandas.dataframe
    '''
    assert (isinstance(min_year, int))
    assert (isinstance(max_year, int))
    environment_data = []
    # we are interested in the co2 and methane emissions
    for column in ['co2', 'methane']:
        environment_co2 = read_co2_continent(year_start=min_year, year_end=max_year,
                                             usecols=['country', 'year', 'co2', 'methane'])
        #group by continents
        data_grouped_by_entity = environment_co2.groupby('area')
        co2_groups = [data_grouped_by_entity.get_group(x) for x in data_grouped_by_entity.groups]
        co2_group = co2_groups[0]
        cleaned_co2_df = co2_group[['year', column]]
        cleaned_co2_df = cleaned_co2_df.set_index('year')
        cleaned_co2_df.columns = [co2_group['area'].iloc[0]]

        for i in range(1, len(co2_groups)):
            co2_group = co2_groups[i]
            co2_column = co2_group[['year', 'co2']]
            co2_column = co2_column.set_index('year')
            co2_column.columns = [co2_group['area'].iloc[0]]
            cleaned_co2_df = cleaned_co2_df.join(co2_column)
        cleaned_co2_df = cleaned_co2_df.T[:-1]
        cleaned_co2_df.columns = cleaned_co2_df.columns.map(str)
        cleaned_co2_df = - cleaned_co2_df
        environment_data.append(cleaned_co2_df)

    environment_data = adaptDataForPCT(environment_data)
    avg_env_df = pd.concat([environment_data[0], environment_data[1]], axis=1).groupby(axis=1, level=0).mean()
    return avg_env_df


def run():
    '''general run function to generate the plots for our presentation for the overall world plot
    the method uses different indicators for the three categories health, economy and environment,
    filters the data and prepares for predictions and plotting'''

    data_list_health = ['./data/health/cleaned_data/cleaned_Life expectancy at birth.csv',
                    './data/health/cleaned_data/cleaned_Mortality rate, infant (per 1,000 live births).csv']
    data_list_economy = ['./data/economy/cleaned_data/cleaned_GDP.csv',
                     './data/economy/cleaned_data/cleaned_Unemployment, total (% of labour force).csv']

    min_year = 1991
    max_year = 2016

    avg_health_df = prepareHealthDataFramesForPrediction(data_list_health, min_year, max_year)
    avg_economy_df = prepareEconomyDataForPrediction(data_list_economy, min_year, max_year)
    avg_env_df = loadAndPrepareEnvironmentDataForPrediction(min_year, max_year)

    # only use data from the same years for all categories and drop first year
    common_cols =  avg_health_df.columns & avg_economy_df.columns & avg_env_df.columns
    avg_env_df = avg_env_df[common_cols]
    avg_health_df = avg_health_df[common_cols]
    avg_economy_df = avg_economy_df[common_cols]

    categories_dfs = [avg_env_df, avg_health_df, avg_economy_df]

    # predict for all categories
    for i, df in enumerate(categories_dfs):
        df = df.drop(columns='1991')
        data, predictions = autoregressive_integrated_moving_average(df.T, 14, seasonal_order = (1, 1, 0, 1))
        data = data.set_index('Year')
        predictions = predictions.set_index('Year')
        avg_env_df = pd.concat([data.T,predictions[8:].T], axis=1) # remove the overlap
        categories_dfs[i] = avg_env_df

    create_world_bubble_map(categories_dfs[0],categories_dfs[1], categories_dfs[2], 'presentation_images/')


if __name__ == "__main__":
    run()