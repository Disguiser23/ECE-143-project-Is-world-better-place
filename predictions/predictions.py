import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm

def autoregressive_integrated_moving_average(data, xlabel, ylabel, filename = 'predictions.png'):
    '''this method plots predictions for a dataframe with years as columns and countries or continents as rows
    input: pandas dataframe
    xlabel, ylabel: str axis labels
    optional filename: str
    saves figure
    returns None'''
    assert (isinstance(data, pd.DataFrame))
    assert(isinstance(xlabel, str) and isinstance(ylabel, str) and isinstance(filename, str))
    preds = []
    data.index.name = 'Year'
    start_year = int(min(list(data.index)))
    for column_name in data:
        #prediction
        mod = sm.tsa.statespace.SARIMAX(data[column_name], order=(1, 1, 1), seasonal_order=(1, 1, 0, 12), enforce_stationarity=False, enforce_invertibility=False)
        results = mod.fit()
        start = int(len(data)/4) * 3 #start predicting after 3/4 of the data
        pred = results.get_prediction(start=start, dynamic=False)
        forecast = results.get_forecast(steps=20).predicted_mean
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

    #set up the plot
    colors = ['#F8B195', '#F67280', '#C06C84', '#6C5B7B', '#355C7D', '#000000']
    ax = data.plot(label='Observed', color=colors)
    pred_df.plot(ax = ax, label='Forecast', alpha=.7, figsize=(14, 7), color=colors, legend=False)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    plt.savefig(filename, bbox_inches='tight')

if __name__ == "__main__":
    csv = pd.read_csv('./visualizations/test/avg_gdp_continents.csv', index_col=0)
    autoregressive_integrated_moving_average(csv.T, 'Year', 'GDP')

