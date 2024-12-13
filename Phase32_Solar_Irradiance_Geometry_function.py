#Calcualtion
import math
import numpy as np
import csv
import pandas as pd
import time


# Output of Solar Radiation Geometry: Delicnation, Solar Hour Angle, Zenith
def solar_irradiance_geometry_function(uid, building_fields_table_df, julian_date_df, local_standard_time_df, global_rooftop_geometry_df, global_solar_irradiance_geometry_csvfile_location, steps, std_longitude, start_time, stop_time):
    start_time_record    = time.time()
    # Checking Input
    longitude   = building_fields_table_df.loc[0,'lat']
    latitude    = building_fields_table_df.loc[0,'long']
    #print(f'\nUID: {uid}, Latitude: {latitude}, Longitude: {longitude}')

    # Data Frame Time Fields
    # No. of days in a year
    end_julian_date         = julian_date_df.shape[0]
    # Julian Date Calculation Data Frame
    julian_date_calculation_df = pd.DataFrame(julian_date_df[['julian date']].transpose().values.tolist()*local_standard_time_df.shape[1]).transpose()

    # Standard Longitude at Khon Kaen Province is 102.5 degree
    std_longitude_df        = pd.DataFrame([list([std_longitude]*local_standard_time_df.shape[1])]*julian_date_df.shape[0])

    # Separtor Data Frame
    separator_df            = create_separator_df_function(end_julian_date)

    # Acquire Rooftop Geometry from Rooftop Geometry Data Frame
    global_rooftop_geometry_filter              = (global_rooftop_geometry_df['uid'] == uid)
    local_uid_rooftop_geometry_df               = global_rooftop_geometry_df.loc[global_rooftop_geometry_filter,  ['width', 'length', 'rooftop slope', 'rooftop azimuth angle']]
    local_uid_rooftop_geometry_df.columns       = ['rooftop width', 'rooftop length', 'rooftop slope', 'rooftop azimuth angle']
    local_uid_rooftop_geometry_df               = local_uid_rooftop_geometry_df.reset_index(drop=True)

    # Building Characteristic Tables Data Frame
    new_building_fields_tables_df_column_index  = ['uid', 'lat', 'long', 'height', 'area', 'rooftype', 'rooftop', 'rooftop width', 'rooftop length', 'rooftop slope', 'rooftop azimuth angle']
    new_building_fields_tables_df               = pd.DataFrame((pd.concat([building_fields_table_df, local_uid_rooftop_geometry_df], axis=1).values.tolist())*end_julian_date, columns=new_building_fields_tables_df_column_index)
    #print("\nnew local buidling fields table df:\n", new_building_fields_tables_df)

    # Building Characteristic Fields
    longitude_series                = new_building_fields_tables_df['long']
    latitude_series                 = new_building_fields_tables_df['lat']
    rooftype_series                 = new_building_fields_tables_df['rooftype']
    rooftop_slope_angle_series      = new_building_fields_tables_df['rooftop slope']
    rooftop_azimuth_angle_series    = new_building_fields_tables_df['rooftop azimuth angle']

    # Longitude Calculation Data Frame
    longitude_calculation_df                = pd.DataFrame([longitude_series.values.tolist()]*local_standard_time_df.shape[1]).transpose()
    # Latitude Calculation Data Frame
    latitude_calculation_df                 = pd.DataFrame([latitude_series.values.tolist()]*local_standard_time_df.shape[1]).transpose()
    # Rooftop Slope Angle Data Frame
    rooftop_slope_angle_calculaiton_df      = pd.DataFrame([rooftop_slope_angle_series.values.tolist()]*local_standard_time_df.shape[1]).transpose()
    # Rooftop Azimuth Angle Data Frame
    rooftop_azimuth_angle_calculation_df    = pd.DataFrame([rooftop_azimuth_angle_series.values.tolist()]*local_standard_time_df.shape[1]).transpose()

    # Declination Calculation
    declination_angle_df                    = declination_angle_function(julian_date_df[['julian date']])
    declination_angle_df.columns            = ['Declination Angle']
    declination_angle_calculation_df        = pd.DataFrame(declination_angle_df.transpose().values.tolist()*local_standard_time_df.shape[1]).transpose()

    # Eccentricity Correction Factor
    eccentricity_correction_factor_df           = eccentricity_correction_factor_function(julian_date_df[['julian date']])
    eccentricity_correction_factor_df.columns   = ['Eccentricity Correction Factor']
    #print('\nEccentricity Correction Factor Data Frame:\n', eccentricity_correction_factor_df)

    # Solar Hour Angle Calculation
    solar_hour_angle_df = solar_hour_angle_function(julian_date_calculation_df, local_standard_time_df, std_longitude_df, longitude_calculation_df)

    # Altitude Angle Calculation
    altitude_angle_df   = altitude_angle_function(declination_angle_calculation_df, latitude_calculation_df, solar_hour_angle_df)

    # Azimuth Angle Calculation
    azimuth_angle_df    = azimuth_angle_function(declination_angle_calculation_df, altitude_angle_df, solar_hour_angle_df)

    # Zenith Angle Calculaltion
    if rooftype_series[0] == "Flat":
        zenith_angle_df = zenith_angle_on_horizontal_plane_function(declination_angle_calculation_df, latitude_calculation_df, solar_hour_angle_df)
    elif rooftype_series[0] == "Complex":
        zenith_angle_df = zenith_angle_on_horizontal_plane_function(declination_angle_calculation_df, latitude_calculation_df, solar_hour_angle_df)
    elif rooftype_series[0] == "Gable":
        zenith_angle_gable_condition1 = zenith_angle_on_inclined_plane_facing_south_direction_function(declination_angle_calculation_df, latitude_calculation_df, solar_hour_angle_df, rooftop_slope_angle_calculaiton_df)
        rooftop_azimuth_angle_calculation_side1_df = rooftop_azimuth_angle_calculation_df.copy()
        if 180 >= rooftop_azimuth_angle_series[0] > 0 :
            rooftop_azimuth_angle_calculation_side2_df = rooftop_azimuth_angle_calculation_df.copy() - 180
        elif 0 > rooftop_azimuth_angle_series[0] >= -180:
            rooftop_azimuth_angle_calculation_side2_df = rooftop_azimuth_angle_calculation_df.copy() + 180
        zenith_angle_gable_condition2_side1 = zenith_angle_on_inclined_plane_facing_any_direction_function(declination_angle_calculation_df, latitude_calculation_df, solar_hour_angle_df, rooftop_slope_angle_calculaiton_df, rooftop_azimuth_angle_calculation_side1_df)
        zenith_angle_gable_condition2_side2 = zenith_angle_on_inclined_plane_facing_any_direction_function(declination_angle_calculation_df, latitude_calculation_df, solar_hour_angle_df, rooftop_slope_angle_calculaiton_df, rooftop_azimuth_angle_calculation_side2_df)
        zenith_angle_gable_condition2       = pd.DataFrame(np.where(zenith_angle_gable_condition2_side1<zenith_angle_gable_condition2_side2, zenith_angle_gable_condition2_side1, zenith_angle_gable_condition2_side2))
        zenith_angle_df                     = pd.DataFrame(np.where(rooftop_azimuth_angle_calculation_df==0, zenith_angle_gable_condition1, zenith_angle_gable_condition2))
    elif rooftype_series[0] == "Hip":
        zenith_angle_hip_condition1 = zenith_angle_on_inclined_plane_facing_south_direction_function(declination_angle_calculation_df, latitude_calculation_df, solar_hour_angle_df, rooftop_slope_angle_calculaiton_df)
        rooftop_azimuth_angle_calculation_side1_df = rooftop_azimuth_angle_calculation_df.copy()
        if 180 >= rooftop_azimuth_angle_series[0] > 0:
            rooftop_azimuth_angle_calculation_side2_df = rooftop_azimuth_angle_calculation_df.copy() - 180
        elif 0 > rooftop_azimuth_angle_series[0] >= -180:
            rooftop_azimuth_angle_calculation_side2_df = rooftop_azimuth_angle_calculation_df.copy() + 180

        if 180 >= rooftop_azimuth_angle_series[0] > 90:
            rooftop_azimuth_angle_calculation_side3_df = rooftop_azimuth_angle_calculation_df.copy() - 270
        elif 90 >= rooftop_azimuth_angle_series[0] >= -180:
            rooftop_azimuth_angle_calculation_side3_df = rooftop_azimuth_angle_calculation_df.copy() + 90

        if -90 > rooftop_azimuth_angle_series[0] >= -180:
            rooftop_azimuth_angle_calculation_side4_df = rooftop_azimuth_angle_calculation_df.copy() + 270
        elif 180 >= rooftop_azimuth_angle_series[0] >= -90:
            rooftop_azimuth_angle_calculation_side4_df = rooftop_azimuth_angle_calculation_df.copy() - 90
        zenith_angle_hip_condition2_side1 = zenith_angle_on_inclined_plane_facing_any_direction_function(declination_angle_calculation_df, latitude_calculation_df, solar_hour_angle_df, rooftop_slope_angle_calculaiton_df, rooftop_azimuth_angle_calculation_side1_df)
        zenith_angle_hip_condition2_side2 = zenith_angle_on_inclined_plane_facing_any_direction_function(declination_angle_calculation_df, latitude_calculation_df, solar_hour_angle_df, rooftop_slope_angle_calculaiton_df, rooftop_azimuth_angle_calculation_side2_df)
        zenith_angle_hip_condition2_side3 = zenith_angle_on_inclined_plane_facing_any_direction_function(declination_angle_calculation_df, latitude_calculation_df, solar_hour_angle_df, rooftop_slope_angle_calculaiton_df, rooftop_azimuth_angle_calculation_side3_df)
        zenith_angle_hip_condition2_side4 = zenith_angle_on_inclined_plane_facing_any_direction_function(declination_angle_calculation_df, latitude_calculation_df, solar_hour_angle_df, rooftop_slope_angle_calculaiton_df, rooftop_azimuth_angle_calculation_side4_df)

        zenith_angle_hip_condition2_filter_condition1 = (zenith_angle_hip_condition2_side1<zenith_angle_hip_condition2_side2)&(zenith_angle_hip_condition2_side1<zenith_angle_hip_condition2_side3)&(zenith_angle_hip_condition2_side1<zenith_angle_hip_condition2_side4)
        zenith_angle_hip_condition2_filter_condition2 = (zenith_angle_hip_condition2_side2<zenith_angle_hip_condition2_side1)&(zenith_angle_hip_condition2_side2<zenith_angle_hip_condition2_side3)&(zenith_angle_hip_condition2_side2<zenith_angle_hip_condition2_side4)
        zenith_angle_hip_condition2_filter_condition3 = (zenith_angle_hip_condition2_side3<zenith_angle_hip_condition2_side1)&(zenith_angle_hip_condition2_side3<zenith_angle_hip_condition2_side2)&(zenith_angle_hip_condition2_side3<zenith_angle_hip_condition2_side4)
        zenith_angle_hip_condition2_filter_condition4 = (zenith_angle_hip_condition2_side4<zenith_angle_hip_condition2_side1)&(zenith_angle_hip_condition2_side4<zenith_angle_hip_condition2_side2)&(zenith_angle_hip_condition2_side4<zenith_angle_hip_condition2_side3)
        zenith_angle_hip_condition2_filter_conditions = [zenith_angle_hip_condition2_filter_condition1, zenith_angle_hip_condition2_filter_condition2, zenith_angle_hip_condition2_filter_condition3, zenith_angle_hip_condition2_filter_condition4]

        zenith_angle_hip_condition2_filter_choices = [zenith_angle_hip_condition2_side1,zenith_angle_hip_condition2_side2, zenith_angle_hip_condition2_side3, zenith_angle_hip_condition2_side4]

        zenith_angle_hip_condition2 = pd.DataFrame(np.select(zenith_angle_hip_condition2_filter_conditions, zenith_angle_hip_condition2_filter_choices, 0))
        zenith_angle_df = pd.DataFrame(np.where(rooftop_azimuth_angle_calculation_df==0, zenith_angle_hip_condition1, zenith_angle_hip_condition2))
        
    # Sunrise and Sunset Calcultions
    sunrise_solar_hour_angle_df, sunset_solar_hour_angle_df, local_sunrise_time_df, local_sunset_time_df = rise_solar_hour_angle_function(rooftype_series[0],declination_angle_df['Declination Angle'], latitude_series, rooftop_slope_angle_series, rooftop_azimuth_angle_series)

    # Organize Solar Hour Angle into Global Data Frame
    # Data Frame Column Index
    # Solar Hour Angle Data Frame Column Index
    solar_hour_angle_df_column_index    = list(f"Solar Hour Angle-{hour_time}:{minute_time}" for hour_time in range(start_time,stop_time+1) for minute_time in range(0,60,steps))
    solar_hour_angle_global_df          = solar_hour_angle_df.copy().round(6)
    solar_hour_angle_global_df.columns  = solar_hour_angle_df_column_index
    #print(f'\nGlobal Solar Hour Angle Data Frame:\n', solar_hour_angle_global_df)

    # Organize Altitude Angle into Global Data Frame
    # Sun Altitude Angle Data Frame Column Index
    altitude_angle_df_column_index      = list(f"Altitude-{hour_time}:{minute_time}" for hour_time in range(start_time,stop_time+1) for minute_time in range(0,60,steps))
    altitude_angle_global_df            = altitude_angle_df.copy().round(6)
    altitude_angle_global_df.columns    = altitude_angle_df_column_index
    #print(f'\nGlobal Altitude Angle Data Frame:\n', altitude_angle_global_df)

    # Organize Azimuth Angle into Global Data Frame
    # Sun Azimuth Angle Data Frame Column Index
    azimuth_angle_df_column_index       = list(f"Azimuth-{hour_time}:{minute_time}" for hour_time in range(start_time,stop_time+1) for minute_time in range(0,60,steps))
    azimuth_angle_global_df             = azimuth_angle_df.copy().round(6)
    azimuth_angle_global_df.columns     = azimuth_angle_df_column_index
    #print(f'\nGlobal Azimuth Angle Data Frame:\n', azimuth_angle_global_df)

    # Organise Zenith Hour Angle into Global Data Frame
    # Sun Zenith Angle Data Frame Column Index
    zenith_angle_df_column_index        = list(f"Zenith-{hour_time}:{minute_time}" for hour_time in range(start_time,stop_time+1) for minute_time in range(0,60,steps))
    zenith_angle_global_df              = zenith_angle_df.copy().round(6)
    zenith_angle_global_df.columns      = zenith_angle_df_column_index
    #print('\nGlobal Zenith Angle Data Frame:\n', zenith_angle_global_df)
    
    # Date Field Data Frame
    date_field_df = pd.concat([julian_date_df, declination_angle_df, eccentricity_correction_factor_df, local_sunrise_time_df, local_sunset_time_df],axis=1)
    # Global Solar Irradiance Geometry Data Frame
    global_solar_irradiance_geometry_df = pd.concat([date_field_df, sunrise_solar_hour_angle_df, sunset_solar_hour_angle_df, solar_hour_angle_global_df, separator_df, altitude_angle_global_df, separator_df, azimuth_angle_global_df, separator_df, zenith_angle_global_df], axis=1)
    #print(f'\nSolar Radiance Geometery:\n', global_solar_irradiance_geometry_df)

    # Writing Data Frame to CSV File
    new_global_solar_irradiance_geometry_df = pd.concat([new_building_fields_tables_df ,global_solar_irradiance_geometry_df], axis=1)
    #print(new_global_solar_irradiance_geometry_df)
    

    # Create CSV File Name
    solar_irradiance_geometry_csvfile_local_name = f'Solar_Irradiance_Geometry_uid_{uid}'
    # Create CSV File to Store Global Irradiance Geometry Data
    writer, global_solar_irradiance_geometry_csvfile_name = create_csvfile(global_solar_irradiance_geometry_csvfile_location, solar_irradiance_geometry_csvfile_local_name)
    #print(f'CSV File name: {global_solar_irradiance_geometry_csvfile_name}')

    new_global_solar_irradiance_geometry_df.to_csv(global_solar_irradiance_geometry_csvfile_name, index=False)
    
    end_time_record    = time.time()
    total_time  = end_time_record - start_time_record
    print("\n***** DONE PROCESSING SOLAR IRRADIANCE GEOMETRY FUCNTION *****")
    print(f"Solar Irradaince Geometry Program Total execution time: {total_time:.4f} seconds")
    return date_field_df, solar_hour_angle_df, altitude_angle_df, azimuth_angle_df, zenith_angle_df

