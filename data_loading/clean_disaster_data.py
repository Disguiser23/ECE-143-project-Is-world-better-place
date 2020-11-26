import pandas as pd

if __name__ == "__main__":

    disaster_csv = pd.read_csv('./data/environmental/number-of-natural-disaster-events.csv')
    disaster_csv = disaster_csv.rename({'n': 'Number of disasters (EMDAT (2020))'})
    print(disaster_csv)
    disaster_grouped_by_entity = disaster_csv.groupby('Entity')
    disaster_groups = [disaster_grouped_by_entity.get_group(x) for x in disaster_grouped_by_entity.groups]

    years = [1900, 1910, 1920, 1930, 1940, 1950, 1960, 1970, 1980, 1990, 2000, 2010, 2020]
    years_labels = ['1900-1910', '1910-1920', '1920-1930', '1930-1940', '1940-1950', '1950-1960', '1960-1970', '1970-1980', '1980-1990', '1990-2000', '2000-2010', '2010-2020']
    disaster_group = disaster_groups[0]

    cleaned_disaster_df = pd.DataFrame()
    cleaned_disaster_df = disaster_group[['Year', 'Number of disasters (EMDAT (2020))']]
    cleaned_disaster_df = cleaned_disaster_df.set_index('Year')
    print(cleaned_disaster_df)
    cleaned_disaster_df.columns = [disaster_group['Entity'].iloc[0]]
    cleaned_disaster_df.to_csv('./data/environmental/cleaned_data/clean_all_natural_disasters.csv')
    new_col_gro = pd.cut(x=cleaned_disaster_df.index, bins=years, labels=years_labels)
    cleaned_disaster_df['decade'] = new_col_gro
    cleaned_disaster_df = cleaned_disaster_df.groupby('decade').sum()

    for i in range(1,len(disaster_groups)):
        disaster_group = disaster_groups[i]
        disaster_column = disaster_group[['Year', 'Number of disasters (EMDAT (2020))']]
        disaster_column = disaster_column.set_index('Year')
        disaster_column.columns = [disaster_group['Entity'].iloc[0]]
        print(disaster_group)
        disaster_column_grouped = pd.cut(x=disaster_column.index, bins=years, labels=years_labels)
        disaster_column['decade'] = disaster_column_grouped
        disaster_column = disaster_column.groupby('decade').sum()
        cleaned_disaster_df = cleaned_disaster_df.join(disaster_column)
    cleaned_disaster_df = cleaned_disaster_df.drop(columns=["Impact"])
    print(cleaned_disaster_df)
    cleaned_disaster_df.to_csv('./data/environmental/cleaned_data/cleaned_number-of-natural-disaster-events.csv')