import math
from datetime import date, time

import csv
import numpy as np
import pandas as pd

# Solar Constant (Isc = 1.3667 kilo Watts per square meter)
solar_constant = 1.3667 #kilo watts

def global_solar_irradiance_and_irrdiation_calculation_function(uid, building_fields_table_df, julian_date_df, declination_angle_df, eccentricity_correction_factor_df, solar_hour_angle_df, zenith_angle_df, global_solar_irradiance_csvfile_location, global_solar_irradiation_csvfile_location, global_solar_building_analysis_csvfile_location, global_transmittance_coeff_df_list, steps, barometric_pressure, angstrom_turbidity, start_time, stop_time):

    '''
    # Creating CSV File Name
    solar_irradiance_csvfile_local_name = f'Solar_Irradiance_uid_{uid}'
    solar_irradiation_csvfile_local_name = f'Solar_Irradiation_uid_{uid}'
    solar_building_analysis_csvfile_local_name = f'Building_Solar_Analysis_uid_{uid}'
    # Creating CSV File to Store Solar Irradiance Data
    solar_irradiance_writer, global_solar_irradiance_csvfile_name = create_csvfile(global_solar_irradiance_csvfile_location, solar_irradiance_csvfile_local_name)
    solar_irradiaction_writer, global_solar_irradiation_csvfile_name = create_csvfile(global_solar_irradiation_csvfile_location, solar_irradiation_csvfile_local_name)
    building_solar_analysis_writer, global_building_solar_analysis_csvfile_name = create_csvfile(global_solar_building_analysis_csvfile_location, solar_building_analysis_csvfile_local_name)
    '''

    # Global Transmittance Coefficient Data Base
    global_solar_irradiance_df       = pd.DataFrame([])
    global_solar_irradiation_df      = pd.DataFrame([])
    # Direct Normal Irradiance Data Base
    direct_normal_irradiance_column_index = []
    direct_normal_hourly_irradiance_field_list = []
    direct_normal_irradiance_global_df  = pd.DataFrame([])
    direct_normal_hourly_irradiance_global_df = pd.DataFrame([])
    # Direct Normal Irradiatiom Data Base
    direct_normal_irradiation_column_index = []
    direct_normal_hourly_irradiation_field_list = []
    direct_normal_irradiation_global_df = pd.DataFrame([])
    direct_normal_hourly_irradiation_global_df = pd.DataFrame([])
    # Diffuse Irradiance Data Base
    diffuse_irradiance_column_index = []
    diffuse_hourly_irradiance_field_list = []
    diffuse_irradiance_global_df = pd.DataFrame([])
    diffuse_hourly_irradiance_global_df = pd.DataFrame([])
    # Diffuse Irradiation Data Base
    diffuse_irradiation_column_index = []
    diffuse_hourly_irradiation_field_list = []
    diffuse_irradiation_global_df = pd.DataFrame([])
    diffuse_hourly_irradiation_global_df = pd.DataFrame([])
    # Diffuse Irradiance from Rayleigh Atmosphere Data Base
    diffuse_irradiance_from_rayleigh_atmosphere_column_index = []
    diffuse_irradiance_from_rayleigh_atmosphere_global_df = pd.DataFrame([])
    # Diffuse Irradiation from Rayleigh Atmosphere Data Base
    diffuse_irradiation_from_rayleigh_atmosphere_column_index = []
    diffuse_irradiation_from_rayleigh_atmosphere_global_df = pd.DataFrame([])
    # Diffuse Irradiance from Aerosol Scattering Data Base
    diffuse_irradiance_from_aerosol_scattering_column_index = []
    diffuse_irradiance_from_aerosol_scattering_global_df = pd.DataFrame([])
    # Diffuse Irradiation from Aerosol Scattering Data Base
    diffuse_irradiation_from_aerosol_scattering_column_index = []
    diffuse_irradiation_from_aerosol_scattering_global_df = pd.DataFrame([])
    # Diffuse Irradiance from Mutiple Reflection Data Base
    diffuse_irradiance_from_multiple_reflection_column_index = []
    diffuse_irradiance_from_multiple_reflection_global_df = pd.DataFrame([])
    # Diffuse Irradistion from Mutiple Reflection Data Base
    diffuse_irradiation_from_multiple_reflection_column_index = []
    diffuse_irradiation_from_multiple_reflection_global_df = pd.DataFrame([])

    # No. of Date in a Year
    end_julian_date = julian_date_df.shape[0]

    # Acquire Latitude of Builiding from Building Fields Table Data Frame
    uid_building_latitude       = building_fields_table_df.loc[0,'long']
    uid_building_latitude       = building_fields_table_df.loc[0,'lat']
    building_area               = building_fields_table_df.loc[0, 'Area']
    
    # Writing Building characteristics to each row
    new_building_fields_tables_df = pd.DataFrame((building_fields_table_df.values.tolist())*end_julian_date, columns=building_fields_table_df.columns)

    separator_df = create_separator_df_function(end_julian_date)

    # Writing Irradiance Fields
    direct_normal_irradiance_column_index                       = list(f"Direct Normal Irradiance-{hour_time}:{minute_time}" for hour_time in range (start_time, stop_time) for minute_time in range(0, 60, steps))
    diffuse_irradiance_column_index                             = list(f"Diffuse Irradiance-{hour_time}:{minute_time}" for hour_time in range (start_time, stop_time) for minute_time in range(0, 60, steps))
    diffuse_irradiance_from_rayleigh_atmosphere_column_index    = list(f"Diffuse Irradiance from Rayleigh Atmosphere-{hour_time}:{minute_time}" for hour_time in range (start_time, stop_time) for minute_time in range(0, 60, steps))
    diffuse_irradiance_from_aerosol_scattering_column_index     = list(f"Diffuse Irradiance from Aerosol Scattering-{hour_time}:{minute_time}" for hour_time in range (start_time, stop_time) for minute_time in range(0, 60, steps))
    diffuse_irradiance_from_multiple_reflection_column_index    = list(f"Diffuse Irradiance from Mutiple Reflection-{hour_time}:{minute_time}" for hour_time in range (start_time, stop_time) for minute_time in range(0, 60, steps))
    
    # Writing Irradiation Fields
    direct_normal_irradiation_column_index                      = list(f"Direct Normal Irradiation-{hour_time}:{minute_time}" for hour_time in range (start_time, stop_time) for minute_time in range(0, 60, steps))
    diffuse_irradiation_column_index                            = list(f"Diffuse Irradiation-{hour_time}:{minute_time}" for hour_time in range (start_time, stop_time) for minute_time in range(0, 60, steps))
    diffuse_irradiation_from_rayleigh_atmosphere_column_index   = list(f"Diffuse Irradiation from Rayleigh Atmosphere-{hour_time}:{minute_time}" for hour_time in range (start_time, stop_time) for minute_time in range(0, 60, steps))
    diffuse_irradiation_from_aerosol_scattering_column_index    = list(f"Diffuse Irradiation from Aerosol Scattering-{hour_time}:{minute_time}" for hour_time in range (start_time, stop_time) for minute_time in range(0, 60, steps))
    diffuse_irradiation_from_multiple_reflection_column_index   = list(f"Diffuse Irradiation from Mutiple Reflection-{hour_time}:{minute_time}" for hour_time in range (start_time, stop_time) for minute_time in range(0, 60, steps))

    # Acquire Solar Hour Angle from Global Solar Irradiance Geometry csvfile
    solar_hour_angle1_df = solar_hour_angle_df
    solar_hour_angle2_df = pd.concat([pd.DataFrame([[0]] for n in range (0,end_julian_date)), solar_hour_angle_df],axis=1)

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
    direct_normal_irradiance_df = direct_normal_irradiance_on_horizontal_surface_function(eccentricity_correction_factor_df, zenith_angle_df, cloud_transmittance_coeff_df, absorption_transmittance_coeff_df, rayleigh_transmittance_coeff_df, scattering_by_aerosol_transmittance_coeff_df)

    # Direct Normal Irradiation Calculation:
    direct_normal_irradiation = direct_normal_irradiation_on_horizontal_surface_function(eccentricity_correction_factor_df, cloud_transmittance_coeff_df, absorption_transmittance_coeff_df, rayleigh_transmittance_coeff_df, scattering_by_aerosol_transmittance_coeff_df, declination_angle_df, uid_building_latitude, solar_hour_angle1_df, solar_hour_angle2_df)
    direct_normal_irradiation = direct_normal_irradiation * building_area
    direct_normal_irradiation_local_list.append(direct_normal_irradiation)
    direct_normal_hourly_irradiation_list.append(direct_normal_irradiation)

    # Diffuse Irradiance on Horizontal Surface Calcualtion
    diffuse_irradiance, diffuse_irradiance_from_rayleigh_atmosphere, diffuse_irradiance_from_aerosol_scattering, diffuse_irradiance_from_multiple_reflection = diffuse_irradiance_on_horizontal_surface_function(direct_normal_irradiance_df, rayleigh_transmittance_coeff_df, scattering_by_aerosol_transmittance_coeff_df, absorption_transmittance_coeff_df, barometric_pressure, angstrom_turbidity)
    diffuse_irradiance_local_list.append(diffuse_irradiance)
    if minute_time == "00":
        diffuse_hourly_irradiance_list.append(diffuse_irradiance)

    diffuse_irradiance_from_rayleigh_atmosphere_local_list.append(diffuse_irradiance_from_rayleigh_atmosphere)
    diffuse_irradiance_from_aerosol_scattering_local_list.append(diffuse_irradiance_from_aerosol_scattering)
    diffuse_irradiance_from_multiple_reflection = diffuse_irradiance_from_multiple_reflection * building_area
    diffuse_irradiance_from_multiple_reflection_local_list.append(diffuse_irradiance_from_multiple_reflection)
    # Diffuse Irradiation on Horizontal Surface Calculation
    diffuse_irradiation, diffuse_irradiation_from_rayleigh_atmosphere, diffuse_irradiation_from_aerosol_scattering, diffuse_irradiation_from_multiple_reflection = diffuse_irradiation_on_horizontal_surface_function(direct_normal_irradiation, rayleigh_transmittance_coeff_df, scattering_by_aerosol_transmittance_coeff_df, absorption_transmittance_coeff_df, barometric_pressure, angstrom_turbidity)
    diffuse_irradiation = diffuse_irradiation
    diffuse_irradiation_local_list.append(diffuse_irradiation)
    diffuse_hourly_irradiation_list.append(diffuse_irradiation)

    diffuse_irradiation_from_rayleigh_atmosphere = diffuse_irradiation_from_rayleigh_atmosphere * building_area
    diffuse_irradiation_from_rayleigh_atmosphere_local_list.append(diffuse_irradiation_from_rayleigh_atmosphere)
    diffuse_irradiation_from_aerosol_scattering = diffuse_irradiation_from_aerosol_scattering * building_area
    diffuse_irradiation_from_aerosol_scattering_local_list.append(diffuse_irradiation_from_aerosol_scattering)
    diffuse_irradiation_from_multiple_reflection = diffuse_irradiation_from_multiple_reflection * building_area
    diffuse_irradiation_from_multiple_reflection_local_list.append(diffuse_irradiation_from_multiple_reflection)


    for julian_date in range (1, end_julian_date):

        # Local List for storing daily data
        direct_normal_irradiance_local_list = []
        direct_normal_irradiation_local_list = []
        diffuse_irradiance_local_list = []
        diffuse_irradiation_local_list = []
        diffuse_irradiance_from_rayleigh_atmosphere_local_list = []
        diffuse_irradiation_from_rayleigh_atmosphere_local_list = []
        diffuse_irradiance_from_aerosol_scattering_local_list = []
        diffuse_irradiation_from_aerosol_scattering_local_list = []
        diffuse_irradiance_from_multiple_reflection_local_list = []
        diffuse_irradiation_from_multiple_reflection_local_list = []

        direct_normal_hourly_irradiance_local_list = []
        direct_normal_hourly_irradiation_local_list = []
        diffuse_hourly_irradiance_local_list=[]
        diffuse_hourly_irradiation_local_list = []


        for hour in range (start_time, stop_time+1):
            if hour<10:
                hour_time = "0"+str(hour)
            else:
                hour_time = str(hour)

            # Hourly Solar Irradiance Data List
            direct_normal_hourly_irradiance_list = []
            direct_normal_hourly_irradiation_list = []
            diffuse_hourly_irradiance_list = []
            diffuse_hourly_irradiation_list = []

            for minute in range(0, 60, steps):
                if minute<10:
                    minute_time = "0"+str(minute)
                else:
                    minute_time = str(minute)

            # Acquire Daily Direct Normal Irradiance 
            direct_normal_hourly_irradiance_local = sum(direct_normal_hourly_irradiance_list)
            direct_normal_hourly_irradiance_local_list.append(direct_normal_hourly_irradiance_local)

            # Acquire Daily Direct Normal Irradiation
            direct_normal_hourly_irradiation_local = sum(direct_normal_hourly_irradiation_list)
            direct_normal_hourly_irradiation_local_list.append(direct_normal_hourly_irradiation_local)

            # Acquire Daily Diffuse Irradiance
            diffuse_hourly_irradiance_local = sum(diffuse_hourly_irradiance_list)
            diffuse_hourly_irradiance_local_list.append(diffuse_hourly_irradiance_local)

            # Acquire Daily Diffuse Irradiation
            diffuse_hourly_irradiation_local = sum(diffuse_hourly_irradiation_list)
            diffuse_hourly_irradiation_local_list.append(diffuse_hourly_irradiation_local)

        # Acquire Direct Normal Irradiance into Data Frame 
        direct_normal_irradiance_local_df = pd.DataFrame(direct_normal_irradiance_local_list)
        direct_normal_irradiance_global_df = pd.concat([direct_normal_irradiance_global_df, direct_normal_irradiance_local_df], axis=1)
        # Acquire Direct Normal Irradiation into Data Frame
        direct_normal_irradiation_local_df = pd.DataFrame(direct_normal_irradiation_local_list)
        direct_normal_irradiation_global_df = pd.concat([direct_normal_irradiation_global_df, direct_normal_irradiation_local_df], axis=1)

        # Acquire Direct Normal Daily Irradiance into Data Frame
        direct_normal_hourly_irradiance_local_df = pd.DataFrame(direct_normal_hourly_irradiance_local_list)
        direct_normal_hourly_irradiance_global_df = pd.concat([direct_normal_hourly_irradiance_global_df, direct_normal_hourly_irradiance_local_df], axis=1)
        # Acquire Direct Normal Daily Irradiation into Data Frame
        direct_normal_hourly_irradiation_local_df = pd.DataFrame(direct_normal_hourly_irradiation_local_list)
        direct_normal_hourly_irradiation_global_df =pd.concat([direct_normal_hourly_irradiation_global_df, direct_normal_hourly_irradiation_local_df], axis=1)

        # Acquire Diffuse Irradiance into Data Frame
        diffuse_irradiance_local_df = pd.DataFrame(diffuse_irradiance_local_list)
        diffuse_irradiance_global_df = pd.concat([diffuse_irradiance_global_df, diffuse_irradiance_local_df], axis=1)
        # Acquire Diffuse Irradiation into Data Frame
        diffuse_irradiation_local_df = pd.DataFrame(diffuse_irradiation_local_list)
        diffuse_irradiation_global_df = pd.concat([diffuse_irradiation_global_df, diffuse_irradiation_local_df], axis=1)

        # Acquire Diffuse Daily Irradiance into Data Frame
        diffuse_hourly_irradiance_local_df = pd.DataFrame(diffuse_hourly_irradiance_local_list)
        diffuse_hourly_irradiance_global_df = pd.concat([diffuse_hourly_irradiance_global_df, diffuse_hourly_irradiance_local_df], axis=1)
        # Acquire Diffuse Daily Irradiation into Data Frame
        diffuse_hourly_irradiation_local_df = pd.DataFrame(diffuse_hourly_irradiation_local_list)
        diffuse_hourly_irradiation_global_df = pd.concat([diffuse_hourly_irradiation_global_df, diffuse_hourly_irradiation_local_df], axis=1)
        
        
        # Acquire Diffuse Irradiance from Rayleigh Atmosphere into Data Frame
        diffuse_irradiance_from_rayleigh_atmosphere_local_df = pd.DataFrame(diffuse_irradiance_from_rayleigh_atmosphere_local_list)
        diffuse_irradiance_from_rayleigh_atmosphere_global_df = pd.concat([diffuse_irradiance_from_rayleigh_atmosphere_global_df, diffuse_irradiance_from_rayleigh_atmosphere_local_df], axis=1)
        # Acquire Diffuse Irradiation from Rayleigh Atmosphere into Data Frame
        diffuse_irradiation_from_rayleigh_atmosphere_local_df = pd.DataFrame(diffuse_irradiation_from_rayleigh_atmosphere_local_list)
        diffuse_irradiation_from_rayleigh_atmosphere_global_df = pd.concat([diffuse_irradiation_from_rayleigh_atmosphere_global_df, diffuse_irradiation_from_rayleigh_atmosphere_local_df], axis=1)

        # Acquire Diffuse Irradiance from Aerosol Scattering into Data Frame
        diffuse_irradiance_from_aerosol_scattering_local_df = pd.DataFrame(diffuse_irradiance_from_aerosol_scattering_local_list)
        diffuse_irradiance_from_aerosol_scattering_global_df = pd.concat([diffuse_irradiance_from_aerosol_scattering_global_df, diffuse_irradiance_from_aerosol_scattering_local_df], axis=1)
        # Acquire Diffuse Irradiation from Aerosol Scattering into Data Frame
        diffuse_irradiation_from_aerosol_scattering_local_df = pd.DataFrame(diffuse_irradiation_from_aerosol_scattering_local_list)
        diffuse_irradiation_from_aerosol_scattering_global_df = pd.concat([diffuse_irradiation_from_aerosol_scattering_global_df, diffuse_irradiation_from_aerosol_scattering_local_df], axis=1)

        # Acquire Diffuse Irradiance from Mutiple Reflection into Data Frame
        diffuse_irradiance_from_multiple_reflection_local_df = pd.DataFrame(diffuse_irradiance_from_multiple_reflection_local_list)
        diffuse_irradiance_from_multiple_reflection_global_df = pd.concat([diffuse_irradiance_from_multiple_reflection_global_df, diffuse_irradiance_from_multiple_reflection_local_df], axis=1)
        # Acquire Diffuse Irradiation from Mutiple Reflection into Data Frame
        diffuse_irradiation_from_multiple_reflection_local_df = pd.DataFrame(diffuse_irradiation_from_multiple_reflection_local_list)
        diffuse_irradiation_from_multiple_reflection_global_df = pd.concat([diffuse_irradiation_from_multiple_reflection_global_df, diffuse_irradiation_from_multiple_reflection_local_df], axis=1)

    # Organize New Building Organsize Field
    new_building_fields_tables_df = new_building_fields_tables_df.reset_index(drop=True)    

    # Organize Direct Normal Irradiance into Data Frame
    direct_normal_irradiance_global_df = direct_normal_irradiance_global_df.transpose()
    direct_normal_irradiance_global_df = direct_normal_irradiance_global_df.reset_index(drop=True)
    direct_normal_irradiance_global_df.columns = direct_normal_irradiance_column_index
    # Qrganize Direct Normal Irradiation into Data Frame
    direct_normal_irradiation_global_df = direct_normal_irradiation_global_df.transpose()
    direct_normal_irradiation_global_df = direct_normal_irradiation_global_df.reset_index(drop=True)
    direct_normal_irradiation_global_df.columns = direct_normal_irradiation_column_index

    # Organize Direct Normal Hourly Irradiance into Data Frame
    direct_normal_hourly_irradiance_global_df = direct_normal_hourly_irradiance_global_df.transpose()
    direct_normal_hourly_irradiance_global_df = direct_normal_hourly_irradiance_global_df.reset_index(drop=True)
    direct_normal_hourly_irradiance_global_df.columns = direct_normal_hourly_irradiance_field_list
    # Organize Direct Normal Hourly Irradiation into Data Frame
    direct_normal_hourly_irradiation_global_df = direct_normal_hourly_irradiation_global_df.transpose()
    direct_normal_hourly_irradiation_global_df = direct_normal_hourly_irradiation_global_df.reset_index(drop=True)
    direct_normal_hourly_irradiation_global_df.columns = direct_normal_hourly_irradiation_field_list
    # Organsize Direct Normal Daily Irradiation into Data Frame
    direct_normal_daily_irradiation_global_series = direct_normal_hourly_irradiation_global_df.sum(axis=1, skipna=True)
    direct_normal_daily_irradiation_global_df = pd.DataFrame(direct_normal_daily_irradiation_global_series)
    direct_normal_daily_irradiation_global_df.columns = ['Daily Direct Normal Irradiation']
    
    # Organize Diffuse Irradiance into Data Frame
    diffuse_irradiance_global_df = diffuse_irradiance_global_df.transpose()
    diffuse_irradiance_global_df = diffuse_irradiance_global_df.reset_index(drop=True)
    diffuse_irradiance_global_df.columns = diffuse_irradiance_column_index
    # Organize Diffuse Irradiation into Data Frame
    diffuse_irradiation_global_df = diffuse_irradiation_global_df.transpose()
    diffuse_irradiation_global_df = diffuse_irradiation_global_df.reset_index(drop=True)
    diffuse_irradiation_global_df.columns = diffuse_irradiation_column_index

    # Organize Diffuse Hourly Irradiance into Data Frame
    diffuse_hourly_irradiance_global_df = diffuse_hourly_irradiance_global_df.transpose()
    diffuse_hourly_irradiance_global_df = diffuse_hourly_irradiance_global_df.reset_index(drop=True)
    diffuse_hourly_irradiance_global_df.columns = diffuse_hourly_irradiance_field_list
    # Organize Diffuse Hourly Irradiation into Data Frame
    diffuse_hourly_irradiation_global_df = diffuse_hourly_irradiation_global_df.transpose()
    diffuse_hourly_irradiation_global_df = diffuse_hourly_irradiation_global_df.reset_index(drop=True)
    diffuse_hourly_irradiation_global_df.columns = diffuse_hourly_irradiation_field_list
    # Organize Diffuse Daily Irradiation into Data Frame
    diffuse_daily_irradiation_global_series = diffuse_hourly_irradiation_global_df.sum(axis=1, skipna=True)
    diffuse_daily_irradiation_global_df = pd.DataFrame(diffuse_daily_irradiation_global_series)
    diffuse_daily_irradiation_global_df.columns = ['Daily Diffuse Irradiation']

    # Organise Diffuse Irradiance from Rayleigh Atmosphere into Data Frame
    diffuse_irradiance_from_rayleigh_atmosphere_global_df = diffuse_irradiance_from_rayleigh_atmosphere_global_df.transpose()
    diffuse_irradiance_from_rayleigh_atmosphere_global_df = diffuse_irradiance_from_rayleigh_atmosphere_global_df.reset_index(drop=True)
    diffuse_irradiance_from_rayleigh_atmosphere_global_df.columns = diffuse_irradiance_from_rayleigh_atmosphere_column_index
    # Organize Diffuse Irradiaton from Raylrigh Atmosphere into Data Frame
    diffuse_irradiation_from_rayleigh_atmosphere_global_df = diffuse_irradiation_from_rayleigh_atmosphere_global_df.transpose()
    diffuse_irradiation_from_rayleigh_atmosphere_global_df = diffuse_irradiation_from_rayleigh_atmosphere_global_df.reset_index(drop=True)
    diffuse_irradiation_from_rayleigh_atmosphere_global_df.columns = diffuse_irradiation_from_rayleigh_atmosphere_column_index

    # Organize Diffuse Irradiance from Aerosol Scattering into Data Frame
    diffuse_irradiance_from_aerosol_scattering_global_df = diffuse_irradiance_from_aerosol_scattering_global_df.transpose()
    diffuse_irradiance_from_aerosol_scattering_global_df = diffuse_irradiance_from_aerosol_scattering_global_df.reset_index(drop=True)
    diffuse_irradiance_from_aerosol_scattering_global_df.columns = diffuse_irradiance_from_aerosol_scattering_column_index
    # Organize Diffuse Irradiation from Aerosol Scattering into Data Frame
    diffuse_irradiation_from_aerosol_scattering_global_df = diffuse_irradiation_from_aerosol_scattering_global_df.transpose()
    diffuse_irradiation_from_aerosol_scattering_global_df = diffuse_irradiation_from_aerosol_scattering_global_df.reset_index(drop=True)
    diffuse_irradiation_from_aerosol_scattering_global_df.columns = diffuse_irradiation_from_aerosol_scattering_column_index

    # Organize Diffuse Irradiance from Mutiple Reflection into Data Frame
    diffuse_irradiance_from_multiple_reflection_global_df = diffuse_irradiance_from_multiple_reflection_global_df.transpose()
    diffuse_irradiance_from_multiple_reflection_global_df = diffuse_irradiance_from_multiple_reflection_global_df.reset_index(drop=True)
    diffuse_irradiance_from_multiple_reflection_global_df.columns = diffuse_irradiance_from_multiple_reflection_column_index
    # Organize Diffuse Irradiation form Mutiple Reflection into Data Frame
    diffuse_irradiation_from_multiple_reflection_global_df = diffuse_irradiation_from_multiple_reflection_global_df.transpose()
    diffuse_irradiation_from_multiple_reflection_global_df = diffuse_irradiation_from_multiple_reflection_global_df.reset_index(drop=True)
    diffuse_irradiation_from_multiple_reflection_global_df.columns = diffuse_irradiation_from_multiple_reflection_column_index

    # Combine All Transmittance Coefficient Data Frames into Global 
    global_solar_irradiance_df = pd.concat([direct_normal_irradiance_global_df, separator_df, diffuse_irradiance_global_df, separator_df, diffuse_irradiance_from_rayleigh_atmosphere_global_df, separator_df, diffuse_irradiance_from_aerosol_scattering_global_df, separator_df, diffuse_irradiance_from_multiple_reflection_global_df], axis=1)
    #print(f'\nGlobal Solar Irradiance Data Frame:\n{global_solar_irradiance_df}')
    global_solar_irradiation_df = pd.concat([direct_normal_irradiation_global_df, separator_df, diffuse_irradiation_global_df, separator_df, diffuse_irradiation_from_rayleigh_atmosphere_global_df, separator_df, diffuse_irradiation_from_aerosol_scattering_global_df, separator_df, diffuse_irradiation_from_multiple_reflection_global_df], axis=1)
    #print(f'\nGlobal Solar Irradiation Data Frame:\n{global_solar_irradiation_df}')
    global_building_solar_analysis_df = pd.concat([direct_normal_daily_irradiation_global_df, diffuse_daily_irradiation_global_df, separator_df, direct_normal_hourly_irradiance_global_df, separator_df, direct_normal_hourly_irradiation_global_df, separator_df, diffuse_hourly_irradiance_global_df, separator_df, diffuse_hourly_irradiation_global_df], axis=1)


    new_global_solar_irradiance_df = pd.concat([new_building_fields_tables_df, date_table_df, julian_date_table_df, sunrise_table_df, sunset_table_df, global_solar_irradiance_df], axis=1)
    #print(f'new_global_solar_irradiance_df')
    new_global_solar_irradiation_df = pd.concat([new_building_fields_tables_df, date_table_df, julian_date_table_df, sunrise_table_df, sunset_table_df, global_solar_irradiation_df], axis=1)
    #print(f'new_global_solar_irradiation_df')
    new_global_building_solar_analysis_df = pd.concat([new_building_fields_tables_df, date_table_df, julian_date_table_df, sunrise_table_df, sunset_table_df, global_building_solar_analysis_df], axis=1)

    new_global_solar_irradiance_df.to_csv(global_solar_irradiance_csvfile_name, index=False)
    new_global_solar_irradiation_df.to_csv(global_solar_irradiation_csvfile_name, index=False)
    new_global_building_solar_analysis_df.to_csv(global_building_solar_analysis_csvfile_name, index=False)

    return global_solar_irradiance_csvfile_name, global_solar_irradiation_csvfile_name

