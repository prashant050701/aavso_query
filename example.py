from aavsoquery import AAVSODataFetcher, Plotter

fetcher = AAVSODataFetcher(
    star_name='T CrB',
    obs_types='vis',
    num_results=100,
    pages=1
)

julian_dates, magnitudes = fetcher.fetch_and_parse_data(include_uncertain=False)

if len(julian_dates) > 0 and len(magnitudes) > 0:
    plotter = Plotter(julian_dates, magnitudes)
    plotter.plot_light_curve(interval_hours=1)
else:
    print("No data available to plot.")
