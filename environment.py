import utils
import pandas as pd
import plotly.express as px
import Environment  #.read_co2
#import Environment.envi_merge
from predictions.predictions import autoregressive_integrated_moving_average
from visualizations.graphs import plot_prediction_line_graph, stacked_bar_graph_prediction


def plot_natural_disaster_prediction(file_name=None):
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
    all_data['Decade'] = years_labels
    all_data = all_data.set_index('Decade')
    stacked_bar_graph_prediction(
        all_data,
        filename=file_name,
        title="Number of Natural Disasters (1900-2020) and Predictions (2030-2050)",
        ylabel="Number of Incidents",
    )


def plot_predict_co2_continent(year_start=1900, year_end=2018, file_name=None):
    '''
    This function call plot_prediction_line_graph to draw the line graph
    '''
    df, df_pre = Environment.read_co2.get_predict_co2_continent(
        year_start, year_end)
    plot_prediction_line_graph(
        df, df_pre, 'Year', 'CO${_2}$',
        'CO${_2}$ of Each Continent and the World with Prediction', file_name)


def plot_co2_world_map(year_start=1990, year_end=2018):
    '''

    '''
    fig = Environment.read_co2.fig_map_co2_country(year_start, year_end)
    fig.show()


def plot_predict_co2_continent_person(year_start=1950,
                                      year_end=2018,
                                      file_name=None):
    '''
    This function call plot_prediction_line_graph to draw the line graph
    '''
    df, df_pre = Environment.envi_merge.get_predict_co2_continent_person(
        year_start, year_end)
    plot_prediction_line_graph(
        df, df_pre, 'Year', 'Annual CO${_2}$ Emission, Kg',
        'CO${_2}$ of Each Continent and the World Per Person with Prediction',
        file_name)


def plot_world_co2_disaster(year_start=1900, year_end=2018):
    '''

    '''
    fig = Environment.envi_merge.fig_world_co2_disaster(year_start, year_end)
    fig.show()


if __name__ == "__main__":
    plot_natural_disaster_prediction(file_name='presentation_images/filename="stacked_bar_graph_disasters.png')

    plot_predict_co2_continent(year_start=1950,
                               year_end=2018,
                               file_name='presentation_images/co2-continent-prediction.png')

    plot_predict_co2_continent_person(year_start=1950,
                                      year_end=2018,
                                      file_name='presentation_images/co2-personal-prediction.png')

