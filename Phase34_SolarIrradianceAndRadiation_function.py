import math
import time
from datetime import datetime
import csv
import numpy as np
import pandas as pd

# Solar Constant (Isc = 1.3667 kilo Watts per square meter)
solar_constant = 1.3667 #kilo watts

def global_solar_irradiance_calculation_function(uid, building_fields_table_df, date_field_df, global_rooftop_geometry_df, solar_hour_angle_df, sun_azimuth_angle_df, sun_altitude_angle_df, shading_factor_df, global_transmittance_coeff_df_list, global_solar_irradiance_csvfile_location, global_solar_irradiation_csvfile_location, steps, barometric_pressure, angstrom_turbidity, start_time, stop_time):
    start_time_record = time.time()
    #end_julian_date = 2
    julian_date_df  = date_field_df[['julian date']]
    end_julian_date = julian_date_df.shape[0]

    # Writing Building characteristics to each row
    new_building_fields_tables_df = pd.DataFrame((building_fields_table_df.values.tolist())*end_julian_date, columns=building_fields_table_df.columns)

    separator_df = create_separator_df_function(end_julian_date)

    # Acquire Rooftop Geometry from Rooftop Geometry Data Frame
    global_rooftop_geometry_filter  = (global_rooftop_geometry_df['uid'] == uid)
    # Acquire latitide from Global Solar Irradiance Geometry Data Frame
    latitude_calculation_df         = pd.DataFrame([[building_fields_table_df.loc[0,'lat']]*solar_hour_angle_df.shape[1]]*solar_hour_angle_df.shape[0])
    # Acquire Rooftype e
    rooftype_series                 = global_rooftop_geometry_df.loc[global_rooftop_geometry_filter, 'rooftype']
    rooftype                        = rooftype_series.iloc[0]
    # Acquire Rooftop width 
    rooftop_width_calculation_df    = pd.DataFrame([global_rooftop_geometry_df.loc[global_rooftop_geometry_filter, 'width'].tolist()*solar_hour_angle_df.shape[1]]*solar_hour_angle_df.shape[0])
    # Acquire Rooftop length 
    rooftop_length_calculation_df   = pd.DataFrame([global_rooftop_geometry_df.loc[global_rooftop_geometry_filter, 'length'].tolist()*solar_hour_angle_df.shape[1]]*solar_hour_angle_df.shape[0])
    # Acquire Flat Rooftop Aream 
    flat_rooftop_area_df            = pd.DataFrame([global_rooftop_geometry_df.loc[global_rooftop_geometry_filter, 'area'].tolist()*solar_hour_angle_df.shape[1]]*solar_hour_angle_df.shape[0])
    # Acquire Rooftop Slope
    rooftop_slope_angle_df          = pd.DataFrame([global_rooftop_geometry_df.loc[global_rooftop_geometry_filter, 'rooftop slope'].tolist()*solar_hour_angle_df.shape[1]]*solar_hour_angle_df.shape[0])
    # Acquire Rooftop Azimuth
    rooftop_azimuth_angle_df        = pd.DataFrame([global_rooftop_geometry_df.loc[global_rooftop_geometry_filter, 'rooftop azimuth angle'].tolist()*solar_hour_angle_df.shape[1]]*solar_hour_angle_df.shape[0])

    # Adding Rooftop Slope and Rooftop Azimuth to Building Fields Tables
    new_rooftop_slope_df                    = rooftop_slope_angle_df[[0]]
    new_rooftop_slope_df.columns            = ['rooftop slope']
    new_rooftop_azimuth_angle_df            = rooftop_azimuth_angle_df[[0]]
    new_rooftop_azimuth_angle_df.columns    = ['rooftop azimuth angle']
    new_building_fields_tables_df           = pd.concat([new_building_fields_tables_df, new_rooftop_slope_df, new_rooftop_azimuth_angle_df],axis=1)

    # Writing Irradiance Fields
    total_solar_irradiance_global_df_column_index               = list(f"Solar Irradiance-{hour_time}:{minute_time}" for hour_time in range (start_time, stop_time+1) for minute_time in range(0, 60, steps))
    direct_normal_irradiance_column_index                       = list(f"Direct Normal Irradiance-{hour_time}:{minute_time}" for hour_time in range (start_time, stop_time+1) for minute_time in range(0, 60, steps))
    diffuse_irradiance_column_index                             = list(f"Diffuse Irradiance-{hour_time}:{minute_time}" for hour_time in range (start_time, stop_time+1) for minute_time in range(0, 60, steps))
    diffuse_irradiance_from_rayleigh_atmosphere_column_index    = list(f"Diffuse Irradiance from Rayleigh Atmosphere-{hour_time}:{minute_time}" for hour_time in range (start_time, stop_time+1) for minute_time in range(0, 60, steps))
    diffuse_irradiance_from_aerosol_scattering_column_index     = list(f"Diffuse Irradiance from Aerosol Scattering-{hour_time}:{minute_time}" for hour_time in range (start_time, stop_time+1) for minute_time in range(0, 60, steps))
    diffuse_irradiance_from_multiple_reflection_column_index    = list(f"Diffuse Irradiance from Multiple Reflection-{hour_time}:{minute_time}" for hour_time in range (start_time, stop_time+1) for minute_time in range(0, 60, steps))
    
    # Writing Irradiation Fields
    total_solar_irradiation_global_df_column_index              = list(f"Solar Irradiation-{hour_time}:{minute_time}" for hour_time in range (start_time, stop_time+1) for minute_time in range(0, 60, steps))
    direct_normal_irradiation_column_index                      = list(f"Direct Normal Irradiation-{hour_time}:{minute_time}" for hour_time in range (start_time, stop_time+1) for minute_time in range(0, 60, steps))
    diffuse_irradiation_column_index                            = list(f"Diffuse Irradiation-{hour_time}:{minute_time}" for hour_time in range (start_time, stop_time+1) for minute_time in range(0, 60, steps))
    diffuse_irradiation_from_rayleigh_atmosphere_column_index   = list(f"Diffuse Irradiation from Rayleigh Atmosphere-{hour_time}:{minute_time}" for hour_time in range (start_time, stop_time+1) for minute_time in range(0, 60, steps))
    diffuse_irradiation_from_aerosol_scattering_column_index    = list(f"Diffuse Irradiation from Aerosol Scattering-{hour_time}:{minute_time}" for hour_time in range (start_time, stop_time+1) for minute_time in range(0, 60, steps))
    diffuse_irradiation_from_multiple_reflection_column_index   = list(f"Diffuse Irradiation from Multiple Reflection-{hour_time}:{minute_time}" for hour_time in range (start_time, stop_time+1) for minute_time in range(0, 60, steps))

    # Acquire Declination Angle Data Frame and Eccentricity Correction Factor DataFrame
    declination_angle_df = pd.DataFrame(date_field_df[['Declination Angle']].transpose().values.tolist()*solar_hour_angle_df.shape[1]).transpose()
    eccentricity_correction_factor_df = pd.DataFrame(date_field_df[['Eccentricity Correction Factor']].transpose().values.tolist()*solar_hour_angle_df.shape[1]).transpose()

    # Acquire Transmittance Coefficient from Global Transmittance Coefficient csvfile
    # Acquire Cloud Transmittance Coefficient
    cloud_transmittance_coeff_df                    = global_transmittance_coeff_df_list[0]
    # Acquire Rayleigh Transmittance Coefficient
    rayleigh_transmittance_coeff_df                 = global_transmittance_coeff_df_list[1]
    # Acquire Scattering by Aerosol Transmittance Coefficient
    scattering_by_aerosol_transmittance_coeff_df    = global_transmittance_coeff_df_list[2]
    # Acquire Aerosol Transmittance Coefficient
    aerosol_transmittance_coeff_df                  = global_transmittance_coeff_df_list[3]
    # Acquire Water Vapor Transmittance Coefficient
    water_vapor_transmittance_coeff_df              = global_transmittance_coeff_df_list[4]
    # Acquire Mixed Gases Transmittance Coefficient
    mixed_gases_transmittance_coeff_df              = global_transmittance_coeff_df_list[5]
    # Acquire Ozone Transimittance Coefficient
    ozone_transmittance_coeff_df                    = global_transmittance_coeff_df_list[6]
    # Absorption Transmittance Coefficient Calculation
    absorption_transmittance_coeff_df = (aerosol_transmittance_coeff_df)*(water_vapor_transmittance_coeff_df)*(mixed_gases_transmittance_coeff_df)*(ozone_transmittance_coeff_df)

    # Direct Normal Irradiance Calculation:
    direct_normal_irradiance_df = direct_normal_irradiance_calculation_function(rooftype, rooftop_azimuth_angle_df, rooftop_slope_angle_df, declination_angle_df, eccentricity_correction_factor_df, latitude_calculation_df, solar_hour_angle_df, cloud_transmittance_coeff_df, absorption_transmittance_coeff_df, rayleigh_transmittance_coeff_df, scattering_by_aerosol_transmittance_coeff_df)
    
    # Direct Normal Irradiation Calculation:
    direct_normal_irradiation_df = direct_normal_irradiation_calculation_function(end_julian_date, rooftype, rooftop_width_calculation_df, rooftop_length_calculation_df, flat_rooftop_area_df, rooftop_azimuth_angle_df, rooftop_slope_angle_df, declination_angle_df, latitude_calculation_df, sun_azimuth_angle_df, sun_altitude_angle_df, solar_hour_angle_df, eccentricity_correction_factor_df, cloud_transmittance_coeff_df, absorption_transmittance_coeff_df, rayleigh_transmittance_coeff_df, scattering_by_aerosol_transmittance_coeff_df)

    # Diffuse Irradiance Calcualtion:
    diffuse_irradiance_df_list = diffuse_irradiance_calculation_function(direct_normal_irradiance_df, rayleigh_transmittance_coeff_df, scattering_by_aerosol_transmittance_coeff_df, absorption_transmittance_coeff_df, barometric_pressure, angstrom_turbidity)
    diffuse_irrandiance_on_any_surface_df           = diffuse_irradiance_df_list[0].round(6)
    diffuse_irradiance_from_rayleigh_atmosphere_df  = diffuse_irradiance_df_list[1].round(6)
    diffuse_irradiance_from_aerosol_scattering_df   = diffuse_irradiance_df_list[2].round(6)
    diffuse_irradiance_from_mutiple_reflection_df   = diffuse_irradiance_df_list[3].round(6)
    
    # Diffuse Irradiation Calculation:
    diffuse_irradiation_df_list = diffuse_irradiation_calculation_function(direct_normal_irradiation_df, rayleigh_transmittance_coeff_df, scattering_by_aerosol_transmittance_coeff_df, absorption_transmittance_coeff_df, barometric_pressure, angstrom_turbidity)
    diffuse_irrandiation_any_surface_df             = diffuse_irradiation_df_list[0].round(6)
    diffuse_irradiation_from_rayleigh_atmosphere_df = diffuse_irradiation_df_list[1].round(6)
    diffuse_irradiation_from_aerosol_scattering_df  = diffuse_irradiation_df_list[2].round(6)
    diffuse_irradiation_from_mutiple_reflection_df  = diffuse_irradiation_df_list[3].round(6)

    
    # Total Solar Irradiation into Data Frame
    # Total Irradiation Calculation:
    total_solar_irradiation_global_df                               = (direct_normal_irradiation_df.copy())*(shading_factor_df) + diffuse_irrandiation_any_surface_df.copy()
    total_solar_irradiation_global_df.columns                       = total_solar_irradiation_global_df_column_index

    # Total Solar Irradiance into Data Frame
    # Total Irradiance Calculation:
    total_solar_irradiance_global_df                                = (direct_normal_irradiance_df.copy())*(shading_factor_df) + diffuse_irrandiance_on_any_surface_df.copy()
    total_solar_irradiance_global_df                                = pd.DataFrame(np.where(total_solar_irradiation_global_df>0, total_solar_irradiance_global_df, 0))
    total_solar_irradiance_global_df.columns                        = total_solar_irradiance_global_df_column_index

    # Organize Direct Normal Irradiance into Data Frame
    direct_normal_irradiance_global_df                              = direct_normal_irradiance_df.copy()
    direct_normal_irradiance_global_df.columns                      = direct_normal_irradiance_column_index
    # Qrganize Direct Normal Irradiation into Data Frame
    direct_normal_irradiation_global_df                             = direct_normal_irradiation_df.copy()
    direct_normal_irradiation_global_df.columns                     = direct_normal_irradiation_column_index

    # Organize Diffuse Irradiance into Data Frame
    diffuse_irradiance_global_df                                    = diffuse_irrandiance_on_any_surface_df.copy()
    diffuse_irradiance_global_df.columns                            = diffuse_irradiance_column_index
    # Organize Diffuse Irradiation into Data Frame
    diffuse_irradiation_global_df                                   = diffuse_irrandiation_any_surface_df.copy()
    diffuse_irradiation_global_df.columns                           = diffuse_irradiation_column_index

    # Organise Diffuse Irradiance from Rayleigh Atmosphere into Data Frame
    diffuse_irradiance_from_rayleigh_atmosphere_global_df           = diffuse_irradiance_from_rayleigh_atmosphere_df.copy()
    diffuse_irradiance_from_rayleigh_atmosphere_global_df.columns   = diffuse_irradiance_from_rayleigh_atmosphere_column_index
    # Organize Diffuse Irradiaton from Raylrigh Atmosphere into Data Frame
    diffuse_irradiation_from_rayleigh_atmosphere_global_df          = diffuse_irradiation_from_rayleigh_atmosphere_df.copy()
    diffuse_irradiation_from_rayleigh_atmosphere_global_df.columns  = diffuse_irradiation_from_rayleigh_atmosphere_column_index

    # Organize Diffuse Irradiance from Aerosol Scattering into Data Frame
    diffuse_irradiance_from_aerosol_scattering_global_df            = diffuse_irradiance_from_aerosol_scattering_df.copy()
    diffuse_irradiance_from_aerosol_scattering_global_df.columns    = diffuse_irradiance_from_aerosol_scattering_column_index
    # Organize Diffuse Irradiation from Aerosol Scattering into Data Frame
    diffuse_irradiation_from_aerosol_scattering_global_df           = diffuse_irradiation_from_aerosol_scattering_df.copy()
    diffuse_irradiation_from_aerosol_scattering_global_df.columns   = diffuse_irradiation_from_aerosol_scattering_column_index

    # Organize Diffuse Irradiance from Mutiple Reflection into Data Frame
    diffuse_irradiance_from_multiple_reflection_global_df           = diffuse_irradiance_from_mutiple_reflection_df.copy()
    diffuse_irradiance_from_multiple_reflection_global_df.columns   = diffuse_irradiance_from_multiple_reflection_column_index
    # Organize Diffuse Irradiation form Mutiple Reflection into Data Frame
    diffuse_irradiation_from_multiple_reflection_global_df          = diffuse_irradiation_from_mutiple_reflection_df.copy()
    diffuse_irradiation_from_multiple_reflection_global_df.columns  = diffuse_irradiation_from_multiple_reflection_column_index

    # Combine All Transmittance Coefficient Data Frames into Global 
    global_solar_irradiance_df = pd.concat([total_solar_irradiance_global_df, separator_df, direct_normal_irradiance_global_df, separator_df, diffuse_irradiance_global_df, separator_df, diffuse_irradiance_from_rayleigh_atmosphere_global_df, separator_df, diffuse_irradiance_from_aerosol_scattering_global_df, separator_df, diffuse_irradiance_from_multiple_reflection_global_df], axis=1)
    #print(f'\nGlobal Solar Irradiance Data Frame:\n{global_solar_irradiance_df}')
    global_solar_irradiation_df = pd.concat([total_solar_irradiation_global_df, separator_df, direct_normal_irradiation_global_df, separator_df, diffuse_irradiation_global_df, separator_df, diffuse_irradiation_from_rayleigh_atmosphere_global_df, separator_df, diffuse_irradiation_from_aerosol_scattering_global_df, separator_df, diffuse_irradiation_from_multiple_reflection_global_df], axis=1)
    #print(f'\nGlobal Solar Irradiation Data Frame:\n{global_solar_irradiation_df}')

    new_global_solar_irradiance_df = pd.concat([new_building_fields_tables_df, date_field_df, global_solar_irradiance_df], axis=1)
    #print('new_global_solar_irradiance_df:\n', new_global_solar_irradiance_df)
    new_global_solar_irradiation_df = pd.concat([new_building_fields_tables_df, date_field_df, global_solar_irradiation_df], axis=1)
    #print('new_global_solar_irradiation_df:\n', new_global_solar_irradiation_df)

    
    # Creating CSV File Name
    solar_irradiance_csvfile_local_name = f'Solar_Irradiance_uid_{uid}'
    solar_irradiation_csvfile_local_name = f'Solar_Irradiation_uid_{uid}'
    
    # Creating CSV File to Store Solar Irradiance Data
    solar_irradiance_writer, global_solar_irradiance_csvfile_name = create_csvfile(global_solar_irradiance_csvfile_location, solar_irradiance_csvfile_local_name)
    solar_irradiaction_writer, global_solar_irradiation_csvfile_name = create_csvfile(global_solar_irradiation_csvfile_location, solar_irradiation_csvfile_local_name)
    
    new_global_solar_irradiance_df.to_csv(global_solar_irradiance_csvfile_name, index=False)
    new_global_solar_irradiation_df.to_csv(global_solar_irradiation_csvfile_name, index=False)
    
    end_time_record    = time.time()
    total_time  = end_time_record - start_time_record
    print("\n***** DONE PROCESSING SOLAR IRRADIANCE & IRRADIATION FUNCTION *****")
    print(f"Total execution time: {total_time:.4f} seconds")
    return new_global_solar_irradiance_df, new_global_solar_irradiation_df

