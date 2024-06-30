# AAVSO Query

This Python package `aavsoquery` allows fetching and visualizing astronomical observational data from the AAVSO (American Association of Variable Star Observers) database. It provides tools to retrieve data, plot light curves, and optionally fit models to the observed data.

## Features

- **Data Fetching**: Fetch observational data for a specific star including visual observations.
- **Light Curve Plotting**: Plot light curves with customizable time intervals.
- **Model Fitting**: Optional fitting of Gaussian models to the light curve data.

## Installation

You can install `aavsoquery` via pip:

```bash
pip install aavsoquery
```
## Usage

Here is an example of how to use `aavsoquery`:

```python
from query import AAVSODataFetcher
from plotter import Plotter

fetcher = AAVSODataFetcher(
    star_name='T CrB',
    obs_types='vis',
    num_results=100,
    pages=1
) #query by star's name (Example: T CrB), ability to fetch by a particular observer by obscode = 'Observer's code'


julian_dates, magnitudes = fetcher.fetch_and_parse_data(include_uncertain=True) # you can exclude uncertain values that begins with <

if len(julian_dates) > 0 and len(magnitudes) > 0: #if data fetched then plot it
    plotter = Plotter(julian_dates, magnitudes) 
    plotter.plot_light_curve(interval_hours=1, fit_model=True) #ability to fit a simple gaussian model, also defaults to mean hourly data if more datapoints present
else:
    print("No data available to plot.")
```
## Dependencies

- requests
- beautifulsoup4
- numpy
- matplotlib
- lmfit

