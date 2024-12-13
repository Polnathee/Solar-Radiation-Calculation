import math
import numpy as np
import csv
import pandas as pd
import time


# Processing and Storing Transmittance Coefficient Data
def transmittance_coeff_calculation_function(uid, building_fields_table_df, date_field_df, julian_date_df, zenith_angle_df, global_transmittance_coeff_csvfile_location, steps, meter_above_sea_level, angstrom_turbidity, saturated_vapor_pressure, relative_humidity, ambient_temperature, ozone_layer_thickness, start_time, stop_time):
    start_time_record = time.time()
    building_height =  building_fields_table_df['height'].values[0]
    # Area height above Sea Level Data Frame
    meter_above_sea_level_df = pd.DataFrame([[meter_above_sea_level+building_height]*zenith_angle_df.shape[1]]*zenith_angle_df.shape[0])
    
    # Angstrom Turbidity Data Frame
    angstrom_turbidity_df = pd.DataFrame([[angstrom_turbidity]*zenith_angle_df.shape[1]]*zenith_angle_df.shape[0])
    #print("Angstrom Turbidity df:\n", angstrom_turbidity_df)

    saturated_vapor_pressure_df = pd.DataFrame([[saturated_vapor_pressure]*zenith_angle_df.shape[1]]*zenith_angle_df.shape[0])
    #print("Saturated Vapor Pressure df:\n", saturated_vapor_pressure_df)

    relative_humidity_df = pd.DataFrame([[relative_humidity]*zenith_angle_df.shape[1]]*zenith_angle_df.shape[0])
    #print("Relative Humidity df:\n", relative_humidity_df)

    ambient_temperature_df = pd.DataFrame([[ambient_temperature]*zenith_angle_df.shape[1]]*zenith_angle_df.shape[0])
    #print("Ambient Temperature df:\n", ambient_temperature_df)

    ozone_layer_thickness_df = pd.DataFrame([[ozone_layer_thickness]*zenith_angle_df.shape[1]]*zenith_angle_df.shape[0])
    #print("Ozone Layer Thickness df:\n", ozone_layer_thickness_df)

    # No.of Date in a year
    end_julian_date = julian_date_df.shape[0]

    separator_df = create_separator_df_function(end_julian_date)

    # Solar Irradiance Transmittance Column Index
    cloud_transmittance_coeff_column_index                  = list(f"Cloud Transmittance-{hour_time}:{minute_time}" for hour_time in range(start_time,stop_time+1) for minute_time in range(0,60,steps))
    rayleigh_transmittance_coeff_column_index               = list(f"Rayleigh Transmittance-{hour_time}:{minute_time}" for hour_time in range(start_time,stop_time+1) for minute_time in range(0,60,steps))
    scattering_by_aerosol_transmittance_coeff_columns_index = list(f"Scattering by Aerosol Transmittance-{hour_time}:{minute_time}" for hour_time in range(start_time,stop_time+1) for minute_time in range(0,60,steps))
    aerosol_transmittance_coeff_column_index                = list(f"Aersol Transmittance-{hour_time}:{minute_time}" for hour_time in range(start_time,stop_time+1) for minute_time in range(0,60,steps))
    water_vapor_transmittance_coeff_column_index            = list(f"Water Vapor Transmittance-{hour_time}:{minute_time}" for hour_time in range(start_time,stop_time+1) for minute_time in range(0,60,steps))
    mixed_gases_transmittance_coeff_column_index            = list(f"Mixed Gases Transmittance-{hour_time}:{minute_time}" for hour_time in range(start_time,stop_time+1) for minute_time in range(0,60,steps))
    ozone_transmittance_coeff_column_index                  = list(f"Ozone Absorption Transmittance-{hour_time}:{minute_time}" for hour_time in range(start_time,stop_time+1) for minute_time in range(0,60,steps))

    # Transmittance Coefficients Calculation
    global_transmittance_coeff_df_list = transmittance_coeff_function(zenith_angle_df, meter_above_sea_level_df, angstrom_turbidity_df, saturated_vapor_pressure_df, relative_humidity_df, ambient_temperature_df, ozone_layer_thickness_df)

    # Organize New Building Organsize Field
    new_building_fields_tables_df = pd.DataFrame((building_fields_table_df.values.tolist())*end_julian_date, columns=building_fields_table_df.columns)

    # Organize Cloud Transmittance into Global Data Frame
    cloud_transmittance_coeff_global_df                     = global_transmittance_coeff_df_list[0].copy()
    cloud_transmittance_coeff_global_df.columns             = cloud_transmittance_coeff_column_index

    # Organize Rayleigh Transmittance into Global Data Frame
    rayleigh_transmittance_coeff_global_df                  = global_transmittance_coeff_df_list[1].copy()
    rayleigh_transmittance_coeff_global_df.columns          = rayleigh_transmittance_coeff_column_index

    # Organize Scattering by Aerosol Transmittance into Global Data Frame
    scattering_by_aerosol_transmittance_coeff_global_df     = global_transmittance_coeff_df_list[2].copy()
    scattering_by_aerosol_transmittance_coeff_global_df.columns = scattering_by_aerosol_transmittance_coeff_columns_index

    # Organize Aerosol Transmittance into Global Data Frame
    aerosol_transmittance_coeff_global_df                   = global_transmittance_coeff_df_list[3].copy()
    aerosol_transmittance_coeff_global_df.columns           = aerosol_transmittance_coeff_column_index

    # Organize Water Vapor Transmittance into Global Data Frame
    water_vapor_transmittance_coeff_global_df               = global_transmittance_coeff_df_list[4].copy()
    water_vapor_transmittance_coeff_global_df.columns       = water_vapor_transmittance_coeff_column_index

    # Organize Mixed Gases Transmittance into Global Data Frame
    mixed_gases_transmittance_coeff_global_df               = global_transmittance_coeff_df_list[5].copy()
    mixed_gases_transmittance_coeff_global_df.columns       = mixed_gases_transmittance_coeff_column_index

    # Organize Ozone Transmittance into Global Data Frame
    ozone_transmittance_coeff_global_df                     = global_transmittance_coeff_df_list[6].copy()
    ozone_transmittance_coeff_global_df.columns             = ozone_transmittance_coeff_column_index

    # Combine All Transmittance Coefficient Data Frames into Global 
    global_transmittance_coeff_df = pd.concat([cloud_transmittance_coeff_global_df, separator_df, rayleigh_transmittance_coeff_global_df, separator_df, scattering_by_aerosol_transmittance_coeff_global_df, separator_df, aerosol_transmittance_coeff_global_df, separator_df, water_vapor_transmittance_coeff_global_df, separator_df, mixed_gases_transmittance_coeff_global_df, separator_df, ozone_transmittance_coeff_global_df], axis=1)
    #print(f'\nGlobal Transmittance Coefficient Data Frame:\n{transmittance_coeff_global_df}')

    new_global_transmittance_coeff_df = pd.concat([new_building_fields_tables_df, date_field_df, global_transmittance_coeff_df], axis=1)
    #print("new_global_transmittance_coeff_df:\n", new_global_transmittance_coeff_df)
    

    # Create CSV File to store Transmittance Data
    transmittance_coeff_csvfile_local_name = f'Transmittance_coefficient_uid_{uid}'
    writer, global_transmittance_coeff_csvfile_name = create_csvfile(global_transmittance_coeff_csvfile_location, transmittance_coeff_csvfile_local_name)
    new_global_transmittance_coeff_df.to_csv(global_transmittance_coeff_csvfile_name, index=False)
    
    end_time_record    = time.time()
    total_time  = end_time_record - start_time_record
    print("\n***** DONE PROCESSING TRANSMITTANCE FUNCTION *****")
    print(f"Total execution time: {total_time:.4f} seconds")
    return global_transmittance_coeff_df_list