# Date and Time Function
def date_function():
    from datetime import date
    import calendar

    today = date.today()
    year = today.year
    if calendar.isleap(year):
        len_year = 366
    else:
        len_year = 365

    julian_date_df = pd.DataFrame(list(range(1,len_year+1)), columns=['julian date'])
    date_range = pd.date_range(f'{year}', periods=len(julian_date_df), freq='1d')
    date_df = pd.DataFrame(date_range, columns=['date'])
    # Combine Julian Date data frame with Date data frame
    date_df = pd.concat([date_df, julian_date_df], axis=1)
    #print(date_df)

    return date_df

# Declination Calculation Function (degree)
def declination_angle_function(julian_date_df):
    day_angle_df = day_angle_function(julian_date_df)
    declination_angle_df = ((0.006918)-(0.39912*(np.cos(day_angle_df)))+(0.070257*(np.sin(day_angle_df)))-(0.006758*(np.cos(2*day_angle_df)))+(0.000907*(np.sin(2*day_angle_df)))-(0.002697*(np.cos(3*day_angle_df)))+(0.00148*(np.sin(3*day_angle_df))))
    declination_angle_df = Rad2Deg(declination_angle_df)
    #print(f'Day: {julian_date}, Earth Decilnation Angle : {declination_angle}')
    
    return declination_angle_df.round(6)

