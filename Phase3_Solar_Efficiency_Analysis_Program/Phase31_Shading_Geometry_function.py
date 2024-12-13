import math
import numpy as np
import pandas as pd


def shading_geometry_function(attribute_table_csv_df, uid):

    uid_building_latitude = 16.4434
    uid_building_longitude = 102.839
    sun_azimuth_angle_df = pd.DataFrame([[45,135,55],[-45,-135,-55]])
    
    # Filtering uid Building causing shading on rooftop that computed solar irradiance and irradiation 
    feasible_shading_coordinate_df                = shading_filter_for_horizontal_angle_function(uid_building_latitude, uid_building_longitude, sun_azimuth_angle_df)
    feasible_shading_uid_building_coordinate_keys = list(feasible_shading_coordinate_df.columns.values)[0:2]
    attribute_table_csv_filter_df                 = attribute_table_csv_df.set_index(feasible_shading_uid_building_coordinate_keys).index
    feasible_shading_coordinate_filter_df         = feasible_shading_coordinate_df.set_index(feasible_shading_uid_building_coordinate_keys).index
    feasible_shading_uid_building_coordinate_df   = attribute_table_csv_df[attribute_table_csv_filter_df.isin(feasible_shading_coordinate_filter_df)].reset_index(drop=True)
    #print(feasible_shading_uid_building_coordinate_df)

    uid_building_rooftop_height = 3
    sun_altitude_angle = 1
    uid_building_digital_elevation_model_height = 0

    shading_angle_df = shading_filter_for_vertical_angle_function(uid_building_latitude, uid_building_longitude, uid_building_digital_elevation_model_height, uid_building_rooftop_height, sun_altitude_angle, feasible_shading_uid_building_coordinate_df)

    shading_factor = 1 

    return shading_factor

