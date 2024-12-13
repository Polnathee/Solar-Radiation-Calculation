#Calcualtion
import math

# Data Base
import csv
import pandas as pd
from datetime import date

# Output of Solar Radiation Geometry: Delicnation, Solar Hour Angle, Zenith
def solar_radiation_geometry_funciton(uid, buildign_fields_table_df, global_solar_irradiance_geometry_csvfile_location, steps, std_longitude, longitude, latitude):
    # Checking Input
    print(f'\nUID: {uid}, Latitude: {latitude}, Longitude: {longitude}')
    date_df = date_function()
    global_solar_irradiance_geometry_df = pd.DataFrame()

    # Create CAV File Name
    solar_irradiance_geometry_csvfile_local_name = f'Solar_Irradiance_Geometry_uid_{uid}'
    # Create CSV File to Store Global Irradiance Geometry Data
    writer, global_solar_irradiance_geometry_csvfile_name = create_csvfile(global_solar_irradiance_geometry_csvfile_location, solar_irradiance_geometry_csvfile_local_name)
    print(f'CSV File name: {global_solar_irradiance_geometry_csvfile_name}')

    # Declination Data Base
    declination_angle_list = []
    # Eccentricity Correction Factor Data Base
    eccentricity_correction_factor_list = []
    # Solar Hour Angle Data Base
    solar_hour_angle_field_list    = []
    solar_hour_angle_global_list   = []
    # Altitude Angle Data Base
    altitude_angle_field_list      = []
    altitude_angle_global_list     = []
    # Azimuth Angle Data Base
    azimuth_angle_field_list       = []
    azimuth_angle_global_list      = []
    # Zenith Angle Data Base
    zenith_angle_field_list        = []
    zenith_angle_global_list       = []
    # Sunrise and Sunset Hour Angle Data Base
    sunrise_local_time_list        = []
    sunrise_solar_hour_angle_list  = []
    sunset_local_time_list         = []
    sunset_solar_hour_angle_list   = []

    # Creating Data Frame
    solar_hour_angle_global_df = pd.DataFrame(solar_hour_angle_global_list)
    altitude_angle_global_df   = pd.DataFrame(altitude_angle_global_list)
    azimuth_angle_global_df    = pd.DataFrame(azimuth_angle_global_list)
    zenith_angle_global_df     = pd.DataFrame(zenith_angle_global_list)

    #end_julian_date = 3 
    end_julian_date = len(date_df['Julian Date'])+1

    # Data Frame
    separator_df = create_separator_df_function(end_julian_date)

    for julian_date in range (1, end_julian_date):
        # Declination Calculation
        declination_angle = declination_angle_function(julian_date)
        declination_angle_list.append(declination_angle)

        # Eccentricity Correction Factor
        eccentricity_correction_factor = eccentricity_correction_factor_function(julian_date)
        eccentricity_correction_factor_list.append(eccentricity_correction_factor)

        # Sunrise and Sunset Calcultions
        sunrise_solar_hour_angle, local_sunrise_time, local_sunset_time = rise_solar_hour_angle_function(declination_angle, latitude)
        sunset_solar_hour_angle = -(sunrise_solar_hour_angle)
        local_sunrise_time = float("{:.6f}".format(local_sunrise_time))
        local_sunset_time  = float("{:.6f}".format(local_sunset_time))

        # Sunrise
        sunrise_local_time_list.append(local_sunrise_time)
        sunrise_solar_hour_angle_list.append(sunrise_solar_hour_angle)
        # Sunset
        sunset_local_time_list.append(local_sunset_time)
        sunset_solar_hour_angle_list.append(sunset_solar_hour_angle)

    sunrise_local_time = solar_hour_angle2local_time(max(sunrise_solar_hour_angle_list))
    sunset_local_time  = solar_hour_angle2local_time(min(sunset_solar_hour_angle_list))

    start_time = int(sunrise_local_time)
    stop_time  = int(sunset_local_time)
    #print(f'Start time: {start_time}, Stop time: {stop_time}')

    for julian_date in range (1, end_julian_date):
        program_name = "SOLAR IRRADIANCE GEOMETERY"
        checking_program_progress(uid, end_julian_date ,julian_date, program_name)

        # Local List for storing daily data
        solar_hour_angle_local_list = []
        altitude_angle_local_list   = []
        azimuth_angle_local_list    = []
        zenith_angle_local_list     = []

        for hour in range (start_time, stop_time+1):
            for minute in range (0,60,steps):
                local_standard_time = hour + (minute/60)
                if julian_date == 1:
                    # Solar Hour Angle Indication
                    if hour<10:
                        hour_time = "0"+str(hour)
                    else:
                        hour_time = str(hour)

                    if minute<10:
                        minute_time = "0" + str(minute)
                    else:
                        minute_time = str(minute)
                    # Writng Solar Hour Angle Field
                    solar_hour_angle_field = f"HRA-{hour_time}:{minute_time}"
                    solar_hour_angle_field_list.append(solar_hour_angle_field)
                    # Writing Altitude Angle Field
                    altitude_angle_field = f"Altitude-{hour_time}:{minute_time}"
                    altitude_angle_field_list.append(altitude_angle_field)
                    # Wrintng Azimuth Angle Field
                    azimuth_angle_field = f"Azimuth-{hour_time}:{minute_time}"
                    azimuth_angle_field_list.append(azimuth_angle_field)
                    # Writing Zenith Angle Field
                    zenith_angle_field = f"Zenith-{hour_time}:{minute_time}"
                    zenith_angle_field_list.append(zenith_angle_field)

                # Solar Hour Angle Calculation
                solar_hour_angle = solar_hour_angle_function(julian_date, local_standard_time, std_longitude, longitude)
                solar_hour_angle_local_list.append(solar_hour_angle)

                # Altitude Angle Calculation
                altitude_angle = altitude_angle_function(declination_angle, latitude, solar_hour_angle)
                altitude_angle_local_list.append(altitude_angle)

                # Azimuth Angle Calculation
                azimuth_angle = azimuth_angle_function(declination_angle, altitude_angle, solar_hour_angle)
                azimuth_angle_local_list.append(azimuth_angle)

                # Zenith Angle Calculaltion
                zenith_angle = zenith_angle_function(declination_angle, latitude, solar_hour_angle)
                zenith_angle_local_list.append(zenith_angle)

        # Acquire Solar Hour Angle into Data Frame
        solar_hour_angle_local_df  = pd.DataFrame(solar_hour_angle_local_list)
        solar_hour_angle_global_df = pd.concat([solar_hour_angle_global_df, solar_hour_angle_local_df], axis=1)
        #print(f'Global Solar Hour Angle Data Frame:\n{solar_hour_angle_global_df}')

        # Acquire Altitude Angle into Data Frame
        altitude_angle_local_df  = pd.DataFrame(altitude_angle_local_list)
        altitude_angle_global_df = pd.concat([altitude_angle_global_df, altitude_angle_local_df], axis=1)

        # Acquire Azimuth Angle into Data Frame
        azimuth_angle_local_df  = pd.DataFrame(azimuth_angle_local_list)
        azimuth_angle_global_df = pd.concat([azimuth_angle_global_df, azimuth_angle_local_df], axis=1)

        # Acquire Zenith Angle into Data Frame
        zenith_angle_local_df  = pd.DataFrame(zenith_angle_local_list)
        zenith_angle_global_df = pd.concat([zenith_angle_global_df, zenith_angle_local_df], axis=1)
        
    # Acquire Declination Data into Data Frame
    declination_angle_df = pd.DataFrame(declination_angle_list)
    declination_angle_df.columns = ['Declination Angle']
    #print(f'Declination Data Frame:\n{declination_angle_df}')

    # Acquire Eccentricity Correction Factor Data into Data Frame
    eccentricity_correction_factor_df = pd.DataFrame(eccentricity_correction_factor_list)
    eccentricity_correction_factor_df.columns = ['Eccentricity Correction Factor']

    # Acquire Sunrise and Sunset Local Time into Data Frame
    sunrise_local_time_df = pd.DataFrame(sunrise_local_time_list)
    sunrise_local_time_df.columns = ['Local Sunrise Time']
    sunset_local_time_df = pd.DataFrame(sunset_local_time_list)
    sunset_local_time_df.columns = ['Local Sunset Time']


    # Acquire Sunrise and Sunset Solar Hour Angle into Data Frame
    sunrise_solar_hour_angle_df = pd.DataFrame(sunrise_solar_hour_angle_list)
    sunrise_solar_hour_angle_df.columns = ['Sunrise HRA']
    sunset_solar_hour_angle_df = pd.DataFrame(sunset_solar_hour_angle_list)
    sunset_solar_hour_angle_df.columns = ['Sunset HRA']
    
    # Organize Solar Hour Angle into Global Data Frame
    solar_hour_angle_global_df = solar_hour_angle_global_df.transpose()
    solar_hour_angle_global_df = solar_hour_angle_global_df.reset_index(drop=True)
    solar_hour_angle_global_df.columns = solar_hour_angle_field_list
    #print(f'\nGlobal Solar Hour Angle Data Field:\n{solar_hour_angle_field_list}')
    #print(f'\nGlobal Solar Hour Angle Data Frame:\n{solar_hour_angle_global_df}')

    # Organize Altitude Angle into Global Data Frame
    altitude_angle_global_df = altitude_angle_global_df.transpose()
    altitude_angle_global_df = altitude_angle_global_df.reset_index(drop=True)
    altitude_angle_global_df.columns = altitude_angle_field_list
    #print(f'\nGlobal Altitude Angle Data Fields:\n{altitude_angle_field_list}')
    #print(f'\nGlobal Altitude Angle Data Frame:\n{altitude_angle_global_df}')

    # Organize Azimuth Angle into Global Data Frame
    azimuth_angle_global_df = azimuth_angle_global_df.transpose()
    azimuth_angle_global_df = azimuth_angle_global_df.reset_index(drop=True)
    azimuth_angle_global_df.columns = azimuth_angle_field_list
    #print(f'\nGlobal Azimuth Angle Data Fields:\n{azimuth_angle_field_list}')
    #print(f'\nGlobal Azimuth Angle Data Frame:\n{azimuth_angle_global_df}')

    # Organise Zenith Hour Angle into Global Data Frame
    zenith_angle_global_df = zenith_angle_global_df.transpose()
    zenith_angle_global_df = zenith_angle_global_df.reset_index(drop=True)
    zenith_angle_global_df.columns = zenith_angle_field_list
    #print(f'\nGlobal Zenith Angle Data Field:\n{zenith_angle_field_list}')
    #print(f'\nGlobal Zenith Angle Data Frame:\n{zenith_angle_global_df}')
    
    # Combine into one Data Frame
    #print(f'Start time: {start_time}, Stop time: {stop_time}')
    global_solar_irradiance_geometry_df = pd.concat([date_df, declination_angle_df, eccentricity_correction_factor_df, sunrise_local_time_df, sunset_local_time_df, sunrise_solar_hour_angle_df, sunset_solar_hour_angle_df, solar_hour_angle_global_df, separator_df, altitude_angle_global_df, separator_df, azimuth_angle_global_df, separator_df, zenith_angle_global_df], axis=1)
    #print(f'\nSolar Radiation Geometery:\n{global_solar_radiation_geometry_df}')

    # Writing Data Frame to CSV File
    new_global_solar_irradiance_geometry_df = pd.concat([buildign_fields_table_df,global_solar_irradiance_geometry_df], axis=1)
    #print(new_global_solar_irradiance_geometry_df)
    new_global_solar_irradiance_geometry_df.to_csv(global_solar_irradiance_geometry_csvfile_name, index=False)

    return global_solar_irradiance_geometry_csvfile_name, new_global_solar_irradiance_geometry_df