# Eccentricity Correction Factor
def eccentricity_correction_factor_function(julian_date_df):
    day_angle_df = day_angle_function(julian_date_df)
    eccentricity_correction_factor_df = ((1.000110)+(0.034221*(np.cos(day_angle_df)))+(0.001280*(np.sin(day_angle_df)))+(0.000719*(np.cos(2*day_angle_df)))+(0.000077*(np.sin(2*day_angle_df))))
    return eccentricity_correction_factor_df.round(6)

# Solar Hour Angle (HRA) Calculation Function (degree)
def solar_hour_angle_function(julian_date_df, local_standard_time_df, std_longitude_df, longitude_df):
    # Solar Time Calculation
    solar_time_df= solar_time_function(julian_date_df, local_standard_time_df, std_longitude_df, longitude_df)
    # Solar Hour Angle Calculation
    solar_hour_angle = 15.0 * (12.0-solar_time_df)
    return solar_hour_angle.round(6)

# Altitude Angle Calculation Function (degree)
def altitude_angle_function(declination_angle_df, latitude_df, solar_hour_angle_df):
    altitude_angle_df = Rad2Deg(np.asin((  (np.sin(Deg2Rad(declination_angle_df)))  *  (np.sin(Deg2Rad(latitude_df)))  ) + (  (np.cos(Deg2Rad(declination_angle_df))) * (np.cos(Deg2Rad(latitude_df))) * (np.cos(Deg2Rad(solar_hour_angle_df)))  )))
    return altitude_angle_df.round(6)

# Azimuth Angle Calculation Function (degree)
def azimuth_angle_function(declination_angle_df, altitude_angle_df, solar_hour_angle_df):
    azimuth_angle_df = Rad2Deg(np.asin(  ((np.sin(Deg2Rad(solar_hour_angle_df))) * (np.cos(Deg2Rad(declination_angle_df)))) / (np.cos(Deg2Rad(altitude_angle_df))) ))
    return azimuth_angle_df.round(6)

# Zenith Angle on Horizontal Plane Calculation Function (degree)
def zenith_angle_on_horizontal_plane_function(declination_angle_df, latitude_df, solar_hour_angle_df):
    zenith_angle_df = Rad2Deg(np.acos( ((np.sin(Deg2Rad(declination_angle_df)))*(np.sin(Deg2Rad(latitude_df)))) + ((np.cos(Deg2Rad(declination_angle_df)))*(np.cos(Deg2Rad(latitude_df)))*(np.cos(Deg2Rad(solar_hour_angle_df)))) ))
    return zenith_angle_df.round(6)

# Zenith Angle on Inclined Plane that faced South Direction (degree)
def zenith_angle_on_inclined_plane_facing_south_direction_function(declination_angle_df, latitude_df, solar_hour_angle_df, rooftop_slope_angle_df):
    zenith_angle_df = Rad2Deg(np.acos( ((np.sin(Deg2Rad(declination_angle_df)))*(np.sin((Deg2Rad(latitude_df))-(Deg2Rad(rooftop_slope_angle_df))))) + ((np.cos(Deg2Rad(declination_angle_df)))*(np.cos((Deg2Rad(latitude_df))-(Deg2Rad(rooftop_slope_angle_df))))*(np.cos(Deg2Rad(solar_hour_angle_df)))) ))
    return zenith_angle_df.round(6)

# Zenith Angle on Inclined Plane that faced at any Azimuth Angle (degree)
def zenith_angle_on_inclined_plane_facing_any_direction_function(declination_angle_df, latitude_df, solar_hour_angle_df, rooftop_slope_angle_df, rooftop_azimuth_angle_df):
    zenith_angle_df = Rad2Deg(np.acos(((np.cos(Deg2Rad(declination_angle_df)))*(np.sin(Deg2Rad(rooftop_slope_angle_df)))*(np.sin(Deg2Rad(rooftop_azimuth_angle_df)))*(np.sin(Deg2Rad(solar_hour_angle_df)))) 
                                   + ((((np.cos(Deg2Rad(latitude_df)))*(np.cos(Deg2Rad(rooftop_slope_angle_df)))*(np.cos(Deg2Rad(declination_angle_df)))) + ((np.sin(Deg2Rad(latitude_df)))*(np.sin(Deg2Rad(rooftop_slope_angle_df)))*(np.cos(Deg2Rad(rooftop_azimuth_angle_df)))*(np.cos(Deg2Rad(declination_angle_df)))))*(np.cos(Deg2Rad(solar_hour_angle_df)))) 
                                   + ((np.sin(Deg2Rad(latitude_df)))*(np.cos(Deg2Rad(rooftop_slope_angle_df)))*(np.sin(Deg2Rad(declination_angle_df)))) 
                                   - ((np.cos(Deg2Rad(latitude_df)))*(np.sin(Deg2Rad(rooftop_slope_angle_df)))*(np.cos(Deg2Rad(rooftop_azimuth_angle_df)))*(np.sin(Deg2Rad(declination_angle_df)))) ))
    return zenith_angle_df.round(6)

# Solar Time Calculation Function (hour)
def solar_time_function(julian_date_df, local_standard_time_df, std_longitude_df, longitude_df):
    # Equation of Time Calculation
    e_t_df = equation_of_time_function(julian_date_df)
    # Solar Time Calculation
    solar_time_df = local_standard_time_df + (4*(-std_longitude_df + longitude_df)*(1/60)) + (e_t_df*(1/60))
    return solar_time_df

# Equation of Time Calculation Function (minute)
def equation_of_time_function(julian_date_df):
    day_angle_df = day_angle_function(julian_date_df)
    e_t_df = 229.18 * ((0.000075) + ((0.001868)*np.cos(day_angle_df)) - (0.032077*(np.sin(day_angle_df))) - (0.014615*(np.cos(2*day_angle_df))) - (0.040849*(np.sin(2 * day_angle_df))))
    return e_t_df

# Day Angle Calculation Function (radian)
def day_angle_function(julian_date_df):
    day_angle_df = (2*np.pi)*(julian_date_df)*(1/365)
    return day_angle_df