def shading_filter_for_horizontal_angle_function(uid_building_latitude, uid_building_longitude, sun_azimuth_angle_df):
    # Test Building Latitude and Longtitude
    #print(f"Building Latitude:{uid_building_latitude}, Building Longitude:{uid_building_longitude}")
    #print(f"Sun Azimuth Angle: {sun_azimuth_angle}")

    radius_of_shading_calculation = 2 # 0.050 degree of latitude and longitude
    horizontal_angle_interval_of_shading_calculation = 7.5 # +-7.5 degree of horizontal plane angle
    latitude_interval             = radius_of_shading_calculation
    longitude_interval            = radius_of_shading_calculation

    # Calculate Shading only Direction of Sun Azimuth Angle
    sun_azimuth_angle_df = convert_azimuth_angle_system2trigonometry_system(sun_azimuth_angle_df)

    # Coordinate Plane (Quadrant1-4)
    feasible_shading_coordinate_plane_row_level_zero_list    = list(range(1,(sun_azimuth_angle_df.shape[0])+1))
    feasible_shading_coordinate_plane_row_level_one_list     = list(range(-latitude_interval, latitude_interval+1))
    feasible_shading_coordinate_plane_row_iterables          = [feasible_shading_coordinate_plane_row_level_zero_list, feasible_shading_coordinate_plane_row_level_one_list]
    feasible_shading_coordinate_plane_row_index_df           = pd.MultiIndex.from_product(feasible_shading_coordinate_plane_row_iterables, names=["1st row", "2nd row"])
    feasible_shading_coordinate_plane_row_index_list         = list(range(-latitude_interval, latitude_interval+1))
    
    feasible_shading_coordinate_plane_column_level_zero_list = list(range(1,(sun_azimuth_angle_df.shape[1])+1))
    feasible_shading_coordinate_plane_column_level_one_list  = list(range(-longitude_interval, longitude_interval+1))
    feasible_shading_coordinate_plane_column_iterables       = [feasible_shading_coordinate_plane_column_level_zero_list, feasible_shading_coordinate_plane_column_level_one_list]
    feasible_shading_coordinate_plane_column_index_df        = pd.MultiIndex.from_product(feasible_shading_coordinate_plane_column_iterables, names=["1st col", "2nd col"])

    coordinate_plane_list                        = list(range(-latitude_interval,(latitude_interval+1),1) for x in range (-longitude_interval,(longitude_interval+1),1))
    feasible_shading_coordinate_plane_df         = pd.DataFrame(list(zip(*(coordinate_plane_list*(sun_azimuth_angle_df.shape[1]))))*((sun_azimuth_angle_df.shape[0])), index=feasible_shading_coordinate_plane_row_index_df, columns=feasible_shading_coordinate_plane_column_index_df)
    feasible_shading_coordinate_plane_df         = pd.DataFrame(np.where(feasible_shading_coordinate_plane_df==0, 1, feasible_shading_coordinate_plane_df))
    feasible_shading_coordinate_plane_df.columns = feasible_shading_coordinate_plane_column_index_df
    feasible_shading_coordinate_plane_df         = feasible_shading_coordinate_plane_df.set_index([feasible_shading_coordinate_plane_row_index_df])

    # Filter only Latitude that is feasible with calculation radius
    feasible_shading_coordinate_plane_df         = pd.DataFrame(np.where(abs(feasible_shading_coordinate_plane_df)<(((latitude_interval**2)-(feasible_shading_coordinate_plane_df.columns.get_level_values(1)**2))**(1/2)), feasible_shading_coordinate_plane_df, 0), index=feasible_shading_coordinate_plane_row_index_df, columns=feasible_shading_coordinate_plane_column_index_df)
    
    # Computing uid Building Azimuth Angle
    azimuth_angle_upper_bound_df = sun_azimuth_angle_df + horizontal_angle_interval_of_shading_calculation
    azimuth_angle_lower_bound_df = sun_azimuth_angle_df - horizontal_angle_interval_of_shading_calculation

    azimuth_angle_upper_bound_df = pd.DataFrame(azimuth_angle_upper_bound_df.values.tolist()*len(feasible_shading_coordinate_plane_column_level_one_list))
    print(azimuth_angle_upper_bound_df.stack(future_stack=True))
    azimuth_angle_upper_bound_df = pd.DataFrame(azimuth_angle_upper_bound_df.stack(future_stack=True).reset_index(drop=True)).transpose()
    print(azimuth_angle_upper_bound_df)
    azimuth_angle_lower_bound_df = pd.DataFrame(azimuth_angle_lower_bound_df.values.tolist()*len(feasible_shading_coordinate_plane_column_level_one_list))
    azimuth_angle_lower_bound_df = pd.DataFrame(azimuth_angle_lower_bound_df.stack(future_stack=True).reset_index(drop=True)).transpose()

    azimuth_angle_upper_bound_df = pd.DataFrame(np.where(azimuth_angle_upper_bound_df>360,azimuth_angle_upper_bound_df-360,azimuth_angle_upper_bound_df ))
    azimuth_angle_lower_bound_df = pd.DataFrame(np.where(azimuth_angle_lower_bound_df<0, azimuth_angle_lower_bound_df+360,azimuth_angle_lower_bound_df))
    azimuth_angle_upper_bound_factor_df = np.tan(Deg2Rad(azimuth_angle_upper_bound_df))
    azimuth_angle_lower_bound_factor_df = np.tan(Deg2Rad(azimuth_angle_lower_bound_df))

    print(feasible_shading_coordinate_plane_df.columns.get_level_values(1))
    print(azimuth_angle_upper_bound_factor_df)

    azimuth_angle_upper_bound_factor_check_condition_df = pd.DataFrame((pd.DataFrame(pd.DataFrame(feasible_shading_coordinate_plane_df.columns.get_level_values(1)*azimuth_angle_upper_bound_factor_df)).values.tolist())*len(feasible_shading_coordinate_plane_row_index_df), index=feasible_shading_coordinate_plane_row_index_df, columns=feasible_shading_coordinate_plane_column_index_df)
    azimuth_angle_lower_bound_factor_check_condition_df = pd.DataFrame((pd.DataFrame(pd.DataFrame(feasible_shading_coordinate_plane_df.columns.get_level_values(1)*azimuth_angle_lower_bound_factor_df)).values.tolist())*len(feasible_shading_coordinate_plane_row_index_df), index=feasible_shading_coordinate_plane_row_index_df, columns=feasible_shading_coordinate_plane_column_index_df)
   
    #print(f"Condition1: {(90>azimuth_upper_bound>=0 or 360>=azimuth_upper_bound>270) and (90>azimuth_lower_bound>=0 or 360>=azimuth_lower_bound>270)}")
    #print(f"Condition2: {270>azimuth_upper_bound>90 and 270>azimuth_lower_bound>90}")
    #print(f"Condition3: {azimuth_upper_bound>=90 and azimuth_lower_bound<=90}")
    #print(f"Condition4: {azimuth_upper_bound>=270 and azimuth_lower_bound<=270}")

    feasible_shading_coordinate_plane_conditions = [((((90>azimuth_angle_upper_bound_df)&(azimuth_angle_upper_bound_df>=0))|((360>=azimuth_angle_upper_bound_df)&(azimuth_angle_upper_bound_df>270)))&(((90>azimuth_angle_lower_bound_df)&(azimuth_angle_lower_bound_df>=0))|((360>=azimuth_angle_lower_bound_df)&(azimuth_angle_lower_bound_df>270)))), 
                                                    (((270>azimuth_angle_upper_bound_df)&(azimuth_angle_upper_bound_df>90))&((270>azimuth_angle_lower_bound_df)&(azimuth_angle_lower_bound_df>90))),
                                                    ((azimuth_angle_upper_bound_df>=90)&(azimuth_angle_lower_bound_df<=90)),
                                                    ((azimuth_angle_upper_bound_df>=270)&(azimuth_angle_lower_bound_df<=270))
                                                    ]
    
    def feasible_shading_coordinate_plane_condition1_choice(feasible_shading_coordinate_plane_df,azimuth_angle_upper_bound_factor_check_condition_df,azimuth_angle_lower_bound_factor_check_condition_df,feasible_shading_coordinate_plane_row_index_list,feasible_shading_coordinate_plane_column_index_df):
        feasible_shading_coordinate_plane_df = pd.DataFrame((np.where(feasible_shading_coordinate_plane_df <= (azimuth_angle_upper_bound_factor_check_condition_df), feasible_shading_coordinate_plane_df, 0)), index=feasible_shading_coordinate_plane_row_index_list, columns=feasible_shading_coordinate_plane_column_index_df)
        feasible_shading_coordinate_plane_df = pd.DataFrame((np.where(feasible_shading_coordinate_plane_df >= (azimuth_angle_lower_bound_factor_check_condition_df), feasible_shading_coordinate_plane_df, 0)), index=feasible_shading_coordinate_plane_row_index_list, columns=feasible_shading_coordinate_plane_column_index_df)
        return feasible_shading_coordinate_plane_df
    
    def feasible_shading_coordinate_plane_condition2_choice(feasible_shading_coordinate_plane_df,azimuth_angle_upper_bound_factor_check_condition_df,azimuth_angle_lower_bound_factor_check_condition_df,feasible_shading_coordinate_plane_row_index_list,feasible_shading_coordinate_plane_column_index_df):
        feasible_shading_coordinate_plane_df = pd.DataFrame((np.where(feasible_shading_coordinate_plane_df >= (azimuth_angle_upper_bound_factor_check_condition_df), feasible_shading_coordinate_plane_df, 0)), index=feasible_shading_coordinate_plane_row_index_list, columns=feasible_shading_coordinate_plane_column_index_df)
        feasible_shading_coordinate_plane_df = pd.DataFrame((np.where(feasible_shading_coordinate_plane_df <= (azimuth_angle_lower_bound_factor_check_condition_df), feasible_shading_coordinate_plane_df, 0)), index=feasible_shading_coordinate_plane_row_index_list, columns=feasible_shading_coordinate_plane_column_index_df)
        return feasible_shading_coordinate_plane_df
    
    def feasible_shading_coordinate_plane_condition3_choice(feasible_shading_coordinate_plane_df,azimuth_angle_upper_bound_factor_check_condition_df, azimuth_angle_lower_bound_factor_check_condition_df,feasible_shading_coordinate_plane_row_index_list,feasible_shading_coordinate_plane_column_index_df):
        feasible_shading_coordinate_plane_condition3_conditions = [(azimuth_angle_upper_bound_df==90), (azimuth_angle_upper_bound_df!=90)]
        
        def feasible_shading_coordinate_plane_condition3_condition1_choice(feasible_shading_coordinate_plane_df, azimuth_angle_upper_bound_factor_check_condition_df, azimuth_angle_lower_bound_factor_check_condition_df, feasible_shading_coordinate_plane_row_index_list, feasible_shading_coordinate_plane_column_index_df):
            feasible_shading_coordinate_plane_df         = pd.DataFrame((np.where(feasible_shading_coordinate_plane_df <= (azimuth_angle_upper_bound_factor_check_condition_df), feasible_shading_coordinate_plane_df, 0)), index=feasible_shading_coordinate_plane_row_index_list, columns=feasible_shading_coordinate_plane_column_index_df)
            feasible_shading_coordinate_plane_df         = pd.DataFrame((np.where(feasible_shading_coordinate_plane_df >= (azimuth_angle_lower_bound_factor_check_condition_df), feasible_shading_coordinate_plane_df, 0)), index=feasible_shading_coordinate_plane_row_index_list, columns=feasible_shading_coordinate_plane_column_index_df)
            return feasible_shading_coordinate_plane_df
        
        def feasible_shading_coordinate_plane_condition3_condition1_choice(feasible_shading_coordinate_plane_df, azimuth_angle_upper_bound_factor_check_condition_df, azimuth_angle_lower_bound_factor_check_condition_df, feasible_shading_coordinate_plane_row_index_list, feasible_shading_coordinate_plane_column_index_df):
            feasible_shading_coordinate_plane_df         = pd.DataFrame((np.where(feasible_shading_coordinate_plane_df >= (azimuth_angle_upper_bound_factor_check_condition_df), feasible_shading_coordinate_plane_df, 0)), index=feasible_shading_coordinate_plane_row_index_list, columns=feasible_shading_coordinate_plane_column_index_df)
            feasible_shading_coordinate_plane_df         = pd.DataFrame((np.where(feasible_shading_coordinate_plane_df >= (azimuth_angle_lower_bound_factor_check_condition_df), feasible_shading_coordinate_plane_df, 0)), index=feasible_shading_coordinate_plane_row_index_list, columns=feasible_shading_coordinate_plane_column_index_df)
            return feasible_shading_coordinate_plane_df

        feasible_shading_coordinate_plane_condition3_choices = [feasible_shading_coordinate_plane_condition3_condition1_choice(feasible_shading_coordinate_plane_df, azimuth_angle_upper_bound_factor_check_condition_df, azimuth_angle_lower_bound_factor_check_condition_df, feasible_shading_coordinate_plane_row_index_list, feasible_shading_coordinate_plane_column_index_df),
                                                                feasible_shading_coordinate_plane_condition3_condition1_choice(feasible_shading_coordinate_plane_df, azimuth_angle_upper_bound_factor_check_condition_df, azimuth_angle_lower_bound_factor_check_condition_df, feasible_shading_coordinate_plane_row_index_list, feasible_shading_coordinate_plane_column_index_df)
                                                                ]
        feasible_shading_coordinate_plane_df = pd.DataFrame(np.select(feasible_shading_coordinate_plane_condition3_conditions, feasible_shading_coordinate_plane_condition3_choices, default=np.nan), index=feasible_shading_coordinate_plane_row_index_list, columns=feasible_shading_coordinate_plane_column_index_df)
        return feasible_shading_coordinate_plane_df
    
    def feasible_shading_coordinate_plane_condition4_choice(feasible_shading_coordinate_plane_df,azimuth_angle_upper_bound_factor_check_condition_df,aazimuth_angle_lower_bound_factor_check_condition_df,feasible_shading_coordinate_plane_row_index_list,feasible_shading_coordinate_plane_column_index_df):
        feasible_shading_coordinate_plane_condition4_conditons = [(azimuth_angle_upper_bound_df==270), (azimuth_angle_upper_bound_df!=270)]

        def feasible_shading_coordinate_plane_condition4_conditon1_choice(feasible_shading_coordinate_plane_df,azimuth_angle_upper_bound_factor_check_condition_df,azimuth_angle_lower_bound_factor_check_condition_df,feasible_shading_coordinate_plane_row_index_list,feasible_shading_coordinate_plane_column_index_df):
            feasible_shading_coordinate_plane_df         = pd.DataFrame((np.where(feasible_shading_coordinate_plane_df >= (azimuth_angle_upper_bound_factor_check_condition_df), feasible_shading_coordinate_plane_df, 0)), index=feasible_shading_coordinate_plane_row_index_list, columns=feasible_shading_coordinate_plane_column_index_df)
            feasible_shading_coordinate_plane_df         = pd.DataFrame((np.where(feasible_shading_coordinate_plane_df <= (azimuth_angle_lower_bound_factor_check_condition_df), feasible_shading_coordinate_plane_df, 0)), index=feasible_shading_coordinate_plane_row_index_list, columns=feasible_shading_coordinate_plane_column_index_df)
            return feasible_shading_coordinate_plane_df
        
        def feasible_shading_coordinate_plane_condition4_conditon2_choice(feasible_shading_coordinate_plane_df,azimuth_angle_upper_bound_factor_check_condition_df,azimuth_angle_lower_bound_factor_check_condition_df,feasible_shading_coordinate_plane_row_index_list,feasible_shading_coordinate_plane_column_index_df):
            feasible_shading_coordinate_plane_df         = pd.DataFrame((np.where(feasible_shading_coordinate_plane_df <= (azimuth_angle_upper_bound_factor_check_condition_df), feasible_shading_coordinate_plane_df, 0)), index=feasible_shading_coordinate_plane_row_index_list, columns=feasible_shading_coordinate_plane_column_index_df)
            feasible_shading_coordinate_plane_df         = pd.DataFrame((np.where(feasible_shading_coordinate_plane_df <= (azimuth_angle_lower_bound_factor_check_condition_df), feasible_shading_coordinate_plane_df, 0)), index=feasible_shading_coordinate_plane_row_index_list, columns=feasible_shading_coordinate_plane_column_index_df)
            return feasible_shading_coordinate_plane_df

        feasible_shading_coordinate_plane_condition4_choices = [feasible_shading_coordinate_plane_condition4_conditon1_choice(feasible_shading_coordinate_plane_df,azimuth_angle_upper_bound_factor_check_condition_df,azimuth_angle_lower_bound_factor_check_condition_df,feasible_shading_coordinate_plane_row_index_list,feasible_shading_coordinate_plane_column_index_df),
                                                                feasible_shading_coordinate_plane_condition4_conditon2_choice(feasible_shading_coordinate_plane_df,azimuth_angle_upper_bound_factor_check_condition_df,azimuth_angle_lower_bound_factor_check_condition_df,feasible_shading_coordinate_plane_row_index_list,feasible_shading_coordinate_plane_column_index_df)
                                                                ]
        feasible_shading_coordinate_plane_df = pd.DataFrame(np.select(feasible_shading_coordinate_plane_condition4_conditons,feasible_shading_coordinate_plane_condition4_choices, default=np.nan), index=feasible_shading_coordinate_plane_row_index_list, columns=feasible_shading_coordinate_plane_column_index_df)
        return feasible_shading_coordinate_plane_df
    

    feasible_shading_coordinate_plane_condition_choices = [feasible_shading_coordinate_plane_condition1_choice(feasible_shading_coordinate_plane_df,azimuth_angle_upper_bound_factor_check_condition_df,azimuth_angle_lower_bound_factor_check_condition_df,feasible_shading_coordinate_plane_row_index_list,feasible_shading_coordinate_plane_column_index_df),
                                                           feasible_shading_coordinate_plane_condition2_choice(feasible_shading_coordinate_plane_df,azimuth_angle_upper_bound_factor_check_condition_df,azimuth_angle_lower_bound_factor_check_condition_df,feasible_shading_coordinate_plane_row_index_list,feasible_shading_coordinate_plane_column_index_df),
                                                           feasible_shading_coordinate_plane_condition3_choice(feasible_shading_coordinate_plane_df,azimuth_angle_upper_bound_factor_check_condition_df,azimuth_angle_lower_bound_factor_check_condition_df,feasible_shading_coordinate_plane_row_index_list,feasible_shading_coordinate_plane_column_index_df),
                                                           feasible_shading_coordinate_plane_condition4_choice(feasible_shading_coordinate_plane_df,azimuth_angle_upper_bound_factor_check_condition_df,azimuth_angle_lower_bound_factor_check_condition_df,feasible_shading_coordinate_plane_row_index_list,feasible_shading_coordinate_plane_column_index_df)
                                                          ]
    
    feasible_shading_coordinate_plane_df = pd.DataFrame((np.select(feasible_shading_coordinate_plane_conditions,feasible_shading_coordinate_plane_condition_choices, default=np.nan)))
    feasible_shading_coordinate_plane_df = pd.DataFrame(np.where(feasible_shading_coordinate_plane_df!=0, (feasible_shading_coordinate_plane_df/10000)+uid_building_latitude, 0))

    feasible_shading_coordinate_plane_row_index_list         = pd.DataFrame((pd.DataFrame(list(range(-latitude_interval,latitude_interval+1,1)))/10000)+uid_building_latitude).transpose().values.tolist()
    feasible_shading_coordinate_plane_column_level_one_list  = pd.DataFrame((pd.DataFrame(list(range(-longitude_interval,(longitude_interval+1),1)))/10000)+uid_building_longitude).transpose().values.tolist()
    feasible_shading_coordinate_plane_column_iterables       = [feasible_shading_coordinate_plane_column_level_zero_list, feasible_shading_coordinate_plane_column_level_one_list[0]]
    feasible_shading_coordinate_plane_column_index_df        = pd.MultiIndex.from_product(feasible_shading_coordinate_plane_column_iterables, names=["first", "second"])

    feasible_shading_coordinate_plane_df.columns            = feasible_shading_coordinate_plane_column_index_df
    feasible_shading_coordinate_plane_df                    = feasible_shading_coordinate_plane_df.set_index([pd.Index(feasible_shading_coordinate_plane_row_index_list[0])])
    feasible_shading_coordinate_plane_df            = feasible_shading_coordinate_plane_df.sort_index(ascending=False).stack(future_stack=True).reset_index()
    feasible_shading_coordinate_plane_df.columns    = ["lat", "long"] + list(range(1,(sun_azimuth_angle_df.shape[1])+1))
    feasible_shading_coordinate_df = feasible_shading_coordinate_plane_df.loc[np.count_nonzero(feasible_shading_coordinate_plane_df.loc[:,1:],axis=1)>0]
    
    print(feasible_shading_coordinate_plane_df)
    print(feasible_shading_coordinate_df)
    print('Length of Feasible Coordinates:',len(feasible_shading_coordinate_df))
    return  feasible_shading_coordinate_df

