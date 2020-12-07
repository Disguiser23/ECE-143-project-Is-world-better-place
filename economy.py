import utils
import pandas as pd
from predictions.predictions import autoregressive_integrated_moving_average
from visualizations.graphs import plot_prediction_line_graph, stacked_bar_graph_prediction


def run():
    csv = pd.read_csv('./data/economy/cleaned_data/avg_gdp_continents.csv',
                      index_col=0)
    data, pred_df = autoregressive_integrated_moving_average(
        csv.T, steps=20, seasonal_order=(1, 1, 0, 12))
    plot_prediction_line_graph(
        data, pred_df, 'Year', 'GDP (US$)',
        'Annual GDP and Predictions per Continent', 'presentation_images/predictions_gdp.png')

    data_economy = './data/economy/cleaned_data/cleaned_'
    data_list = ['GDP.csv',
                 'annual_work_hrs.csv',
                 'Employment to population ratio (% ages 15 and older).csv',
                 'Labour force participation rate (% ages 1ß and older).csv',
                 'Unemployment, total (% of labour force).csv'
                 ]
    step = [15, 15, 15, 15, 15]
    y_label_name = ['United States dollars', 'hrs', '% ages 15 and older', '% ages 15 and older', '% of labour force']
    title_name = ['GDP', 'Annual Work Hours', 'Employment to Population Ratio', 'Labour Force Participation Rate',
                  'Unemployment']
    for d, s, y, t in zip(data_list, step, y_label_name, title_name):
        df = pd.read_csv(data_economy + d, index_col=0)
        csv = utils.average_countries_to_continents(df)

        data, pred_df = autoregressive_integrated_moving_average(csv.T, steps=s)
        plot_prediction_line_graph(data, pred_df, 'Year', y, t + ' per continent', d[:-4] + '.png')


if __name__ == "__main__":
    run()