# Direct Normal Solar Irradiance on a Horizontal Surface Calculation Function (rate of energy per unit of time)
def direct_normal_irradiance_calculation_function(rooftype, rooftop_azimuth_angle_df, rooftop_slope_angle_df, declination_angle_df, eccentricity_correction_factor_df, latitude_df, solar_hour_angle_df, cloud_transmittance_coeff_df, absorption_transmittance_coeff_df, rayleigh_transmittance_coeff_df, scattering_by_aerosol_transmittance_coeff_df):
    # Solar Constant (Isc = 1.3667 kilo Watts per square meter)
    solar_constant = 1.3667 #kilo watts

    rooftop_azimuth_angle_checker = rooftop_azimuth_angle_df.loc[0,0]

    if rooftype == "Flat":
        flat_rooftop_zenith_angle_df = zenith_angle_on_horizontal_plane_function(declination_angle_df, latitude_df, solar_hour_angle_df)
        direct_normal_irradiance_on_any_surface = (solar_constant)*(eccentricity_correction_factor_df)*(cloud_transmittance_coeff_df)*(absorption_transmittance_coeff_df)*(rayleigh_transmittance_coeff_df)*(scattering_by_aerosol_transmittance_coeff_df)*(np.cos(Deg2Rad(flat_rooftop_zenith_angle_df)))
        direct_normal_irradiance_on_any_surface = positive_interval_feasible_answer_function(direct_normal_irradiance_on_any_surface)
    elif rooftype == "Complex":
        complex_rooftop_zenith_angle = zenith_angle_on_horizontal_plane_function(declination_angle_df, latitude_df, solar_hour_angle_df)
        direct_normal_irradiance_on_any_surface = (solar_constant)*(eccentricity_correction_factor_df)*(cloud_transmittance_coeff_df)*(absorption_transmittance_coeff_df)*(rayleigh_transmittance_coeff_df)*(scattering_by_aerosol_transmittance_coeff_df)*(np.cos(Deg2Rad(complex_rooftop_zenith_angle)))
        direct_normal_irradiance_on_any_surface = positive_interval_feasible_answer_function(direct_normal_irradiance_on_any_surface)
    elif rooftype == "Gable":
        if rooftop_azimuth_angle_checker == 0:
            gable_side1_zenith_angle = zenith_angle_on_inclined_plane_facing_south_direction_function(declination_angle_df, latitude_df, solar_hour_angle_df, rooftop_slope_angle_df)
            gable_side1_direct_normal_irradiance_on_inclined_surface = (solar_constant)*(eccentricity_correction_factor_df)*(cloud_transmittance_coeff_df)*(absorption_transmittance_coeff_df)*(rayleigh_transmittance_coeff_df)*(scattering_by_aerosol_transmittance_coeff_df)*(np.cos(Deg2Rad(gable_side1_zenith_angle)))
            gable_side1_direct_normal_irradiance_on_inclined_surface = positive_interval_feasible_answer_function(gable_side1_direct_normal_irradiance_on_inclined_surface)
            gable_side2_rooftop_azimuth_angle = 180
            gable_side2_zenith_angle = zenith_angle_on_inclined_plane_facing_any_direction_function(declination_angle_df, latitude_df, solar_hour_angle_df, rooftop_slope_angle_df, gable_side2_rooftop_azimuth_angle)
            gable_side2_direct_normal_irradiance_on_inclined_surface = (solar_constant)*(eccentricity_correction_factor_df)*(cloud_transmittance_coeff_df)*(absorption_transmittance_coeff_df)*(rayleigh_transmittance_coeff_df)*(scattering_by_aerosol_transmittance_coeff_df)*(np.cos(Deg2Rad(gable_side2_zenith_angle)))
            gable_side2_direct_normal_irradiance_on_inclined_surface = positive_interval_feasible_answer_function(gable_side2_direct_normal_irradiance_on_inclined_surface)
        else:
            gable_side1_azimuth_angle = rooftop_azimuth_angle_df
            gable_side1_zenith_angle = zenith_angle_on_inclined_plane_facing_any_direction_function(declination_angle_df, latitude_df, solar_hour_angle_df, rooftop_slope_angle_df, gable_side1_azimuth_angle)
            gable_side1_direct_normal_irradiance_on_inclined_surface = (solar_constant)*(eccentricity_correction_factor_df)*(cloud_transmittance_coeff_df)*(absorption_transmittance_coeff_df)*(rayleigh_transmittance_coeff_df)*(scattering_by_aerosol_transmittance_coeff_df)*(np.cos(Deg2Rad(gable_side1_zenith_angle)))
            gable_side1_direct_normal_irradiance_on_inclined_surface = positive_interval_feasible_answer_function(gable_side1_direct_normal_irradiance_on_inclined_surface)
            if 180 >= rooftop_azimuth_angle_checker > 0 :
                gable_side2_rooftop_azimuth_angle = rooftop_azimuth_angle_df - 180
            elif 0 > rooftop_azimuth_angle_checker >= -180:
                gable_side2_rooftop_azimuth_angle = rooftop_azimuth_angle_df + 180
            gable_side2_zenith_angle = zenith_angle_on_inclined_plane_facing_any_direction_function(declination_angle_df, latitude_df, solar_hour_angle_df, rooftop_slope_angle_df, gable_side2_rooftop_azimuth_angle)
            gable_side2_direct_normal_irradiance_on_inclined_surface = (solar_constant)*(eccentricity_correction_factor_df)*(cloud_transmittance_coeff_df)*(absorption_transmittance_coeff_df)*(rayleigh_transmittance_coeff_df)*(scattering_by_aerosol_transmittance_coeff_df)*(np.cos(Deg2Rad(gable_side2_zenith_angle)))
            gable_side2_direct_normal_irradiance_on_inclined_surface = positive_interval_feasible_answer_function(gable_side2_direct_normal_irradiance_on_inclined_surface)
        direct_normal_irradiance_on_any_surface = pd.DataFrame(np.where(gable_side1_direct_normal_irradiance_on_inclined_surface>=gable_side2_direct_normal_irradiance_on_inclined_surface, gable_side1_direct_normal_irradiance_on_inclined_surface, gable_side2_direct_normal_irradiance_on_inclined_surface))
    elif rooftype == "Hip":
        if rooftop_azimuth_angle_checker == 0:
            hip_side1_zenith_angle = zenith_angle_on_inclined_plane_facing_south_direction_function(declination_angle_df, latitude_df, solar_hour_angle_df, rooftop_slope_angle_df)
            hip_side1_direct_normal_irradiance_on_inclined_surface = (solar_constant)*(eccentricity_correction_factor_df)*(cloud_transmittance_coeff_df)*(absorption_transmittance_coeff_df)*(rayleigh_transmittance_coeff_df)*(scattering_by_aerosol_transmittance_coeff_df)*(np.cos(Deg2Rad(hip_side1_zenith_angle)))
            hip_side1_direct_normal_irradiance_on_inclined_surface = positive_interval_feasible_answer_function(hip_side1_direct_normal_irradiance_on_inclined_surface)
            hip_side2_rooftop_azimuth_angle = 180
            hip_side2_zenith_angle = zenith_angle_on_inclined_plane_facing_any_direction_function(declination_angle_df, latitude_df, solar_hour_angle_df, rooftop_slope_angle_df, hip_side2_rooftop_azimuth_angle)
            hip_side2_direct_normal_irradiance_on_inclined_surface = (solar_constant)*(eccentricity_correction_factor_df)*(cloud_transmittance_coeff_df)*(absorption_transmittance_coeff_df)*(rayleigh_transmittance_coeff_df)*(scattering_by_aerosol_transmittance_coeff_df)*(np.cos(Deg2Rad(hip_side2_zenith_angle)))
            hip_side2_direct_normal_irradiance_on_inclined_surface = positive_interval_feasible_answer_function(hip_side2_direct_normal_irradiance_on_inclined_surface)
            hip_side3_rooftop_azimuth_angle = 90
            hip_side3_zenith_angle = zenith_angle_on_inclined_plane_facing_any_direction_function(declination_angle_df, latitude_df, solar_hour_angle_df, rooftop_slope_angle_df, hip_side3_rooftop_azimuth_angle)
            hip_side3_direct_normal_irradiance_on_inclined_surface = (solar_constant)*(eccentricity_correction_factor_df)*(cloud_transmittance_coeff_df)*(absorption_transmittance_coeff_df)*(rayleigh_transmittance_coeff_df)*(scattering_by_aerosol_transmittance_coeff_df)*(np.cos(Deg2Rad(hip_side3_zenith_angle)))
            hip_side3_direct_normal_irradiance_on_inclined_surface = positive_interval_feasible_answer_function(hip_side3_direct_normal_irradiance_on_inclined_surface)
            hip_side4_rooftop_azimuth_angle = -90
            hip_side4_zenith_angle = zenith_angle_on_inclined_plane_facing_any_direction_function(declination_angle_df, latitude_df, solar_hour_angle_df, rooftop_slope_angle_df, hip_side4_rooftop_azimuth_angle)
            hip_side4_direct_normal_irradiance_on_inclined_surface = (solar_constant)*(eccentricity_correction_factor_df)*(cloud_transmittance_coeff_df)*(absorption_transmittance_coeff_df)*(rayleigh_transmittance_coeff_df)*(scattering_by_aerosol_transmittance_coeff_df)*(np.cos(Deg2Rad(hip_side4_zenith_angle)))
            hip_side4_direct_normal_irradiance_on_inclined_surface = positive_interval_feasible_answer_function(hip_side4_direct_normal_irradiance_on_inclined_surface)
        else:
            hip_side1_rooftop_azimuth_angle = rooftop_azimuth_angle_df
            hip_side1_zenith_angle = zenith_angle_on_inclined_plane_facing_any_direction_function(declination_angle_df, latitude_df, solar_hour_angle_df, rooftop_slope_angle_df, hip_side1_rooftop_azimuth_angle)
            hip_side1_direct_normal_irradiance_on_inclined_surface = (solar_constant)*(eccentricity_correction_factor_df)*(cloud_transmittance_coeff_df)*(absorption_transmittance_coeff_df)*(rayleigh_transmittance_coeff_df)*(scattering_by_aerosol_transmittance_coeff_df)*(np.cos(Deg2Rad(hip_side1_zenith_angle)))
            hip_side1_direct_normal_irradiance_on_inclined_surface = positive_interval_feasible_answer_function(hip_side1_direct_normal_irradiance_on_inclined_surface)
            if 180 >= rooftop_azimuth_angle_checker > 0 :
                hip_side2_rooftop_azimuth_angle = hip_side1_rooftop_azimuth_angle - 180
            elif 0 > rooftop_azimuth_angle_checker >= -180:
                hip_side2_rooftop_azimuth_angle = hip_side1_rooftop_azimuth_angle + 180
            hip_side2_zenith_angle = zenith_angle_on_inclined_plane_facing_any_direction_function(declination_angle_df, latitude_df, solar_hour_angle_df, rooftop_slope_angle_df, hip_side2_rooftop_azimuth_angle)
            hip_side2_direct_normal_irradiance_on_inclined_surface = (solar_constant)*(eccentricity_correction_factor_df)*(cloud_transmittance_coeff_df)*(absorption_transmittance_coeff_df)*(rayleigh_transmittance_coeff_df)*(scattering_by_aerosol_transmittance_coeff_df)*(np.cos(Deg2Rad(hip_side2_zenith_angle)))
            hip_side2_direct_normal_irradiance_on_inclined_surface = positive_interval_feasible_answer_function(hip_side2_direct_normal_irradiance_on_inclined_surface)
            if 180 >= rooftop_azimuth_angle_checker > 90:
                hip_side3_rooftop_azimuth_angle = hip_side1_rooftop_azimuth_angle -270
            elif 90 >= rooftop_azimuth_angle_checker >= -180:
                hip_side3_rooftop_azimuth_angle = hip_side1_rooftop_azimuth_angle + 90
            hip_side3_zenith_angle = zenith_angle_on_inclined_plane_facing_any_direction_function(declination_angle_df, latitude_df, solar_hour_angle_df, rooftop_slope_angle_df, hip_side3_rooftop_azimuth_angle)
            hip_side3_direct_normal_irradiance_on_inclined_surface = (solar_constant)*(eccentricity_correction_factor_df)*(cloud_transmittance_coeff_df)*(absorption_transmittance_coeff_df)*(rayleigh_transmittance_coeff_df)*(scattering_by_aerosol_transmittance_coeff_df)*(np.cos(Deg2Rad(hip_side3_zenith_angle)))
            hip_side3_direct_normal_irradiance_on_inclined_surface = positive_interval_feasible_answer_function(hip_side3_direct_normal_irradiance_on_inclined_surface)
            if -90 > rooftop_azimuth_angle_checker >= -180:
                hip_side4_rooftop_azimuth_angle = hip_side1_rooftop_azimuth_angle + 270
            elif 180 >= rooftop_azimuth_angle_checker >= -90:
                hip_side4_rooftop_azimuth_angle = hip_side1_rooftop_azimuth_angle - 90
            hip_side4_zenith_angle = zenith_angle_on_inclined_plane_facing_any_direction_function(declination_angle_df, latitude_df, solar_hour_angle_df, rooftop_slope_angle_df, hip_side4_rooftop_azimuth_angle)
            hip_side4_direct_normal_irradiance_on_inclined_surface = (solar_constant)*(eccentricity_correction_factor_df)*(cloud_transmittance_coeff_df)*(absorption_transmittance_coeff_df)*(rayleigh_transmittance_coeff_df)*(scattering_by_aerosol_transmittance_coeff_df)*(np.cos(Deg2Rad(hip_side4_zenith_angle)))
            hip_side4_direct_normal_irradiance_on_inclined_surface = positive_interval_feasible_answer_function(hip_side4_direct_normal_irradiance_on_inclined_surface)
        
        hip_rooftop_normal_irradiance_condition1 = (hip_side1_direct_normal_irradiance_on_inclined_surface>=hip_side2_direct_normal_irradiance_on_inclined_surface)&(hip_side1_direct_normal_irradiance_on_inclined_surface>=hip_side3_direct_normal_irradiance_on_inclined_surface)&(hip_side1_direct_normal_irradiance_on_inclined_surface>=hip_side4_direct_normal_irradiance_on_inclined_surface)
        hip_rooftop_normal_irradiance_condition2 = (hip_side2_direct_normal_irradiance_on_inclined_surface>=hip_side1_direct_normal_irradiance_on_inclined_surface)&(hip_side2_direct_normal_irradiance_on_inclined_surface>=hip_side3_direct_normal_irradiance_on_inclined_surface)&(hip_side2_direct_normal_irradiance_on_inclined_surface>=hip_side4_direct_normal_irradiance_on_inclined_surface)
        hip_rooftop_normal_irradiance_condition3 = (hip_side3_direct_normal_irradiance_on_inclined_surface>=hip_side1_direct_normal_irradiance_on_inclined_surface)&(hip_side3_direct_normal_irradiance_on_inclined_surface>=hip_side2_direct_normal_irradiance_on_inclined_surface)&(hip_side3_direct_normal_irradiance_on_inclined_surface>=hip_side4_direct_normal_irradiance_on_inclined_surface)
        hip_rooftop_normal_irradiance_condition4 = (hip_side4_direct_normal_irradiance_on_inclined_surface>=hip_side1_direct_normal_irradiance_on_inclined_surface)&(hip_side4_direct_normal_irradiance_on_inclined_surface>=hip_side2_direct_normal_irradiance_on_inclined_surface)&(hip_side4_direct_normal_irradiance_on_inclined_surface>=hip_side3_direct_normal_irradiance_on_inclined_surface)
        hip_rooftop_normal_irradiance_condition_list = [hip_rooftop_normal_irradiance_condition1,
                                                        hip_rooftop_normal_irradiance_condition2,
                                                        hip_rooftop_normal_irradiance_condition3,
                                                        hip_rooftop_normal_irradiance_condition4
                                                        ]
        hip_rooftop_normal_irradiance_condition_choice_list = [hip_side1_direct_normal_irradiance_on_inclined_surface, hip_side2_direct_normal_irradiance_on_inclined_surface, hip_side3_direct_normal_irradiance_on_inclined_surface, hip_side4_direct_normal_irradiance_on_inclined_surface]
        direct_normal_irradiance_on_any_surface = pd.DataFrame((np.select(hip_rooftop_normal_irradiance_condition_list,hip_rooftop_normal_irradiance_condition_choice_list, 0)))
    direct_normal_irradiance_on_any_surface = positive_interval_feasible_answer_function(direct_normal_irradiance_on_any_surface)
    return direct_normal_irradiance_on_any_surface.round(6)