def shading_filter_for_vertical_angle_function(uid_building_latitude, uid_building_longitude, uid_building_digital_elevation_model_height, uid_building_rooftop_height, sun_altitude_angle, feasible_shading_uid_building_coordinate_df):
    # Calcualtion of Distance between Desired Building and Possible Shading Building
    uid_building_coordinate_df = pd.DataFrame([[uid_building_latitude, uid_building_longitude]]*(len(feasible_shading_uid_building_coordinate_df)))
    uid_building_coordinate_df.columns = ['lat', 'long']
    distance_between_desired_building_and_shading_building_df = distance_between_two_coordinate_calculation_function(uid_building_coordinate_df['lat'], uid_building_coordinate_df['long'], feasible_shading_uid_building_coordinate_df['lat'], feasible_shading_uid_building_coordinate_df['long'])
    
    # Calculation of Height Difference between Desired Building and Possible Shading Building
    uid_building_digital_elevation_model_height_df = pd.DataFrame([[uid_building_digital_elevation_model_height]]*(len(feasible_shading_uid_building_coordinate_df)))
    ### Waiting For Digital Elevation Model Data ###
    feasible_shading_uid_building_digital_elevation_model_height_df = pd.DataFrame([[0]]*(len(feasible_shading_uid_building_coordinate_df)))
    uid_building_rooftop_height_df = pd.DataFrame([[uid_building_rooftop_height]]*(len(feasible_shading_uid_building_coordinate_df)))
    height_difference_between_disired_building_and_shading_building_series = (feasible_shading_uid_building_coordinate_df['rooftop']+feasible_shading_uid_building_digital_elevation_model_height_df[0]) - (uid_building_rooftop_height_df[0]+ uid_building_digital_elevation_model_height_df[0])
    height_difference_between_disired_building_and_shading_building_df = height_difference_between_disired_building_and_shading_building_series.to_frame().reset_index(drop=True)
    height_difference_between_desired_building_and_shading_building_filter = height_difference_between_disired_building_and_shading_building_df[0]>=0
    height_difference_between_disired_building_and_shading_building_df = height_difference_between_disired_building_and_shading_building_df[height_difference_between_desired_building_and_shading_building_filter].reset_index(drop=True)
    #print('Height Difference: meter\n', height_difference_between_disired_building_and_shading_building_df)

    # Calculation of Angle between Desired Building Rooftop and Possible Shading Building Rooftop
    shading_angle_df = Rad2Deg(np.arctan(height_difference_between_disired_building_and_shading_building_df/distance_between_desired_building_and_shading_building_df))
    print(shading_angle_df)
    return shading_angle_df

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

