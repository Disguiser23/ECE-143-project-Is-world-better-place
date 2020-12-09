import pandas as pd
import statsmodels.api as sm
import os, sys
import warnings
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.visualizations.graphs import plot_prediction_line_graph, stacked_bar_graph_prediction, average_countries_to_continents

def autoregressive_integrated_moving_average(data, steps=20, seasonal_order = None):
    '''this method plots predictions for a dataframe with years as columns and countries or continents as rows
    :param data: pandas.dataframe
    :param steps: int with default 20
    :param seasonal_order: Tuple with 4 elements
    returns dataframe with predictions'''
    assert(isinstance(steps, int))
    if seasonal_order:
        assert(isinstance(seasonal_order, tuple))
    assert (isinstance(data, pd.DataFrame))
    warnings.filterwarnings("ignore")
    preds = []
    data.index.name = 'Year'
    start_year = int(min(list(data.index)))
    for column_name in data:
        if seasonal_order != None:
            mod = sm.tsa.statespace.SARIMAX(data[column_name], order=(1, 1, 1), seasonal_order=seasonal_order, enforce_stationarity=False, enforce_invertibility=False)
        else:
            mod = sm.tsa.statespace.SARIMAX(data[column_name], order=(1, 1, 1), enforce_stationarity=False, enforce_invertibility=False)
        results = mod.fit()
        start = int(len(data)/4) * 3 #start predicting after 3/4 of the data
        pred = results.get_prediction(start=start, dynamic=False)
        forecast = results.get_forecast(steps=steps).predicted_mean
        pred = pred.predicted_mean.append(forecast)

        #format predictions for plotting
        predicted_mean_df = pd.DataFrame(pred)
        predicted_mean_df = predicted_mean_df.reset_index()
        predicted_mean_df.columns = ['Year', column_name]
        predicted_mean_df['Year'] = predicted_mean_df['Year'].apply(lambda x: str(x).split('-')[0])
        predicted_mean_df = predicted_mean_df.set_index('Year')
        preds.append(predicted_mean_df)

    #clean predictions to be able to plot them correctly
    pred_df = preds[0]
    for i in range(1, len(preds)):
        pred_df = pred_df.join(preds[i])
    data= data.reset_index()
    data.index = data.index + start_year
    pred_df = pred_df.reset_index()
    pred_df.index = pred_df.index + start_year + start
    return data, pred_df


if __name__ == "__main__":
    # test the function on our data
    csv = pd.read_csv('../data/economy/cleaned_data/avg_gdp_continents.csv', index_col=0)
    data, pred_df = autoregressive_integrated_moving_average(csv.T, steps = 20, seasonal_order=(1, 1, 0, 12))
    plot_prediction_line_graph(data, pred_df, 'Year', 'GDP (Billion US$)', 'GDP Predictions per Continent', 'predictions.png')
    
    csv = pd.read_csv('../data/environmental/cleaned_data/cleaned_number-of-natural-disaster-events.csv', index_col=0)
    csv = csv.reset_index()
    csv = csv.drop(columns=['decade'])
    csv = csv.drop(columns=['All natural disasters'])
    number_of_predictions = 3
    data, pred_df = autoregressive_integrated_moving_average(csv, steps = number_of_predictions)
    data = data.set_index('Year')
    pred_df = pred_df.set_index('Year')
    all_data = data.append(pred_df.tail(number_of_predictions))
    years_labels = ['1900-1910', '1910-1920', '1920-1930', '1930-1940', '1940-1950', '1950-1960', '1960-1970', '1970-1980', '1980-1990', '1990-2000', '2000-2010', '2010-2020', '2020-2030', '2030-2040', '2040-2050']
    all_data['labels'] = years_labels
    all_data = all_data.set_index('labels')
    stacked_bar_graph_prediction(all_data, filename="../presentation_images/stacked_bar_graph_disasters.png", title="Natural Disasters from 1900-2020", ylabel="Number of Incidents")
