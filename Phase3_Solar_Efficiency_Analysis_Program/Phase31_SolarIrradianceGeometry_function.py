#Calcualtion
import math

# Data Base
import csv
import pandas as pd
from datetime import date

# Output of Solar Radiation Geometry: Delicnation, Solar Hour Angle, Zenith
def solar_radiation_geometry_funciton(uid, building_fields_table_df, global_rooftop_geometry_df, global_solar_irradiance_geometry_csvfile_location, steps, std_longitude, longitude, latitude):
    # Checking Input
    print(f'\nUID: {uid}, Latitude: {latitude}, Longitude: {longitude}')
    date_df = date_function()
    global_solar_irradiance_geometry_df = pd.DataFrame()

    # Create CAV File Name
    solar_irradiance_geometry_csvfile_local_name = f'Solar_Irradiance_Geometry_uid_{uid}'
    # Create CSV File to Store Global Irradiance Geometry Data
    writer, global_solar_irradiance_geometry_csvfile_name = create_csvfile(global_solar_irradiance_geometry_csvfile_location, solar_irradiance_geometry_csvfile_local_name)
    #print(f'CSV File name: {global_solar_irradiance_geometry_csvfile_name}')

    # Global Building Field Table
    new_building_fields_tables_df = pd.DataFrame([])
    # Declination Data Base
    declination_angle_list         = []
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

    # Separtor Data Frame
    separator_df = create_separator_df_function(end_julian_date)

    # Acquire Rooftop Geometry from Rooftop Geometry Data Frame
    global_rooftop_geometry_filter = (global_rooftop_geometry_df['uid'] == uid) & (global_rooftop_geometry_df['vertex_index'] == 0)
    # Acquire Rooftype from Rooftop Geometry Data Frame
    rooftype_series = global_rooftop_geometry_df.loc[global_rooftop_geometry_filter, 'rooftype']
    rooftype = rooftype_series.iloc[0]
    # Acquire Rooftop width from Rooftop Geometry Data Frame
    rooftop_width_series = global_rooftop_geometry_df.loc[global_rooftop_geometry_filter, 'width']
    rooftop_width = rooftop_width_series.iloc[0]
    rooftop_width_df = pd.DataFrame([rooftop_width])
    # Acquire Rooftop length from Rooftop Geometry Data Frame
    rooftop_length_series = global_rooftop_geometry_df.loc[global_rooftop_geometry_filter, 'length']
    rooftop_length = rooftop_length_series.iloc[0]
    rooftop_length_df = pd.DataFrame([rooftop_length])
    # Acquire Rooftop Slope
    rooftop_slope_angle_series = global_rooftop_geometry_df.loc[global_rooftop_geometry_filter, 'rooftop slope']
    rooftop_slope_angle = rooftop_slope_angle_series.iloc[0]
    rooftop_slope_angle_df = pd.DataFrame([rooftop_slope_angle])
    # Acquire Rooftop Azimuth
    rooftop_azimuth_angle_series = global_rooftop_geometry_df.loc[global_rooftop_geometry_filter, 'rooftop azimuth angle']
    rooftop_azimuth_angle = rooftop_azimuth_angle_series.iloc[0]
    rooftop_azimuth_angle_df = pd.DataFrame([rooftop_azimuth_angle])
    # Acquire Rooftop Geometry into Data Frame
    local_uid_rooftop_geometry_df = pd.concat([rooftop_width_df, rooftop_length_df, rooftop_slope_angle_df, rooftop_azimuth_angle_df])
    local_uid_rooftop_geometry_df = local_uid_rooftop_geometry_df.transpose()
    local_uid_rooftop_geometry_df = local_uid_rooftop_geometry_df.reset_index(drop=True)
    local_uid_rooftop_geometry_df.columns = ['rooftop width', 'rooftop length', 'rooftop slope', 'rooftop azimuth angle']

    for julian_date in range (1, end_julian_date):

        # Writing Building Information to each row
        local_new_building_fields_tables_df = pd.concat([building_fields_table_df, local_uid_rooftop_geometry_df], axis=1)
        new_building_fields_tables_df = pd.concat([new_building_fields_tables_df, local_new_building_fields_tables_df])

        # Declination Calculation
        declination_angle = declination_angle_function(julian_date)
        declination_angle_list.append(declination_angle)

        # Eccentricity Correction Factor
        eccentricity_correction_factor = eccentricity_correction_factor_function(julian_date)
        eccentricity_correction_factor_list.append(eccentricity_correction_factor)

        # Sunrise and Sunset Calcultions
        sunrise_solar_hour_angle, sunset_solar_hour_angle, local_sunrise_time, local_sunset_time = rise_solar_hour_angle_function(rooftype,declination_angle, latitude, rooftop_slope_angle, rooftop_azimuth_angle)
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
                if rooftype == "Flat":
                    zenith_angle = zenith_angle_on_horizontal_plane_function(declination_angle, latitude, solar_hour_angle)
                    zenith_angle_local_list.append(zenith_angle)
                elif rooftype == "Complex":
                    zenith_angle = zenith_angle_on_horizontal_plane_function(declination_angle, latitude, solar_hour_angle)
                    zenith_angle_local_list.append(zenith_angle)
                elif rooftype == "Gable":
                    if rooftop_azimuth_angle == 0:
                        zenith_angle = zenith_angle_on_inclined_plane_facing_south_direction_function(declination_angle, latitude, solar_hour_angle, rooftop_slope_angle)
                        zenith_angle_local_list.append(zenith_angle)
                    else:
                        zenith_angle = zenith_angle_on_inclined_plane_facing_any_direction_function(declination_angle, latitude, solar_hour_angle, rooftop_slope_angle, rooftop_azimuth_angle)
                        zenith_angle_local_list.append(zenith_angle)
                elif rooftype == "Hip":
                    if rooftop_azimuth_angle == 0:
                        zenith_angle = zenith_angle_on_inclined_plane_facing_south_direction_function(declination_angle, latitude, solar_hour_angle, rooftop_slope_angle)
                        zenith_angle_local_list.append(zenith_angle)
                    else:
                        zenith_angle = zenith_angle_on_inclined_plane_facing_any_direction_function(declination_angle, latitude, solar_hour_angle, rooftop_slope_angle, rooftop_azimuth_angle)
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
    
    # Organize New Building Organsize Field
    new_building_fields_tables_df = new_building_fields_tables_df.reset_index(drop=True) 

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
    new_global_solar_irradiance_geometry_df = pd.concat([new_building_fields_tables_df ,global_solar_irradiance_geometry_df], axis=1)
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