# Date and Time Function
def date_function():
    today = date.today()
    year = today.year

    julian_date_list = []
    for day in range (1, 367):
        julian_date_list.append(day)

    julian_date_df = pd.DataFrame(julian_date_list)
    julian_date_df.columns = ['Julian Date']

    date_range = pd.date_range(f'{year}', periods=len(julian_date_df), freq='1d')
    date_df = pd.DataFrame(date_range)
    date_df.columns = ['Date']
    # Combine Julian Date data frame with Date data frame
    date_df = pd.concat([date_df, julian_date_df], axis=1)
    #print(date_df)

    return date_df

# Declination Calculation Function (degree)
def declination_angle_function(julian_date):
    day_angle = day_angle_function(julian_date)
    declination_angle = ((0.006918)-(0.39912*(math.cos(day_angle)))+(0.070257*(math.sin(day_angle)))-(0.006758*(math.cos(2*day_angle)))+(0.000907*(math.sin(2*day_angle)))-(0.002697*(math.cos(3*day_angle)))+(0.00148*(math.sin(3*day_angle))))
    declination_angle = Rad2Deg(declination_angle)
    #print(f'Day: {julian_date}, Earth Decilnation Angle : {declination_angle}')
    
    return declination_angle

# Eccentricity Correction Factor
def eccentricity_correction_factor_function(julian_date):
    day_angle = day_angle_function(julian_date)
    eccentricity_correction_factor = ((1.000110)+(0.034221*(math.cos(day_angle)))+(0.001280*(math.sin(day_angle)))+(0.000719*(math.cos(2*day_angle)))+(0.000077*(math.sin(2*day_angle))))
    return eccentricity_correction_factor