# Direct Normal Solar Irradiance on a Horizontal Surface Calculation Function (rate of energy per unit of time)
def direct_normal_irradiance_on_horizontal_surface_function(eccentricity_correction_factor, zenith_angle, cloud_transmittance_coeff, absorption_transmittance_coeff, rayleigh_transmittance_coeff, scattering_by_aerosol_transmittance_coeff):
    direct_normal_irradiance_on_horizontal_surface = (solar_constant)*(eccentricity_correction_factor)*(cloud_transmittance_coeff)*(absorption_transmittance_coeff)*(rayleigh_transmittance_coeff)*(scattering_by_aerosol_transmittance_coeff)*(math.cos(Deg2Rad(zenith_angle)))
    direct_normal_irradiance_on_horizontal_surface = positive_interval_feasible_answer_function(direct_normal_irradiance_on_horizontal_surface)
    return direct_normal_irradiance_on_horizontal_surface

# Direct Normal Solar Irradiation on a Horzontal Surface Calculation Function (amount of energy per unit of time)
def direct_normal_irradiation_on_horizontal_surface_function(eccentricity_correction_factor, cloud_transmittance_coeff, absorption_transmittance_coeff, rayleigh_transmittance_coeff, scattering_by_aerosol_transmittance_coeff, declination_angle, latitude, solar_hour_angle1, solar_hour_angle2):
    direct_normal_irradiation_on_horizontal_surface = (1)*(12/math.pi)*(solar_constant)*(eccentricity_correction_factor)*(cloud_transmittance_coeff)*(absorption_transmittance_coeff)*(rayleigh_transmittance_coeff)*(scattering_by_aerosol_transmittance_coeff)*(  ( (math.sin(Deg2Rad(declination_angle)))*(math.sin(Deg2Rad(latitude)))*((Deg2Rad(solar_hour_angle1))-(Deg2Rad(solar_hour_angle2)))) + ( (math.cos(Deg2Rad(declination_angle)))*(math.cos(Deg2Rad(latitude)))*( (math.sin(Deg2Rad(-solar_hour_angle2)))-(math.sin(Deg2Rad(-solar_hour_angle1))) ) )  )
    direct_normal_irradiation_on_horizontal_surface = positive_interval_feasible_answer_function(direct_normal_irradiation_on_horizontal_surface)
    return direct_normal_irradiation_on_horizontal_surface