# Solar Hour Angle (HRA) Calculation Function (degree)
def solar_hour_angle_function(julian_date, local_standard_time, std_long, long):
    solar_time= solar_time_function(julian_date, local_standard_time, std_long, long)

    # Solar Hour Angle Calculation
    solar_hour_angle = 15.0 * (12.0-solar_time)
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

# Zenith Angle on Horizontal Plane Calculation Function (degree)
def zenith_angle_on_horizontal_plane_function(declination_angle, latitude, solar_hour_angle):
    zenith_angle = Rad2Deg(math.acos( ((math.sin(Deg2Rad(declination_angle)))*(math.sin(Deg2Rad(latitude)))) + ((math.cos(Deg2Rad(declination_angle)))*(math.cos(Deg2Rad(latitude)))*(math.cos(Deg2Rad(solar_hour_angle)))) ))
    return zenith_angle

# Zenith Angle on Inclined Plane that faced South Direction (degree)
def zenith_angle_on_inclined_plane_facing_south_direction_function(declination_angle, latitude, solar_hour_angle, rooftop_slope_angle):
    zenith_angle = Rad2Deg(math.acos( ((math.sin(Deg2Rad(declination_angle)))*(math.sin((Deg2Rad(latitude))-(Deg2Rad(rooftop_slope_angle))))) + ((math.cos(Deg2Rad(declination_angle)))*(math.cos((Deg2Rad(latitude))-(Deg2Rad(rooftop_slope_angle))))*(math.cos(Deg2Rad(solar_hour_angle)))) ))
    return zenith_angle

# Zenith Angle on Inclined Plane that faced at any Azimuth Angle (degree)
def zenith_angle_on_inclined_plane_facing_any_direction_function(declination_angle, latitude, solar_hour_angle, rooftop_slope_angle, rooftop_azimuth_angle):
    zenith_angle = Rad2Deg(math.acos(((math.cos(Deg2Rad(declination_angle)))*(math.sin(Deg2Rad(rooftop_slope_angle)))*(math.sin(Deg2Rad(rooftop_azimuth_angle)))*(math.sin(Deg2Rad(solar_hour_angle)))) + ((((math.cos(Deg2Rad(latitude)))*(math.cos(Deg2Rad(rooftop_slope_angle)))*(math.cos(Deg2Rad(declination_angle)))) + ((math.sin(Deg2Rad(latitude)))*(math.sin(Deg2Rad(rooftop_slope_angle)))*(math.cos(Deg2Rad(rooftop_azimuth_angle)))*(math.cos(Deg2Rad(declination_angle)))))*(math.cos(Deg2Rad(solar_hour_angle)))) + ((math.sin(Deg2Rad(latitude)))*(math.cos(Deg2Rad(rooftop_slope_angle)))*(math.sin(Deg2Rad(declination_angle)))) - ((math.cos(Deg2Rad(latitude)))*(math.sin(Deg2Rad(rooftop_slope_angle)))*(math.cos(Deg2Rad(rooftop_azimuth_angle)))*(math.sin(Deg2Rad(declination_angle)))) ))
    return zenith_angle

