import time
import csv
import numpy as np
import pandas as pd


def shading_geometry_function(uid, attribute_table_csv_df, global_shading_factor_csvfile_location, building_fields_table_df, global_rooftop_geometry_df, uid_building_digital_elevation_model_height, feasible_shading_uid_building_digital_elevation_model_height_df, date_field_df, sun_altitude_angle_df, sun_azimuth_angle_df, steps, start_time, stop_time):
    start_time_record = time.time()
    print("\n***** PROCESSING SHADING GEOMETRY FUNCTION *****")
    # Checking Input
    uid_building_longitude      = building_fields_table_df.loc[0,'long']
    uid_building_latitude       = building_fields_table_df.loc[0,'lat']
    uid_building_rooftop_height = building_fields_table_df.loc[0,'rooftop']
    global_rooftop_geometry_df  = global_rooftop_geometry_df.loc[global_rooftop_geometry_df['uid']==uid].reset_index(drop=True)
    #print(global_rooftop_geometry_df)
    uid_building_width          = global_rooftop_geometry_df.loc[0,'width'].round(6)

    #end_julian_date is NO. of date in a year
    julian_date_df  = date_field_df[['julian date']]
    end_julian_date = julian_date_df.shape[0]

    # Writing Building characteristics to each row
    new_building_fields_tables_df = pd.DataFrame((building_fields_table_df.values.tolist())*end_julian_date, columns=building_fields_table_df.columns)
    
    # Filtering uid Building causing shading on rooftop that computed solar irradiance and irradiation 
    feasible_shading_coordinate_df                          = shading_filter_for_horizontal_angle_function(uid_building_latitude, uid_building_longitude, sun_azimuth_angle_df)
    feasible_shading_uid_building_coordinate_keys           = list(feasible_shading_coordinate_df.columns.values)[feasible_shading_coordinate_df.columns.get_loc('lat'):feasible_shading_coordinate_df.columns.get_loc('long')+1]
    attribute_table_csv_filter_df                           = attribute_table_csv_df.set_index(feasible_shading_uid_building_coordinate_keys).index
    latitude_longitude_cols                                 = ['lat', 'long']
    feasible_shading_coordinate_df[latitude_longitude_cols] = feasible_shading_coordinate_df[latitude_longitude_cols].round({'lat':4, 'long':3})
    feasible_shading_coordinate_filter_df                   = feasible_shading_coordinate_df.set_index(feasible_shading_uid_building_coordinate_keys).index
    feasible_shading_uid_building_coordinate_df             = attribute_table_csv_df[attribute_table_csv_filter_df.isin(feasible_shading_coordinate_filter_df)].reset_index(drop=True)
    feasible_shading_uid_building_coordinate_df             = feasible_shading_uid_building_coordinate_df.drop(feasible_shading_uid_building_coordinate_df.loc[feasible_shading_uid_building_coordinate_df['uid']==uid].index).reset_index(drop=True)
    feasible_shading_uid_building_coordinate_df             = feasible_shading_uid_building_coordinate_df[['uid', 'lat', 'long', 'height', 'rooftop']]
    feasible_shading_same_uid_building_coordinate_filter    = (feasible_shading_uid_building_coordinate_df['lat']==uid_building_latitude)&(feasible_shading_uid_building_coordinate_df['long']==uid_building_longitude)&((feasible_shading_uid_building_coordinate_df['rooftop']<=uid_building_rooftop_height)|(feasible_shading_uid_building_coordinate_df['rooftop']>=(uid_building_rooftop_height+4)))
    feasible_shading_uid_building_coordinate_df             = feasible_shading_uid_building_coordinate_df.drop(feasible_shading_uid_building_coordinate_df.loc[feasible_shading_same_uid_building_coordinate_filter].index).reset_index(drop=True)
    feasible_shading_uid_building_coordinate_df             = feasible_shading_uid_building_coordinate_df.drop(feasible_shading_uid_building_coordinate_df.loc[feasible_shading_uid_building_coordinate_df['rooftop']<=uid_building_rooftop_height].index).reset_index(drop=True)

    global_shading_factor_uid_building_df           = shading_filter_for_vertical_angle_function(sun_azimuth_angle_df, feasible_shading_coordinate_df, feasible_shading_uid_building_coordinate_df, uid_building_width, uid_building_latitude, uid_building_longitude, uid_building_digital_elevation_model_height, feasible_shading_uid_building_digital_elevation_model_height_df, uid_building_rooftop_height)
    global_shading_angle_uid_building_df            = global_shading_factor_uid_building_df.copy()
    global_shading_angle_uid_building_df            = global_shading_angle_uid_building_df.reindex_like(sun_altitude_angle_df)
    global_shading_factor_uid_building_df           = pd.DataFrame(np.where(global_shading_angle_uid_building_df<sun_altitude_angle_df,1,0),index=global_shading_factor_uid_building_df.index)
    global_shading_angle_uid_building_df.columns    = list(f"uid building Angle-{hour_time}:{minute_time}" for hour_time in range (start_time, stop_time+1) for minute_time in range(0, 60, steps))
    shading_factor_uid_building_df                  = global_shading_factor_uid_building_df.copy()
    shading_factor_uid_building_df.columns          = list(f"Shading Factor-{hour_time}:{minute_time}" for hour_time in range (start_time, stop_time+1) for minute_time in range(0, 60, steps))
    new_global_shading_factor_uid_building_df       = pd.concat([new_building_fields_tables_df, date_field_df, shading_factor_uid_building_df, global_shading_angle_uid_building_df],axis=1)

    # Create CSV File to store Shading Factor Data
    shading_factor_csvfile_local_name = f'Shading_Factor_uid_{uid}'
    writer, global_shading_factor_csvfile_name = create_csvfile(global_shading_factor_csvfile_location, shading_factor_csvfile_local_name)
    new_global_shading_factor_uid_building_df.to_csv(global_shading_factor_csvfile_name, index=False)

    end_time_record    = time.time()
    total_time  = end_time_record - start_time_record
    print("\n***** DONE PROCESSING SHADING GEOMETRY FUNCTION *****")
    print(f"Shading Geometry Program Total execution time: {total_time:.4f} seconds\n")
    return  global_shading_factor_uid_building_df

