import pandas as pd
from utils import average_countries_to_continents
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Environment.read_co2 import read_co2_continent
from visualizations.world_map import create_world_bubble_map

def run():
    data_list_health = ['./data/health/cleaned_data/cleaned_Life expectancy at birth.csv',
                    './data/health/cleaned_data/cleaned_Mortality rate, infant (per 1,000 live births).csv']
    data_list_economy = ['./data/economy/cleaned_data/cleanedGDP.csv',
                     './data/economy/cleaned_data/cleaned_Unemployment, total (% of labour force).csv']

    min_year = 1991
    max_year = 2016
    health_data = []
    for data in data_list_health:
        #cluster to continents
        health_df = pd.read_csv(data, index_col=0)
        avg_health_df_new = average_countries_to_continents(health_df)
        columns_to_drop = []
        for column in avg_health_df_new.columns:
            if int(column) < min_year or int(column) > max_year:
                columns_to_drop.append(column)
        avg_health_df = avg_health_df_new.drop(columns=columns_to_drop)
        health_data.append(avg_health_df)
    health_data[0] = 1- (health_data[0] - health_data[0].mean()) / health_data[0].std() # inversely normalize when the higher the better
    health_data[1] = ( health_data[1] -  health_data[1].mean()) /  health_data[1].std()

    avg_health_df = pd.concat([health_data[0], health_data[1]], axis=1).groupby(axis=1, level=0).mean()


    econ_data = []
    for data in data_list_economy:
        economy_df = pd.read_csv(data, index_col=0)
        avg_economy_df_new = average_countries_to_continents(economy_df)
        columns_to_drop = []
        for column in avg_economy_df_new.columns:
            if int(column) < min_year or int(column) > max_year:
                columns_to_drop.append(column)

        avg_economy_df_new = (avg_economy_df_new - avg_economy_df_new.mean()) / avg_economy_df_new.std()
        avg_economy_df = avg_economy_df_new.drop(columns=columns_to_drop)
        econ_data.append(avg_economy_df)

    econ_data[0] = 1 - (econ_data[0] - econ_data[0].mean()) / econ_data[
        0].std()  # inversely normalize when the higher the better
    econ_data[1] = (econ_data[1] - econ_data[1].mean()) / econ_data[1].std()
    avg_economy_df = pd.concat([econ_data[0], econ_data[1]], axis=1).groupby(axis=1, level=0).mean()

    # read environment data TODO add primary_energy_consumption

    environment_data = []
    for column in ['co2', 'methane']:
        environment_co2 = read_co2_continent(year_start=1990, year_end=2016, usecols=['country', 'year','co2','methane'])
        data_grouped_by_entity = environment_co2.groupby('area')
        co2_groups = [data_grouped_by_entity.get_group(x) for x in data_grouped_by_entity.groups]
        co2_group = co2_groups[0]
        cleaned_co2_df = co2_group[['year', column]]
        cleaned_co2_df = cleaned_co2_df.set_index('year')
        cleaned_co2_df.columns = [co2_group['area'].iloc[0]]

        for i in range(1,len(co2_groups)):
            co2_group = co2_groups[i]
            co2_column = co2_group[['year', 'co2']]
            co2_column = co2_column.set_index('year')
            co2_column.columns = [co2_group['area'].iloc[0]]
            cleaned_co2_df = cleaned_co2_df.join(co2_column)
        cleaned_co2_df = cleaned_co2_df.T[:-1]
        cleaned_co2_df.columns = cleaned_co2_df.columns.map(str)
        cleaned_co2_df = (cleaned_co2_df - cleaned_co2_df.mean()) / cleaned_co2_df.std()
        environment_data.append(cleaned_co2_df)

    avg_env_df = pd.concat([environment_data[0], environment_data[1]], axis=1).groupby(axis=1, level=0).mean()
    common_cols =  avg_health_df.columns & avg_economy_df.columns & avg_env_df.columns
    avg_env_df = avg_env_df[common_cols]
    avg_health_df = avg_health_df[common_cols]
    avg_economy_df = avg_economy_df[common_cols]
    create_world_bubble_map(avg_health_df, avg_env_df, avg_economy_df, 'world_overall.png')




if __name__ == "__main__":
    run()