# According to Parameterization Model B, iqbal
# Transmittance Coefficient Calculation Function
def transmittance_coeff_function(zenith_angle_df, meter_above_sea_level_df, angstrom_turbidity_df, saturated_vapor_pressure_df, relative_humidity_df, ambient_temperature_df, ozone_layer_df):

    # Calculation of Mass of Air and Relative Air Mass
    mass_of_air_df, relative_air_mass_df =  optical_mass_of_air_function(zenith_angle_df, meter_above_sea_level_df)

    # Calculation of Cloud Transmittance
    cloud_transmittance = 0.95
    cloud_transmittance = pd.DataFrame([[cloud_transmittance]*zenith_angle_df.shape[1]]*zenith_angle_df.shape[0])

    # Calculation of Rayleigh Scattering Transmittance
    rayleigh_transmittance_coeff_df = rayleigh_transmittance_coeff_function(mass_of_air_df)

    # Calculation of Scattering by Aerosol Transnittance
    scattering_by_aerosol_transmittance_coeff_df = scattering_by_aerosol_transmittance_coeff_funciton(angstrom_turbidity_df, mass_of_air_df)

    # Calculation of Aerosol Transmittance
    aerosol_transmittance_coeff_df = aerosol_transmittance_coeff_function(angstrom_turbidity_df, mass_of_air_df)

    # Calculation of Water Vapor Transmittance
    water_vapor_transmittance_coeff_df = water_vapor_transmittance_coeff_function(saturated_vapor_pressure_df, relative_humidity_df, ambient_temperature_df, relative_air_mass_df)

    # Calculation of Uniformly Mixed Gases Transmittance
    mixed_gases_transmittance_coeff_df = mixed_gases_transmittance_coeff_function(mass_of_air_df)

    # Calculation of Ozone Transmittance
    ozone_transmittance_coeff_df = ozone_transmittance_coeff_function(ozone_layer_df, mass_of_air_df)

    #print(f'\nt_aerosol:\n{aerosol_transmittance_coeff_df},\nt_water_vapor:\n{water_vapor_transmittance_coeff_df},\nt_mixed_gases:\n{mixed_gases_transmittance_coeff_df},\nt_ozone:\n{ozone_transmittance_coeff_df}')
    #print(f'\nRayleigh Transmittance:\n{rayleigh_transmittance_coeff_df},\nScattering by Aerosol Transmittance:\n{scattering_by_aerosol_transmittance_coeff_df}')
    return cloud_transmittance, rayleigh_transmittance_coeff_df, scattering_by_aerosol_transmittance_coeff_df, aerosol_transmittance_coeff_df, water_vapor_transmittance_coeff_df, mixed_gases_transmittance_coeff_df, ozone_transmittance_coeff_df