def shading_filter_for_horizontal_angle_function(uid_building_latitude, uid_building_longitude, sun_azimuth_angle_df):

    horizontal_angle_interval_of_shading_long_range_calculation = 7.5 # +-7.5 degree of horizontal plane angle
    horizontal_angle_interval_of_shading_short_range_calculation = 20 # +-20 degree of horizontal plane angle
    latitude_interval             = 25 # 0.0025 degree of latitude (aroung 0.277 km on lattitude axis)
    longitude_interval            = 3 # 0.003 degree of longitude   (around 0.319 km on longitude axis)

    # Calculate Shading only Direction of Sun Azimuth Angle
    sun_azimuth_angle_df = convert_azimuth_angle_system2trigonometry_system(sun_azimuth_angle_df)

    # Coordinate Plane (Quadrant1-4)
    feasible_shading_coordinate_plane_row_level_zero_list    = list(range(1,(sun_azimuth_angle_df.shape[0])+1))
    feasible_shading_coordinate_plane_row_level_one_list     = list(range(-latitude_interval, latitude_interval+1))
    feasible_shading_coordinate_plane_row_iterables          = [feasible_shading_coordinate_plane_row_level_zero_list, feasible_shading_coordinate_plane_row_level_one_list]
    feasible_shading_coordinate_plane_row_index_df           = pd.MultiIndex.from_product(feasible_shading_coordinate_plane_row_iterables, names=["1st row", "2nd row"])
    
    feasible_shading_coordinate_plane_column_level_zero_list = list(range(1,(sun_azimuth_angle_df.shape[1])+1))
    feasible_shading_coordinate_plane_column_level_one_list  = list(range(-longitude_interval, longitude_interval+1))
    feasible_shading_coordinate_plane_column_iterables       = [feasible_shading_coordinate_plane_column_level_zero_list, feasible_shading_coordinate_plane_column_level_one_list]
    feasible_shading_coordinate_plane_column_index_df        = pd.MultiIndex.from_product(feasible_shading_coordinate_plane_column_iterables, names=["1st col", "2nd level col"])

    coordinate_plane_list                                   = list(range(-latitude_interval,(latitude_interval+1),1) for x in range (-longitude_interval,(longitude_interval+1),1))
    feasible_shading_coordinate_long_range_plane_df         = pd.DataFrame(list(zip(*(coordinate_plane_list*(sun_azimuth_angle_df.shape[1]))))*((sun_azimuth_angle_df.shape[0])), index=feasible_shading_coordinate_plane_row_index_df, columns=feasible_shading_coordinate_plane_column_index_df)
    feasible_shading_coordinate_long_range_plane_df         = pd.DataFrame(np.where(feasible_shading_coordinate_long_range_plane_df==0, 1, feasible_shading_coordinate_long_range_plane_df))
    feasible_shading_coordinate_long_range_plane_df.columns = feasible_shading_coordinate_plane_column_index_df
    feasible_shading_coordinate_long_range_plane_df         = feasible_shading_coordinate_long_range_plane_df.set_index([feasible_shading_coordinate_plane_row_index_df])
    feasible_shading_coordinate_short_range_plane_df        = feasible_shading_coordinate_long_range_plane_df.copy()
    combine_feasible_shading_coordinate_plane_df            = feasible_shading_coordinate_long_range_plane_df.copy()
    same_building_plane_df                                  = feasible_shading_coordinate_long_range_plane_df.copy()

    # Filter only Latitude that is feasible with calculation radius
    feasible_shading_coordinate_long_range_plane_df         = pd.DataFrame(np.where(abs(feasible_shading_coordinate_long_range_plane_df)<(((latitude_interval**2)-(feasible_shading_coordinate_long_range_plane_df.columns.get_level_values(1)**2))**(1/2)), feasible_shading_coordinate_long_range_plane_df, 0), index=feasible_shading_coordinate_plane_row_index_df, columns=feasible_shading_coordinate_plane_column_index_df)
    feasible_shading_coordinate_short_range_plane_df        = pd.DataFrame(np.where(abs(feasible_shading_coordinate_long_range_plane_df)<((((5)**2)-(feasible_shading_coordinate_long_range_plane_df.columns.get_level_values(1)**2))**(1/2)), feasible_shading_coordinate_long_range_plane_df, 0), index=feasible_shading_coordinate_plane_row_index_df, columns=feasible_shading_coordinate_plane_column_index_df)
    
    same_building_plane_df                       = pd.DataFrame(np.where(same_building_plane_df!=0, 0, 0), index=feasible_shading_coordinate_plane_row_index_df, columns=feasible_shading_coordinate_plane_column_index_df)
    same_building_plane_df.loc[same_building_plane_df.index.get_level_values(1)==0, same_building_plane_df.columns.get_level_values(1)==0] = 1

    # Computing uid Building Azimuth Angle
    azimuth_angle_bound_column_level_zero_list  = list(range(1,(sun_azimuth_angle_df.shape[0])+1))
    azimuth_angle_bound_column_level_one_list   = list(range(1,(sun_azimuth_angle_df.shape[1]*len(feasible_shading_coordinate_plane_column_level_one_list))+1))
    azimuth_angle_bound_column_index_iterables  = [azimuth_angle_bound_column_level_zero_list,azimuth_angle_bound_column_level_one_list]
    azimuth_angle_bound_column_index            = pd.MultiIndex.from_product(azimuth_angle_bound_column_index_iterables, names=['1st col A', '2nd col A'])

    azimuth_angle_bound_row_level_zero_list     = list(range(1,2))
    azimuth_angle_bound_row_level_one_list      = list(range(1,(len(feasible_shading_coordinate_plane_row_level_one_list))+1))
    azimuth_angle_bound_row_index_iterables     = [azimuth_angle_bound_row_level_zero_list,azimuth_angle_bound_row_level_one_list]
    azimuth_angle_bound_row_index               = pd.MultiIndex.from_product(azimuth_angle_bound_row_index_iterables, names=['1st row A', '2nd row A'])

    # Long Range Computing
    azimuth_angle_upper_bound_long_range_df                = sun_azimuth_angle_df + horizontal_angle_interval_of_shading_long_range_calculation
    azimuth_angle_lower_bound_long_range_df                = sun_azimuth_angle_df - horizontal_angle_interval_of_shading_long_range_calculation

    azimuth_angle_upper_bound_long_range_df                = pd.DataFrame((pd.DataFrame(pd.DataFrame((pd.DataFrame(azimuth_angle_upper_bound_long_range_df.stack(future_stack=True)).values.transpose().tolist())*len(feasible_shading_coordinate_plane_column_level_one_list)).transpose().stack(future_stack=True)).transpose()).values.tolist()*len(feasible_shading_coordinate_plane_row_level_one_list))
    azimuth_angle_upper_bound_long_range_df.columns        = azimuth_angle_bound_column_index
    azimuth_angle_upper_bound_long_range_df                = azimuth_angle_upper_bound_long_range_df.set_index(azimuth_angle_bound_row_index)
    azimuth_angle_upper_bound_long_range_df                = azimuth_angle_upper_bound_long_range_df.transpose().stack(future_stack=True).transpose().stack(1,future_stack=True).transpose() 
    azimuth_angle_lower_bound_long_range_df                = pd.DataFrame((pd.DataFrame(pd.DataFrame((pd.DataFrame(azimuth_angle_lower_bound_long_range_df.stack(future_stack=True)).values.transpose().tolist())*len(feasible_shading_coordinate_plane_column_level_one_list)).transpose().stack(future_stack=True)).transpose()).values.tolist()*len(feasible_shading_coordinate_plane_row_level_one_list))
    azimuth_angle_lower_bound_long_range_df.columns        = azimuth_angle_bound_column_index
    azimuth_angle_lower_bound_long_range_df                = azimuth_angle_lower_bound_long_range_df.set_index(azimuth_angle_bound_row_index)
    azimuth_angle_lower_bound_long_range_df                = azimuth_angle_lower_bound_long_range_df.transpose().stack(future_stack=True).transpose().stack(1,future_stack=True).transpose()

    azimuth_angle_upper_bound_long_range_df                = pd.DataFrame(np.where(azimuth_angle_upper_bound_long_range_df>360,azimuth_angle_upper_bound_long_range_df-360,azimuth_angle_upper_bound_long_range_df ))
    azimuth_angle_lower_bound_long_range_df                = pd.DataFrame(np.where(azimuth_angle_lower_bound_long_range_df<0, azimuth_angle_lower_bound_long_range_df+360,azimuth_angle_lower_bound_long_range_df))
    azimuth_angle_upper_bound_long_range_factor_df         = np.tan(Deg2Rad(azimuth_angle_upper_bound_long_range_df))
    azimuth_angle_lower_bound_long_range_factor_df         = np.tan(Deg2Rad(azimuth_angle_lower_bound_long_range_df))

    # Short Range Computing
    azimuth_angle_upper_bound_short_range_df                = sun_azimuth_angle_df + horizontal_angle_interval_of_shading_short_range_calculation
    azimuth_angle_lower_bound_short_range_df                = sun_azimuth_angle_df - horizontal_angle_interval_of_shading_short_range_calculation

    azimuth_angle_upper_bound_short_range_df                = pd.DataFrame((pd.DataFrame(pd.DataFrame((pd.DataFrame(azimuth_angle_upper_bound_short_range_df.stack(future_stack=True)).values.transpose().tolist())*len(feasible_shading_coordinate_plane_column_level_one_list)).transpose().stack(future_stack=True)).transpose()).values.tolist()*len(feasible_shading_coordinate_plane_row_level_one_list))
    azimuth_angle_upper_bound_short_range_df.columns        = azimuth_angle_bound_column_index
    azimuth_angle_upper_bound_short_range_df                = azimuth_angle_upper_bound_short_range_df.set_index(azimuth_angle_bound_row_index)
    azimuth_angle_upper_bound_short_range_df                = azimuth_angle_upper_bound_short_range_df.transpose().stack(future_stack=True).transpose().stack(1,future_stack=True).transpose() 
    azimuth_angle_lower_bound_short_range_df                = pd.DataFrame((pd.DataFrame(pd.DataFrame((pd.DataFrame(azimuth_angle_lower_bound_short_range_df.stack(future_stack=True)).values.transpose().tolist())*len(feasible_shading_coordinate_plane_column_level_one_list)).transpose().stack(future_stack=True)).transpose()).values.tolist()*len(feasible_shading_coordinate_plane_row_level_one_list))
    azimuth_angle_lower_bound_short_range_df.columns        = azimuth_angle_bound_column_index
    azimuth_angle_lower_bound_short_range_df                = azimuth_angle_lower_bound_short_range_df.set_index(azimuth_angle_bound_row_index)
    azimuth_angle_lower_bound_short_range_df                = azimuth_angle_lower_bound_short_range_df.transpose().stack(future_stack=True).transpose().stack(1,future_stack=True).transpose()

    azimuth_angle_upper_bound_short_range_df                = pd.DataFrame(np.where(azimuth_angle_upper_bound_short_range_df>360,azimuth_angle_upper_bound_short_range_df-360,azimuth_angle_upper_bound_short_range_df ))
    azimuth_angle_lower_bound_short_range_df                = pd.DataFrame(np.where(azimuth_angle_lower_bound_short_range_df<0, azimuth_angle_lower_bound_short_range_df+360,azimuth_angle_lower_bound_short_range_df))
    azimuth_angle_upper_bound_short_range_factor_df         = np.tan(Deg2Rad(azimuth_angle_upper_bound_short_range_df))
    azimuth_angle_lower_bound_short_range_factor_df         = np.tan(Deg2Rad(azimuth_angle_lower_bound_short_range_df))

    azimuth_angle_upper_bound_long_range_factor_check_condition_df = pd.DataFrame((pd.DataFrame(pd.DataFrame(feasible_shading_coordinate_long_range_plane_df.columns.get_level_values(1)*azimuth_angle_upper_bound_long_range_factor_df)).values.tolist()), index=feasible_shading_coordinate_plane_row_index_df, columns=feasible_shading_coordinate_plane_column_index_df)
    azimuth_angle_lower_bound_long_range_factor_check_condition_df = pd.DataFrame((pd.DataFrame(pd.DataFrame(feasible_shading_coordinate_long_range_plane_df.columns.get_level_values(1)*azimuth_angle_lower_bound_long_range_factor_df)).values.tolist()), index=feasible_shading_coordinate_plane_row_index_df, columns=feasible_shading_coordinate_plane_column_index_df)

    azimuth_angle_upper_bound_short_range_factor_check_condition_df = pd.DataFrame((pd.DataFrame(pd.DataFrame(feasible_shading_coordinate_short_range_plane_df.columns.get_level_values(1)*azimuth_angle_upper_bound_short_range_factor_df)).values.tolist()), index=feasible_shading_coordinate_plane_row_index_df, columns=feasible_shading_coordinate_plane_column_index_df)
    azimuth_angle_lower_bound_short_range_factor_check_condition_df = pd.DataFrame((pd.DataFrame(pd.DataFrame(feasible_shading_coordinate_short_range_plane_df.columns.get_level_values(1)*azimuth_angle_lower_bound_short_range_factor_df)).values.tolist()), index=feasible_shading_coordinate_plane_row_index_df, columns=feasible_shading_coordinate_plane_column_index_df)
    
    def feasible_shading_coordinate_plane_condition1_choice(feasible_shading_coordinate_plane_df,azimuth_angle_upper_bound_factor_check_condition_df,azimuth_angle_lower_bound_factor_check_condition_df,feasible_shading_coordinate_plane_row_index_list,feasible_shading_coordinate_plane_column_index_df):
        feasible_shading_coordinate_plane_df = pd.DataFrame((np.where(feasible_shading_coordinate_plane_df <= (azimuth_angle_upper_bound_factor_check_condition_df), feasible_shading_coordinate_plane_df, 0)), index=feasible_shading_coordinate_plane_row_index_list, columns=feasible_shading_coordinate_plane_column_index_df)
        feasible_shading_coordinate_plane_df = pd.DataFrame((np.where(feasible_shading_coordinate_plane_df >= (azimuth_angle_lower_bound_factor_check_condition_df), feasible_shading_coordinate_plane_df, 0)), index=feasible_shading_coordinate_plane_row_index_list, columns=feasible_shading_coordinate_plane_column_index_df)
        return feasible_shading_coordinate_plane_df.reset_index(drop=True)
    
    def feasible_shading_coordinate_plane_condition2_choice(feasible_shading_coordinate_plane_df,azimuth_angle_upper_bound_factor_check_condition_df,azimuth_angle_lower_bound_factor_check_condition_df,feasible_shading_coordinate_plane_row_index_list,feasible_shading_coordinate_plane_column_index_df):
        feasible_shading_coordinate_plane_df = pd.DataFrame((np.where(feasible_shading_coordinate_plane_df >= (azimuth_angle_upper_bound_factor_check_condition_df), feasible_shading_coordinate_plane_df, 0)), index=feasible_shading_coordinate_plane_row_index_list, columns=feasible_shading_coordinate_plane_column_index_df)
        feasible_shading_coordinate_plane_df = pd.DataFrame((np.where(feasible_shading_coordinate_plane_df <= (azimuth_angle_lower_bound_factor_check_condition_df), feasible_shading_coordinate_plane_df, 0)), index=feasible_shading_coordinate_plane_row_index_list, columns=feasible_shading_coordinate_plane_column_index_df)
        return feasible_shading_coordinate_plane_df.reset_index(drop=True)
    
    def feasible_shading_coordinate_plane_condition3_choice(feasible_shading_coordinate_plane_df,azimuth_angle_upper_bound_factor_check_condition_df, azimuth_angle_lower_bound_factor_check_condition_df,feasible_shading_coordinate_plane_row_index_list,feasible_shading_coordinate_plane_column_index_df):
        feasible_shading_coordinate_plane_condition3_conditions = [(azimuth_angle_upper_bound_long_range_df==90), (azimuth_angle_upper_bound_long_range_df!=90)]
        
        def feasible_shading_coordinate_plane_condition3_condition1_choice(feasible_shading_coordinate_plane_df, azimuth_angle_upper_bound_factor_check_condition_df, azimuth_angle_lower_bound_factor_check_condition_df, feasible_shading_coordinate_plane_row_index_list, feasible_shading_coordinate_plane_column_index_df):
            feasible_shading_coordinate_plane_df        = pd.DataFrame((np.where(feasible_shading_coordinate_plane_df <= (azimuth_angle_upper_bound_factor_check_condition_df), feasible_shading_coordinate_plane_df, 0)), index=feasible_shading_coordinate_plane_row_index_list, columns=feasible_shading_coordinate_plane_column_index_df)
            feasible_shading_coordinate_plane_df        = pd.DataFrame((np.where(feasible_shading_coordinate_plane_df >= (azimuth_angle_lower_bound_factor_check_condition_df), feasible_shading_coordinate_plane_df, 0)), index=feasible_shading_coordinate_plane_row_index_list, columns=feasible_shading_coordinate_plane_column_index_df)
            return feasible_shading_coordinate_plane_df
        
        def feasible_shading_coordinate_plane_condition3_condition1_choice(feasible_shading_coordinate_plane_df, azimuth_angle_upper_bound_factor_check_condition_df, azimuth_angle_lower_bound_factor_check_condition_df, feasible_shading_coordinate_plane_row_index_list, feasible_shading_coordinate_plane_column_index_df):
            feasible_shading_coordinate_plane_df        = pd.DataFrame((np.where(feasible_shading_coordinate_plane_df >= (azimuth_angle_upper_bound_factor_check_condition_df), feasible_shading_coordinate_plane_df, 0)), index=feasible_shading_coordinate_plane_row_index_list, columns=feasible_shading_coordinate_plane_column_index_df)
            feasible_shading_coordinate_plane_df        = pd.DataFrame((np.where(feasible_shading_coordinate_plane_df >= (azimuth_angle_lower_bound_factor_check_condition_df), feasible_shading_coordinate_plane_df, 0)), index=feasible_shading_coordinate_plane_row_index_list, columns=feasible_shading_coordinate_plane_column_index_df)
            return feasible_shading_coordinate_plane_df

        feasible_shading_coordinate_plane_condition3_choices = [feasible_shading_coordinate_plane_condition3_condition1_choice(feasible_shading_coordinate_plane_df, azimuth_angle_upper_bound_factor_check_condition_df, azimuth_angle_lower_bound_factor_check_condition_df, feasible_shading_coordinate_plane_row_index_list, feasible_shading_coordinate_plane_column_index_df),
                                                                feasible_shading_coordinate_plane_condition3_condition1_choice(feasible_shading_coordinate_plane_df, azimuth_angle_upper_bound_factor_check_condition_df, azimuth_angle_lower_bound_factor_check_condition_df, feasible_shading_coordinate_plane_row_index_list, feasible_shading_coordinate_plane_column_index_df)
                                                                ]
        feasible_shading_coordinate_plane_df            = pd.DataFrame(np.select(feasible_shading_coordinate_plane_condition3_conditions, feasible_shading_coordinate_plane_condition3_choices, default=np.nan), index=feasible_shading_coordinate_plane_row_index_list, columns=feasible_shading_coordinate_plane_column_index_df)
        return feasible_shading_coordinate_plane_df.reset_index(drop=True)
    
    def feasible_shading_coordinate_plane_condition4_choice(feasible_shading_coordinate_plane_df,azimuth_angle_upper_bound_factor_check_condition_df,aazimuth_angle_lower_bound_factor_check_condition_df,feasible_shading_coordinate_plane_row_index_list,feasible_shading_coordinate_plane_column_index_df):
        feasible_shading_coordinate_plane_condition4_conditons = [(azimuth_angle_upper_bound_long_range_df==270), (azimuth_angle_upper_bound_long_range_df!=270)]

        def feasible_shading_coordinate_plane_condition4_conditon1_choice(feasible_shading_coordinate_plane_df,azimuth_angle_upper_bound_factor_check_condition_df,azimuth_angle_lower_bound_factor_check_condition_df,feasible_shading_coordinate_plane_row_index_list,feasible_shading_coordinate_plane_column_index_df):
            feasible_shading_coordinate_plane_df         = pd.DataFrame((np.where(feasible_shading_coordinate_plane_df >= (azimuth_angle_upper_bound_factor_check_condition_df), feasible_shading_coordinate_plane_df, 0)), index=feasible_shading_coordinate_plane_row_index_list, columns=feasible_shading_coordinate_plane_column_index_df)
            feasible_shading_coordinate_plane_df         = pd.DataFrame((np.where(feasible_shading_coordinate_plane_df <= (azimuth_angle_lower_bound_factor_check_condition_df), feasible_shading_coordinate_plane_df, 0)), index=feasible_shading_coordinate_plane_row_index_list, columns=feasible_shading_coordinate_plane_column_index_df)
            return feasible_shading_coordinate_plane_df
        
        def feasible_shading_coordinate_plane_condition4_conditon2_choice(feasible_shading_coordinate_plane_df,azimuth_angle_upper_bound_factor_check_condition_df,azimuth_angle_lower_bound_factor_check_condition_df,feasible_shading_coordinate_plane_row_index_list,feasible_shading_coordinate_plane_column_index_df):
            feasible_shading_coordinate_plane_df         = pd.DataFrame((np.where(feasible_shading_coordinate_plane_df <= (azimuth_angle_upper_bound_factor_check_condition_df), feasible_shading_coordinate_plane_df, 0)), index=feasible_shading_coordinate_plane_row_index_list, columns=feasible_shading_coordinate_plane_column_index_df)
            feasible_shading_coordinate_plane_df         = pd.DataFrame((np.where(feasible_shading_coordinate_plane_df <= (azimuth_angle_lower_bound_factor_check_condition_df), feasible_shading_coordinate_plane_df, 0)), index=feasible_shading_coordinate_plane_row_index_list, columns=feasible_shading_coordinate_plane_column_index_df)
            return feasible_shading_coordinate_plane_df

        feasible_shading_coordinate_plane_condition4_choices = [feasible_shading_coordinate_plane_condition4_conditon1_choice(feasible_shading_coordinate_plane_df,azimuth_angle_upper_bound_factor_check_condition_df,azimuth_angle_lower_bound_long_range_factor_check_condition_df,feasible_shading_coordinate_plane_row_index_list,feasible_shading_coordinate_plane_column_index_df),
                                                                feasible_shading_coordinate_plane_condition4_conditon2_choice(feasible_shading_coordinate_plane_df,azimuth_angle_upper_bound_factor_check_condition_df,azimuth_angle_lower_bound_long_range_factor_check_condition_df,feasible_shading_coordinate_plane_row_index_list,feasible_shading_coordinate_plane_column_index_df)
                                                                ]
        feasible_shading_coordinate_plane_df = pd.DataFrame(np.select(feasible_shading_coordinate_plane_condition4_conditons,feasible_shading_coordinate_plane_condition4_choices, default=np.nan), index=feasible_shading_coordinate_plane_row_index_list, columns=feasible_shading_coordinate_plane_column_index_df)
        return feasible_shading_coordinate_plane_df.reset_index(drop=True)
    
    feasible_shading_coordinate_long_range_plane_conditions = [((((90>azimuth_angle_upper_bound_long_range_df)&(azimuth_angle_upper_bound_long_range_df>=0))|((360>=azimuth_angle_upper_bound_long_range_df)&(azimuth_angle_upper_bound_long_range_df>270)))&(((90>azimuth_angle_lower_bound_long_range_df)&(azimuth_angle_lower_bound_long_range_df>=0))|((360>=azimuth_angle_lower_bound_long_range_df)&(azimuth_angle_lower_bound_long_range_df>270)))), 
                                                    (((270>azimuth_angle_upper_bound_long_range_df)&(azimuth_angle_upper_bound_long_range_df>90))&((270>azimuth_angle_lower_bound_long_range_df)&(azimuth_angle_lower_bound_long_range_df>90))),
                                                    ((azimuth_angle_upper_bound_long_range_df>=90)&(azimuth_angle_lower_bound_long_range_df<=90)),
                                                    ((azimuth_angle_upper_bound_long_range_df>=270)&(azimuth_angle_lower_bound_long_range_df<=270))]

    feasible_shading_coordinate_long_range_plane_condition1_choice_df = feasible_shading_coordinate_plane_condition1_choice(feasible_shading_coordinate_long_range_plane_df,azimuth_angle_upper_bound_long_range_factor_check_condition_df,azimuth_angle_lower_bound_long_range_factor_check_condition_df,feasible_shading_coordinate_plane_row_index_df,feasible_shading_coordinate_plane_column_index_df),
    feasible_shading_coordinate_long_range_plane_condition2_choice_df = feasible_shading_coordinate_plane_condition2_choice(feasible_shading_coordinate_long_range_plane_df,azimuth_angle_upper_bound_long_range_factor_check_condition_df,azimuth_angle_lower_bound_long_range_factor_check_condition_df,feasible_shading_coordinate_plane_row_index_df,feasible_shading_coordinate_plane_column_index_df),
    feasible_shading_coordinate_long_range_plane_condition3_choice_df = feasible_shading_coordinate_plane_condition3_choice(feasible_shading_coordinate_long_range_plane_df,azimuth_angle_upper_bound_long_range_factor_check_condition_df,azimuth_angle_lower_bound_long_range_factor_check_condition_df,feasible_shading_coordinate_plane_row_index_df,feasible_shading_coordinate_plane_column_index_df),
    feasible_shading_coordinate_long_range_plane_condition4_choice_df = feasible_shading_coordinate_plane_condition4_choice(feasible_shading_coordinate_long_range_plane_df,azimuth_angle_upper_bound_long_range_factor_check_condition_df,azimuth_angle_lower_bound_long_range_factor_check_condition_df,feasible_shading_coordinate_plane_row_index_df,feasible_shading_coordinate_plane_column_index_df)
    
    feasible_shading_coordinate_long_range_plane_condition_choices    = [feasible_shading_coordinate_long_range_plane_condition1_choice_df, feasible_shading_coordinate_long_range_plane_condition2_choice_df, feasible_shading_coordinate_long_range_plane_condition3_choice_df, feasible_shading_coordinate_long_range_plane_condition4_choice_df]
    feasible_shading_coordinate_long_range_plane_df                   = pd.DataFrame((np.select(feasible_shading_coordinate_long_range_plane_conditions,feasible_shading_coordinate_long_range_plane_condition_choices, default=np.nan)).tolist()[0], index=feasible_shading_coordinate_plane_row_index_df, columns=feasible_shading_coordinate_plane_column_index_df)
    
    feasible_shading_coordinate_short_range_plane_conditions = [((((90>azimuth_angle_upper_bound_short_range_df)&(azimuth_angle_upper_bound_short_range_df>=0))|((360>=azimuth_angle_upper_bound_short_range_df)&(azimuth_angle_upper_bound_short_range_df>270)))&(((90>azimuth_angle_lower_bound_short_range_df)&(azimuth_angle_lower_bound_short_range_df>=0))|((360>=azimuth_angle_lower_bound_short_range_df)&(azimuth_angle_lower_bound_short_range_df>270)))), 
                                                    (((270>azimuth_angle_upper_bound_short_range_df)&(azimuth_angle_upper_bound_short_range_df>90))&((270>azimuth_angle_lower_bound_long_range_df)&(azimuth_angle_lower_bound_long_range_df>90))),
                                                    ((azimuth_angle_upper_bound_short_range_df>=90)&(azimuth_angle_lower_bound_short_range_df<=90)),
                                                    ((azimuth_angle_upper_bound_short_range_df>=270)&(azimuth_angle_lower_bound_short_range_df<=270))]

    feasible_shading_coordinate_short_range_plane_condition1_choice_df = feasible_shading_coordinate_plane_condition1_choice(feasible_shading_coordinate_short_range_plane_df,azimuth_angle_upper_bound_short_range_factor_check_condition_df,azimuth_angle_lower_bound_short_range_factor_check_condition_df,feasible_shading_coordinate_plane_row_index_df,feasible_shading_coordinate_plane_column_index_df),
    feasible_shading_coordinate_short_range_plane_condition2_choice_df = feasible_shading_coordinate_plane_condition2_choice(feasible_shading_coordinate_short_range_plane_df,azimuth_angle_upper_bound_short_range_factor_check_condition_df,azimuth_angle_lower_bound_short_range_factor_check_condition_df,feasible_shading_coordinate_plane_row_index_df,feasible_shading_coordinate_plane_column_index_df),
    feasible_shading_coordinate_short_range_plane_condition3_choice_df = feasible_shading_coordinate_plane_condition3_choice(feasible_shading_coordinate_short_range_plane_df,azimuth_angle_upper_bound_short_range_factor_check_condition_df,azimuth_angle_lower_bound_short_range_factor_check_condition_df,feasible_shading_coordinate_plane_row_index_df,feasible_shading_coordinate_plane_column_index_df),
    feasible_shading_coordinate_short_range_plane_condition4_choice_df = feasible_shading_coordinate_plane_condition4_choice(feasible_shading_coordinate_short_range_plane_df,azimuth_angle_upper_bound_short_range_factor_check_condition_df,azimuth_angle_lower_bound_short_range_factor_check_condition_df,feasible_shading_coordinate_plane_row_index_df,feasible_shading_coordinate_plane_column_index_df)
    
    feasible_shading_coordinate_short_range_plane_condition_choices    = [feasible_shading_coordinate_short_range_plane_condition1_choice_df, feasible_shading_coordinate_short_range_plane_condition2_choice_df, feasible_shading_coordinate_short_range_plane_condition3_choice_df, feasible_shading_coordinate_short_range_plane_condition4_choice_df]
    feasible_shading_coordinate_short_range_plane_df                   = pd.DataFrame((np.select(feasible_shading_coordinate_short_range_plane_conditions,feasible_shading_coordinate_short_range_plane_condition_choices, default=np.nan)).tolist()[0], index=feasible_shading_coordinate_plane_row_index_df, columns=feasible_shading_coordinate_plane_column_index_df)
    
    same_building_plane_df = pd.DataFrame(np.where(same_building_plane_df!=0, uid_building_latitude, 0), index=same_building_plane_df.index, columns=same_building_plane_df.columns)

    feasible_shading_coordinate_plane_df                        = feasible_shading_coordinate_long_range_plane_df + feasible_shading_coordinate_short_range_plane_df
    feasible_shading_coordinate_plane_df                        = pd.DataFrame(np.where(feasible_shading_coordinate_plane_df!=0, (combine_feasible_shading_coordinate_plane_df/10000)+uid_building_latitude, 0), index=same_building_plane_df.index, columns=same_building_plane_df.columns)

    feasible_shading_coordinate_plane_df                        = feasible_shading_coordinate_plane_df + same_building_plane_df

    feasible_shading_coordinate_plane_row_level_zero_list       = list(range(1,(sun_azimuth_angle_df.shape[0])+1))
    feasible_shading_coordinate_plane_row_level_one_list        = pd.DataFrame((pd.DataFrame(list(range(-latitude_interval,latitude_interval+1,1)))/10000)+uid_building_latitude).transpose().values.tolist()
    feasible_shading_coordinate_plane_row_iterables             = [feasible_shading_coordinate_plane_row_level_zero_list, feasible_shading_coordinate_plane_row_level_one_list[0]]
    feasible_shading_coordinate_plane_row_index_df              = pd.MultiIndex.from_product(feasible_shading_coordinate_plane_row_iterables, names=["Date", "Latitude"])

    feasible_shading_coordinate_plane_column_level_one_list     = pd.DataFrame((pd.DataFrame(list(range(-longitude_interval,(longitude_interval+1),1)))/1000)+uid_building_longitude).transpose().values.tolist()
    feasible_shading_coordinate_plane_column_iterables          = [feasible_shading_coordinate_plane_column_level_zero_list, feasible_shading_coordinate_plane_column_level_one_list[0]]
    feasible_shading_coordinate_plane_column_index_df           = pd.MultiIndex.from_product(feasible_shading_coordinate_plane_column_iterables, names=["Time", "Longitude"])

    feasible_shading_coordinate_plane_df.columns                = feasible_shading_coordinate_plane_column_index_df
    feasible_shading_coordinate_plane_df                        = feasible_shading_coordinate_plane_df.set_index(feasible_shading_coordinate_plane_row_index_df)
    feasible_shading_coordinate_plane_df                        = feasible_shading_coordinate_plane_df.sort_index(ascending=True).stack(future_stack=True).reset_index()
    
    feasible_shading_coordinate_df_row_level_zero_list          = list(range(1,(sun_azimuth_angle_df.shape[0])+1))
    feasible_shading_coordinate_df_row_level_one_list           = list(range(1,(len(feasible_shading_coordinate_plane_row_level_one_list[0])*len(feasible_shading_coordinate_plane_column_level_one_list[0]))+1))
    feasible_shading_coordinate_df_row_iterables                = [feasible_shading_coordinate_df_row_level_zero_list, feasible_shading_coordinate_df_row_level_one_list]
    feasible_shading_coordinate_df_row_index                    = pd.MultiIndex.from_product(feasible_shading_coordinate_df_row_iterables, names=['R1', 'R2'])

    feasible_shading_coordinate_plane_df                        = feasible_shading_coordinate_plane_df.set_index(feasible_shading_coordinate_df_row_index)
    feasible_shading_coordinate_plane_df.columns                = ["Date", "lat", "long"] + list(range(1,(sun_azimuth_angle_df.shape[1])+1))
    feasible_shading_coordinate_df                              = feasible_shading_coordinate_plane_df.loc[np.count_nonzero(feasible_shading_coordinate_plane_df.loc[:,1:],axis=1)>0]
    
    #print("\nfeasible coordinate plane:\n",feasible_shading_coordinate_plane_df)
    #print("\nfeasible coordinate df:\n",feasible_shading_coordinate_df)
    #print('\nLength of Feasible Coordinates:',feasible_shading_coordinate_df.shape[0])
    return  feasible_shading_coordinate_df

