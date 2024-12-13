import math

import csv
import pandas as pd



def building_irradiance_analysis(global_solar_irradiance_csvfile_name, steps):
    global_solar_irradiance_df = pd.read_csv(global_solar_irradiance_csvfile_name)
    
    end_julian_date = len(global_solar_irradiance_df['Julian Date'])+1

    sunrise_local_time = (global_solar_irradiance_df['Local Sunrise Time'].min())
    sunset_local_time  = (global_solar_irradiance_df['Local Sunset Time'].max())

    start_time = int(sunrise_local_time)
    stop_time  = int(sunset_local_time)

    for julian_date in range (1, end_julian_date):

        for hour_time in range (start_time, stop_time):
            for minute_time in range (0, 60, steps):
                # Acquire Irradiances
                building_irradiance_per_steps =  global_solar_irradiance_df.loc[julian_date, f"Direct Normal Irradiance-{hour_time}:{minute_time}"]