# Diffuse Irradiance on a Horizontal Surface Calculation Function (rate of energy per unit of time)
def diffuse_irradiance_on_horizontal_surface_function(direct_normal_irradiance_on_horizontal_surface, rayleigh_transmittance_coeff, scattering_by_aerosol_transmittance_coeff, absorption_transmittance_coeff, barometric_pressure, angstrom_turbidity):
    
    diffuse_irradiance_from_rayleigh_atmosphere = diffuse_irradiance_from_rayleigh_atmosphere_function(direct_normal_irradiance_on_horizontal_surface, rayleigh_transmittance_coeff)
    diffuse_irradiance_from_aerosol_scattering = diffuse_irradiance_from_aerosol_scattering_function(direct_normal_irradiance_on_horizontal_surface, scattering_by_aerosol_transmittance_coeff)
    diffuse_irradiance_from_mutiple_reflection = diffuse_irradiance_from_mutiple_reflection_function(direct_normal_irradiance_on_horizontal_surface, diffuse_irradiance_from_rayleigh_atmosphere, diffuse_irradiance_from_aerosol_scattering, absorption_transmittance_coeff, barometric_pressure, angstrom_turbidity)

    # Calculation Equation of Diffuse Irradiance on a Horizontal Surface
    diffuse_irrandiance_on_horizontal_surface = diffuse_irradiance_from_rayleigh_atmosphere + diffuse_irradiance_from_aerosol_scattering + diffuse_irradiance_from_mutiple_reflection
    return diffuse_irrandiance_on_horizontal_surface, diffuse_irradiance_from_rayleigh_atmosphere, diffuse_irradiance_from_aerosol_scattering, diffuse_irradiance_from_mutiple_reflection

