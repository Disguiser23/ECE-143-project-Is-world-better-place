import utils
import pandas as pd
from predictions.predictions import autoregressive_integrated_moving_average
from visualizations.graphs import plot_prediction_line_graph, stacked_bar_graph_prediction


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
    for d in data_list:
        df = pd.read_csv(data_health + d, index_col=0)
        csv = utils.average_countries_to_continents(df)
        
        data, pred_df = autoregressive_integrated_moving_average(csv.T, steps = 20)
        plot_prediction_line_graph(data, pred_df, 'Year', d, 'per Continent')
        
#    csv = pd.read_csv('./data/environmental/cleaned_data/cleaned_number-of-natural-disaster-events.csv', index_col=0)
#    csv = csv.reset_index()
#    csv = csv.drop(columns=['decade'])
#    csv = csv.drop(columns=['All natural disasters'])
#    number_of_predictions = 3
#    data, pred_df = autoregressive_integrated_moving_average(csv, steps = number_of_predictions)
#    data = data.set_index('Year')
#    pred_df = pred_df.set_index('Year')
#    all_data = data.append(pred_df.tail(number_of_predictions))
#    years_labels = ['1900-1910', '1910-1920', '1920-1930', '1930-1940', '1940-1950', '1950-1960', '1960-1970', '1970-1980', '1980-1990', '1990-2000', '2000-2010', '2010-2020', '2020-2030', '2030-2040', '2040-2050']
#    all_data['labels'] = years_labels
#    all_data = all_data.set_index('labels')
#    stacked_bar_graph_prediction(all_data, filename="stacked_bar_graph_disasters.png", title="Natural Disasters from 1900-2020", ylabel="Number of Incidents")
if __name__ == "__main__":
    run()
