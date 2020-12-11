# ECE143 Project: Is the world going to be a better place? (Team 23)
This project was motivated by the fact that during the 2020 global pandemic, we all needed some encouragement. We wanted to analyze if the world is actually improving, even though we are constantly exposed to more bad than good  news.
## Used Libraries
Pandas (Version 1.1.4)

Numpy (Version 1.17.2)

Matplotlib (Version 3.1.1)

mpl_toolkits.basemap (requires conda install basemap)

statsmodels.api (Version 0.10.1)

plotly (Version 4.12.0)

plotly_express (Version 0.4.1)

## Datasets
* Health
    * Gender equality [[8](http://data.un.org/DocumentData.aspx?id=415)], 
                    [[7](https://databank.worldbank.org/source/gender-statistics)],
                    [[11](http://hdr.undp.org/en/data#)]
    * Death rates by causes [[1](http://data.un.org/Data.aspx?d=POP&f=tableCode%3a105)], 
                    [[2](https://ourworldindata.org/ofdacred-international-disaster-data)]
    * Happiness and Life Satisfaction [[9](https://www.kaggle.com/unsdsn/world-happiness)]
* Economy
    * Employment rates [[3](https://stats.oecd.org/index.aspx?queryid=36324#)], 
                    [[12](http://hdr.undp.org/en/data#)]
    * GDP [[4](http://data.un.org/Data.aspx?d=SNAAMA&f=grID%3a101%3bcurrID%3aUSD%3bpcFlag%3a0%3bitID%3a9)]
* Environmental  
    * Disasters [[6](https://earthdata.nasa.gov/earth-observation-data/near-real-time/hazards-and-disasters/drought)] 
    [[5](https://www.emdat.be/)]
    * Greenhouse Gas Emissions [[10](https://github.com/owid/co2-data)]

## File Structure
```bash
.
├── README.md 
├── data
│   ├── countries_continent                  # Provide an one-on-one mapping from country to its continent
│   ├── economy                              # Time sequence data we use for measuring economy
│   ├── environmental                        # Time sequence data we use for measuring enviromental
│   └── health                               # Time sequence data we use for measuring health
├── src                    
│   ├── data_loading                         # Code uses to load and clean the data in different categories
│   │   ├── clean_health_data.py          
│   │   ├── clean_economy_data.py       
│   │   └── clean_disaster_data.py
│   ├── predictions                          # Code uses to do predictions
│   │   ├── predictions.py       
│   └── visualizations                       # Code uses for visualization purposes 
│       ├── envi_merge.py
│       ├── graphs.py       
│       ├── read_co2.py     
│       ├── read_disaster.py         
│       └── world_map.py
├── main.ipynb                               # The main jupyterNotebook to show the graphs
├── health.py                                # Code to predict and visualize health data
├── economy.py                               # Code to predict and visualize economy data
├── world_overall.py                         # Code to predict and visualize overall world data for the categories
├── environment.py                           # Code to predict and visualize environment data
├── output_images                            # Where all the graphs are stored
├── .gitignore
└── ECE_143_Is_world_better_place.pdf        # Our presentation slides
```
## How to run the code
Within each data, there's a "cleaned" subdirectory that stores the data that will be used.

However, we can re-do the cleaning process by running different python files for each category.

Directly run main.ipynb. It will call the python files for three categories and the world map respectively. 

All outputs are stored into ./output_images directory.

Depending on the operating system used, filestrings might need to be changed from '\\' to '/'.

Some graphs plotted by plotly express cannot be shown correctly because of the limits of github. You can try to click the minus sign on the page to use the nbviewer or run it on a local machine.


## Final Presentation
Can be found in ./ECE_143_Is_world_better_place.pdf



