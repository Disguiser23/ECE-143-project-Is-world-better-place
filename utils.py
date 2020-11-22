import pandas as pd

def average_countries_to_continents(dataframe):
    '''this method transforms the values from the specific countries into an average for the continent
    input: pandas dataframe with countries as index, columns are years
    returns: pandas dataframe with continents as index'''
    assert(isinstance(dataframe, pd.DataFrame))
    countries_continents = pd.read_csv('./data/countries_continents/Countries-Continents.csv', index_col=1)
    countries_continents_index =  list(map(lambda x: x.lower(), list(countries_continents.index)))
    countries_continents.index = countries_continents_index
    dataframe_idx = list(map(lambda x: x.lower(), list(dataframe.index)))
    dataframe.index = dataframe_idx
    res = dataframe.join(countries_continents)
    res = res.groupby('Continent').mean()
    return res


if __name__ == "__main__":
    gdp_df = pd.read_csv('./data/economy/cleaned_data/cleanedGDP.csv', index_col=0)
    gdp_df_continents = average_countries_to_continents(gdp_df)
    print(gdp_df_continents)