def direct_normal_irradiation_calculation_function(end_julian_date, rooftype, rooftop_width, rooftop_length, flat_rooftop_area, rooftop_azimuth_angle_df, rooftop_slope_angle, declination_angle_df, latitude, sun_azimuth_angle_df, sun_altitude_angle_df, solar_hour_angle_df, eccentricity_correction_factor_df, cloud_transmittance_coeff_df, absorption_transmittance_coeff_df, rayleigh_transmittance_coeff_df, scattering_by_aerosol_transmittance_coeff_df):
    rooftop_azimuth_angle_checker = rooftop_azimuth_angle_df.loc[0,0]

    # Direct Normal Solar Irradiation on a Horzontal Surface Calculation Function (amount of energy per unit of time)
    def direct_normal_irradiation_on_horizontal_surface_function(eccentricity_correction_factor, cloud_transmittance_coeff, absorption_transmittance_coeff, rayleigh_transmittance_coeff, scattering_by_aerosol_transmittance_coeff, declination_angle, latitude, solar_hour_angle1, solar_hour_angle2):
        direct_normal_irradiation_on_horizontal_surface = (1)*(12/np.pi)*(solar_constant)*(eccentricity_correction_factor)*(cloud_transmittance_coeff)*(absorption_transmittance_coeff)*(rayleigh_transmittance_coeff)*(scattering_by_aerosol_transmittance_coeff)*(  ( (np.sin(Deg2Rad(declination_angle)))*(np.sin(Deg2Rad(latitude)))*((Deg2Rad(solar_hour_angle1))-(Deg2Rad(solar_hour_angle2)))) + ( (np.cos(Deg2Rad(declination_angle)))*(np.cos(Deg2Rad(latitude)))*( (np.sin(Deg2Rad(-solar_hour_angle2)))-(np.sin(Deg2Rad(-solar_hour_angle1))) ) )  )
        direct_normal_irradiation_on_horizontal_surface = positive_interval_feasible_answer_function(direct_normal_irradiation_on_horizontal_surface)
        return direct_normal_irradiation_on_horizontal_surface

    # Direct Normal Solar Irradiation on a Inclined Surface Facing South Calculation Function (amount of energy per unit of time)
    def direct_normal_irradiation_on_inclined_surface_facing_south_function(eccentricity_correction_factor, cloud_transmittance_coeff, absorption_transmittance_coeff, rayleigh_transmittance_coeff, scattering_by_aerosol_transmittance_coeff, declination_angle, latitude, rooftop_slope_angle, solar_hour_angle1, solar_hour_angle2):
        direct_normal_irradiation_on_inclined_surface_facing_south = (1)*(12/np.pi)*(solar_constant)*(eccentricity_correction_factor)*(cloud_transmittance_coeff)*(absorption_transmittance_coeff)*(rayleigh_transmittance_coeff)*(scattering_by_aerosol_transmittance_coeff)*( ((np.sin(Deg2Rad(declination_angle)))*(np.sin((Deg2Rad(latitude))-(Deg2Rad(rooftop_slope_angle))))*((Deg2Rad(solar_hour_angle1))-(Deg2Rad(solar_hour_angle2)))) + ((np.cos(Deg2Rad(declination_angle)))*(np.cos((Deg2Rad(latitude))-(Deg2Rad(rooftop_slope_angle))))*((np.sin(Deg2Rad(-solar_hour_angle2)))-(np.sin(Deg2Rad(-solar_hour_angle1))))) )
        direct_normal_irradiation_on_inclined_surface_facing_south = positive_interval_feasible_answer_function(direct_normal_irradiation_on_inclined_surface_facing_south)
        return direct_normal_irradiation_on_inclined_surface_facing_south

    # Direct Normal Solar Irradiation in a Inclined Surface Facing Any Dirextion Calculation Function (amount of energy per unity of time)
    def direct_normal_irradiation_on_inclined_surface_facing_any_direction_function(eccentricity_correction_factor, cloud_transmittance_coeff, absorption_transmittance_coeff, rayleigh_transmittance_coeff, scattering_by_aerosol_transmittance_coeff, declination_angle, latitude, sun_azimuth_angle, sun_altitude_angle, rooftop_slope_angle, rooftop_azimuth_angle, solar_hour_angle1, solar_hour_angle2):
        direct_normal_irradiation_on_inclined_surface_facing_any_direction = (1)*(12/np.pi)*(solar_constant)*(eccentricity_correction_factor)*(cloud_transmittance_coeff)*(absorption_transmittance_coeff)*(rayleigh_transmittance_coeff)*(scattering_by_aerosol_transmittance_coeff)*( ((np.sin(Deg2Rad(rooftop_slope_angle)))*(np.cos(Deg2Rad(rooftop_azimuth_angle)))*(np.cos(Deg2Rad(sun_azimuth_angle)))*(np.cos(Deg2Rad(sun_altitude_angle)))*((np.sin(Deg2Rad(-solar_hour_angle2)))-(np.sin(Deg2Rad(-solar_hour_angle1))))) + ((np.sin(Deg2Rad(rooftop_slope_angle)))*(np.sin(Deg2Rad(rooftop_azimuth_angle)))*(np.sin(Deg2Rad(sun_azimuth_angle)))*(np.cos(Deg2Rad(sun_altitude_angle)))*((np.sin(Deg2Rad(-solar_hour_angle2)))-(np.sin(Deg2Rad(-solar_hour_angle1))))) + ((np.cos(Deg2Rad(rooftop_slope_angle)))*(( (np.sin(Deg2Rad(declination_angle)))*(np.sin(Deg2Rad(latitude)))*((Deg2Rad(solar_hour_angle1))-(Deg2Rad(solar_hour_angle2)))) + ((np.cos(Deg2Rad(declination_angle)))*(np.cos(Deg2Rad(latitude)))*((np.sin(Deg2Rad(-solar_hour_angle2)))-(np.sin(Deg2Rad(-solar_hour_angle1))))))) )
        direct_normal_irradiation_on_inclined_surface_facing_any_direction = positive_interval_feasible_answer_function(direct_normal_irradiation_on_inclined_surface_facing_any_direction)
        return direct_normal_irradiation_on_inclined_surface_facing_any_direction
    
    # Calculate Rooftop Height from Rooftop Slope Angle and rooftop Width
    rooftop_height = (rooftop_width/2) * (np.tan(Deg2Rad(rooftop_slope_angle)))
    if rooftype == "Flat" or rooftype == "Complex":
        rooftop_area_df = flat_rooftop_area
    elif rooftype == "Gable":
        rooftop_truss_length = (rooftop_width/2) / (np.cos(Deg2Rad(rooftop_slope_angle)))
        gable_rooftop_area =  rooftop_truss_length * rooftop_length
    elif rooftype == "Hip":
        rooftop_width_truss_length = (rooftop_height) / (np.sin(Deg2Rad(rooftop_slope_angle)))
        hip_width_rooftop_area = (0.5)*(rooftop_width)*rooftop_width_truss_length
        hip_top_rooftop_length = rooftop_length - rooftop_width
        hip_length_rooftop_area =  (0.5)*(rooftop_length + hip_top_rooftop_length)*(rooftop_width_truss_length)

    # Acquire Solar Hour Angle from Global Solar Irradiance Geometry csvfile
    solar_hour_angle1_df = solar_hour_angle_df
    solar_hour_angle2_df = pd.concat([solar_hour_angle_df.loc[:,1:],solar_hour_angle_df[solar_hour_angle_df.shape[1]-1]],axis=1)
    solar_hour_angle2_df.columns = list(range(0,solar_hour_angle2_df.shape[1]))

    if rooftype == "Flat":
        # Direct Normal Irradiation on Horizontal Surface Calculation
        direct_normal_irradiation = direct_normal_irradiation_on_horizontal_surface_function(eccentricity_correction_factor_df, cloud_transmittance_coeff_df, absorption_transmittance_coeff_df, rayleigh_transmittance_coeff_df, scattering_by_aerosol_transmittance_coeff_df, declination_angle_df, latitude, solar_hour_angle1_df, solar_hour_angle2_df)
        direct_normal_irradiation = positive_interval_feasible_answer_function(direct_normal_irradiation)
        direct_normal_irradiation = direct_normal_irradiation
    elif rooftype == "Complex":
        direct_normal_irradiation = direct_normal_irradiation_on_horizontal_surface_function(eccentricity_correction_factor_df, cloud_transmittance_coeff_df, absorption_transmittance_coeff_df, rayleigh_transmittance_coeff_df, scattering_by_aerosol_transmittance_coeff_df, declination_angle_df, latitude, solar_hour_angle1_df, solar_hour_angle2_df)
        direct_normal_irradiation = positive_interval_feasible_answer_function(direct_normal_irradiation)
        direct_normal_irradiation = direct_normal_irradiation
    elif rooftype == "Gable":
        if rooftop_azimuth_angle_checker == 0:
            gable_side1_direct_normal_irradiation = direct_normal_irradiation_on_inclined_surface_facing_south_function(eccentricity_correction_factor_df, cloud_transmittance_coeff_df, absorption_transmittance_coeff_df, rayleigh_transmittance_coeff_df, scattering_by_aerosol_transmittance_coeff_df, declination_angle_df, latitude, rooftop_slope_angle, solar_hour_angle1_df, solar_hour_angle2_df)
            gable_side1_direct_normal_irradiation = positive_interval_feasible_answer_function(gable_side1_direct_normal_irradiation)
            gable_side1_direct_normal_irradiation = gable_side1_direct_normal_irradiation
            gable_side2_rooftop_azimuth_angle     = 180
            gable_side2_direct_normal_irradiation = direct_normal_irradiation_on_inclined_surface_facing_any_direction_function(eccentricity_correction_factor_df, cloud_transmittance_coeff_df, absorption_transmittance_coeff_df, rayleigh_transmittance_coeff_df, scattering_by_aerosol_transmittance_coeff_df, declination_angle_df, latitude, sun_azimuth_angle_df, sun_altitude_angle_df, rooftop_slope_angle, gable_side2_rooftop_azimuth_angle, solar_hour_angle1_df, solar_hour_angle2_df)
            gable_side2_direct_normal_irradiation = positive_interval_feasible_answer_function(gable_side2_direct_normal_irradiation)
            gable_side2_direct_normal_irradiation = gable_side2_direct_normal_irradiation
        else:
            gable_side1_direct_normal_irradiation = direct_normal_irradiation_on_inclined_surface_facing_any_direction_function(eccentricity_correction_factor_df, cloud_transmittance_coeff_df, absorption_transmittance_coeff_df, rayleigh_transmittance_coeff_df, scattering_by_aerosol_transmittance_coeff_df, declination_angle_df, latitude, sun_azimuth_angle_df, sun_altitude_angle_df, rooftop_slope_angle, rooftop_azimuth_angle_df, solar_hour_angle1_df, solar_hour_angle2_df)
            gable_side1_direct_normal_irradiation = positive_interval_feasible_answer_function(gable_side1_direct_normal_irradiation)
            gable_side1_direct_normal_irradiation = gable_side1_direct_normal_irradiation
            if 180 >= rooftop_azimuth_angle_checker > 0:
                gable_side2_rooftop_azimuth_angle = rooftop_azimuth_angle_df - 180
            elif 0 > rooftop_azimuth_angle_checker >= -180:
                gable_side2_rooftop_azimuth_angle = rooftop_azimuth_angle_df + 180
            gable_side2_direct_normal_irradiation = direct_normal_irradiation_on_inclined_surface_facing_any_direction_function(eccentricity_correction_factor_df, cloud_transmittance_coeff_df, absorption_transmittance_coeff_df, rayleigh_transmittance_coeff_df, scattering_by_aerosol_transmittance_coeff_df, declination_angle_df, latitude, sun_azimuth_angle_df, sun_altitude_angle_df, rooftop_slope_angle, gable_side2_rooftop_azimuth_angle, solar_hour_angle1_df, solar_hour_angle2_df)
            gable_side2_direct_normal_irradiation = positive_interval_feasible_answer_function(gable_side2_direct_normal_irradiation)
            gable_side2_direct_normal_irradiation = gable_side2_direct_normal_irradiation
        direct_normal_irradiation = (gable_side1_direct_normal_irradiation + gable_side2_direct_normal_irradiation)/2
    elif rooftype == "Hip":
        if rooftop_azimuth_angle_checker == 0:
            hip_side1_direct_normal_irradiation = direct_normal_irradiation_on_inclined_surface_facing_south_function(eccentricity_correction_factor_df, cloud_transmittance_coeff_df, absorption_transmittance_coeff_df, rayleigh_transmittance_coeff_df, scattering_by_aerosol_transmittance_coeff_df, declination_angle_df, latitude, rooftop_slope_angle, solar_hour_angle1_df, solar_hour_angle2_df)
            hip_side1_direct_normal_irradiation = positive_interval_feasible_answer_function(hip_side1_direct_normal_irradiation)
            hip_side1_direct_normal_irradiation = hip_side1_direct_normal_irradiation
            hip_side2_rooftop_azimuth_angle = 180
            hip_side2_direct_normal_irradiation = direct_normal_irradiation_on_inclined_surface_facing_any_direction_function(eccentricity_correction_factor_df, cloud_transmittance_coeff_df, absorption_transmittance_coeff_df, rayleigh_transmittance_coeff_df, scattering_by_aerosol_transmittance_coeff_df, declination_angle_df, latitude, sun_azimuth_angle_df, sun_altitude_angle_df, rooftop_slope_angle, hip_side2_rooftop_azimuth_angle, solar_hour_angle1_df, solar_hour_angle2_df)
            hip_side2_direct_normal_irradiation = positive_interval_feasible_answer_function(hip_side2_direct_normal_irradiation)
            hip_side2_direct_normal_irradiation = hip_side2_direct_normal_irradiation
            hip_side3_rooftop_azimuth_angle = 90
            hip_side3_direct_normal_irradiation = direct_normal_irradiation_on_inclined_surface_facing_any_direction_function(eccentricity_correction_factor_df, cloud_transmittance_coeff_df, absorption_transmittance_coeff_df, rayleigh_transmittance_coeff_df, scattering_by_aerosol_transmittance_coeff_df, declination_angle_df, latitude, sun_azimuth_angle_df, sun_altitude_angle_df, rooftop_slope_angle, hip_side3_rooftop_azimuth_angle, solar_hour_angle1_df, solar_hour_angle2_df)
            hip_side3_direct_normal_irradiation = positive_interval_feasible_answer_function(hip_side3_direct_normal_irradiation)
            hip_side3_direct_normal_irradiation = hip_side3_direct_normal_irradiation
            hip_side4_rooftop_azimuth_angle = (-90)
            hip_side4_direct_normal_irradiation = direct_normal_irradiation_on_inclined_surface_facing_any_direction_function(eccentricity_correction_factor_df, cloud_transmittance_coeff_df, absorption_transmittance_coeff_df, rayleigh_transmittance_coeff_df, scattering_by_aerosol_transmittance_coeff_df, declination_angle_df, latitude, sun_azimuth_angle_df, sun_altitude_angle_df, rooftop_slope_angle, hip_side4_rooftop_azimuth_angle, solar_hour_angle1_df, solar_hour_angle2_df)
            hip_side4_direct_normal_irradiation = positive_interval_feasible_answer_function(hip_side4_direct_normal_irradiation)
            hip_side4_direct_normal_irradiation = hip_side4_direct_normal_irradiation
        else:
            hip_side1_direct_normal_irradiation = direct_normal_irradiation_on_inclined_surface_facing_any_direction_function(eccentricity_correction_factor_df, cloud_transmittance_coeff_df, absorption_transmittance_coeff_df, rayleigh_transmittance_coeff_df, scattering_by_aerosol_transmittance_coeff_df, declination_angle_df, latitude, sun_azimuth_angle_df, sun_altitude_angle_df, rooftop_slope_angle, rooftop_azimuth_angle_df, solar_hour_angle1_df, solar_hour_angle2_df)
            hip_side1_direct_normal_irradiation = positive_interval_feasible_answer_function(hip_side1_direct_normal_irradiation)
            hip_side1_direct_normal_irradiation = hip_side1_direct_normal_irradiation
            if 180 >= rooftop_azimuth_angle_checker > 0:
                hip_side2_rooftop_azimuth_angle = rooftop_azimuth_angle_df - 180
            elif 0 > rooftop_azimuth_angle_checker >= -180:
                hip_side2_rooftop_azimuth_angle = rooftop_azimuth_angle_df + 180
            hip_side2_direct_normal_irradiation = direct_normal_irradiation_on_inclined_surface_facing_any_direction_function(eccentricity_correction_factor_df, cloud_transmittance_coeff_df, absorption_transmittance_coeff_df, rayleigh_transmittance_coeff_df, scattering_by_aerosol_transmittance_coeff_df, declination_angle_df, latitude, sun_azimuth_angle_df, sun_altitude_angle_df, rooftop_slope_angle, hip_side2_rooftop_azimuth_angle, solar_hour_angle1_df, solar_hour_angle2_df)
            hip_side2_direct_normal_irradiation = positive_interval_feasible_answer_function(hip_side2_direct_normal_irradiation)
            hip_side2_direct_normal_irradiation = hip_side2_direct_normal_irradiation
            if 180 >= rooftop_azimuth_angle_checker > 90:
                hip_side3_rooftop_azimuth_angle = rooftop_azimuth_angle_df - 270
            elif 90 >= rooftop_azimuth_angle_checker >= -180:
                hip_side3_rooftop_azimuth_angle = rooftop_azimuth_angle_df + 90
            hip_side3_direct_normal_irradiation = direct_normal_irradiation_on_inclined_surface_facing_any_direction_function(eccentricity_correction_factor_df, cloud_transmittance_coeff_df, absorption_transmittance_coeff_df, rayleigh_transmittance_coeff_df, scattering_by_aerosol_transmittance_coeff_df, declination_angle_df, latitude, sun_azimuth_angle_df, sun_altitude_angle_df, rooftop_slope_angle, hip_side3_rooftop_azimuth_angle, solar_hour_angle1_df, solar_hour_angle2_df)
            hip_side3_direct_normal_irradiation = positive_interval_feasible_answer_function(hip_side3_direct_normal_irradiation)
            hip_side3_direct_normal_irradiation = hip_side3_direct_normal_irradiation
            if -90 > rooftop_azimuth_angle_checker >= -180:
                hip_side4_rooftop_azimuth_angle = rooftop_azimuth_angle_df + 270
            elif 180 >= rooftop_azimuth_angle_checker >= -90:
                hip_side4_rooftop_azimuth_angle = rooftop_azimuth_angle_df - 90
            hip_side4_direct_normal_irradiation = direct_normal_irradiation_on_inclined_surface_facing_any_direction_function(eccentricity_correction_factor_df, cloud_transmittance_coeff_df, absorption_transmittance_coeff_df, rayleigh_transmittance_coeff_df, scattering_by_aerosol_transmittance_coeff_df, declination_angle_df, latitude, sun_azimuth_angle_df, sun_altitude_angle_df, rooftop_slope_angle, hip_side4_rooftop_azimuth_angle, solar_hour_angle1_df, solar_hour_angle2_df)
            hip_side4_direct_normal_irradiation = positive_interval_feasible_answer_function(hip_side4_direct_normal_irradiation)
            hip_side4_direct_normal_irradiation = hip_side4_direct_normal_irradiation
        direct_normal_irradiation = (hip_side1_direct_normal_irradiation + hip_side2_direct_normal_irradiation + hip_side3_direct_normal_irradiation + hip_side4_direct_normal_irradiation)/4
   
    return direct_normal_irradiation.round(6)

