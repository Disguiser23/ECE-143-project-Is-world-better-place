import pandas as pd
from utils import average_countries_to_continents
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Environment.read_co2 import read_co2_continent
from visualizations import world_map

def run():
    data_list_health = ['./data/health/cleaned_data/cleaned_Life expectancy at birth.csv',
                    './data/health/cleaned_data/cleaned_Mortality rate, infant (per 1,000 live births).csv']
    data_list_economy = ['./data/economy/cleaned_data/cleanedGDP.csv',
                     './data/economy/cleaned_data/cleaned_Unemployment, total (% of labour force).csv']

    min_year = 1991
    max_year = 2016
    for data in data_list_health:
        #cluster to continents
        health_df = pd.read_csv(data, index_col=0)
        avg_health_df = average_countries_to_continents(health_df)
        columns_to_drop = []
        for column in avg_health_df.columns:
            if int(column) < min_year or int(column) > max_year:
                columns_to_drop.append(column)
        avg_health_df = avg_health_df.drop(columns=columns_to_drop)
        print(data, avg_health_df)


    for data in data_list_economy:
        economy_df = pd.read_csv(data, index_col=0)
        avg_economy_df = average_countries_to_continents(economy_df)
        columns_to_drop = []
        for column in avg_economy_df.columns:
            if int(column) < min_year or int(column) > max_year:
                columns_to_drop.append(column)
        avg_economy_df = avg_economy_df.drop(columns=columns_to_drop)
        print(data, avg_economy_df.T)



    # read environment data TODO add primary_energy_consumption

    environment_co2 = read_co2_continent(year_start=1990, year_end=2016)
    data_grouped_by_entity = environment_co2.groupby('area')
    co2_groups = [data_grouped_by_entity.get_group(x) for x in data_grouped_by_entity.groups]
    co2_group = co2_groups[0]
    cleaned_co2_df = co2_group[['year', 'co2']]
    cleaned_co2_df = cleaned_co2_df.set_index('year')
    cleaned_co2_df.columns = [co2_group['area'].iloc[0]]

    for i in range(1,len(co2_groups)):
        co2_group = co2_groups[i]
        co2_column = co2_group[['year', 'co2']]
        co2_column = co2_column.set_index('year')
        co2_column.columns = [co2_group['area'].iloc[0]]
        cleaned_co2_df = cleaned_co2_df.join(co2_column)
    cleaned_co2_df = cleaned_co2_df.T[:-2]
    print(cleaned_co2_df)

    create_world_bubble_map(data, label, filename)
    '''input: data is a pandas dataframe with a column 'data' and 'Continent


if __name__ == "__main__":
run()