# Solar Time Calculation Function (hour)
def solar_time_function(julian_date, local_standard_time, std_long, long):
    e_t = equation_of_time_function(julian_date)
    solar_time = local_standard_time + (4*(-std_long + long)*(1/60)) + (e_t*(1/60))
    #print(f'Et: {e_t}, diff: {std_long - long}')
    return solar_time

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
def rise_solar_hour_angle_function(rooftype,declination_angle, latitude, rooftop_slope_angle, rooftop_azimuth_angle):
    if rooftype == "Flat":
        sunrise_solar_hour_angle = Rad2Deg(math.acos((-1)*(math.tan(Deg2Rad(declination_angle)))*(math.tan(Deg2Rad(latitude)))))
        sunset_solar_hour_angle = -(sunrise_solar_hour_angle)
        local_sunrise_time = solar_hour_angle2local_time(sunrise_solar_hour_angle)
        local_sunset_time = solar_hour_angle2local_time(-sunrise_solar_hour_angle)
    elif rooftype == "Complex":
        sunrise_solar_hour_angle = Rad2Deg(math.acos((-1)*(math.tan(Deg2Rad(declination_angle)))*(math.tan(Deg2Rad(latitude)))))
        sunset_solar_hour_angle = -(sunrise_solar_hour_angle)
        local_sunrise_time = solar_hour_angle2local_time(sunrise_solar_hour_angle)
        local_sunset_time = solar_hour_angle2local_time(-sunrise_solar_hour_angle)
    elif rooftype == "Gable":
        local_gable_sunrise_solar_hour_angle_list = []
        local_gable_sunset_solar_hour_angle_list  = []
        horizontal_plane_sunrise_solar_hour_angle = Rad2Deg(math.acos((-1)*(math.tan(Deg2Rad(declination_angle)))*(math.tan(Deg2Rad(latitude)))))
        local_gable_sunrise_solar_hour_angle_list.append(horizontal_plane_sunrise_solar_hour_angle)
        local_gable_sunset_solar_hour_angle_list.append(horizontal_plane_sunrise_solar_hour_angle)
        x_factor = ( ( ((math.cos(Deg2Rad(latitude)))*(math.cos(Deg2Rad(rooftop_slope_angle)))*(math.cos(Deg2Rad(declination_angle)))) + ((math.sin(Deg2Rad(latitude)))*(math.sin(Deg2Rad(rooftop_slope_angle)))*(math.cos(Deg2Rad(rooftop_azimuth_angle)))*(math.cos(Deg2Rad(declination_angle)))) ) / ( (math.cos(Deg2Rad(declination_angle)))*(math.sin(Deg2Rad(rooftop_slope_angle)))*(math.sin(Deg2Rad(rooftop_azimuth_angle))) ) )
        y_factor = ( ( ((math.sin(Deg2Rad(latitude)))*(math.cos(Deg2Rad(rooftop_slope_angle)))*(math.sin(Deg2Rad(declination_angle)))) - ((math.cos(Deg2Rad(latitude)))*(math.sin(Deg2Rad(rooftop_slope_angle)))*(math.cos(Deg2Rad(rooftop_azimuth_angle)))*(math.sin(Deg2Rad(declination_angle)))) ) / ( (math.cos(Deg2Rad(declination_angle)))*(math.sin(Deg2Rad(rooftop_slope_angle)))*(math.sin(Deg2Rad(rooftop_azimuth_angle))) ) )
        if rooftop_azimuth_angle > 0:
            inclined_plane_sunrise_solar_hour_angle = Rad2Deg(math.acos( ( ((-1)*(x_factor)*(y_factor)) - (math.sqrt(((x_factor)**2)-((y_factor)**2)+(1))) ) / (((x_factor)**2)+1) ))
            local_gable_sunrise_solar_hour_angle_list.append(inclined_plane_sunrise_solar_hour_angle)
            sunrise_solar_hour_angle = min(local_gable_sunrise_solar_hour_angle_list)
            local_sunrise_time = solar_hour_angle2local_time(sunrise_solar_hour_angle)

            inclined_plane_sunset_solar_hour_angle = Rad2Deg(math.acos( ( ((-1)*(x_factor)*(y_factor)) + (math.sqrt(((x_factor)**2)-((y_factor)**2)+(1))) ) / (((x_factor)**2)+1) ))
            local_gable_sunset_solar_hour_angle_list.append(inclined_plane_sunset_solar_hour_angle)
            sunset_solar_hour_angle = (-1)*(min(local_gable_sunset_solar_hour_angle_list))
            local_sunset_time = solar_hour_angle2local_time(sunset_solar_hour_angle)
        elif rooftop_azimuth_angle < 0:
            inclined_plane_sunrise_solar_hour_angle = Rad2Deg(math.acos( ( ((-1)*(x_factor)*(y_factor)) + (math.sqrt(((x_factor)**2)-((y_factor)**2)+(1))) ) / (((x_factor)**2)+1) ))
            local_gable_sunrise_solar_hour_angle_list.append(inclined_plane_sunrise_solar_hour_angle)
            sunrise_solar_hour_angle = min(local_gable_sunrise_solar_hour_angle_list)
            local_sunrise_time = solar_hour_angle2local_time(sunrise_solar_hour_angle)

            inclined_plane_sunset_solar_hour_angle = Rad2Deg(math.acos( ( ((-1)*(x_factor)*(y_factor)) - (math.sqrt(((x_factor)**2)-((y_factor)**2)+(1))) ) / (((x_factor)**2)+1) ))
            local_gable_sunset_solar_hour_angle_list.append(inclined_plane_sunset_solar_hour_angle)
            sunset_solar_hour_angle = (-1)*(min(local_gable_sunset_solar_hour_angle_list))
            local_sunset_time = solar_hour_angle2local_time(sunset_solar_hour_angle)
        elif rooftop_azimuth_angle == 0:
            inclined_plane_sunrise_solar_hour_angle1 = Rad2Deg(math.acos((-1)*(math.tan(Deg2Rad(declination_angle)))*(math.tan(Deg2Rad(latitude)))))
            local_gable_sunrise_solar_hour_angle_list.append(inclined_plane_sunrise_solar_hour_angle1)
            inclined_plane_sunrise_solar_hour_angle2 = Rad2Deg(math.acos((-1)*(math.tan(Deg2Rad(declination_angle)))*(math.tan((Deg2Rad(latitude))-(Deg2Rad(rooftop_slope_angle))))))
            local_gable_sunrise_solar_hour_angle_list.append(inclined_plane_sunrise_solar_hour_angle2)
            sunrise_solar_hour_angle = min(local_gable_sunrise_solar_hour_angle_list)
            local_sunrise_time = solar_hour_angle2local_time(sunrise_solar_hour_angle)
            sunset_solar_hour_angle = (-1)*(min(local_gable_sunrise_solar_hour_angle_list))
            local_sunset_time = solar_hour_angle2local_time(sunset_solar_hour_angle)
        else:
            sunrise_solar_hour_angle = Rad2Deg(math.acos((-1)*(math.tan(Deg2Rad(declination_angle)))*(math.tan(Deg2Rad(latitude)))))
            sunset_solar_hour_angle = -(sunrise_solar_hour_angle)
            local_sunrise_time = solar_hour_angle2local_time(sunrise_solar_hour_angle)
            local_sunset_time = solar_hour_angle2local_time(-sunrise_solar_hour_angle)
    elif rooftype == "Hip":
        local_hip_sunrise_solar_hour_angle_list = []
        local_hip_sunset_solar_hour_angle_list  = []
        horizontal_plane_sunrise_solar_hour_angle = Rad2Deg(math.acos((-1)*(math.tan(Deg2Rad(declination_angle)))*(math.tan(Deg2Rad(latitude)))))
        local_hip_sunrise_solar_hour_angle_list.append(horizontal_plane_sunrise_solar_hour_angle)
        local_hip_sunset_solar_hour_angle_list.append(horizontal_plane_sunrise_solar_hour_angle)
        x_factor = ( ( ((math.cos(Deg2Rad(latitude)))*(math.cos(Deg2Rad(rooftop_slope_angle)))*(math.cos(Deg2Rad(declination_angle)))) + ((math.sin(Deg2Rad(latitude)))*(math.sin(Deg2Rad(rooftop_slope_angle)))*(math.cos(Deg2Rad(rooftop_azimuth_angle)))*(math.cos(Deg2Rad(declination_angle)))) ) / ( (math.cos(Deg2Rad(declination_angle)))*(math.sin(Deg2Rad(rooftop_slope_angle)))*(math.sin(Deg2Rad(rooftop_azimuth_angle))) ) )
        y_factor = ( ( ((math.sin(Deg2Rad(latitude)))*(math.cos(Deg2Rad(rooftop_slope_angle)))*(math.sin(Deg2Rad(declination_angle)))) - ((math.cos(Deg2Rad(latitude)))*(math.sin(Deg2Rad(rooftop_slope_angle)))*(math.cos(Deg2Rad(rooftop_azimuth_angle)))*(math.sin(Deg2Rad(declination_angle)))) ) / ( (math.cos(Deg2Rad(declination_angle)))*(math.sin(Deg2Rad(rooftop_slope_angle)))*(math.sin(Deg2Rad(rooftop_azimuth_angle))) ) )
        if rooftop_azimuth_angle > 0:
            inclined_plane_sunrise_solar_hour_angle = Rad2Deg(math.acos( ( ((-1)*(x_factor)*(y_factor)) - (math.sqrt(((x_factor)**2)-((y_factor)**2)+(1))) ) / (((x_factor)**2)+1) ))
            local_hip_sunrise_solar_hour_angle_list.append(inclined_plane_sunrise_solar_hour_angle)
            sunrise_solar_hour_angle = min(local_hip_sunrise_solar_hour_angle_list)
            local_sunrise_time = solar_hour_angle2local_time(sunrise_solar_hour_angle)

            inclined_plane_sunset_solar_hour_angle = Rad2Deg(math.acos( ( ((-1)*(x_factor)*(y_factor)) + (math.sqrt(((x_factor)**2)-((y_factor)**2)+(1))) ) / (((x_factor)**2)+1) ))
            local_hip_sunset_solar_hour_angle_list.append(inclined_plane_sunset_solar_hour_angle)
            sunset_solar_hour_angle = (-1)*(min(local_hip_sunset_solar_hour_angle_list))
            local_sunset_time = solar_hour_angle2local_time(sunset_solar_hour_angle)
        elif rooftop_azimuth_angle < 0:
            inclined_plane_sunrise_solar_hour_angle = Rad2Deg(math.acos( ( ((-1)*(x_factor)*(y_factor)) + (math.sqrt(((x_factor)**2)-((y_factor)**2)+(1))) ) / (((x_factor)**2)+1) ))
            local_hip_sunrise_solar_hour_angle_list.append(inclined_plane_sunrise_solar_hour_angle)
            sunrise_solar_hour_angle = min(local_hip_sunrise_solar_hour_angle_list)
            local_sunrise_time = solar_hour_angle2local_time(sunrise_solar_hour_angle)

            inclined_plane_sunset_solar_hour_angle = Rad2Deg(math.acos( ( ((-1)*(x_factor)*(y_factor)) - (math.sqrt(((x_factor)**2)-((y_factor)**2)+(1))) ) / (((x_factor)**2)+1) ))
            local_hip_sunset_solar_hour_angle_list.append(inclined_plane_sunset_solar_hour_angle)
            sunset_solar_hour_angle = (-1)*(min(local_hip_sunset_solar_hour_angle_list))
            local_sunset_time = solar_hour_angle2local_time(sunset_solar_hour_angle)
        elif rooftop_azimuth_angle == 0:
            inclined_plane_sunrise_solar_hour_angle1 = Rad2Deg(math.acos((-1)*(math.tan(Deg2Rad(declination_angle)))*(math.tan(Deg2Rad(latitude)))))
            local_hip_sunrise_solar_hour_angle_list.append(inclined_plane_sunrise_solar_hour_angle1)
            inclined_plane_sunrise_solar_hour_angle2 = Rad2Deg(math.acos((-1)*(math.tan(Deg2Rad(declination_angle)))*(math.tan((Deg2Rad(latitude))-(Deg2Rad(rooftop_slope_angle))))))
            local_hip_sunrise_solar_hour_angle_list.append(inclined_plane_sunrise_solar_hour_angle2)
            sunrise_solar_hour_angle = min(local_hip_sunrise_solar_hour_angle_list)
            local_sunrise_time = solar_hour_angle2local_time(sunrise_solar_hour_angle)
            sunset_solar_hour_angle = (-1)*(min(local_hip_sunrise_solar_hour_angle_list))
            local_sunset_time = solar_hour_angle2local_time(sunset_solar_hour_angle)
        else:
            sunrise_solar_hour_angle = Rad2Deg(math.acos((-1)*(math.tan(Deg2Rad(declination_angle)))*(math.tan(Deg2Rad(latitude)))))
            sunset_solar_hour_angle = -(sunrise_solar_hour_angle)
            local_sunrise_time = solar_hour_angle2local_time(sunrise_solar_hour_angle)
            local_sunset_time = solar_hour_angle2local_time(-sunrise_solar_hour_angle)

    #print(f'Sunrise Solar Hour Angle: {sunrise_solar_hour_angle}, Local Sunrise Time: {local_sunrise_time}, Local Sunset Time: {local_sunset_time} ')
    return  sunrise_solar_hour_angle, sunset_solar_hour_angle, local_sunrise_time, local_sunset_time

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