# Sunrise and Sunset Solar Angle Hour Calculaiton Function (degree)
def rise_solar_hour_angle_function(rooftype,declination_angle_df, latitude_df, rooftop_slope_angle_df, rooftop_azimuth_angle_df):
    if rooftype == "Flat":
        sunrise_solar_hour_angle_df                         = Rad2Deg(np.acos((-1)*(np.tan(Deg2Rad(declination_angle_df)))*(np.tan(Deg2Rad(latitude_df)))))
        sunset_solar_hour_angle_df                          = -(sunrise_solar_hour_angle_df)
        local_sunrise_time_df                               = solar_hour_angle2local_time(sunrise_solar_hour_angle_df)
        local_sunset_time_df                                = solar_hour_angle2local_time(-sunrise_solar_hour_angle_df)
    elif rooftype == "Complex":
        sunrise_solar_hour_angle_df                         = Rad2Deg(np.acos((-1)*(np.tan(Deg2Rad(declination_angle_df)))*(np.tan(Deg2Rad(latitude_df)))))
        sunset_solar_hour_angle_df                          = -(sunrise_solar_hour_angle_df)
        local_sunrise_time_df                               = solar_hour_angle2local_time(sunrise_solar_hour_angle_df)
        local_sunset_time_df                                = solar_hour_angle2local_time(-sunrise_solar_hour_angle_df)
    elif rooftype == "Gable":
        horizontal_plane_sunrise_solar_hour_angle_df        = Rad2Deg(np.acos((-1)*(np.tan(Deg2Rad(declination_angle_df)))*(np.tan(Deg2Rad(latitude_df)))))
        gable_rooftop_azimuth_angle_side1_df = rooftop_azimuth_angle_df.copy()
        if 180 >= rooftop_azimuth_angle_df[0] > 0 :
            gable_rooftop_azimuth_angle_side2_df = rooftop_azimuth_angle_df.copy() - 180
        elif 0 > rooftop_azimuth_angle_df[0] >= -180:
            gable_rooftop_azimuth_angle_side2_df = rooftop_azimuth_angle_df.copy() + 180

        def gable_rooftop_local_sunrise_sunset_time_calculation_function(horizontal_plane_sunrise_solar_hour_angle_df, rooftop_azimuth_angle_df, latitude_df, rooftop_slope_angle_df, declination_angle_df):
            x_factor                                        = ( ( ((np.cos(Deg2Rad(latitude_df)))*(np.cos(Deg2Rad(rooftop_slope_angle_df)))*(np.cos(Deg2Rad(declination_angle_df)))) + ((np.sin(Deg2Rad(latitude_df)))*(np.sin(Deg2Rad(rooftop_slope_angle_df)))*(np.cos(Deg2Rad(rooftop_azimuth_angle_df)))*(np.cos(Deg2Rad(declination_angle_df)))) ) / ( (np.cos(Deg2Rad(declination_angle_df)))*(np.sin(Deg2Rad(rooftop_slope_angle_df)))*(np.sin(Deg2Rad(rooftop_azimuth_angle_df))) ) )
            y_factor                                        = ( ( ((np.sin(Deg2Rad(latitude_df)))*(np.cos(Deg2Rad(rooftop_slope_angle_df)))*(np.sin(Deg2Rad(declination_angle_df)))) - ((np.cos(Deg2Rad(latitude_df)))*(np.sin(Deg2Rad(rooftop_slope_angle_df)))*(np.cos(Deg2Rad(rooftop_azimuth_angle_df)))*(np.sin(Deg2Rad(declination_angle_df)))) ) / ( (np.cos(Deg2Rad(declination_angle_df)))*(np.sin(Deg2Rad(rooftop_slope_angle_df)))*(np.sin(Deg2Rad(rooftop_azimuth_angle_df))) ) )
            # Gable Azimuth Angle Condition:
            gable_rooftype_condition1 = rooftop_azimuth_angle_df>0
            gable_rooftype_condition2 = rooftop_azimuth_angle_df<0
            gable_rooftype_condition3 = rooftop_azimuth_angle_df==0
            gable_rooftype_conditions = [gable_rooftype_condition1, gable_rooftype_condition2, gable_rooftype_condition3]
            # Gable Condition Local Sunrise Time and Local Sunset Time
            def gable_rooftop_azimuth_angle_df_more_than_zero(horizontal_plane_sunrise_solar_hour_angle_df, x_factor, y_factor):
                inclined_plane_sunrise_solar_hour_angle_df      = Rad2Deg(np.acos( ( ((-1)*(x_factor)*(y_factor)) - (np.sqrt(((x_factor)**2)-((y_factor)**2)+(1))) ) / (((x_factor)**2)+1) ))
                sunrise_solar_hour_angle_df                     = pd.DataFrame(np.where(inclined_plane_sunrise_solar_hour_angle_df<horizontal_plane_sunrise_solar_hour_angle_df, inclined_plane_sunrise_solar_hour_angle_df, horizontal_plane_sunrise_solar_hour_angle_df))
                local_sunrise_time_df                           = solar_hour_angle2local_time(sunrise_solar_hour_angle_df)

                inclined_plane_sunset_solar_hour_angle_df       = Rad2Deg(np.acos( ( ((-1)*(x_factor)*(y_factor)) + (np.sqrt(((x_factor)**2)-((y_factor)**2)+(1))) ) / (((x_factor)**2)+1) ))
                sunset_solar_hour_angle_df                      = pd.DataFrame(np.where(inclined_plane_sunset_solar_hour_angle_df<horizontal_plane_sunrise_solar_hour_angle_df, inclined_plane_sunset_solar_hour_angle_df, horizontal_plane_sunrise_solar_hour_angle_df))
                local_sunset_time_df                            = solar_hour_angle2local_time((-1)*sunset_solar_hour_angle_df)
                return sunrise_solar_hour_angle_df, sunset_solar_hour_angle_df, local_sunrise_time_df, local_sunset_time_df
            
            def gable_rooftop_azimuth_angle_df_less_than_zero(horizontal_plane_sunrise_solar_hour_angle_df, x_factor, y_factor):
                inclined_plane_sunrise_solar_hour_angle_df      = Rad2Deg(np.acos( ( ((-1)*(x_factor)*(y_factor)) + (np.sqrt(((x_factor)**2)-((y_factor)**2)+(1))) ) / (((x_factor)**2)+1) ))
                sunrise_solar_hour_angle_df                     = pd.DataFrame(np.where(inclined_plane_sunrise_solar_hour_angle_df<horizontal_plane_sunrise_solar_hour_angle_df, inclined_plane_sunrise_solar_hour_angle_df, horizontal_plane_sunrise_solar_hour_angle_df))
                local_sunrise_time_df                           = solar_hour_angle2local_time(sunrise_solar_hour_angle_df)

                inclined_plane_sunset_solar_hour_angle_df       = Rad2Deg(np.acos( ( ((-1)*(x_factor)*(y_factor)) - (np.sqrt(((x_factor)**2)-((y_factor)**2)+(1))) ) / (((x_factor)**2)+1) ))
                sunset_solar_hour_angle_df                     = pd.DataFrame(np.where(inclined_plane_sunset_solar_hour_angle_df<horizontal_plane_sunrise_solar_hour_angle_df, inclined_plane_sunset_solar_hour_angle_df, horizontal_plane_sunrise_solar_hour_angle_df))
                local_sunset_time_df                            = solar_hour_angle2local_time((-1)*sunset_solar_hour_angle_df)
                return sunrise_solar_hour_angle_df, sunset_solar_hour_angle_df, local_sunrise_time_df, local_sunset_time_df
            
            def gable_rooftop_azimuth_angle_df_is_zero(declination_angle_df, latitude_df, horizontal_plane_sunrise_solar_hour_angle_df):
                inclined_plane_sunrise_solar_hour_angle1_df         = Rad2Deg(np.acos((-1)*(np.tan(Deg2Rad(declination_angle_df)))*(np.tan(Deg2Rad(latitude_df)))))
                inclined_plane_sunrise_solar_hour_angle2_df         = Rad2Deg(np.acos((-1)*(np.tan(Deg2Rad(declination_angle_df)))*(np.tan((Deg2Rad(latitude_df))-(Deg2Rad(rooftop_slope_angle_df))))))
                local_gable_sunrise_solar_hour_angle_df_condition1  = (inclined_plane_sunrise_solar_hour_angle1_df<horizontal_plane_sunrise_solar_hour_angle_df)&(inclined_plane_sunrise_solar_hour_angle1_df<inclined_plane_sunrise_solar_hour_angle2_df)
                local_gable_sunrise_solar_hour_angle_df_condition2  = (inclined_plane_sunrise_solar_hour_angle2_df<horizontal_plane_sunrise_solar_hour_angle_df)&(inclined_plane_sunrise_solar_hour_angle2_df<inclined_plane_sunrise_solar_hour_angle1_df)
                local_gable_sunrise_solar_hour_angle_df_condition3  = (horizontal_plane_sunrise_solar_hour_angle_df<inclined_plane_sunrise_solar_hour_angle1_df)&(horizontal_plane_sunrise_solar_hour_angle_df<inclined_plane_sunrise_solar_hour_angle2_df)
                local_gable_sunrise_solar_hour_angle_df_conditions  = [local_gable_sunrise_solar_hour_angle_df_condition1, local_gable_sunrise_solar_hour_angle_df_condition2, local_gable_sunrise_solar_hour_angle_df_condition3]
                
                local_gable_sunrise_solar_hour_angle_df_choices     = [inclined_plane_sunrise_solar_hour_angle1_df, inclined_plane_sunrise_solar_hour_angle2_df, horizontal_plane_sunrise_solar_hour_angle_df]

                sunrise_solar_hour_angle_df                         = pd.DataFrame((np.select(local_gable_sunrise_solar_hour_angle_df_conditions, local_gable_sunrise_solar_hour_angle_df_choices, horizontal_plane_sunrise_solar_hour_angle_df)))
                local_sunrise_time_df                               = solar_hour_angle2local_time(sunrise_solar_hour_angle_df)
                sunset_solar_hour_angle_df                          = (-1)*(sunrise_solar_hour_angle_df)
                local_sunset_time_df                                = solar_hour_angle2local_time(sunset_solar_hour_angle_df)
                return sunrise_solar_hour_angle_df, sunset_solar_hour_angle_df, local_sunrise_time_df, local_sunset_time_df
            
            def gable_rooftop_azimuth_angle_df_is_else(declination_angle_df, latitude_df):
                sunrise_solar_hour_angle_df                     = Rad2Deg(np.acos((-1)*(np.tan(Deg2Rad(declination_angle_df)))*(np.tan(Deg2Rad(latitude_df)))))
                sunset_solar_hour_angle_df                      = (-1)*(sunrise_solar_hour_angle_df)
                local_sunrise_time_df                           = solar_hour_angle2local_time(sunrise_solar_hour_angle_df)
                local_sunset_time_df                            = solar_hour_angle2local_time(sunset_solar_hour_angle_df)
                return sunrise_solar_hour_angle_df, sunset_solar_hour_angle_df, local_sunrise_time_df, local_sunset_time_df
            
            gable_rooftype_choices = [gable_rooftop_azimuth_angle_df_more_than_zero(horizontal_plane_sunrise_solar_hour_angle_df, x_factor, y_factor),
                                        gable_rooftop_azimuth_angle_df_less_than_zero(horizontal_plane_sunrise_solar_hour_angle_df, x_factor, y_factor),
                                        gable_rooftop_azimuth_angle_df_is_zero(declination_angle_df, latitude_df, horizontal_plane_sunrise_solar_hour_angle_df)]
            
            sunrise_solar_hour_angle_df, sunset_solar_hour_angle_df, local_sunrise_time_df, local_sunset_time_df = np.select(gable_rooftype_conditions, gable_rooftype_choices, 0)
            return sunrise_solar_hour_angle_df, sunset_solar_hour_angle_df, local_sunrise_time_df, local_sunset_time_df
        
        sunrise_solar_hour_angle_df_side1, sunset_solar_hour_angle_df_side1, local_sunrise_time_df_side1, local_sunset_time_df_side1 = gable_rooftop_local_sunrise_sunset_time_calculation_function(horizontal_plane_sunrise_solar_hour_angle_df, gable_rooftop_azimuth_angle_side1_df, latitude_df, rooftop_slope_angle_df, declination_angle_df)
        sunrise_solar_hour_angle_df_side2, sunset_solar_hour_angle_df_side2, local_sunrise_time_df_side2, local_sunset_time_df_side2 = gable_rooftop_local_sunrise_sunset_time_calculation_function(horizontal_plane_sunrise_solar_hour_angle_df, gable_rooftop_azimuth_angle_side2_df, latitude_df, rooftop_slope_angle_df, declination_angle_df)

        sunrise_solar_hour_angle_df = pd.DataFrame(np.where(sunrise_solar_hour_angle_df_side1>=sunrise_solar_hour_angle_df_side2, sunrise_solar_hour_angle_df_side1, sunrise_solar_hour_angle_df_side2))
        sunset_solar_hour_angle_df  = pd.DataFrame(np.where(sunset_solar_hour_angle_df_side1<=sunset_solar_hour_angle_df_side2, sunset_solar_hour_angle_df_side1, sunset_solar_hour_angle_df_side2))
        local_sunrise_time_df       = pd.DataFrame(np.where(local_sunrise_time_df_side1<=local_sunrise_time_df_side2, local_sunrise_time_df_side1, local_sunrise_time_df_side2))
        local_sunset_time_df        = pd.DataFrame(np.where(local_sunset_time_df_side1>=local_sunset_time_df_side2, local_sunset_time_df_side1, local_sunset_time_df_side2)) 
    elif rooftype == "Hip":
        horizontal_plane_sunrise_solar_hour_angle_df        = Rad2Deg(np.acos((-1)*(np.tan(Deg2Rad(declination_angle_df)))*(np.tan(Deg2Rad(latitude_df)))))
        hip_side1_rooftop_azimuth_angle_df = rooftop_azimuth_angle_df.copy()
        if 180 >= rooftop_azimuth_angle_df[0] > 0:
                hip_side2_rooftop_azimuth_angle_df = rooftop_azimuth_angle_df.copy() - 180
        elif 0 > rooftop_azimuth_angle_df[0] >= -180:
            hip_side2_rooftop_azimuth_angle_df = rooftop_azimuth_angle_df.copy() + 180
        if 180 >= rooftop_azimuth_angle_df[0] > 90:
            hip_side3_rooftop_azimuth_angle_df = rooftop_azimuth_angle_df.copy() - 270
        elif 90 >= rooftop_azimuth_angle_df[0] >= -180:
            hip_side3_rooftop_azimuth_angle_df = rooftop_azimuth_angle_df.copy() + 90
        if -90 > rooftop_azimuth_angle_df[0] >= -180:
            hip_side4_rooftop_azimuth_angle_df = rooftop_azimuth_angle_df.copy() + 270
        elif 180 >= rooftop_azimuth_angle_df[0] >= -90:
            hip_side4_rooftop_azimuth_angle_df = rooftop_azimuth_angle_df.copy() - 90

        def hip_rooftop_local_sunrise_sunset_calculation_function(horizontal_plane_sunrise_solar_hour_angle_df, rooftop_azimuth_angle_df, latitude_df, rooftop_slope_angle_df, declination_angle_df):
            x_factor                                            = ( ( ((np.cos(Deg2Rad(latitude_df)))*(np.cos(Deg2Rad(rooftop_slope_angle_df)))*(np.cos(Deg2Rad(declination_angle_df)))) + ((np.sin(Deg2Rad(latitude_df)))*(np.sin(Deg2Rad(rooftop_slope_angle_df)))*(np.cos(Deg2Rad(rooftop_azimuth_angle_df)))*(np.cos(Deg2Rad(declination_angle_df)))) ) / ( (np.cos(Deg2Rad(declination_angle_df)))*(np.sin(Deg2Rad(rooftop_slope_angle_df)))*(np.sin(Deg2Rad(rooftop_azimuth_angle_df))) ) )
            y_factor                                            = ( ( ((np.sin(Deg2Rad(latitude_df)))*(np.cos(Deg2Rad(rooftop_slope_angle_df)))*(np.sin(Deg2Rad(declination_angle_df)))) - ((np.cos(Deg2Rad(latitude_df)))*(np.sin(Deg2Rad(rooftop_slope_angle_df)))*(np.cos(Deg2Rad(rooftop_azimuth_angle_df)))*(np.sin(Deg2Rad(declination_angle_df)))) ) / ( (np.cos(Deg2Rad(declination_angle_df)))*(np.sin(Deg2Rad(rooftop_slope_angle_df)))*(np.sin(Deg2Rad(rooftop_azimuth_angle_df))) ) )
            # Hip Azimuth Angle Conditions:
            hip_rooftype_condition1 = rooftop_azimuth_angle_df>0
            hip_rooftype_condition2 = rooftop_azimuth_angle_df<0
            hip_rooftype_condition3 = rooftop_azimuth_angle_df==0
            hip_rooftype_conditions = [hip_rooftype_condition1, hip_rooftype_condition2, hip_rooftype_condition3]
            # Hip Condition Local Sunrise Time and Local Sunset Time
            def hip_rooftop_azimuth_angle_df_more_than_zero(horizontal_plane_sunrise_solar_hour_angle_df, x_factor, y_factor):
                inclined_plane_sunrise_solar_hour_angle_df      = Rad2Deg(np.acos( ( ((-1)*(x_factor)*(y_factor)) - (np.sqrt(((x_factor)**2)-((y_factor)**2)+(1))) ) / (((x_factor)**2)+1) ))
                sunrise_solar_hour_angle_df                     = pd.DataFrame(np.where(inclined_plane_sunrise_solar_hour_angle_df<horizontal_plane_sunrise_solar_hour_angle_df, inclined_plane_sunrise_solar_hour_angle_df, horizontal_plane_sunrise_solar_hour_angle_df))
                local_sunrise_time_df                           = solar_hour_angle2local_time(sunrise_solar_hour_angle_df)

                inclined_plane_sunset_solar_hour_angle          = Rad2Deg(np.acos( ( ((-1)*(x_factor)*(y_factor)) + (np.sqrt(((x_factor)**2)-((y_factor)**2)+(1))) ) / (((x_factor)**2)+1) ))
                sunset_solar_hour_angle_df                      = pd.DataFrame(np.where(inclined_plane_sunset_solar_hour_angle<horizontal_plane_sunrise_solar_hour_angle_df, inclined_plane_sunset_solar_hour_angle, horizontal_plane_sunrise_solar_hour_angle_df))*(-1)
                local_sunset_time_df                            = solar_hour_angle2local_time(sunset_solar_hour_angle_df)
                return sunrise_solar_hour_angle_df, sunset_solar_hour_angle_df, local_sunrise_time_df, local_sunset_time_df
            
            def hip_rooftop_azimuth_angle_df_less_than_zero(horizontal_plane_sunrise_solar_hour_angle_df, x_factor, y_factor):
                inclined_plane_sunrise_solar_hour_angle         = Rad2Deg(np.acos( ( ((-1)*(x_factor)*(y_factor)) + (np.sqrt(((x_factor)**2)-((y_factor)**2)+(1))) ) / (((x_factor)**2)+1) ))
                sunrise_solar_hour_angle_df                     = pd.DataFrame(np.where(inclined_plane_sunrise_solar_hour_angle<horizontal_plane_sunrise_solar_hour_angle_df, inclined_plane_sunrise_solar_hour_angle, horizontal_plane_sunrise_solar_hour_angle_df))
                local_sunrise_time_df                           = solar_hour_angle2local_time(sunrise_solar_hour_angle_df)

                inclined_plane_sunset_solar_hour_angle          = Rad2Deg(np.acos( ( ((-1)*(x_factor)*(y_factor)) - (np.sqrt(((x_factor)**2)-((y_factor)**2)+(1))) ) / (((x_factor)**2)+1) ))
                sunset_solar_hour_angle_df                      = pd.DataFrame(np.where(inclined_plane_sunset_solar_hour_angle<horizontal_plane_sunrise_solar_hour_angle_df, inclined_plane_sunset_solar_hour_angle, horizontal_plane_sunrise_solar_hour_angle_df))
                local_sunset_time_df                            = solar_hour_angle2local_time((-1)*sunset_solar_hour_angle_df)
                return sunrise_solar_hour_angle_df, sunset_solar_hour_angle_df, local_sunrise_time_df, local_sunset_time_df
            
            def hip_rooftop_azimuth_angle_df_is_zero(declination_angle_df, latitude_df, horizontal_plane_sunrise_solar_hour_angle_df):
                inclined_plane_sunrise_solar_hour_angle1_df        = Rad2Deg(np.acos((-1)*(np.tan(Deg2Rad(declination_angle_df)))*(np.tan(Deg2Rad(latitude_df)))))
                inclined_plane_sunrise_solar_hour_angle2_df        = Rad2Deg(np.acos((-1)*(np.tan(Deg2Rad(declination_angle_df)))*(np.tan((Deg2Rad(latitude_df))-(Deg2Rad(rooftop_slope_angle_df))))))

                sunrise_solar_hour_angle_df_condition1 = (inclined_plane_sunrise_solar_hour_angle1_df<horizontal_plane_sunrise_solar_hour_angle_df)&(inclined_plane_sunrise_solar_hour_angle1_df<inclined_plane_sunrise_solar_hour_angle2_df)
                sunrise_solar_hour_angle_df_condition2 = (inclined_plane_sunrise_solar_hour_angle2_df<horizontal_plane_sunrise_solar_hour_angle_df)&(inclined_plane_sunrise_solar_hour_angle2_df<inclined_plane_sunrise_solar_hour_angle1_df)
                sunrise_solar_hour_angle_df_condition3 = (horizontal_plane_sunrise_solar_hour_angle_df<inclined_plane_sunrise_solar_hour_angle1_df)&(horizontal_plane_sunrise_solar_hour_angle_df<inclined_plane_sunrise_solar_hour_angle2_df)
                sunrise_solar_hour_angle_df_conditions = [sunrise_solar_hour_angle_df_condition1, sunrise_solar_hour_angle_df_condition2, sunrise_solar_hour_angle_df_condition3]

                sunrise_solar_hour_angle_df_choices             = [inclined_plane_sunrise_solar_hour_angle1_df, inclined_plane_sunrise_solar_hour_angle2_df, horizontal_plane_sunrise_solar_hour_angle_df]

                sunrise_solar_hour_angle_df                     = pd.DataFrame((np.select(sunrise_solar_hour_angle_df_conditions, sunrise_solar_hour_angle_df_choices, horizontal_plane_sunrise_solar_hour_angle_df)))
                local_sunrise_time_df                           = solar_hour_angle2local_time(sunrise_solar_hour_angle_df)
                sunset_solar_hour_angle_df                      = (-1)*sunrise_solar_hour_angle_df
                local_sunset_time_df                            = solar_hour_angle2local_time((-1)*sunrise_solar_hour_angle_df)
                return sunrise_solar_hour_angle_df, sunset_solar_hour_angle_df, local_sunrise_time_df, local_sunset_time_df
            
            def hip_rooftop_azimuth_angle_df_is_else(declination_angle_df, latitude_df):
                sunrise_solar_hour_angle_df                     = Rad2Deg(np.acos((-1)*(np.tan(Deg2Rad(declination_angle_df)))*(np.tan(Deg2Rad(latitude_df)))))
                sunset_solar_hour_angle_df                      = (-1)*(sunrise_solar_hour_angle_df)
                local_sunrise_time_df                           = solar_hour_angle2local_time(sunrise_solar_hour_angle_df)
                local_sunset_time_df                            = solar_hour_angle2local_time(sunset_solar_hour_angle_df)
                return sunrise_solar_hour_angle_df, sunset_solar_hour_angle_df, local_sunrise_time_df, local_sunset_time_df
            
            hip_rooftype_choices = [hip_rooftop_azimuth_angle_df_more_than_zero(horizontal_plane_sunrise_solar_hour_angle_df, x_factor, y_factor),
                                    hip_rooftop_azimuth_angle_df_less_than_zero(horizontal_plane_sunrise_solar_hour_angle_df, x_factor, y_factor),
                                    hip_rooftop_azimuth_angle_df_is_zero(declination_angle_df, latitude_df, horizontal_plane_sunrise_solar_hour_angle_df)]
            
            sunrise_solar_hour_angle_df, sunset_solar_hour_angle_df, local_sunrise_time_df, local_sunset_time_df = np.select(hip_rooftype_conditions, hip_rooftype_choices, 0)
            return sunrise_solar_hour_angle_df, sunset_solar_hour_angle_df, local_sunrise_time_df, local_sunset_time_df

        sunrise_solar_hour_angle_df_side1, sunset_solar_hour_angle_df_side1, local_sunrise_time_df_side1, local_sunset_time_df_side1 = hip_rooftop_local_sunrise_sunset_calculation_function(horizontal_plane_sunrise_solar_hour_angle_df, hip_side1_rooftop_azimuth_angle_df, latitude_df, rooftop_slope_angle_df, declination_angle_df)
        sunrise_solar_hour_angle_df_side2, sunset_solar_hour_angle_df_side2, local_sunrise_time_df_side2, local_sunset_time_df_side2 = hip_rooftop_local_sunrise_sunset_calculation_function(horizontal_plane_sunrise_solar_hour_angle_df, hip_side2_rooftop_azimuth_angle_df, latitude_df, rooftop_slope_angle_df, declination_angle_df)
        sunrise_solar_hour_angle_df_side3, sunset_solar_hour_angle_df_side3, local_sunrise_time_df_side3, local_sunset_time_df_side3 = hip_rooftop_local_sunrise_sunset_calculation_function(horizontal_plane_sunrise_solar_hour_angle_df, hip_side3_rooftop_azimuth_angle_df, latitude_df, rooftop_slope_angle_df, declination_angle_df)
        sunrise_solar_hour_angle_df_side4, sunset_solar_hour_angle_df_side4, local_sunrise_time_df_side4, local_sunset_time_df_side4 = hip_rooftop_local_sunrise_sunset_calculation_function(horizontal_plane_sunrise_solar_hour_angle_df, hip_side4_rooftop_azimuth_angle_df, latitude_df, rooftop_slope_angle_df, declination_angle_df)

        sunrise_solar_hour_angle_conditions = [(sunrise_solar_hour_angle_df_side1>=sunrise_solar_hour_angle_df_side2)&(sunrise_solar_hour_angle_df_side1>=sunrise_solar_hour_angle_df_side3)&(sunrise_solar_hour_angle_df_side1>=sunrise_solar_hour_angle_df_side4),
                                               (sunrise_solar_hour_angle_df_side2>=sunrise_solar_hour_angle_df_side1)&(sunrise_solar_hour_angle_df_side2>=sunrise_solar_hour_angle_df_side3)&(sunrise_solar_hour_angle_df_side2>=sunrise_solar_hour_angle_df_side4),
                                               (sunrise_solar_hour_angle_df_side3>=sunrise_solar_hour_angle_df_side1)&(sunrise_solar_hour_angle_df_side3>=sunrise_solar_hour_angle_df_side2)&(sunrise_solar_hour_angle_df_side3>=sunrise_solar_hour_angle_df_side4),
                                               (sunrise_solar_hour_angle_df_side4>=sunrise_solar_hour_angle_df_side1)&(sunrise_solar_hour_angle_df_side4>=sunrise_solar_hour_angle_df_side2)&(sunrise_solar_hour_angle_df_side4>=sunrise_solar_hour_angle_df_side3)]
        sunrise_solar_hour_angle_choices = [sunrise_solar_hour_angle_df_side1, sunrise_solar_hour_angle_df_side2, sunrise_solar_hour_angle_df_side3, sunrise_solar_hour_angle_df_side4]
        sunrise_solar_hour_angle_df = pd.DataFrame(np.select(sunrise_solar_hour_angle_conditions, sunrise_solar_hour_angle_choices, 0))

        sunset_solar_hour_angle_conditions = [(sunset_solar_hour_angle_df_side1<=sunset_solar_hour_angle_df_side2)&(sunset_solar_hour_angle_df_side1<=sunset_solar_hour_angle_df_side3)&(sunset_solar_hour_angle_df_side1<=sunset_solar_hour_angle_df_side4),
                                              (sunset_solar_hour_angle_df_side2<=sunset_solar_hour_angle_df_side1)&(sunset_solar_hour_angle_df_side2<=sunset_solar_hour_angle_df_side3)&(sunset_solar_hour_angle_df_side2<=sunset_solar_hour_angle_df_side4),
                                              (sunset_solar_hour_angle_df_side3<=sunset_solar_hour_angle_df_side1)&(sunset_solar_hour_angle_df_side3<=sunset_solar_hour_angle_df_side2)&(sunset_solar_hour_angle_df_side3<=sunset_solar_hour_angle_df_side4),
                                              (sunset_solar_hour_angle_df_side4<=sunset_solar_hour_angle_df_side1)&(sunset_solar_hour_angle_df_side4<=sunset_solar_hour_angle_df_side2)&(sunset_solar_hour_angle_df_side4<=sunset_solar_hour_angle_df_side3)]
        sunset_solar_hour_angle_choices = [sunset_solar_hour_angle_df_side1, sunset_solar_hour_angle_df_side2, sunset_solar_hour_angle_df_side3, sunset_solar_hour_angle_df_side4]
        sunset_solar_hour_angle_df = pd.DataFrame(np.select(sunset_solar_hour_angle_conditions, sunset_solar_hour_angle_choices, 0))

        local_sunrise_time_conditions = [(local_sunrise_time_df_side1<=local_sunrise_time_df_side2)&(local_sunrise_time_df_side1<=local_sunrise_time_df_side3)&(local_sunrise_time_df_side1<=local_sunrise_time_df_side4),
                                         (local_sunrise_time_df_side2<=local_sunrise_time_df_side1)&(local_sunrise_time_df_side2<=local_sunrise_time_df_side3)&(local_sunrise_time_df_side2<=local_sunrise_time_df_side4),
                                         (local_sunrise_time_df_side3<=local_sunrise_time_df_side1)&(local_sunrise_time_df_side3<=local_sunrise_time_df_side2)&(local_sunrise_time_df_side3<=local_sunrise_time_df_side4),
                                         (local_sunrise_time_df_side4<=local_sunrise_time_df_side1)&(local_sunrise_time_df_side4<=local_sunrise_time_df_side2)&(local_sunrise_time_df_side4<local_sunrise_time_df_side3)]
        local_sunrise_time_choices = [local_sunrise_time_df_side1, local_sunrise_time_df_side2, local_sunrise_time_df_side3, local_sunrise_time_df_side4]
        local_sunrise_time_df = pd.DataFrame(np.select(local_sunrise_time_conditions, local_sunrise_time_choices, 0))

        local_sunset_time_conditions = [(local_sunset_time_df_side1>=local_sunset_time_df_side2)&(local_sunset_time_df_side1>=local_sunset_time_df_side3)&(local_sunset_time_df_side1>=local_sunset_time_df_side4),
                                        (local_sunset_time_df_side2>=local_sunset_time_df_side1)&(local_sunset_time_df_side2>=local_sunset_time_df_side3)&(local_sunset_time_df_side2>=local_sunset_time_df_side4),
                                        (local_sunset_time_df_side3>=local_sunset_time_df_side1)&(local_sunset_time_df_side3>=local_sunset_time_df_side2)&(local_sunset_time_df_side3>=local_sunset_time_df_side4),
                                        (local_sunset_time_df_side4>=local_sunset_time_df_side1)&(local_sunset_time_df_side4>=local_sunset_time_df_side2)&(local_sunset_time_df_side4>=local_sunset_time_df_side3)]
        local_sunset_time_choices = [local_sunset_time_df_side1, local_sunset_time_df_side2, local_sunset_time_df_side3, local_sunset_time_df_side4]
        local_sunset_time_df = pd.DataFrame(np.select(local_sunset_time_conditions, local_sunset_time_choices, 0))

    sunrise_solar_hour_angle_df         = pd.DataFrame(pd.DataFrame(sunrise_solar_hour_angle_df)[0]).round(6)
    sunrise_solar_hour_angle_df.columns = ['Sunrise HRA']
    sunset_solar_hour_angle_df          = pd.DataFrame(pd.DataFrame(sunset_solar_hour_angle_df)[0]).round(6)
    sunset_solar_hour_angle_df.columns  = ['Sunset HRA']
    local_sunrise_time_df               = pd.DataFrame(pd.DataFrame(local_sunrise_time_df)[0]).round(6)
    local_sunrise_time_df.columns       = ['Sunrise Time']
    local_sunset_time_df                = pd.DataFrame(pd.DataFrame(local_sunset_time_df)[0]).round(6)
    local_sunset_time_df.columns        = ['Sunset Time']
    return  sunrise_solar_hour_angle_df, sunset_solar_hour_angle_df, local_sunrise_time_df, local_sunset_time_df