# Diffuse Irradiance on a Horizontal Surface Calculation Function (rate of energy per unit of time)
def diffuse_irradiance_calculation_function(direct_normal_irradiance_on_horizontal_surface_df, rayleigh_transmittance_coeff_df, scattering_by_aerosol_transmittance_coeff_df, absorption_transmittance_coeff_df, barometric_pressure, angstrom_turbidity):
    
    diffuse_irradiance_from_rayleigh_atmosphere_df  = diffuse_irradiance_from_rayleigh_atmosphere_function(direct_normal_irradiance_on_horizontal_surface_df, rayleigh_transmittance_coeff_df)
    diffuse_irradiance_from_aerosol_scattering_df   = diffuse_irradiance_from_aerosol_scattering_function(direct_normal_irradiance_on_horizontal_surface_df, scattering_by_aerosol_transmittance_coeff_df)
    diffuse_irradiance_from_mutiple_reflection_df   = diffuse_irradiance_from_mutiple_reflection_function(direct_normal_irradiance_on_horizontal_surface_df, diffuse_irradiance_from_rayleigh_atmosphere_df, diffuse_irradiance_from_aerosol_scattering_df, absorption_transmittance_coeff_df, barometric_pressure, angstrom_turbidity)

    # Calculation Equation of Diffuse Irradiance on a Horizontal Surface
    diffuse_irrandiance_on_any_surface_df = diffuse_irradiance_from_rayleigh_atmosphere_df + diffuse_irradiance_from_aerosol_scattering_df + diffuse_irradiance_from_mutiple_reflection_df
    return diffuse_irrandiance_on_any_surface_df, diffuse_irradiance_from_rayleigh_atmosphere_df, diffuse_irradiance_from_aerosol_scattering_df, diffuse_irradiance_from_mutiple_reflection_df