# Transmittance due to Rayleigh Scattering Calculation Function
def rayleigh_transmittance_coeff_function(mass_of_air_df):
    rayleigh_transmittance_coeff_df = 0.615958 + 0.375566*(np.exp((-0.221158)*(mass_of_air_df)))
    rayleigh_transmittance_coeff_df = feasible_transmittance_coeff_answer_function(rayleigh_transmittance_coeff_df)
    return rayleigh_transmittance_coeff_df

# Transmittance due to Scattering by Aerosol Calculation Function
def scattering_by_aerosol_transmittance_coeff_funciton(angstrom_turbidity_df, mass_of_air_df):
    scattering_by_aerosol_transmittance_coeff_df = ((-0.914000)+((1.909267)*(np.exp((-0.667023)*(angstrom_turbidity_df)))))**(mass_of_air_df)
    scattering_by_aerosol_transmittance_coeff_df = feasible_transmittance_coeff_answer_function(scattering_by_aerosol_transmittance_coeff_df)
    return scattering_by_aerosol_transmittance_coeff_df

# Transmittance due to Absorptance by Aerosol Calculation Function
def aerosol_transmittance_coeff_function(angstrom_turbidity_df, mass_of_air_df):
    ratio_of_energy_scattered_to_total_attentuation = 0.95 # A value is recommended by Hoyt
    ratio_of_energy_scattered_to_total_attentuation_df = pd.DataFrame([[ratio_of_energy_scattered_to_total_attentuation ]*mass_of_air_df.shape[1]]*mass_of_air_df.shape[0])
    
    aerosol_aborptance_direct_irradiance_df = (1 - ratio_of_energy_scattered_to_total_attentuation_df)*((-0.914000)+((1.909267)*(np.exp((-0.667023)*(angstrom_turbidity_df)))))**(mass_of_air_df)
    aerosol_transmittance_coeff_df = 1 - aerosol_aborptance_direct_irradiance_df
    aerosol_transmittance_coeff_df = feasible_transmittance_coeff_answer_function(aerosol_transmittance_coeff_df) 
    return aerosol_transmittance_coeff_df