# Convert Solar Hour Angle to Local Time (hour)
def solar_hour_angle2local_time (solar_hour_angle_df):
    sun_time_df = 12-(solar_hour_angle_df/15)
    local_rise_time = sun_time_df.round(2)
    return local_rise_time

# Roof Inclination Calculation Function (Slope)
def rooftop_geometry_function(attribute_table_csv_df, vertices_attribute_df):
    start_time                      = time.time()
    uid_df                          = pd.DataFrame(attribute_table_csv_df['uid'])
    global_building_width_df        = pd.DataFrame([])
    global_building_length_df       = pd.DataFrame([])
    global_rooftop_incline_df       = pd.DataFrame([])
    global_rooftop_azimuth_angle_df = pd.DataFrame([])
    global_rooftop_geometry_df      = pd.DataFrame([])
    new_global_rooftop_geometry_df  = pd.DataFrame([])

    previous_uid = "null"
    n=0
    def rooftop_coordinate_calculation_function(uid_df, vertices_attribute_df):
        feasible_mapping_vertex_attribute_with_uid_keys = list(uid_df.columns.values)[0]
        vertices_attribute_df_filter_df                 = vertices_attribute_df.set_index(feasible_mapping_vertex_attribute_with_uid_keys).index
        uid_df_filter_df                                = uid_df.set_index(feasible_mapping_vertex_attribute_with_uid_keys).index
        vertices_attribute_df                           = vertices_attribute_df[vertices_attribute_df_filter_df.isin(uid_df_filter_df)].reset_index(drop=True)
        vertices_attribute_row_index                    = vertices_attribute_df.index
        local_uid_vertices_attribute_df                 = vertices_attribute_df
        #print(f'\nuid vertices attribute table:\n{local_uid_vertices_attribute_df}')

        vertex1_distance_df         = pd.DataFrame(local_uid_vertices_attribute_df[['distance']])
        vertex1_distance_df.loc[-1] = vertex1_distance_df.loc[0]
        vertex2_distance_df         = vertex1_distance_df.copy()
        vertex1_distance_df         = vertex1_distance_df.sort_index().reset_index(list(range(0,vertex1_distance_df.shape[1])),drop=True)
        vertex2_distance_df         = vertex2_distance_df.reset_index(list(range(0,vertex2_distance_df.shape[1])),drop=True)
        distance_between_vertex_df  = abs(vertex2_distance_df - vertex1_distance_df).loc[0:vertex1_distance_df.shape[0]-2,]
        #print("distance between coordinate df\n", distance_between_vertex_df)

        local_vertex1_coordinate_df = pd.DataFrame(local_uid_vertices_attribute_df[['lat', 'long']])
        local_vertex2_coordinate_df = local_vertex1_coordinate_df.copy()
        local_vertex2_coordinate_df.loc[-1] = local_vertex2_coordinate_df.loc[local_vertex2_coordinate_df.shape[0]-1]
        local_vertex2_coordinate_df = local_vertex2_coordinate_df.reset_index(drop=True)
        local_vertex2_coordinate_df = local_vertex2_coordinate_df.loc[1:local_vertex2_coordinate_df.shape[0]-1]
        local_vertex2_coordinate_df = local_vertex2_coordinate_df.reset_index(drop=True) 

        local_vertex1_coordinate_df.columns = ['vertex1_lat', 'vertex1_long']
        local_vertex2_coordinate_df.columns = ['vertex2_lat', 'vertex2_long']
        distance_between_vertex_df.columns  = ['distance']

        local_uid_building_coordinate_df = pd.concat([distance_between_vertex_df, local_vertex1_coordinate_df, local_vertex2_coordinate_df], axis=1)
        local_uid_building_coordinate_df.index = vertices_attribute_row_index
        #print("local uid building coordinate:\n",local_uid_building_coordinate_df)
        return local_uid_building_coordinate_df
    local_uid_vertices_attribute_df = rooftop_coordinate_calculation_function(uid_df, vertices_attribute_df)

    for uid in vertices_attribute_df['uid']:
        n+=1
        program_name = "ROOFTOP GEOMETRY FUNCTION"
        rooftop_geometry_field_length = len(vertices_attribute_df['uid'])
        if n == 1:
            print(f"\nPROCESSING {program_name}-(0/4)...")
        elif n == int(rooftop_geometry_field_length-1*(4/4)):
            print(f"PROCESSING {program_name}-(4/4)...")

        distance_between_vertex_list = []

        if uid != previous_uid:
            uid_vertices_filter = (vertices_attribute_df['uid'] == uid)

            previous_uid = uid
        
            local_uid_building_coordinate_df = local_uid_vertices_attribute_df.loc[uid_vertices_filter]
            #print(f'\nuid:{uid} vertex coordinate:\n{local_uid_building_coordinate_df}')
            distance_between_vertex_list = (local_uid_vertices_attribute_df.loc[uid_vertices_filter, 'distance']).tolist()
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

    global_building_width_df = global_building_width_df.round(6).reset_index(drop=True)
    global_building_width_df.columns = ['width']

    global_building_length_df = global_building_length_df.round(6).reset_index(drop=True)
    global_building_length_df.columns = ['length']

    global_rooftop_incline_df = global_rooftop_incline_df.round(6).reset_index(drop=True)
    global_rooftop_incline_df.columns = ['rooftop slope']

    global_rooftop_azimuth_angle_df = global_rooftop_azimuth_angle_df.round(6).reset_index(drop=True)
    global_rooftop_azimuth_angle_df.columns = ['rooftop azimuth angle']

    global_rooftop_geometry_df = pd.concat([global_building_width_df, global_building_length_df, global_rooftop_incline_df, global_rooftop_azimuth_angle_df], axis=1)

    vertices_global_rooftop_geometry_df = pd.concat([vertices_attribute_df, global_rooftop_geometry_df], axis=1)
    #print("vertices global rooftop geometry:\n", vertices_global_rooftop_geometry_df)

    previous_uid = "Null"

    for uid in vertices_global_rooftop_geometry_df['uid']:
        if uid != previous_uid:
            uid_global_rooftop_filter = (vertices_global_rooftop_geometry_df['uid'] == uid) & (vertices_global_rooftop_geometry_df['vertex_index'] == 0)
            local_uid_rooftop_df = vertices_global_rooftop_geometry_df.loc[uid_global_rooftop_filter]
            local_uid_rooftop_df = local_uid_rooftop_df.reset_index(drop=True)
            
            new_global_rooftop_geometry_df = pd.concat([new_global_rooftop_geometry_df, local_uid_rooftop_df])
            previous_uid = uid

    new_global_rooftop_geometry_df = new_global_rooftop_geometry_df.reset_index(drop=True)
    print(f'Rooftop Geometry:\n{new_global_rooftop_geometry_df}')

    end_time    = time.time()
    total_time  = end_time - start_time
    print("\n***** DONE PROCESSING ROOFTOP GEOMETRY FUNCTION *****")
    print(f"Rooftop Geometry Program Total execution time: {total_time:.4f} seconds\n")
    return new_global_rooftop_geometry_df



def Deg2Rad(deg):
    return deg * (np.pi / 180)
    
def Rad2Deg(rad):
    return rad * (180 / np.pi)


# Creating CSV File Function
def create_csvfile(csvfile_location, csvfile_local_name):
    csvfile_name = str(csvfile_location) + '/' + str(csvfile_local_name) + '.csv'
    with open(csvfile_name, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
    return writer, csvfile_name

def create_separator_df_function(end_row):
    separator_df = pd.DataFrame(list(["/////"]) for n in range (0,end_row))
    separator_df.columns = ['Separator Column']
    return separator_df