# Diffuse Irradiance from Rayleigh Atmosphere (after the first pass) Calculation Function
def diffuse_irradiance_from_rayleigh_atmosphere_function(direct_normal_irradiation_on_any_surface_df, rayleigh_transmittance_coeff_df):
    diffuse_irradiance_from_rayleigh_atmosphere_df = (direct_normal_irradiation_on_any_surface_df)*((0.5)*(1-rayleigh_transmittance_coeff_df))
    return diffuse_irradiance_from_rayleigh_atmosphere_df

# Diffuse Irradiance from Aerosol Scattering (after the first pass) Calculation Function
def diffuse_irradiance_from_aerosol_scattering_function(direct_normal_irradiance_on_any_surface_df, scattering_by_aerosol_transmittance_coeff):
    diffuse_irradiance_from_aerosol_scattering_df = (direct_normal_irradiance_on_any_surface_df)*((0.75)*(1-scattering_by_aerosol_transmittance_coeff))
    return diffuse_irradiance_from_aerosol_scattering_df

# Diffuse Irradiance from Mutiple Reflections between Ground and Cloudless-sky Atmosphere Calculation Function
def diffuse_irradiance_from_mutiple_reflection_function(direct_normal_irradiance_on_any_surface_df, diffuse_irradiance_from_rayleigh_atmosphere_df, diffuse_irradiance_from_aerosol_scattering_df, absorption_transmittance_df, barometric_pressure, angstrom_turbidity):
    # Rayleigh and Aerosol Scattering Upwelling Transmittance Coefficient (Prime Over Transmittance)
    # 1.66 times the minimum air mass for the bean radiation accounts for an overall air mass for the upwelling diffuse irradiance
    # Rayleigh Upwelling Transmittance Coefficient
    rayleigh_upwelling_transmittance_coeff = 0.615958 + 0.375566*(math.exp((-0.221158)*((1.66)*(barometric_pressure/1013.25))))
    # Aerosol Scattering Upwelling Transmittance Coefficient
    scattering_by_aerosol_upwelling_transmittance_coeff = ((-0.914000)+((1.909267)*(math.exp((-0.667023)*(angstrom_turbidity)))))**((1.66)*(barometric_pressure/1013.25))
    # The Ground Albedo
    ground_albedo = 0.2
    
    # Calculation Equation of Diffuse Irradiance form Mutiple Reflections
    diffuse_irradiance_from_mutiple_reflection = (ground_albedo)*((direct_normal_irradiance_on_any_surface_df)+(diffuse_irradiance_from_rayleigh_atmosphere_df)+(diffuse_irradiance_from_aerosol_scattering_df))*(absorption_transmittance_df)*((0.5*(1-rayleigh_upwelling_transmittance_coeff))+(0.25*(1-scattering_by_aerosol_upwelling_transmittance_coeff)))
    return diffuse_irradiance_from_mutiple_reflection

