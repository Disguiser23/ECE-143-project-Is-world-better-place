# requires conda install basemap
# adapted to generalize from https://python-graph-gallery.com/315-a-world-map-of-surf-tweets/
import pandas as pd
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def create_world_bubble_map(data_health, data_env, data_econ, filename):
    '''input: data is a 3 pandas dataframe with 'Continent' for the three domains we want to show
    filename must include file suffix'''

    my_dpi = 96
    plt.figure(figsize=(2800 / my_dpi, 2000 / my_dpi), dpi=my_dpi)
    # Make the background map
    m = Basemap(llcrnrlon=-180, llcrnrlat=-65, urcrnrlon=180, urcrnrlat=80)
    m.drawmapboundary(fill_color=(0,0,0,0), linewidth=0)
    m.fillcontinents(color='#ffffff')
    m.drawcoastlines(linewidth=0.1, color="#f6f6f6")

    coords = [[-65.59, -30, 'South America'],
                           [-3.69, 43.53, 'Europe'],
                           [14, -20.77, 'Africa'],
                           [79.57, 40.52, 'Asia'],
                           [125.69, -25.45, 'Oceania'],
                           [-100.04, 42.51, 'North America']]

    coords_health = pd.DataFrame(coords)
    c_env = list(map(lambda x: [x[0]+22] + [x[1]] + [x[2]], coords))
    coords_env = pd.DataFrame(c_env)
    c_econ = list(map(lambda x: [x[0]+11] + [x[1]+22] + [x[2]], coords))
    coords_econ = pd.DataFrame(c_econ)
    coords_health.columns = ['lon', 'lat', 'Continent']
    coords_health = coords_health.set_index('Continent')
    coords_env.columns = ['lon', 'lat', 'Continent']
    coords_env = coords_env.set_index('Continent')
    coords_econ.columns = ['lon', 'lat', 'Continent']
    coords_econ = coords_econ.set_index('Continent')

    data_health = data_health.join(coords_health)
    data_env = data_env.join(coords_env)
    data_econ = data_econ.join(coords_econ)

    for column in data_health.columns:
        m.scatter(data_health['lon'], data_health['lat'], vmax = 0.025, vmin= -0.1, s=17000,  c=data_health[column], cmap='RdYlGn', zorder=1000, alpha=0.9)# big value -> green, small value -> red
        m.scatter(data_env['lon'], data_env['lat'], vmax = 0.025, vmin= -0.1, s=17000, c=data_env[column], cmap='RdYlGn', zorder=1000, alpha=0.9)
        m.scatter(data_econ['lon'], data_econ['lat'],vmax = 0.025, vmin= -0.1, s=17000,  c=data_econ[column], cmap='RdYlGn', zorder=1000, alpha=0.9)
        for elem in coords:
            plt.text(elem[0]-20, elem[1]-25, elem[2],
            ha='left', va='bottom', size=30, color='#555555')


        '''for elem in coords:
            plt.text(elem[0]-7, elem[1], 'Health',
                 ha='left', va='bottom', size=14, color='#555555', zorder=1001)
        for elem in c_econ:
            plt.text(elem[0]-8, elem[1], 'Economy',
                 ha='left', va='bottom', size=14, color='#555555', zorder=1001)
        for elem in c_env:
            plt.text(elem[0]-10, elem[1], 'Environment',
                 ha='left', va='bottom', size=14, color='#555555', zorder=1001)'''

        plt.text(-180, -68, column,
            ha='left', va='bottom', size=30, color='#555555', backgroundcolor='#E7E7E7')
        plt.savefig(column + '_' + filename, bbox_inches='tight', transparent=True)

if __name__ =="__main__":
    csv = pd.read_csv('./visualizations/avg_gdp_continents.csv', index_col=0)
    data = pd.DataFrame(csv['1970']/ 1000000)
    data = data.rename(columns={"1970": "data"})
    create_world_bubble_map(data, "label", 'test.png')