# Solar Hour Angle(HRA) Calculation Funciton (degree)
def solar_hour_angle_function(julian_date, local_standard_time, std_long, long):
    sun_time= sun_time_function(julian_date, local_standard_time, std_long, long)

    # Solar Hour Angle Calculation
    solar_hour_angle = 15.0 * (12.0-sun_time)
    #print(f'Day : {julian_date}, Local Time: {local_standard_time}, Sun Time : {sun_time} Hour Angle : {solar_hour_angle}')
    return solar_hour_angle

# Altitude Angle Calculation Function (degree)
def altitude_angle_function(declination_angle, lat, solar_hour_angle):
    altitude_angle = Rad2Deg(math.asin((  (math.sin(Deg2Rad(declination_angle)))  *  (math.sin(Deg2Rad(lat)))  ) + (  (math.cos(Deg2Rad(declination_angle))) * (math.cos(Deg2Rad(lat))) * (math.cos(Deg2Rad(solar_hour_angle)))  )))
    return altitude_angle

# Azimuth Angle Calculation Function (degree)
def azimuth_angle_function(declination_angle, altitude_angle, solar_hour_angle):
    azimuth_angle = Rad2Deg(math.asin(  ((math.sin(Deg2Rad(solar_hour_angle))) * (math.cos(Deg2Rad(declination_angle)))) / (math.cos(Deg2Rad(altitude_angle))) ))
    return azimuth_angle

