import pandas as pd
import numpy as np


def read_natural_disaster():
    '''
    This function read number-of-natural-disaster.cvs and rearrange
    the data into a dataframe with years as index and types of disaster
    as colums
    :returns: pd.Dataframe
    '''

    origin_data = pd.read_csv('./data/number-of-natural-disaster-events.csv')
    disaster_types = origin_data['Entity'].drop_duplicates().values
    years = list(range(1900, 2020))

    temp = np.zeros([len(years), len(disaster_types)])
    output_df = pd.DataFrame(temp,
                             columns=disaster_types,
                             index=years,
                             dtype=int)

    for _, row in origin_data.iterrows():
        output_df[row['Entity']][
            row['Year']] = row['Number of disasters (EMDAT (2020))']

    return output_df