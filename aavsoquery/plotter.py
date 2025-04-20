import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime, timedelta
from lmfit import Model

class Plotter:
    def __init__(self, julian_dates, magnitudes):
        self.julian_dates = julian_dates
        self.magnitudes = magnitudes

    def mean_magnitudes(self, interval_hours=1):
        if len(self.julian_dates) == 0:
            return [], []

        dates = [datetime.fromtimestamp((jd - 2440587.5) * 86400.0) for jd in self.julian_dates]

        rounded_dates = [datetime(date.year, date.month, date.day, date.hour // interval_hours * interval_hours) for date in dates]

        unique_dates = np.unique(rounded_dates)
        mean_mags = []

        for unique_date in unique_dates:
            mask = [date == unique_date for date in rounded_dates]
            mean_mags.append(np.mean(np.array(self.magnitudes)[mask]))

        return unique_dates, mean_mags

    def fit_gaussian_model(self, dates, mean_mags):
        days = np.array([(date - dates[0]).total_seconds() / (24 * 3600) for date in dates]) #dates to days since the first observation
        # pretty basic, will modify later
        def gaussian_func(x, amp, mean, sigma):
            return amp * np.exp(-(x - mean)**2 / (2 * sigma**2))

        model = Model(gaussian_func)
        params = model.make_params(amp=np.max(mean_mags) - np.min(mean_mags),
                                   mean=np.mean(days),
                                   sigma=np.std(days))
        result = model.fit(mean_mags, x=days, params=params)
        fitted_mags = result.best_fit
        fitted_dates = [dates[0] + timedelta(days=day) for day in days] #days back to dates

        return fitted_dates, fitted_mags

    def plot_light_curve(self, interval_hours=1, fit_model=False):
        dates, mean_mags = self.mean_magnitudes(interval_hours)
        if len(dates) == 0:
            print("No data available to plot.")
            return

        plt.figure(figsize=(10, 5))
        plt.scatter(dates, mean_mags, color='blue', label=f'Mean Magnitudes ({interval_hours}-hour interval)')
        plt.gca().invert_yaxis()  # Magnitude scale: brighter objects have lower magnitudes
        plt.title('Light Curve with Custom Interval Averaging')

        if fit_model:
            fitted_dates, fitted_mags = self.fit_gaussian_model(dates, mean_mags)
            plt.plot(fitted_dates, fitted_mags, color='red', label='Fitted Gaussian Model')

        plt.xlabel('Date and Time')
        plt.ylabel('Magnitude')
        plt.legend()
        plt.tight_layout()
        plt.show()