# Roof Inclination Calculation Function (Slope)
def rooftop_geometry_function(vertices_attribute_csvfile_name):
    vertices_attribute_df = pd.read_csv(vertices_attribute_csvfile_name)

    global_building_width_df = pd.DataFrame([])
    global_building_length_df = pd.DataFrame([])
    global_rooftop_incline_df = pd.DataFrame([])
    global_rooftop_azimuth_angle_df = pd.DataFrame([])
    global_rooftop_geometry_df = pd.DataFrame([])

    new_global_rooftop_geometry_df = pd.DataFrame([])

    previous_uid = "null"
    n=0

    for uid in vertices_attribute_df['uid']:
        n+=1
        program_name = "ROOFTOP GEOMETRY FUNCTION"
        rooftop_geometry_field_length = len(vertices_attribute_df['uid'])
        if n == 1:
            print(f"\nPROCESSING {program_name}-(0/4)...")
        elif n == int(rooftop_geometry_field_length*(1/4)):
            print(f"PROCESSING {program_name}-(1/4)...")
        elif n == int(rooftop_geometry_field_length*(2/4)):
            print(f"PROCESSING {program_name}-(2/4)...")
        elif n == int(rooftop_geometry_field_length*(3/4)):
            print(f"PROCESSING {program_name}-(3/4)...")
        elif n == int(rooftop_geometry_field_length-1*(4/4)):
            print(f"PROCESSING {program_name}-(4/4)...")

        distance_buffer_list = []
        distance_between_vertex_list = []

        local_vertex1_coordinate_df = pd.DataFrame([])
        local_vertex2_coordinate_df = pd.DataFrame([])

        if uid != previous_uid:
            uid_vertices_filter = (vertices_attribute_df['uid'] == uid)
            local_uid_vertices_attribute_df = vertices_attribute_df.loc[uid_vertices_filter, ['uid', 'heightmax', 'rooftop', 'rooftype', 'area', 'vertex_index', 'distance', 'lat', 'long']]
            local_uid_vertices_attribute_df = local_uid_vertices_attribute_df.reset_index(drop=True)

            #print(f'\nuid vertices attribute table:\n{local_uid_vertices_attribute_df}')
            previous_uid = uid

            local_uid_max_vertex_index = local_uid_vertices_attribute_df['vertex_index'].max()

            for vertex_index in range (0,local_uid_max_vertex_index+1):
                vertex1_distance = local_uid_vertices_attribute_df.loc[vertex_index, 'distance']
                vertex1_coordinate_df = local_uid_vertices_attribute_df.loc[vertex_index, ['lat', 'long']]
                if vertex_index == local_uid_max_vertex_index:
                    vertex2_distance = local_uid_vertices_attribute_df.loc[vertex_index, 'distance']
                else:
                    vertex2_distance = local_uid_vertices_attribute_df.loc[vertex_index+1, 'distance']
                    vertex2_coordinate_df = local_uid_vertices_attribute_df.loc[vertex_index+1, ['lat', 'long']]

                distance_between_vertex = abs(vertex2_distance - vertex1_distance)
                if distance_between_vertex > 0:
                    distance_between_vertex_list.append(distance_between_vertex)

                local_vertex1_coordinate_df = pd.concat([local_vertex1_coordinate_df, vertex1_coordinate_df], axis=1)
                local_vertex2_coordinate_df = pd.concat([local_vertex2_coordinate_df, vertex2_coordinate_df], axis=1)

            #print(f'Distance Between Vertex: \n{pd.DataFrame(distance_between_vertex_list)}')

            local_vertex1_coordinate_df = local_vertex1_coordinate_df.transpose()
            local_vertex1_coordinate_df = local_vertex1_coordinate_df.reset_index(drop=True)
            local_vertex1_coordinate_df.columns = ['vertex1_lat', 'vertex1_long']

            local_vertex2_coordinate_df = local_vertex2_coordinate_df.transpose()
            local_vertex2_coordinate_df = local_vertex2_coordinate_df.reset_index(drop=True)
            local_vertex2_coordinate_df.columns = ['vertex2_lat', 'vertex2_long']

            distance_between_vertex_df = pd.DataFrame(distance_between_vertex_list)
            distance_between_vertex_df = distance_between_vertex_df.reset_index(drop=True)
            distance_between_vertex_df.columns = ['distance']

            local_uid_building_coordinate_df = pd.concat([distance_between_vertex_df, local_vertex1_coordinate_df, local_vertex2_coordinate_df], axis=1)
            #print(f'\nuid:{uid} vertex coordinate:\n{local_uid_building_coordinate_df}')
            
            distance_between_vertex_list.sort()
            distance_between_vertex_list.reverse()

            # Checking Square or Rectangle or Complex building Shape
            if len(distance_between_vertex_list) == 4:
                # Square or Rectangle Building Shape
                building_perimeter = sum(distance_between_vertex_list)
                average_building_size = building_perimeter/4
                if (average_building_size+0.1) >= distance_between_vertex_list[0] >= (average_building_size-0.1):
                    distance_between_vertex_list_index = 1
                else:
                    distance_between_vertex_list_index = 2
            elif len(distance_between_vertex_list) > 4:
                # Complex Building Shape
                distance_between_vertex_list_index = 3
            elif len(distance_between_vertex_list) < 4:
                distance_between_vertex_list_index = 1
            else:
                distance_between_vertex_list_index = 3

            building_length = max(distance_between_vertex_list)
            building_width = distance_between_vertex_list[distance_between_vertex_list_index]
            building_width_condition_check = (building_length >= building_width > 0)

            while building_width_condition_check == False :
                distance_between_vertex_list_index +=1
                building_width = distance_between_vertex_list[distance_between_vertex_list_index]
                building_width_condition_check = (building_length >= building_width > 0)

            # Calculate Building Azimuth Angle that parallel with building width
            rooftop_azimuth_angle_filter = (local_uid_building_coordinate_df['distance'] == building_width)
            # Vertex1 Coordinate (latitude1, longitude1)
            rooftop_azimuth_angle_vertex1_lat_series = local_uid_building_coordinate_df.loc[rooftop_azimuth_angle_filter, 'vertex1_lat']
            rooftop_azimuth_angle_vertex1_lat = rooftop_azimuth_angle_vertex1_lat_series.iloc[0]
            rooftop_azimuth_angle_vertex1_long_series = local_uid_building_coordinate_df.loc[rooftop_azimuth_angle_filter, 'vertex1_long']
            rooftop_azimuth_angle_vertex1_long = rooftop_azimuth_angle_vertex1_long_series.iloc[0]
            # Vertex2 Coordinate (latitude2, longitude2)
            rooftop_azimuth_angle_vertex2_lat_series = local_uid_building_coordinate_df.loc[rooftop_azimuth_angle_filter, 'vertex2_lat']
            rooftop_azimuth_angle_vertex2_lat = rooftop_azimuth_angle_vertex2_lat_series.iloc[0]
            rooftop_azimuth_angle_vertex2_long_series = local_uid_building_coordinate_df.loc[rooftop_azimuth_angle_filter, 'vertex2_long']
            rooftop_azimuth_angle_vertex2_long = rooftop_azimuth_angle_vertex2_long_series.iloc[0]

            # Azimuth Angle Calculation
            difference_in_lat = rooftop_azimuth_angle_vertex2_lat - rooftop_azimuth_angle_vertex1_lat
            difference_in_long = rooftop_azimuth_angle_vertex2_long - rooftop_azimuth_angle_vertex1_long
            if difference_in_lat > 0 and difference_in_long >= 0:
                rooftop_azimuth_angle = Rad2Deg((math.atan(difference_in_long/difference_in_lat))+(math.pi/2))
            elif difference_in_lat == 0 and difference_in_long > 0:
                rooftop_azimuth_angle = Rad2Deg(math.pi)
            elif difference_in_lat < 0 and difference_in_long >= 0:
                rooftop_azimuth_angle = Rad2Deg((math.atan(difference_in_long/difference_in_lat))-(math.pi/2))
            elif difference_in_lat < 0 and difference_in_long <= 0:
                rooftop_azimuth_angle = Rad2Deg((math.atan(difference_in_long/difference_in_lat))-(math.pi/2))
            elif difference_in_lat == 0 and difference_in_long < 0:
                rooftop_azimuth_angle = Rad2Deg(0)
            elif difference_in_lat > 0 and difference_in_long <= 0:
                rooftop_azimuth_angle = Rad2Deg((math.atan(difference_in_long/difference_in_lat))+(math.pi/2))
            
            # Rooftype Classification
            rooftype_filter = (vertices_attribute_df['uid'] == uid) & (vertices_attribute_df['vertex_index'] == 0)
            building_rooftype_series = vertices_attribute_df.loc[rooftype_filter, 'rooftype']
            building_rooftype = building_rooftype_series.iloc[0]

            #print(f'\nRooftype: {building_rooftype}')
            if building_rooftype == "Complex":
                rooftop_incline = 0
            elif building_rooftype == "Flat":
                rooftop_incline = 0
            else:
                building_rise_filter = (vertices_attribute_df['uid'] == uid) & (vertices_attribute_df['vertex_index'] == 0)
                building_rooftop_height_series = vertices_attribute_df.loc[building_rise_filter, 'rooftop']
                building_rooftop_height = building_rooftop_height_series.iloc[0]
                building_heightmax_series = vertices_attribute_df.loc[building_rise_filter, 'heightmax']
                building_heightmax = building_heightmax_series.iloc[0]

                rooftop_rise = building_rooftop_height - building_heightmax
                rooftop_run = building_width/2
                rooftop_incline = Rad2Deg(math.atan(rooftop_rise/rooftop_run))

        #print(f'{uid} Rooftop Incline: {rooftop_incline}')
        local_building_width_df = pd.DataFrame([building_width])
        global_building_width_df = pd.concat([global_building_width_df, local_building_width_df])

        local_building_length_df = pd.DataFrame([building_length])
        global_building_length_df = pd.concat([global_building_length_df, local_building_length_df])

        local_rooftop_incline_df = pd.DataFrame([rooftop_incline])
        global_rooftop_incline_df = pd.concat([global_rooftop_incline_df, local_rooftop_incline_df])

        local_rooftop_azimuth_angle_df = pd.DataFrame([rooftop_azimuth_angle])
        global_rooftop_azimuth_angle_df = pd.concat([global_rooftop_azimuth_angle_df, local_rooftop_azimuth_angle_df])

    global_building_width_df = global_building_width_df.reset_index(drop=True)
    global_building_width_df.columns = ['width']

    global_building_length_df = global_building_length_df.reset_index(drop=True)
    global_building_length_df.columns = ['length']

    global_rooftop_incline_df = global_rooftop_incline_df.reset_index(drop=True)
    global_rooftop_incline_df.columns = ['rooftop slope']

    global_rooftop_azimuth_angle_df = global_rooftop_azimuth_angle_df.reset_index(drop=True)
    global_rooftop_azimuth_angle_df.columns = ['rooftop azimuth angle']

    global_rooftop_geometry_df = pd.concat([global_building_width_df, global_building_length_df, global_rooftop_incline_df, global_rooftop_azimuth_angle_df], axis=1)

    vertices_global_rooftop_geometry_df = pd.concat([vertices_attribute_df, global_rooftop_geometry_df], axis=1)

    previous_uid = "Null"
    for uid in vertices_global_rooftop_geometry_df['uid']:
        if uid != previous_uid:
            uid_global_rooftop_filter = (vertices_global_rooftop_geometry_df['uid'] == uid) & (vertices_global_rooftop_geometry_df['vertex_index'] == 0)
            uid_rooftop_df = vertices_global_rooftop_geometry_df.loc[uid_global_rooftop_filter]
            uid_rooftop_df = uid_rooftop_df.reset_index(drop=True)
            
            local_uid_rooftop_df = uid_rooftop_df
            new_global_rooftop_geometry_df = pd.concat([new_global_rooftop_geometry_df, local_uid_rooftop_df])
            previous_uid = uid

    new_global_rooftop_geometry_df = new_global_rooftop_geometry_df.reset_index(drop=True)
    #print(f'Rooftop Geometry:\n{new_global_rooftop_geometry_df}')

    return new_global_rooftop_geometry_df



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
def main():
   rooftype = "Hip"
   declination_angle = -23.01325091
   latitude = 16.4403
   rooftop_slope_angle = 17.07098538
   rooftop_azimuth_angle = -81.77363301

   
   sunrise_solar_hour_angle, sunset_solar_hour_angle, local_sunrise_time, local_sunset_time = rise_solar_hour_angle_function(rooftype,declination_angle, latitude, rooftop_slope_angle, rooftop_azimuth_angle)
   print(f'Sunrise HRA: {sunrise_solar_hour_angle}, Sunset HRA : {sunset_solar_hour_angle}')
   print(f'local Sunrise Time: {local_sunrise_time}, local Sunset Time: {local_sunset_time}')


#main()