# Diffuse Irradiance from Rayleigh Atmosphere (after the first pass) Calculation Function
def diffuse_irradiance_from_rayleigh_atmosphere_function(direct_normal_irradiation_on_horizontal_surface, rayleigh_transmittance_coeff):
    diffuse_irradiance_from_rayleigh_atmosphere = (direct_normal_irradiation_on_horizontal_surface)*((0.5)*(1-rayleigh_transmittance_coeff))
    return diffuse_irradiance_from_rayleigh_atmosphere

# Diffuse Irradiance from Aerosol Scattering (after the first pass) Calculation Function
def diffuse_irradiance_from_aerosol_scattering_function(direct_normal_irradiance_on_horizontal_surface, scattering_by_aerosol_transmittance_coeff):
    diffuse_irradiance_from_aerosol_scattering = (direct_normal_irradiance_on_horizontal_surface)*((0.75)*(1-scattering_by_aerosol_transmittance_coeff))
    return diffuse_irradiance_from_aerosol_scattering

# Diffuse Irradiance from Mutiple Reflections between Ground and Cloudless-sky Atmosphere Calculation Function
def diffuse_irradiance_from_mutiple_reflection_function(direct_normal_irradiance_on_horizontal_surface, diffuse_irradiance_from_rayleigh_atmosphere, diffuse_irradiance_from_aerosol_scattering, absorption_transmittance, barometric_pressure, angstrom_turbidity):
    
    # Rayleigh and Aerosol Scattering Upwelling Transmittance Coefficient (Prime Over Transmittance)
    # 1.66 times the minimum air mass for the bean radiation accounts for an overall air mass for the upwelling diffuse irradiance
     # Rayleigh Upwelling Transmittance Coefficient
    rayleigh_upwelling_transmittance_coeff = 0.615958 + 0.375566*(math.exp((-0.221158)*((1.66)*(barometric_pressure/1013.25))))
    # Aerosol Scattering Upwelling Transmittance Coefficient
    scattering_by_aerosol_upwelling_transmittance_coeff = ((-0.914000)+((1.909267)*(math.exp((-0.667023)*(angstrom_turbidity)))))**((1.66)*(barometric_pressure/1013.25))
    # The Ground Albedo
    ground_albedo = 0.2
    
    # Calculation Equation of Diffuse Irradiance form Mutiple Reflections
    diffuse_irradiance_from_mutiple_reflection = (ground_albedo)*((direct_normal_irradiance_on_horizontal_surface)+(diffuse_irradiance_from_rayleigh_atmosphere)+(diffuse_irradiance_from_aerosol_scattering))*(absorption_transmittance)*((0.5*(1-rayleigh_upwelling_transmittance_coeff))+(0.25*(1-scattering_by_aerosol_upwelling_transmittance_coeff)))
    return diffuse_irradiance_from_mutiple_reflection