# Diffuse Irradiation on a Horizontal Surface Calculation Function (rate of energy per unit of time)
def diffuse_irradiation_calculation_function(direct_normal_irradiation_on_any_surface_df, rayleigh_transmittance_coeff_df, scattering_by_aerosol_transmittance_coeff_df, absorption_transmittance_coeff_df, barometric_pressure, angstrom_turbidity):
    
    diffuse_irradiation_from_rayleigh_atmosphere_df = diffuse_irradiation_from_rayleigh_atmosphere_function(direct_normal_irradiation_on_any_surface_df, rayleigh_transmittance_coeff_df)
    diffuse_irradiation_from_aerosol_scattering_df = diffuse_irradiance_from_aerosol_scattering_function(direct_normal_irradiation_on_any_surface_df, scattering_by_aerosol_transmittance_coeff_df)
    diffuse_irradiation_from_mutiple_reflection_df = diffuse_irradiance_from_mutiple_reflection_function(direct_normal_irradiation_on_any_surface_df, diffuse_irradiation_from_rayleigh_atmosphere_df, diffuse_irradiation_from_aerosol_scattering_df, absorption_transmittance_coeff_df, barometric_pressure, angstrom_turbidity)

    # Calculation Equation of Diffuse Irradiance on a Horizontal Surface
    diffuse_irrandiation_any_horizontal_surface_df = diffuse_irradiation_from_rayleigh_atmosphere_df + diffuse_irradiation_from_aerosol_scattering_df + diffuse_irradiation_from_mutiple_reflection_df

    return diffuse_irrandiation_any_horizontal_surface_df, diffuse_irradiation_from_rayleigh_atmosphere_df, diffuse_irradiation_from_aerosol_scattering_df, diffuse_irradiation_from_mutiple_reflection_df

# Diffuse Irradiation from Rayleigh Atmosphere (after the first pass) Calculation Function
def diffuse_irradiation_from_rayleigh_atmosphere_function(direct_normal_irradiation_on_any_surface_df, rayleigh_transmittance_coeff_df):
    diffuse_irradiation_from_rayleigh_atmosphere_df = (direct_normal_irradiation_on_any_surface_df)*((0.5)*(1-rayleigh_transmittance_coeff_df))
    return diffuse_irradiation_from_rayleigh_atmosphere_df

# Diffuse Irradiation from Aerosol Scattering (after the first pass) Calculation Function
def diffuse_irradiation_from_aerosol_scattering_function(direct_normal_irradiation_on_any_surface_df, scattering_by_aerosol_transmittance_coeff_df):
    diffuse_irradiation_from_aerosol_scattering_df = (direct_normal_irradiation_on_any_surface_df)*((0.75)*(1-scattering_by_aerosol_transmittance_coeff_df))
    return diffuse_irradiation_from_aerosol_scattering_df

# Diffuse Irradiation from Mutiple Reflections between Ground and Cloudless-sky Atmosphere Calculation Function
def diffuse_irradiation_from_mutiple_reflection_function(direct_normal_irradiation_on_any_surface_df, diffuse_irradiation_from_rayleigh_atmosphere_df, diffuse_irradiation_from_aerosol_scattering_df, absorption_transmittance_df, barometric_pressure, angstrom_turbidity):
    
    # Rayleigh and Aerosol Scattering Upwelling Transmittance Coefficient (Prime Over Transmittance)
    # 1.66 times the minimum air mass for the bean radiation accounts for an overall air mass for the upwelling diffuse irradiance
     # Rayleigh Upwelling Transmittance Coefficient
    rayleigh_upwelling_transmittance_coeff = 0.615958 + 0.375566*(math.exp((-0.221158)*((1.66)*(barometric_pressure/1013.25))))
    # Aerosol Scattering Upwelling Transmittance Coefficient
    scattering_by_aerosol_upwelling_transmittance_coeff = ((-0.914000)+((1.909267)*(math.exp((-0.667023)*(angstrom_turbidity)))))**((1.66)*(barometric_pressure/1013.25))
    # The Ground Albedo
    ground_albedo = 0.2
    
    # Calculation Equation of Diffuse Irradiance form Mutiple Reflections
    diffuse_irradiance_from_mutiple_reflection_df = (ground_albedo)*((direct_normal_irradiation_on_any_surface_df)+(diffuse_irradiation_from_rayleigh_atmosphere_df)+(diffuse_irradiation_from_aerosol_scattering_df))*(absorption_transmittance_df)*((0.5*(1-rayleigh_upwelling_transmittance_coeff))+(0.25*(1-scattering_by_aerosol_upwelling_transmittance_coeff)))

    return diffuse_irradiance_from_mutiple_reflection_df