def shading_filter_for_vertical_angle_function(sun_azimuth_angle_df, feasible_shading_coordinate_df, feasible_shading_uid_building_coordinate_df, uid_building_width, uid_building_latitude, uid_building_longitude, center_uid_building_digital_elevation_model_height, feasible_shading_uid_building_digital_elevation_model_height_df, uid_building_rooftop_height):
    idx = pd.IndexSlice
    
    # Shading Angle Data Frame
    shading_angle_df                = sun_azimuth_angle_df.copy()
    shading_angle_col_fixture_df    = pd.DataFrame(list(range(1,sun_azimuth_angle_df.shape[1]+1)))
    shading_angle_col_fixture_df    = shading_angle_col_fixture_df.set_index(shading_angle_col_fixture_df[0])
    shading_angle_row_fixture_df    = pd.DataFrame(list(range(1,sun_azimuth_angle_df.shape[0]+1)))
    shading_angle_row_fixture_df    = shading_angle_row_fixture_df.set_index(shading_angle_row_fixture_df[0])
    
    def feasible_shading_coordinate_calculation_function(feasible_shading_coordinate_df, feasible_shading_uid_building_coordinate_df):
        #Mapping Feasible uid building into Feasible shading Coordinate
        feasible_mapping_uid_building_shading_coordinate_condition_keys = list(feasible_shading_coordinate_df.columns.values)[feasible_shading_coordinate_df.columns.get_loc('lat'):feasible_shading_coordinate_df.columns.get_loc('long')+1]
        feasible_shading_uid_building_coordinate_df_filter_df           = feasible_shading_uid_building_coordinate_df.set_index(feasible_mapping_uid_building_shading_coordinate_condition_keys).index
        feasible_shading_coordinate_filter_df                           = feasible_shading_coordinate_df.set_index(feasible_mapping_uid_building_shading_coordinate_condition_keys).index
        feasible_shading_uid_building_coordinate_df                     = feasible_shading_uid_building_coordinate_df[feasible_shading_uid_building_coordinate_df_filter_df.isin(feasible_shading_coordinate_filter_df)].reset_index(drop=True)
        feasible_shading_coordinate_df                                  = feasible_shading_coordinate_df.join(feasible_shading_uid_building_coordinate_df.set_index(feasible_mapping_uid_building_shading_coordinate_condition_keys), on=feasible_mapping_uid_building_shading_coordinate_condition_keys, validate='m:m')
        feasible_shading_coordinate_df                                  = feasible_shading_coordinate_df.dropna()
        #print("\nFeasible Shading Coordinate Data Frame \n", feasible_shading_coordinate_df)
        return feasible_shading_coordinate_df

    def shading_altitude_angle_calculation_function(uid_building_width, uid_building_latitude, uid_building_longitude, shading_angle_row_fixture_df, shading_angle_col_fixture_df,  shading_angle_df, feasible_shading_coordinate_df, feasible_shading_uid_building_digital_elevation_model_height_df):
        
        if feasible_shading_coordinate_df.shape[0]!=0:
            uid_building_coordinate_df          = pd.DataFrame([[uid_building_latitude, uid_building_longitude]]*(feasible_shading_coordinate_df.shape[0]))
            uid_building_coordinate_df.columns  = ['lat', 'long']

             # Calculation of Distance between Desired Building and Possible Shading Building
            distance_between_desired_building_and_shading_building_df = distance_between_two_coordinate_calculation_function(uid_building_coordinate_df['lat'], uid_building_coordinate_df['long'], feasible_shading_coordinate_df['lat'], feasible_shading_coordinate_df['long'])

            #Mapping Feasible uid building DEM into Feasible shading Coordinate
            feasible_mapping_uid_building_dem_coordinate_condition_keys                 = list(feasible_shading_coordinate_df.columns.values)[feasible_shading_coordinate_df.columns.get_loc('uid')]
            feasible_shading_uid_building_digital_elevation_model_height_df_filter_df   = feasible_shading_uid_building_digital_elevation_model_height_df.set_index(feasible_mapping_uid_building_dem_coordinate_condition_keys).index
            feasible_shading_coordinate_filter_df                                       = feasible_shading_coordinate_df.set_index(feasible_mapping_uid_building_dem_coordinate_condition_keys).index
            feasible_shading_uid_building_digital_elevation_model_height_df             = feasible_shading_uid_building_digital_elevation_model_height_df[feasible_shading_uid_building_digital_elevation_model_height_df_filter_df.isin(feasible_shading_coordinate_filter_df)].reset_index(drop=True)
            feasible_shading_coordinate_df                                              = feasible_shading_coordinate_df.join(feasible_shading_uid_building_digital_elevation_model_height_df.set_index(feasible_mapping_uid_building_dem_coordinate_condition_keys), on=feasible_mapping_uid_building_dem_coordinate_condition_keys, validate='m:m')

            # Calculation of Height Difference between Desired Building and Possible Shading Building
            center_uid_building_digital_elevation_model_height_df = pd.DataFrame([[center_uid_building_digital_elevation_model_height]]*(feasible_shading_coordinate_df.shape[0])).set_index(feasible_shading_coordinate_df.index)
            
            uid_building_rooftop_height_df                                          = pd.DataFrame([[uid_building_rooftop_height]]*(feasible_shading_coordinate_df.shape[0])).set_index(feasible_shading_coordinate_df.index)
            height_difference_between_disired_building_and_shading_building_series  = (feasible_shading_coordinate_df['rooftop']+feasible_shading_coordinate_df['DEM']) - (uid_building_rooftop_height_df[0]+ center_uid_building_digital_elevation_model_height_df[0])
            height_difference_between_disired_building_and_shading_building_df      = height_difference_between_disired_building_and_shading_building_series.to_frame().reset_index(drop=True).set_index(feasible_shading_coordinate_df.index)

            # Calculation of Angle between Desired Building Rooftop and Possible Shading Building Rooftop
            shading_angle_df                = Rad2Deg(np.arctan(height_difference_between_disired_building_and_shading_building_df/distance_between_desired_building_and_shading_building_df)).round(6)
            shading_angle_df_condition      = (distance_between_desired_building_and_shading_building_df<=(uid_building_width/2))
            shading_angle_df                = pd.DataFrame(np.where(shading_angle_df_condition, 90, shading_angle_df), index=distance_between_desired_building_and_shading_building_df.index, columns=['shading angle'])
            feasible_shading_coordinate_df  = feasible_shading_coordinate_df.drop(feasible_shading_coordinate_df.columns[[0,1,2,-4,-3,-2,-1]], axis=1)
            feasible_shading_angle_df       =  pd.DataFrame(shading_angle_df.transpose().values.tolist()*feasible_shading_coordinate_df.shape[1]).transpose()
            feasible_shading_angle_df       = pd.DataFrame(np.where(feasible_shading_coordinate_df!=0, feasible_shading_angle_df, 0), index=distance_between_desired_building_and_shading_building_df.index)
            feasible_shading_angle_df       = feasible_shading_angle_df.groupby(level=0).max()
        else:
            feasible_shading_angle_df       = pd.DataFrame([[0]*shading_angle_col_fixture_df.shape[0]]*shading_angle_row_fixture_df.shape[0], index=shading_angle_row_fixture_df.index)

        return feasible_shading_angle_df
    
    #print("Feasible uid Coordinate:\n", feasible_shading_uid_building_coordinate_df)
    if feasible_shading_uid_building_coordinate_df.shape[0] > 0:
        print("Feasible Shading uid Building: TRUE")
        feasible_shading_coordinate_df                                  = feasible_shading_coordinate_calculation_function(feasible_shading_coordinate_df, feasible_shading_uid_building_coordinate_df)
        shading_angle_df                                                = shading_altitude_angle_calculation_function(uid_building_width, uid_building_latitude, uid_building_longitude, shading_angle_row_fixture_df, shading_angle_col_fixture_df, shading_angle_df, feasible_shading_coordinate_df, feasible_shading_uid_building_digital_elevation_model_height_df)
        feasible_shading_coordinate_mapping_shading_angle_df            = feasible_shading_coordinate_df.groupby(level=0).max().copy()
        desired_feasible_shading_coordinate_mapping_shading_angle_df    = feasible_shading_coordinate_mapping_shading_angle_df.drop(feasible_shading_coordinate_mapping_shading_angle_df.columns[[0,1,2,-3,-2,-1]], axis=1)
        if desired_feasible_shading_coordinate_mapping_shading_angle_df.shape[0]!=0:
            global_shading_angle_uid_building_df                        = pd.DataFrame(np.where(desired_feasible_shading_coordinate_mapping_shading_angle_df!=0, shading_angle_df,0), index=desired_feasible_shading_coordinate_mapping_shading_angle_df.index)
        else:
            global_shading_angle_uid_building_df                        = pd.DataFrame([[1]*shading_angle_col_fixture_df.shape[0]]*shading_angle_row_fixture_df.shape[0], index=sun_azimuth_angle_df.index)
    else:
        print("Feasible Shading uid Building: FALSE")
        feasible_shading_coordinate_mapping_shading_angle_df            = feasible_shading_coordinate_df.groupby(level=0).max().copy()
        desired_feasible_shading_coordinate_mapping_shading_angle_df    = feasible_shading_coordinate_mapping_shading_angle_df.drop(feasible_shading_coordinate_mapping_shading_angle_df.columns[[0,1,2]], axis=1)
        global_shading_angle_uid_building_df                            = pd.DataFrame(np.where(desired_feasible_shading_coordinate_mapping_shading_angle_df!=0, 0,0), index=desired_feasible_shading_coordinate_mapping_shading_angle_df.index)
    
    global_shading_angle_uid_building_df = global_shading_angle_uid_building_df.groupby(level=0).max()
    global_shading_angle_uid_building_df = shading_angle_row_fixture_df.join(global_shading_angle_uid_building_df, lsuffix='_left')
    global_shading_angle_uid_building_df = global_shading_angle_uid_building_df.fillna(0)
    global_shading_angle_uid_building_df = global_shading_angle_uid_building_df[global_shading_angle_uid_building_df.columns[1:]].reset_index(drop=True)
    #print("global shading angle uid :\n", global_shading_angle_uid_building_df)
    return global_shading_angle_uid_building_df


