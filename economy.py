import utils
import pandas as pd
from predictions.predictions import autoregressive_integrated_moving_average
from visualizations.graphs import plot_prediction_line_graph, stacked_bar_graph_prediction


def run():
    #csv = pd.read_csv('./data/economy/cleaned_data/avg_gdp_continents.csv',
    #                  index_col=0)
    #data, pred_df = autoregressive_integrated_moving_average(
    #    csv.T, steps=20, seasonal_order=(1, 1, 0, 12))
    #plot_prediction_line_graph(
    #    data, pred_df, 'Year', 'GDP (Billion US$)',
    #    'GDP Predictions per Continent')  #, 'predictions.png'

    # csv = pd.read_csv('./data/environmental/cleaned_data/cleaned_number-of-natural-disaster-events.csv', index_col=0)
    # csv = csv.reset_index()
    # csv = csv.drop(columns=['decade'])
    # csv = csv.drop(columns=['All natural disasters'])
    # number_of_predictions = 3
    # data, pred_df = autoregressive_integrated_moving_average(csv, steps = number_of_predictions)
    # data = data.set_index('Year')
    # pred_df = pred_df.set_index('Year')
    # all_data = data.append(pred_df.tail(number_of_predictions))
    # years_labels = ['1900-1910', '1910-1920', '1920-1930', '1930-1940', '1940-1950', '1950-1960', '1960-1970', '1970-1980', '1980-1990', '1990-2000', '2000-2010', '2010-2020', '2020-2030', '2030-2040', '2040-2050']
    # all_data['labels'] = years_labels
    # all_data = all_data.set_index('labels')
    # stacked_bar_graph_prediction(all_data, filename="stacked_bar_graph_disasters.png", title="Natural Disasters from 1900-2020", ylabel="Number of Incidents")


    data_economy = './data/economy/cleaned_data/cleaned_'
    data_list = ['GDP.csv',
                'annual_work_hrs.csv',
                'Employment to population ratio (% ages 15 and older).csv',
                'Labour force participation rate (% ages 15 and older).csv',
                'Unemployment, total (% of labour force).csv'
                ]
    step = [15, 15, 15, 15, 15]
    y_label_name = ['United States dollars', 'hrs', '% ages 15 and older', '% ages 15 and older', '% of labour force']
    title_name = ['GDP', 'Annual Work Hours', 'Employment to Population Ratio', 'Labour Force Participation Rate', 'Unemployment']
    for d, s, y, t in zip(data_list, step, y_label_name, title_name):
        df = pd.read_csv(data_economy + d, index_col=0)
        csv = utils.average_countries_to_continents(df)
        
        data, pred_df = autoregressive_integrated_moving_average(csv.T, steps = s)
        plot_prediction_line_graph(data, pred_df, 'Year', y, t + ' per continent', d[:-4]+'.png')
        
if __name__ == "__main__":
    run()


# def run():
#     csv = pd.read_csv('./data/economy/cleaned_data/avg_gdp_continents.csv', index_col=0)
#     data, pred_df = autoregressive_integrated_moving_average(csv.T, steps = 20, seasonal_order=(1, 1, 0, 12))
#     plot_prediction_line_graph(data, pred_df, 'Year', 'GDP (Billion US$)', 'GDP Predictions per Continent', 'predictions.png')
    
#     csv = pd.read_csv('./data/environmental/cleaned_data/cleaned_number-of-natural-disaster-events.csv', index_col=0)
#     csv = csv.reset_index()
#     csv = csv.drop(columns=['decade'])
#     csv = csv.drop(columns=['All natural disasters'])
#     number_of_predictions = 3
#     data, pred_df = autoregressive_integrated_moving_average(csv, steps = number_of_predictions)
#     data = data.set_index('Year')
#     pred_df = pred_df.set_index('Year')
#     all_data = data.append(pred_df.tail(number_of_predictions))
#     years_labels = ['1900-1910', '1910-1920', '1920-1930', '1930-1940', '1940-1950', '1950-1960', '1960-1970', '1970-1980', '1980-1990', '1990-2000', '2000-2010', '2010-2020', '2020-2030', '2030-2040', '2040-2050']
#     all_data['labels'] = years_labels
#     all_data = all_data.set_index('labels')
#     stacked_bar_graph_prediction(all_data, filename="stacked_bar_graph_disasters.png", title="Natural Disasters from 1900-2020", ylabel="Number of Incidents")

# if __name__ == "__main__":
#     run()