# Diffuse Irradiation on a Horizontal Surface Calculation Function (rate of energy per unit of time)
def diffuse_irradiation_on_horizontal_surface_function(direct_normal_irradiation_on_horizontal_surface, rayleigh_transmittance_coeff, scattering_by_aerosol_transmittance_coeff, absorption_transmittance_coeff, barometric_pressure, angstrom_turbidity):
    
    diffuse_irradiation_from_rayleigh_atmosphere = diffuse_irradiation_from_rayleigh_atmosphere_function(direct_normal_irradiation_on_horizontal_surface, rayleigh_transmittance_coeff)
    diffuse_irradiation_from_aerosol_scattering = diffuse_irradiance_from_aerosol_scattering_function(direct_normal_irradiation_on_horizontal_surface, scattering_by_aerosol_transmittance_coeff)
    diffuse_irradiation_from_mutiple_reflection = diffuse_irradiance_from_mutiple_reflection_function(direct_normal_irradiation_on_horizontal_surface, diffuse_irradiation_from_rayleigh_atmosphere, diffuse_irradiation_from_aerosol_scattering, absorption_transmittance_coeff, barometric_pressure, angstrom_turbidity)

    # Calculation Equation of Diffuse Irradiance on a Horizontal Surface
    diffuse_irrandiation_on_horizontal_surface = diffuse_irradiation_from_rayleigh_atmosphere + diffuse_irradiation_from_aerosol_scattering + diffuse_irradiation_from_mutiple_reflection

    return diffuse_irrandiation_on_horizontal_surface, diffuse_irradiation_from_rayleigh_atmosphere, diffuse_irradiation_from_aerosol_scattering, diffuse_irradiation_from_mutiple_reflection