def convert_azimuth_angle_system2trigonometry_system(azimuth_angle_df):

    convert_azimuth_angle_system2trigonometry_system_conditions = [((180>=azimuth_angle_df)&(azimuth_angle_df>0)),
                                                                   ((0>=azimuth_angle_df)&(azimuth_angle_df>=-180))
                                                                   ]
    def convert_azimuth_angle_system2trigonometry_system_condition1_choice(azimuth_angle_df):
        azimuth_angle_df = pd.DataFrame(np.where((180>=azimuth_angle_df)&(azimuth_angle_df>0), azimuth_angle_df-90, azimuth_angle_df))
        azimuth_angle_df = pd.DataFrame(np.where((0>azimuth_angle_df), azimuth_angle_df+360, azimuth_angle_df))
        return azimuth_angle_df
    
    def convert_azimuth_angle_system2trigonometry_system_condition2_choice(azimuth_angle_df):
        azimuth_angle_df = pd.DataFrame(np.where((0>=azimuth_angle_df)&(azimuth_angle_df>=-180), azimuth_angle_df+270, azimuth_angle_df))
        azimuth_angle_df = pd.DataFrame(np.where((0>azimuth_angle_df), azimuth_angle_df+360, azimuth_angle_df))
        return azimuth_angle_df
    
    convert_azimuth_angle_system2trigonometry_system_choices = [convert_azimuth_angle_system2trigonometry_system_condition1_choice(azimuth_angle_df),
                                                                convert_azimuth_angle_system2trigonometry_system_condition2_choice(azimuth_angle_df)
                                                                ]
    azimuth_angle_df = pd.DataFrame(np.select(convert_azimuth_angle_system2trigonometry_system_conditions, convert_azimuth_angle_system2trigonometry_system_choices, default=np.nan))

    return azimuth_angle_df