def distance_between_two_coordinate_calculation_function(latitude1, longitude1, latitude2, longitude2):
    earth_radius = 6373.0 # Kilometers
    difference_longitude = Deg2Rad(longitude2 - longitude1)
    difference_latitude  = Deg2Rad(latitude2 - latitude1)
    a = (np.sin(difference_latitude/2))**2 + np.cos(Deg2Rad(latitude1)) * np.cos(Deg2Rad(latitude2)) * (np.sin(difference_longitude/2))**2
    c = 2 * np.atan2(np.sqrt(a), np.sqrt(1-a))
    distance_series = earth_radius * c * 1000
    distance_df = distance_series.to_frame().reset_index(drop=True)
    #print(f"Distance: meters\n", distance_df)
    return distance_df

def Deg2Rad(deg):
    return deg * (np.pi / 180)
    
def Rad2Deg(rad):
    return rad * (180 / np.pi)

uid_building_latitude = 16.4421
uid_building_longitude = 102.839
sun_azimuth_angle_df = 45

uid_building_latitude2 = 16.4421
uid_building_longitude2 = 102.840

attribute_table_csvfile_name = r"C:\GISTDA\Solarcells_Project\Solar_Efficiency_Analysis_Program2.1\Attribute_Table_Data\Building_Attribute_Table_LOD200_Draft2.2.csv"
attribute_table_csv_df = pd.read_csv(attribute_table_csvfile_name)

uid = 1
shading_geometry_function(attribute_table_csv_df, uid)