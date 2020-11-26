import utils
import pandas as pd
from predictions.predictions import autoregressive_integrated_moving_average
from visualizations.graphs import plot_prediction_line_graph, stacked_bar_graph_prediction


def run():
    #     csv = pd.read_csv('./data/economy/cleaned_data/avg_gdp_continents.csv', index_col=0)
    #     data, pred_df = autoregressive_integrated_moving_average(csv.T, steps = 20, seasonal_order=(1, 1, 0, 12))
    #     plot_prediction_line_graph(data, pred_df, 'Year', 'GDP (Billion US$)', 'GDP Predictions per Continent', 'predictions.png')

    csv = pd.read_csv(
        './data/environmental/cleaned_data/cleaned_number-of-natural-disaster-events.csv',
        index_col=0)
    csv = csv.reset_index()
    csv = csv.drop(columns=['decade'])
    csv = csv.drop(columns=['All natural disasters'])
    number_of_predictions = 3
    data, pred_df = autoregressive_integrated_moving_average(
        csv, steps=number_of_predictions)
    data = data.set_index('Year')
    pred_df = pred_df.set_index('Year')
    all_data = data.append(pred_df.tail(number_of_predictions))
    years_labels = [
        '1900-1910', '1910-1920', '1920-1930', '1930-1940', '1940-1950',
        '1950-1960', '1960-1970', '1970-1980', '1980-1990', '1990-2000',
        '2000-2010', '2010-2020', '2020-2030', '2030-2040', '2040-2050'
    ]
    all_data['labels'] = years_labels
    all_data = all_data.set_index('labels')
    stacked_bar_graph_prediction(all_data,
                                 filename=None,
                                 title="Natural Disasters from 1900-2020",
                                 ylabel="Number of Incidents"
                                 )  #filename="stacked_bar_graph_disasters.png"