def distance_between_two_coordinate_calculation_function(latitude1_df, longitude1_df, latitude2_df, longitude2_df):
    earth_radius            = 6373.0 # Kilometers
    longitude1_df           = longitude1_df.to_frame().set_index([list(range(1,longitude1_df.shape[0]+1))]).squeeze()
    longitude1_df           = longitude1_df.reindex(longitude2_df.index, level=0)
    latitude1_df            = latitude1_df.to_frame().set_index([list(range(1,latitude1_df.shape[0]+1))]).squeeze()
    latitude1_df            = latitude1_df.reindex(latitude2_df.index, level=0)
    longitude2_df           = longitude2_df
    latitude2_df            = latitude2_df
    difference_longitude_df = (Deg2Rad(longitude2_df - longitude1_df))
    difference_latitude_df  = (Deg2Rad(latitude2_df - latitude1_df))
    a                       = (np.sin(difference_latitude_df/2))**2 + np.cos(Deg2Rad(latitude1_df)) * np.cos(Deg2Rad(latitude2_df)) * (np.sin(difference_longitude_df/2))**2
    c                       = 2 * np.atan2(np.sqrt(a), np.sqrt(1-a))
    distance_series         = earth_radius * c * 1000
    distance_df             = distance_series.to_frame().reset_index(drop=True).set_index(latitude2_df.index)
    #print(f"\nDistance: meters\n", distance_df)
    return distance_df

def Deg2Rad(deg):
    return deg * (np.pi / 180)
    
def Rad2Deg(rad):
    return rad * (180 / np.pi)

# Create CSV file for storing transmittance Data
def create_csvfile(csvfile_location, csvfile_local_name):
    csvfile_name = str(csvfile_location) + '/' + str(csvfile_local_name) + '.csv'
    with open(csvfile_name, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
    #print(f'csv file name: {csvfile_name}')
    return writer, csvfile_name