# Zenith Angle on Horizontal Plane Calculation Function (degree)
def zenith_angle_on_horizontal_plane_function(declination_angle_df, latitude_df, solar_hour_angle_df):
    zenith_angle_df = Rad2Deg(np.acos( ((np.sin(Deg2Rad(declination_angle_df)))*(np.sin(Deg2Rad(latitude_df)))) + ((np.cos(Deg2Rad(declination_angle_df)))*(np.cos(Deg2Rad(latitude_df)))*(np.cos(Deg2Rad(solar_hour_angle_df)))) ))
    return zenith_angle_df

# Zenith Angle on Inclined Plane that faced South Direction (degree)
def zenith_angle_on_inclined_plane_facing_south_direction_function(declination_angle_df, latitude_df, solar_hour_angle_df, rooftop_slope_angle_df):
    zenith_angle_df = Rad2Deg(np.acos( ((np.sin(Deg2Rad(declination_angle_df)))*(np.sin((Deg2Rad(latitude_df))-(Deg2Rad(rooftop_slope_angle_df))))) + ((np.cos(Deg2Rad(declination_angle_df)))*(np.cos((Deg2Rad(latitude_df))-(Deg2Rad(rooftop_slope_angle_df))))*(np.cos(Deg2Rad(solar_hour_angle_df)))) ))
    return zenith_angle_df

# Zenith Angle on Inclined Plane that faced at any Azimuth Angle (degree)
def zenith_angle_on_inclined_plane_facing_any_direction_function(declination_angle_df, latitude_df, solar_hour_angle_df, rooftop_slope_angle_df, rooftop_azimuth_angle_df):
    zenith_angle_df = Rad2Deg(np.acos(((np.cos(Deg2Rad(declination_angle_df)))*(np.sin(Deg2Rad(rooftop_slope_angle_df)))*(np.sin(Deg2Rad(rooftop_azimuth_angle_df)))*(np.sin(Deg2Rad(solar_hour_angle_df)))) + ((((np.cos(Deg2Rad(latitude_df)))*(np.cos(Deg2Rad(rooftop_slope_angle_df)))*(np.cos(Deg2Rad(declination_angle_df)))) + ((np.sin(Deg2Rad(latitude_df)))*(np.sin(Deg2Rad(rooftop_slope_angle_df)))*(np.cos(Deg2Rad(rooftop_azimuth_angle_df)))*(np.cos(Deg2Rad(declination_angle_df)))))*(np.cos(Deg2Rad(solar_hour_angle_df)))) + ((np.sin(Deg2Rad(latitude_df)))*(np.cos(Deg2Rad(rooftop_slope_angle_df)))*(np.sin(Deg2Rad(declination_angle_df)))) - ((np.cos(Deg2Rad(latitude_df)))*(np.sin(Deg2Rad(rooftop_slope_angle_df)))*(np.cos(Deg2Rad(rooftop_azimuth_angle_df)))*(np.sin(Deg2Rad(declination_angle_df)))) ))
    return zenith_angle_df


def loading_and_prepareing_data_for_qgis341(attribute_table_csvfile_name, global_solar_irradiance_csvfile_location, global_solar_irradiation_csvfile_location, global_solar_analysis_csvfile_location, steps, start_time, stop_time):
    #Select Attribute Table File (shape file, .shp)
    # Read Attribute Table File
    attribute_table_csv_df = pd.read_csv(attribute_table_csvfile_name)
    
    # Writing Analysis Column Index
    irradiance_df_column_index      = list(f"Solar Irradiance-{hour_time}:{minute_time}" for hour_time in range(start_time, stop_time+1) for minute_time in range(0,60,steps))
    irradiation_df_column_index     = list(f"Solar Irradiation-{hour_time}:{minute_time}" for hour_time in range(start_time, stop_time+1) for minute_time in range(0,60,steps))
    
    start_time_record = time.time()
    global_solar_analysis_df       = pd.DataFrame([])
    n=0
    #'''
    #uid = attribute_table_csv_df.loc[0, 'uid']
    for uid in attribute_table_csv_df['uid']:
        n+=1
        program_name = f"*****LOADING DATA: IRRADIANCE IRRADIATION AND SHADING FACTOR*****"
        rooftop_geometry_field_length = len(attribute_table_csv_df['uid'])
        if n == 1:
            print(f"\nPROCESSING {program_name}-(0/4)...")
        elif n == int(rooftop_geometry_field_length-1*(4/4)):
            print(f"PROCESSING {program_name}-(4/4)...")

        # Reading Solar Irradiance CSV file:
        solar_irradiance_csvfile_local_name            = f'Solar_Irradiance_uid_{uid}'
        solar_irradiance_csvfile_name                  = str(global_solar_irradiance_csvfile_location) + '/' + str(solar_irradiance_csvfile_local_name) + ".csv"
        global_solar_irradiance_building_analysis_df   = pd.read_csv(solar_irradiance_csvfile_name)

        # Reading Solar Irradiation CSV file:
        solar_irradiation_csvfile_local_name            = f'Solar_Irradiation_uid_{uid}'
        solar_irradiation_csvfile_name                  = str(global_solar_irradiation_csvfile_location) + '/' + str(solar_irradiation_csvfile_local_name) + ".csv"
        global_solar_irradiation_building_analysis_df   = pd.read_csv(solar_irradiation_csvfile_name)

        # Acquire Irradiance:
        #print("local uid irradiance df:\n", global_solar_irradiance_building_analysis_df)
        local_uid_building_irradiance_df                        = global_solar_irradiance_building_analysis_df.iloc[:,15:len(irradiance_df_column_index)+15]
        solar_irradiance_date_month_index_df                    = pd.to_datetime(global_solar_irradiance_building_analysis_df.date, format='%Y-%m-%d')
        local_uid_building_irradiance_df['day']                 = solar_irradiance_date_month_index_df.dt.day
        local_uid_building_irradiance_df['month']               = solar_irradiance_date_month_index_df.dt.month
        local_uid_building_irradiance_df                        = local_uid_building_irradiance_df.set_index(['month', 'day'])
        local_uid_building_irradiance_df                        = pd.DataFrame([local_uid_building_irradiance_df.replace(0, np.nan).mean(axis=1)]).transpose().groupby(level=0).mean().reset_index(level='month').round(6)
        local_uid_building_irradiance_df.columns                = ['month', 'sun_irr']
        local_uid_building_irradiance_primary_key_df            = pd.DataFrame([[global_solar_irradiation_building_analysis_df.loc[0, 'uid']]]*local_uid_building_irradiance_df.shape[0], columns=['uid'])
        local_uid_building_irradiance_lat_long_df               = pd.DataFrame([global_solar_irradiation_building_analysis_df.loc[0, ['lat', 'long']]]*local_uid_building_irradiance_df.shape[0]).reset_index(drop=True)
        year_df                                                 = pd.DataFrame([solar_irradiance_date_month_index_df.dt.year[0]]*local_uid_building_irradiance_df.shape[0], columns=['year']).reset_index(drop=True)
        local_uid_building_irradiance_df                        = pd.concat([local_uid_building_irradiance_primary_key_df, year_df, local_uid_building_irradiance_lat_long_df, local_uid_building_irradiance_df], axis=1)
        local_uid_building_irradiance_df                        = local_uid_building_irradiance_df.set_index(['uid', 'month'])
        
        # Acquire Irradiation:
        #print("local uid irradiation df:\n", global_solar_irradiation_building_analysis_df)
        local_uid_building_irradiation_df                       = global_solar_irradiation_building_analysis_df.iloc[:,15:len(irradiation_df_column_index)+15]
        solar_irradiation_date_month_index_df                   = pd.to_datetime(global_solar_irradiation_building_analysis_df.date, format='%Y-%m-%d')
        local_uid_building_irradiation_df['day']                = solar_irradiation_date_month_index_df.dt.day
        local_uid_building_irradiation_df['month']              = solar_irradiation_date_month_index_df.dt.month
        local_uid_building_irradiation_df                       = local_uid_building_irradiation_df.set_index(['month', 'day'])
        local_uid_building_irradiation_df                       = pd.DataFrame([local_uid_building_irradiation_df.sum(axis=1)]).transpose().groupby(level=0).sum().reset_index(level='month').round(6)
        local_uid_building_irradiation_df.columns               = ['month', 'sun_irrdt']
        local_uid_building_irradiation_primary_key_df           = pd.DataFrame([[global_solar_irradiation_building_analysis_df.loc[0, 'uid']]]*local_uid_building_irradiance_df.shape[0], columns=['uid'])
        local_uid_building_irradiation_df                       = pd.concat([local_uid_building_irradiation_primary_key_df, local_uid_building_irradiation_df], axis=1)
        local_uid_building_irradiation_df                       = local_uid_building_irradiation_df.set_index(['uid', 'month'])

        local_uid_buillding_solar_analysis_df                   = local_uid_building_irradiance_df.join(local_uid_building_irradiation_df)
        local_uid_buillding_solar_analysis_df                   = local_uid_buillding_solar_analysis_df.reset_index(level=['uid', 'month'])
        recorder_column                                         = ['uid', 'lat', 'long', 'year', 'month', 'sun_irr', 'sun_irrdt']
        local_uid_buillding_solar_analysis_df                   = local_uid_buillding_solar_analysis_df[recorder_column]
        local_uid_buillding_solar_analysis_df['update']         = pd.Timestamp("today").strftime(format='%Y-%d-%m')
        #print("local uid building solar analysis df:\n", local_uid_buillding_solar_analysis_df)
        global_solar_analysis_df                                = pd.concat([global_solar_analysis_df, local_uid_buillding_solar_analysis_df])

    #'''
    
    global_solar_analysis_df                                = global_solar_analysis_df.reset_index(drop=True)

    solar_daily_irradiance_analysis_csvfile_local_name      = f'solar_analysis_khonkaen'
    global_solar_daily_irradiance_writer, global_solar_analysis_csvfile_name = create_csvfile(global_solar_analysis_csvfile_location, solar_daily_irradiance_analysis_csvfile_local_name)
    global_solar_analysis_df.to_csv(global_solar_analysis_csvfile_name, index=False)

    end_time_record    = time.time()
    total_time  = end_time_record - start_time_record
    print("\n***** DONE LOADING DATA *****")
    print(f"Total execution time: {total_time:.4f} seconds\n")
        
    print("\n***** DONE PROCESSING DATA FOR QGIS *****")

    return 

