import pandas as pd
import numpy as np
import plotly.express as px

import os, sys
sys.path.append('../')
#sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from read_co2 import read_co2_continent
from read_disaster import read_natural_disaster
from predictions.predictions import autoregressive_integrated_moving_average
from visualizations.graphs import plot_prediction_line_graph, stacked_bar_graph_prediction
from utils import colors_pastel

curr_path = os.path.split(os.path.realpath(__file__))[0]
curr_path += '/data/'


def get_predict_co2_continent_person(year_start=1950, year_end=2018):
    '''
    Annual co2 emission per person, kg, with prediction
    '''
    assert isinstance(year_start, int)
    assert isinstance(year_end, int)
    assert year_start >= 1950 and year_end <= 2018

    df_pop = pd.read_csv(curr_path + 'world-population-by-continent.csv')
    df_pop = df_pop.drop(df_pop[df_pop['Year'] < year_start].index)
    df_pop = df_pop.drop(df_pop[df_pop['Year'] > year_end].index)
    df_pop.set_index('Year', inplace=True)

    df_origin = read_co2_continent(year_start, year_end)
    area = [
        'World', 'Africa', 'Asia', 'Europe', 'Oceania', 'North America',
        'South America'
    ]
    year = list(range(year_start, year_end + 1))
    temp = np.zeros([len(year), len(area)])
    df_emi = pd.DataFrame(temp, columns=area, index=year, dtype=float)

    for _, row in df_origin.iterrows():
        df_emi[row['area']][row['year']] = row['co2']

    df_emi.index.name = 'Year'

    df_avg = df_emi.div(df_pop, axis=0) * 1e6

    _, df_pre = autoregressive_integrated_moving_average(df_avg,
                                                         steps=20,
                                                         seasonal_order=None)
    df_pre = df_pre.drop(labels='Year', axis=1)

    return df_avg, df_pre


def plot_predict_co2_continent_person(year_start=1950,
                                      year_end=2018,
                                      file_name=None):
    '''
    This function call plot_prediction_line_graph to draw the line graph
    '''
    df, df_pre = get_predict_co2_continent_person(year_start, year_end)
    plot_prediction_line_graph(
        df, df_pre, 'Year', 'Annual CO${_2}$ Emission, Kg',
        'CO${_2}$ of Each Continent and the World Per Person with Prediction',
        file_name)

def get_world_co2_disaster(year_start=1900, year_end=2018):
    '''

    '''
    df_emi = read_co2_continent(year_start, year_end)
    df_emi = df_emi.drop(df_emi[
        ~df_emi['area'].str.contains('World')].index)
    df_emi.drop(labels = 'area', axis = 1, inplace = True)
    df_emi = df_emi.drop(df_emi[df_emi['year'] < year_start].index)
    df_emi = df_emi.drop(df_emi[df_emi['year'] > year_end].index)
    df_emi.set_index('year', inplace = True)
    df_emi['disaster'] = 0

    df_disaster = read_natural_disaster()
    df_disaster = df_disaster.drop(df_disaster[df_disaster['Year'] < year_start].index)
    df_disaster = df_disaster.drop(df_disaster[df_disaster['Year'] > year_end].index)
    concern_list = ['Drought', 'Extreme temperature', 'Extreme weather', 'Flood', 'Landslide', 'Wildfire']
    for _, row in df_disaster.iterrows():
        if row['Type'] in concern_list:
            df_emi['disaster'][row['Year']] += row['Number of disasters (EMDAT (2020))']

    return df_emi

def fig_world_co2_disaster(year_start=1900, year_end=2018):
    '''

    '''
    df = get_world_co2_disaster(year_start, year_end)
    df.reset_index(inplace = True)
    fig = px.scatter(df, x="co2", y="disaster", hover_name="year")

    fig.update_layout(
        title= 'The amount of CO<sub>2</sub> Emission VS Number of Natural Disasters<br>Related to Global Warming',
        xaxis_title= 'Annual CO<sub>2</sub> Emission, Million Tonnes per Year',
        yaxis_title= 'Number of Natural Disasters')

    return fig