# Diffuse Irradiation from Rayleigh Atmosphere (after the first pass) Calculation Function
def diffuse_irradiation_from_rayleigh_atmosphere_function(direct_normal_irradiation_on_horizontal_surface, rayleigh_transmittance_coeff):
    diffuse_irradiation_from_rayleigh_atmosphere = (direct_normal_irradiation_on_horizontal_surface)*((0.5)*(1-rayleigh_transmittance_coeff))
    return diffuse_irradiation_from_rayleigh_atmosphere

# Diffuse Irradiation from Aerosol Scattering (after the first pass) Calculation Function
def diffuse_irradiation_from_aerosol_scattering_function(direct_normal_irradiation_on_horizontal_surface, scattering_by_aerosol_transmittance_coeff):
    diffuse_irradiation_from_aerosol_scattering = (direct_normal_irradiation_on_horizontal_surface)*((0.75)*(1-scattering_by_aerosol_transmittance_coeff))
    return diffuse_irradiation_from_aerosol_scattering

# Diffuse Irradiation from Mutiple Reflections between Ground and Cloudless-sky Atmosphere Calculation Function
def diffuse_irradiation_from_mutiple_reflection_function(direct_normal_irradiation_on_horizontal_surface, diffuse_irradiation_from_rayleigh_atmosphere, diffuse_irradiation_from_aerosol_scattering, absorption_transmittance, barometric_pressure, angstrom_turbidity):
    
    # Rayleigh and Aerosol Scattering Upwelling Transmittance Coefficient (Prime Over Transmittance)
    # 1.66 times the minimum air mass for the bean radiation accounts for an overall air mass for the upwelling diffuse irradiance
     # Rayleigh Upwelling Transmittance Coefficient
    rayleigh_upwelling_transmittance_coeff = 0.615958 + 0.375566*(math.exp((-0.221158)*((1.66)*(barometric_pressure/1013.25))))
    # Aerosol Scattering Upwelling Transmittance Coefficient
    scattering_by_aerosol_upwelling_transmittance_coeff = ((-0.914000)+((1.909267)*(math.exp((-0.667023)*(angstrom_turbidity)))))**((1.66)*(barometric_pressure/1013.25))
    # The Ground Albedo
    ground_albedo = 0.2
    
    # Calculation Equation of Diffuse Irradiance form Mutiple Reflections
    diffuse_irradiance_from_mutiple_reflection = (ground_albedo)*((direct_normal_irradiation_on_horizontal_surface)+(diffuse_irradiation_from_rayleigh_atmosphere)+(diffuse_irradiation_from_aerosol_scattering))*(absorption_transmittance)*((0.5*(1-rayleigh_upwelling_transmittance_coeff))+(0.25*(1-scattering_by_aerosol_upwelling_transmittance_coeff)))

    return diffuse_irradiance_from_mutiple_reflection