def loading_and_prepareing_data_for_qgis331(attribute_table_csvfile_name, date_field_df, global_solar_irradiance_csvfile_location, global_solar_irradiation_csvfile_location, global_shading_factor_csvfile_location, global_solar_irradiance_analysis_csvfile_location, global_solar_irradiation_analysis_csvfile_location, global_shading_factor_analysis_csvfile_location, steps, desired_interval_steps, start_time, stop_time):
    #Select Attribute Table File (shape file, .shp)
    # Read Attribute Table File
    attribute_table_csv_df = pd.read_csv(attribute_table_csvfile_name)
    
    # No. of Date in a Year
    end_julian_date = date_field_df.shape[0]

    # Writing Analysis Column Index
    irradiance_df_column_index      = list(f"Solar Irradiance-{hour_time}:{minute_time}" for hour_time in range(start_time, stop_time+1) for minute_time in range(0,60,steps))
    irradiation_df_column_index     = list(f"Solar Irradiation-{hour_time}:{minute_time}" for hour_time in range(start_time, stop_time+1) for minute_time in range(0,60,steps))
    shading_factor_df_column_index  = list(f"Shading Factor-{hour_time}:{minute_time}" for hour_time in range(start_time, stop_time+1) for minute_time in range(0,60,steps))

    global_desired_interval_irradiance_df_column_index  = list(f"Solar Irradiance-{hour_time}:{minute_time}" for hour_time in range(start_time, stop_time+1) for minute_time in range(0,60,desired_interval_steps))
    global_desired_interval_irradiation_df_column_index = list(f"Solar Irradiation-{hour_time}:{minute_time}" for hour_time in range(start_time, stop_time+1) for minute_time in range(0,60,desired_interval_steps))
    global_desired_interval_shading_factor_column_index = list(f"Shading Factor-{hour_time}:{minute_time}" for hour_time in range(start_time, stop_time+1) for minute_time in range(0,60,desired_interval_steps))

    # Writing Analysis Multi-Index
    desired_irradiation_interval_row_index_level_zero_stop_interval = int(len(irradiation_df_column_index)/(desired_interval_steps/steps))
    desired_irradiation_interval_row_index_level_one_stop_interval  = int(desired_interval_steps/steps)
    desired_irradiation_interval_row_index_level_zero_list          = list(range(0, desired_irradiation_interval_row_index_level_zero_stop_interval))
    desired_irradiation_interval_row_index_level_one_list           = list(range(0, desired_irradiation_interval_row_index_level_one_stop_interval))
    desired_irradiation_interval_row_index_iterables                = [desired_irradiation_interval_row_index_level_zero_list, desired_irradiation_interval_row_index_level_one_list]
    desired_irradiation_interval_row_index_df                       = pd.MultiIndex.from_product(desired_irradiation_interval_row_index_iterables, names=["1st row", "2nd row"])
    
    
    for julian_date in range(1, end_julian_date):
        print(f"\nSOLAR ANALYSIS FUCNTION: DAY {julian_date}")
        global_desired_interval_irradiance_df       = pd.DataFrame([])
        global_desired_interval_irradiation_df      = pd.DataFrame([])
        global_desired_interval_shading_factor_df   = pd.DataFrame([])
        global_uid_building_characteristic_df       = pd.DataFrame([])
        
        #uid = attribute_table_csv_df.loc[0, 'uid']
        for uid in attribute_table_csv_df['uid']:
            
            # Reading Solar Irradiance CSV file:
            solar_irradiance_csvfile_local_name            = f'Solar_Irradiance_uid_{uid}'
            solar_irradiance_csvfile_name                  = str(global_solar_irradiance_csvfile_location) + '/' + str(solar_irradiance_csvfile_local_name) + ".csv"
            global_solar_irradiance_building_analysis_df   = pd.read_csv(solar_irradiance_csvfile_name)

            # Reading Solar Irradiation CSV file:
            solar_irradiation_csvfile_local_name            = f'Solar_Irradiation_uid_{uid}'
            solar_irradiation_csvfile_name                  = str(global_solar_irradiation_csvfile_location) + '/' + str(solar_irradiation_csvfile_local_name) + ".csv"
            global_solar_irradiation_building_analysis_df   = pd.read_csv(solar_irradiation_csvfile_name)

            # Reading Shading Factor CSV file:
            shading_factor_csvfile_local_name            = f'Shading_Factor_uid_{uid}'
            shading_factor_csvfile_name                  = str(global_shading_factor_csvfile_location) + '/' + str(shading_factor_csvfile_local_name) + ".csv"
            global_shading_factor_building_analysis_df   = pd.read_csv(shading_factor_csvfile_name)

            local_uid_building_characteristic_df = global_solar_irradiation_building_analysis_df.loc[0, global_solar_irradiation_building_analysis_df.columns[0:11]].to_frame().transpose()

            # Acquire Irradiance:
            global_solar_irradiance_building_analysis_df_column_index_filter    = global_solar_irradiance_building_analysis_df.columns[15:len(irradiance_df_column_index)+15]
            local_uid_building_irradiance_df                                    = global_solar_irradiance_building_analysis_df.loc[julian_date-1, global_solar_irradiance_building_analysis_df_column_index_filter]
            local_uid_building_irradiance_df                                    = local_uid_building_irradiance_df.transpose().to_frame().set_index(desired_irradiation_interval_row_index_df)
            local_uid_building_irradiance_df                                    = local_uid_building_irradiance_df.groupby(level=0).mean().transpose()

            # Acquire Irradiation:
            global_solar_irradiation_building_analysis_df_column_index_filter   = global_solar_irradiation_building_analysis_df.columns[15:len(irradiation_df_column_index)+15]
            local_uid_building_irradiation_df                                   = global_solar_irradiation_building_analysis_df.loc[julian_date-1, global_solar_irradiation_building_analysis_df_column_index_filter]
            local_uid_building_irradiation_df                                   = local_uid_building_irradiation_df.transpose().to_frame().set_index(desired_irradiation_interval_row_index_df)
            local_uid_building_irradiation_df                                   = local_uid_building_irradiation_df.groupby(level=0).sum().transpose()

            # Acquire Shading Factor:
            global_shading_factor_building_analysis_df_column_index_filter          = global_shading_factor_building_analysis_df.columns[13:len(shading_factor_df_column_index)+13]
            local_uid_building_shading_factor_df                                    = global_shading_factor_building_analysis_df.loc[julian_date-1, global_shading_factor_building_analysis_df_column_index_filter]
            local_uid_building_shading_factor_df                                    = local_uid_building_shading_factor_df.transpose().to_frame().set_index(desired_irradiation_interval_row_index_df)
            local_uid_building_shading_factor_df                                    = local_uid_building_shading_factor_df.groupby(level=0).mean().transpose()
            
            global_desired_interval_irradiance_df       = pd.concat([global_desired_interval_irradiance_df, local_uid_building_irradiance_df])
            global_desired_interval_irradiation_df      = pd.concat([global_desired_interval_irradiation_df, local_uid_building_irradiation_df])
            global_desired_interval_shading_factor_df   = pd.concat([global_desired_interval_shading_factor_df, local_uid_building_shading_factor_df])
            global_uid_building_characteristic_df       = pd.concat([global_uid_building_characteristic_df, local_uid_building_characteristic_df])
        
        global_uid_building_characteristic_df                   = global_uid_building_characteristic_df.reset_index(drop=True)

        global_desired_interval_irradiance_df                   = global_desired_interval_irradiance_df.reset_index(drop=True)
        global_desired_interval_irradiance_df.columns           = global_desired_interval_irradiance_df_column_index
        new_global_desired_interval_irradiance_df               = pd.concat([global_uid_building_characteristic_df, global_desired_interval_irradiance_df], axis=1)

        global_desired_interval_irradiation_df                  = global_desired_interval_irradiation_df.reset_index(drop=True)
        global_desired_interval_irradiation_df.columns          = global_desired_interval_irradiation_df_column_index
        new_global_desired_interval_irradiation_df              = pd.concat([global_uid_building_characteristic_df, global_desired_interval_irradiation_df], axis=1)

        global_desired_interval_shading_factor_df               = global_desired_interval_shading_factor_df.reset_index(drop=True)
        global_desired_interval_shading_factor_df.columns       = global_desired_interval_shading_factor_column_index
        new_global_desired_interval_shading_factor_df           = pd.concat([global_uid_building_characteristic_df, global_desired_interval_shading_factor_df], axis=1)

        date_csvfile_name_df    = pd.to_datetime(global_solar_irradiation_building_analysis_df.date, format='%Y-%m-%d')
        date_csvfile_name       = date_csvfile_name_df[julian_date-1].strftime(format = '%Y%m%d')
        
        solar_daily_irradiance_analysis_csvfile_local_name = f'solar_irradiance_khonkaen_{date_csvfile_name}'
        global_solar_daily_irradiance_writer, global_solar_daily_irradiance_analysis_csvfile_name = create_csvfile(global_solar_irradiance_analysis_csvfile_location, solar_daily_irradiance_analysis_csvfile_local_name)
        new_global_desired_interval_irradiance_df.to_csv(global_solar_daily_irradiance_analysis_csvfile_name, index=False)

        solar_daily_irradiation_analysis_csvfile_local_name = f'solar_irradiation_khonkaen_{date_csvfile_name}'
        global_solar_daily_irradiance_writer, global_solar_daily_irradiation_analysis_csvfile_name = create_csvfile(global_solar_irradiation_analysis_csvfile_location, solar_daily_irradiation_analysis_csvfile_local_name)
        new_global_desired_interval_irradiation_df.to_csv(global_solar_daily_irradiation_analysis_csvfile_name, index=False)

        shading_factor_analysis_csvfile_local_name = f'shading_factor_khonkaen_{date_csvfile_name}'
        global_shading_factor_writer, global_shading_factor_analysis_csvfile_name = create_csvfile(global_shading_factor_analysis_csvfile_location, shading_factor_analysis_csvfile_local_name)
        new_global_desired_interval_shading_factor_df.to_csv(global_shading_factor_analysis_csvfile_name, index=False)
        
    print("\n***** DONE PROCESSING SOLAR ANALYSIS FUCNTION *****")

    return 

# Positive Interval Feasible Answer
def positive_interval_feasible_answer_function(answer_df):
    feasible_answer_condition = (isinstance(answer_df, complex))|(answer_df < 0)
    answer_df = pd.DataFrame(np.where(feasible_answer_condition, 0, answer_df))
    return answer_df

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

def create_separator_df_function(end_row):
    separator_df = pd.DataFrame(list(["/////"]) for n in range (0,end_row))
    separator_df.columns = ['Separator Column']
    return separator_df