# Zenith Angle Calculation Function (degree)
def zenith_angle_function(declination_angle, lat, solar_hour_angle):
    zenith_angle = Rad2Deg(math.acos((  (math.sin(Deg2Rad(declination_angle)))  *  (math.sin(Deg2Rad(lat)))  ) + (  (math.cos(Deg2Rad(declination_angle))) * (math.cos(Deg2Rad(lat))) * (math.cos(Deg2Rad(solar_hour_angle)))  )))
    return zenith_angle

# Sun Time Calculation Function (hour)
def sun_time_function(julian_date, local_standard_time, std_long, long):
    e_t = equation_of_time_function(julian_date)
    sun_time = local_standard_time + (4*(-std_long + long)*(1/60)) + (e_t*(1/60))
    #print(f'Et: {e_t}, diff: {std_long - long}')
    return sun_time

# Equation of Time Calculation Function (minute)
def equation_of_time_function(julian_date):
    day_angle = day_angle_function(julian_date)
    e_t = 229.18 * ((0.000075) + ((0.001868)*math.cos(day_angle)) - (0.032077*(math.sin(day_angle))) - (0.014615*(math.cos(2*day_angle))) - (0.040849*(math.sin(2 * day_angle))))
    return e_t

# Day Angle Calculation Function (radian)
def day_angle_function(julian_date):
    day_angle = (2*math.pi)*(julian_date-1)*(1/365)
    return day_angle

