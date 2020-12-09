import pandas as pd
from src.predictions.predictions import autoregressive_integrated_moving_average
from src.visualizations.graphs import plot_prediction_line_graph, average_countries_to_continents


def run():
    data_health = './data/health/cleaned_data/cleaned_'
    data_list = ['Adolescent birth rate (births per 1,000 women ages 15-19).csv',
                'Life expectancy at birth.csv',
                'Maternal mortality ratio (deaths per 100,000 live births).csv',
                'Mortality rate, infant (per 1,000 live births).csv',
                'Mortality rate, under-five (per 1,000 live births).csv',
                'Proportion of births attended by skilled health personnel (%).csv',
                'Share of seats in parliament (% held by women).csv',
                'world_happiness.csv'
                ]
    step = [10, 10, 10, 10, 10, 10, 10, 2]
    y_label_name = ['births per 1,000 women ages 15-19', 'year', 'deaths per 100,000 live births', 'per 1,000 live births', 'per 1,000 live births', '%', '% held by women', 'Happiness index']
    title_name = ['Adolescent Birth Rate', 'Life Expectancy at Birth', 'Maternal Mortality Ratio', 'Mortality Rate, infant', 'Mortality Rate, under-five', 'Proportion of Births Sttended by Skilled Health Personnel', 'Share of Seats in Parliament', 'World Happiness']
    
    for d, s, y, t in zip(data_list, step, y_label_name, title_name):
        df = pd.read_csv(data_health + d, index_col=0)
        df = average_countries_to_continents(df)
        df.to_csv( './data/health/cleaned_data/continent/' + d[:-4] + '_continent.csv')
        
        data, pred_df = autoregressive_integrated_moving_average(df.T, steps = s)
        fname = d[:-4] + '.png'
        plot_prediction_line_graph(data, pred_df, 'Year', y, t+' per Continent', fname)

if __name__ == "__main__":
    run()