def loading_and_prepareing_data_for_qgis(attribute_table_csvfile_name, global_solar_irradiance_geometry_csvfile_location, global_solar_irradiation_csvfile_location, globla_solar_daily_irradiance_analysis_csvfile_location, desired_steps):

    #Select Attribute Table File (shape file, .shp)
    #attribute_table_csvfile_name = r"C:\GISTDA\Solarcells_Project\Solar_Efficiency_Analysis_Program2.1\Attribute_Table_Data\Building_Attribute_Table_LOD200_Draft2.1.csv"
    # Read Attribute Table File
    attribute_table_csv_df = pd.read_csv(attribute_table_csvfile_name)

    # end_julian_date = 367
    end_julian_date = len(global_solar_irradiance_geometry_df['Julian Date'])+1
    
    #uid = attribute_table_csv_df.loc[0, 'uid']

    #Creating CSV File for Joining with Attribute Table (Qgis)
    for uid in attribute_table_csv_df['uid']:

        # Reading Data in CSV File
        solar_irradiance_geometry_csvfile_local_name = f'Solar_Irradiance_Geometry_uid_{uid}'
        solar_irradiance_geometry_csvfile_name = str(global_solar_irradiance_geometry_csvfile_location) + '/' + str(solar_irradiance_geometry_csvfile_local_name) + ".csv"
        global_solar_irradiance_geometry_df = pd.read_csv(solar_irradiance_geometry_csvfile_name)

        solar_daily_irradiance_analysis_csvfile_local_name = f'QGIS_Solar_Irradiance_Gov_Building_{uid}'
        global_solar_daily_irradiance_writer, global_solar_daily_irradiance_analysis_csvfile_name = create_csvfile(globla_solar_daily_irradiance_analysis_csvfile_location, solar_daily_irradiance_analysis_csvfile_local_name)

        #for uid in attribute_table_csv_df['uid']:

        solar_irradiation_csvfile_local_name = f'Solar_Irradiation_uid_{uid}'
        solar_irradiation_csvfile_name = str(global_solar_irradiation_csvfile_location) + '/' + str(solar_irradiation_csvfile_local_name) + ".csv"
        global_solar_irradiation_building_analysis_df = pd.read_csv(solar_irradiation_csvfile_name)
        
        start_time = int((global_solar_irradiation_building_analysis_df['Local Sunrise Time']).max())
        stop_time = int((global_solar_irradiation_building_analysis_df['Local Sunset Time']).min())

        global_uid_df = pd.DataFrame([])
        global_date_time_table_df = pd.DataFrame([])
        global_julian_date_df = pd.DataFrame([])
        global_irradiation_df = pd.DataFrame([])
        new_global_hourly_irradiance_df = pd.DataFrame([])

        #uid = attribute_table_csv_df.loc[0, 'uid']
        for julian_date in range(1, end_julian_date):
            program_name = "QGIS SOLAR IRRADIATION"
            checking_program_progress(uid, end_julian_date ,julian_date, program_name)
            local_irradiation_list = []

            for hour in range (start_time, stop_time+1):
                for minute in range(0, 60, desired_steps):
                    if hour<10:
                        hour_time = "0"+str(hour)
                    else:
                        hour_time = str(hour)
                    if minute<10:
                        minute_time = "0"+str(minute)
                    else:
                        minute_time = str(minute)

                    # Wrinting Uid
                    global_uid_df = pd.concat([global_uid_df, pd.DataFrame([uid])])
                    # Writing Date Field
                    local_date_table = global_solar_irradiation_building_analysis_df.iloc[julian_date-1, 7]
                    local_julian_date_table =  global_solar_irradiation_building_analysis_df.iloc[julian_date-1, 8]
                    # Writing Time Field
                    local_time_table = time.fromisoformat(f"{hour_time}:{minute_time}")
                    local_date_time_table = f"{str(local_date_table)} {local_time_table}"

                    local_julian_date_df = pd.DataFrame([local_julian_date_table])
                    global_julian_date_df = pd.concat([global_julian_date_df, local_julian_date_df])

                    local_date_time_table_df = pd.DataFrame([local_date_time_table])
                    global_date_time_table_df = pd.concat([global_date_time_table_df, local_date_time_table_df])

                    # Acquire Irradiance and Irradiation
                    local_direct_normal_irradiation = global_solar_irradiation_building_analysis_df.loc[julian_date-1, f"Direct Normal Irradiation-{hour_time}:{minute_time}"]
                    local_diffuse_irradiation = global_solar_irradiation_building_analysis_df.loc[julian_date-1, f"Diffuse Irradiation-{hour_time}:{minute_time}"]
                    local_irradiation = local_direct_normal_irradiation + local_diffuse_irradiation
                    local_irradiation_list.append(local_irradiation)
            
            local_irradiation_df = pd.DataFrame(local_irradiation_list)
            global_irradiation_df = pd.concat([global_irradiation_df, local_irradiation_df])

        global_uid_df               = global_uid_df.reset_index(drop=True)
        global_uid_df.columns       = ['uid']

        global_date_time_table_df   = global_date_time_table_df.reset_index(drop=True)
        global_julian_date_df       = global_julian_date_df.reset_index(drop=True)
        global_date_time_table_df   = pd.concat([global_julian_date_df, global_date_time_table_df], axis=1)
        global_date_time_table_df   = global_date_time_table_df.reset_index(drop=True)
        global_date_time_table_df.columns = ['Julian Date', 'Date Time']

        global_irradiation_df = global_irradiation_df.reset_index(drop=True)
        global_irradiation_df.columns = ['Irradiation (Kwh/hr)']

        new_global_hourly_irradiance_df = pd.concat([global_uid_df, global_date_time_table_df, global_irradiation_df], axis=1)
        new_global_hourly_irradiance_df.to_csv(global_solar_daily_irradiance_analysis_csvfile_name, index=False)

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

def main():

    cloud_transmittance_coeff = 0.8
    absorption_transmittance_coeff = 0.95*0.95*0.95*0.8
    rayleigh_transmittance_coeff= 0.95
    scattering_by_aerosol_transmittance_coeff = 0.95

    eccentricity_correction_factor =  1.0085638
    declination_angle = -9.96626
    latitude = 14.88

    zenith_angle = 40.8986894405153
    solar_hour_angle1 = 13.50956
    solar_hour_angle2 = -1.49044

    x = direct_normal_irradiance_on_horizontal_surface_function(eccentricity_correction_factor, zenith_angle, cloud_transmittance_coeff, absorption_transmittance_coeff, rayleigh_transmittance_coeff, scattering_by_aerosol_transmittance_coeff)
    print(f'x:{x}')

    y = direct_normal_irradiation_on_horizontal_surface_function(eccentricity_correction_factor, cloud_transmittance_coeff, absorption_transmittance_coeff, rayleigh_transmittance_coeff, scattering_by_aerosol_transmittance_coeff, declination_angle, latitude, solar_hour_angle1, solar_hour_angle2)
    print(f'y: {y}')


#main()