# Sunrise and Sunset Solar Angle Hour Calculaiton Function (degree)
def rise_solar_hour_angle_function(declination_angle, lat):
    sunrise_solar_hour_angle = Rad2Deg(math.acos((-1)*(math.tan(Deg2Rad(declination_angle)))*(math.tan(Deg2Rad(lat)))))
    local_sunrise_time = solar_hour_angle2local_time(sunrise_solar_hour_angle)
    local_sunset_time = solar_hour_angle2local_time(-sunrise_solar_hour_angle)
    #print(f'Sunrise Solar Hour Angle: {sunrise_solar_hour_angle}, Local Sunrise Time: {local_sunrise_time}, Local Sunset Time: {local_sunset_time} ')
    return  sunrise_solar_hour_angle, local_sunrise_time, local_sunset_time

# Convert Solar Hour Angle to Local Time (hour)
def solar_hour_angle2local_time (solar_hour_angle):
    sun_time = 12-(solar_hour_angle/15)
    local_rise_time = int(sun_time)
    diff_time = sun_time - local_rise_time
    if (1/6)  > diff_time >= 0:
        local_rise_time = int(local_rise_time)
    elif (1/3)> diff_time >=(1/6):
        local_rise_time += (1/6)
    elif (1/2)> diff_time >=(1/3):
        local_rise_time += (1/3)
    elif (2/3)> diff_time >=(1/2):
        local_rise_time += (1/2)
    elif (5/6)> diff_time >=(2/3):
        local_rise_time += (2/3)
    elif 1    > diff_time >=(5/6):
        local_rise_time += (5/6)
    else:
        local_rise_time = int(sun_time)
    return local_rise_time

def Deg2Rad(deg):
    return deg * (math.pi / 180)
    
def Rad2Deg(rad):
    return rad * (180 / math.pi)


# Creating CSV File Function
def create_csvfile(csvfile_location, csvfile_local_name):
    csvfile_name = str(csvfile_location) + '/' + str(csvfile_local_name) + '.csv'
    with open(csvfile_name, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
    print(f'csv file name: {csvfile_name}')
    return writer, csvfile_name

def create_separator_df_function(end_row):
    separator_list = []
    for i in range(1, end_row):
        separator = "/////"
        separator_list.append(separator)
    separator_df = pd.DataFrame(separator_list)
    separator_df.columns = ['Separator Column']
    return separator_df

# Checking Program Progress
def checking_program_progress(uid, end_julian_date ,julian_date, program_name):
    if julian_date == 1:
        print(f"\nUID: {uid}-PROCESSING {program_name}-(0/4)...")
    elif julian_date == int(end_julian_date*(1/4)):
        print(f"UID: {uid}-PROCESSING {program_name}-(1/4)...")
    elif julian_date == int(end_julian_date*(2/4)):
        print(f"UID: {uid}-PROCESSING {program_name}-(2/4)...")
    elif julian_date == int(end_julian_date*(3/4)):
        print(f"UID: {uid}-PROCESSING {program_name}-(3/4)...")
    elif julian_date == int(end_julian_date-1*(4/4)):
        print(f"UID: {uid}-PROCESSING {program_name}-(4/4)...")



# Testing
def main1():
    for day in range (1,2):
        std_long =105.00
        longitude = 100.1703
        latitude = 13.9789
        dDelta = declination_angle_function(1)
        print(f'Ddelta: {dDelta}')

        rise_hra = rise_solar_hour_angle_function(dDelta, latitude )

        for hour in range (14, 19):
            for minute in range (0, 60, 30):
                time = hour + (minute / 60)
                hra = solar_hour_angle_function(day, time, std_long, longitude)
    return hra

def main2():
    uid = 12345678
    std_long =105.00
    longitude = 100.1703
    latitude = 13.9789
    steps = 10

    solar_radiation_geometry_funciton(uid, steps, std_long, longitude, latitude)

#main2()