# Transmittance due to Absorptance by Water Vapor Calculation Function
def water_vapor_transmittance_coeff_function(saturated_vapor_pressure_df, relative_humidity_df, ambient_temperature_df, relative_air_mass_df):
    # Saturated Vapor Pressure (Milibar)
    # Relative Humidity (-)
    # Ambient Temperature (Kelvin)
    precipitable_water_df = (0.8933)*(np.exp((0.1715*(relative_humidity_df)*(saturated_vapor_pressure_df))/(ambient_temperature_df)))
    u1_df =  precipitable_water_df * relative_air_mass_df
    water_vapor_absorptance_direct_irradiance_df = ((0.110)*((u1_df)+((6.34)*(10**(-4))))**(0.3)) - (0.012)
    water_vapor_transmittance_coeff_df = 1 - water_vapor_absorptance_direct_irradiance_df
    water_vapor_transmittance_coeff_df = feasible_transmittance_coeff_answer_function(water_vapor_transmittance_coeff_df) 
    return water_vapor_transmittance_coeff_df

# Transmttamce due to Absorptance by Uniformly Mixed Gases Calcualtion Function
def mixed_gases_transmittance_coeff_function(mass_of_air_df):
    mixed_gases_absorptance_direct_irradiance_df = ( ((0.00235*((126*(mass_of_air_df) + 0.0123)**0.26))) - (0.75*(10**(-4))) + (0.75*(10**(-3))*((mass_of_air_df)**0.875)) )
    mixed_gases_transmittance_coeff_df = 1 - mixed_gases_absorptance_direct_irradiance_df
    mixed_gases_transmittance_coeff_df = feasible_transmittance_coeff_answer_function(mixed_gases_transmittance_coeff_df) 
    return mixed_gases_transmittance_coeff_df

# Transmittance due to Absorptance by Ozone Calculation Function
def ozone_transmittance_coeff_function(ozone_layer_df, mass_of_air_df):
    # According to Manabe and Stricker
    u3_df = ozone_layer_df * mass_of_air_df
    ozone_absorptance_direct_irradiance_df = (0.045*(((u3_df)+(8.34*(10**-4)))**0.38)) - (3.1*(10**-3))
    ozone_transmittance_coeff_df = 1 - ozone_absorptance_direct_irradiance_df
    ozone_transmittance_coeff_df = positive_interval_feasible_answer_function(ozone_transmittance_coeff_df)
    ozone_transmittance_coeff_df = feasible_transmittance_coeff_answer_function(ozone_transmittance_coeff_df) 
    return ozone_transmittance_coeff_df

# Air Mass Calculation
# Optical Mass of Air Calculation Function
def optical_mass_of_air_function(zenith_angle_df, meter_above_sea_level_df):
    relative_air_mass = relative_optical_air_mass_function(zenith_angle_df)
    mass_of_air = (relative_air_mass)*(1/101.325)*(101.325*(np.exp((-0.0001184)*(meter_above_sea_level_df))))
    #print(f'\nMass of Air:\n{mass_of_air}, \nRelative Air Mass:\n{relative_air_mass}')
    return mass_of_air, relative_air_mass

# Relative Air Mass Calculation Empirical Function
def relative_optical_air_mass_function(zenith_angle_df):
    numpy_error_df = 93.885 - zenith_angle_df
    relative_air_mass_condition1 = (1 / ((np.cos(Deg2Rad(zenith_angle_df))) + (1 / ( (0.15)*(( (-1)*((zenith_angle_df - 93.885 )**(1.253)) )) )) ))
    relative_air_mass_condition2 = (1 / ((np.cos(Deg2Rad(zenith_angle_df))) + (1 / ( (0.15)*(93.885 - zenith_angle_df) )**(1.253)) ))
    
    relative_air_mass_df = pd.DataFrame(np.where(numpy_error_df<0, relative_air_mass_condition1, relative_air_mass_condition2))
    relative_air_mass_df = positive_interval_feasible_answer_function(relative_air_mass_df)
    return relative_air_mass_df

# Positive Interval Feasible Answer
def positive_interval_feasible_answer_function(answer_df):
    feasible_answer_condition = (isinstance(answer_df, complex))|(answer_df < 0)
    answer_df = pd.DataFrame(np.where(feasible_answer_condition, 0, answer_df))
    return answer_df

# Feasible Transmittance Coefficient Answer
def feasible_transmittance_coeff_answer_function(answer_df):
    feasible_answer_condition = (answer_df <= 1)&(answer_df >= 0)
    answer_df = pd.DataFrame(np.where(feasible_answer_condition, answer_df, 0))
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
    return writer, csvfile_name

def create_separator_df_function(end_row):
    separator_df = pd.DataFrame(list(["/////"]) for n in range (0,end_row))
    separator_df.columns = ['Separator Column']
    return separator_df


