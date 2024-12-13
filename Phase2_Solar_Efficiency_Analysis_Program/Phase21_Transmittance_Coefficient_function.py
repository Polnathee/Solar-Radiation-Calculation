import math

import csv
import pandas as pd


# Processing and Storing Transmittance Coefficient Data
def transmittance_coeff_calculation_function(uid, building_fields_table_df, global_transmittance_coeff_csvfile_location, global_solar_irradiance_geometry_csvfile_name, steps, meter_above_sea_level, angstrom_turbidity, saturated_vapor_pressure, relative_humidity, ambient_temperature, ozone_layer):
    
    # Global Transmittance Coefficient Data Base
    global_transmittance_coeff_df               = pd.DataFrame([])
    # Cloud Transimittance Coefficient Data Base
    cloud_transmittance_coeff_field_list        = []
    cloud_transmittance_coeff_global_df         = pd.DataFrame([])
    # Rayleigh Scattering Transmittance Coefficient Data Base
    rayleigh_transmittance_coeff_field_list     = []
    rayleigh_transmittance_coeff_global_df      = pd.DataFrame([])
    # Scattering by Aerosol Transmittance Coefficient Data Base
    scattering_by_aerosol_transmittance_coeff_field_list  = []
    scattering_by_aerosol_transmittance_coeff_global_df   = pd.DataFrame([])
    # Aerosol Transmittance Coefficient Data Base
    aerosol_transmittance_coeff_field_list      = []
    aerosol_transmittance_coeff_global_df       = pd.DataFrame([])
    # Water Vapor Transmittance Coefficient Data Base
    water_vapor_transmittance_coeff_field_list  = []
    water_vapor_transmittance_coeff_global_df   = pd.DataFrame([])
    # Uniformly Mixed Gases Transmittance Coefficient Data Base
    mixed_gases_transmittance_coeff_field_list  = []
    mixed_gases_transmittance_coeff_global_df   = pd.DataFrame([])
    # Ozone Transmittance Coefficient Data Base
    ozone_transmittance_coeff_field_list        = []
    ozone_transmittance_coeff_global_df         = pd.DataFrame([])

    # Reading Data in CSV file
    global_solar_irradiance_geometry_df = pd.read_csv(global_solar_irradiance_geometry_csvfile_name)

    # Create CSV File to store Transmittance Data
    transmittance_coeff_csvfile_local_name = f'Transmittance_coefficient_uid_{uid}'
    writer, global_transmittance_coeff_csvfile_name = create_csvfile(global_transmittance_coeff_csvfile_location, transmittance_coeff_csvfile_local_name)

    sunrise_local_time = solar_hour_angle2local_time(global_solar_irradiance_geometry_df['Sunrise HRA'].max())
    sunset_local_time  = solar_hour_angle2local_time(global_solar_irradiance_geometry_df['Sunset HRA'].min())

    start_time = int(sunrise_local_time)
    stop_time  = int(sunset_local_time)
    #print(f'Start time: {start_time}, Stop time: {stop_time}')

    # end_julian_date = 365
    end_julian_date = len(global_solar_irradiance_geometry_df['Julian Date'])+1

    separator_df = create_separator_df_function(end_julian_date)

    for julian_date in range (1, end_julian_date):
        program_name = "TRANSMITANCE COEFFICIENT"
        checking_program_progress(uid, end_julian_date ,julian_date, program_name)

        # local List for storing daily data
        transmittance_coeff_buffer_list            = []
        cloud_transmittance_coeff_local_list       = []
        rayleigh_transmittance_coeff_local_list    = []
        scattering_by_aerosol_transmittance_coeff_local_list = []
        aerosol_transmittance_coeff_local_list     = []
        water_vapor_transmittance_coeff_local_list = []
        mixed_gases_transmittance_coeff_local_list = []
        ozone_transmittance_coeff_local_list       = []
        
        
        for hour in range (start_time, stop_time+1):
            for minute in range (0, 60, steps):
                if hour<10:
                    hour_time = "0"+str(hour)
                else:
                    hour_time = str(hour)

                if minute<10:
                    minute_time = "0"+str(minute)
                else:
                        minute_time = str(minute)

                # Acquire Zenith Angle from Global Solar Irradiance Geometry csvfile
                zenith_angle = global_solar_irradiance_geometry_df.loc[julian_date-1, f"Zenith-{hour_time}:{minute_time}"]

                if julian_date == 1:
                    # Writing Global Transmittance Fields
                    cloud_transmittance_coeff_field_list.append(f"Cloud Transmittance-{hour_time}:{minute_time}")
                    rayleigh_transmittance_coeff_field_list.append(f"Rayleigh Transmittance-{hour_time}:{minute_time}")
                    scattering_by_aerosol_transmittance_coeff_field_list.append(f"Scattering by Aerosol Transmittance-{hour_time}:{minute_time}")
                    aerosol_transmittance_coeff_field_list.append(f"Aersol Transmittance-{hour_time}:{minute_time}")
                    water_vapor_transmittance_coeff_field_list.append(f"Water Vapor Transmittance-{hour_time}:{minute_time}")
                    mixed_gases_transmittance_coeff_field_list.append(f"Mixed Gases Transmittance-{hour_time}:{minute_time}")
                    ozone_transmittance_coeff_field_list.append(f"Ozone Absorption Transmittance-{hour_time}:{minute_time}")

                # Transmittance Coefficients Calculation
                transmittance_coeff_buffer_list = transmittance_coeff_function(zenith_angle, meter_above_sea_level, angstrom_turbidity, saturated_vapor_pressure, relative_humidity, ambient_temperature, ozone_layer)
                #print(f'Transmittance_coeff_buffer_list: {transmittance_coeff_buffer_list}')
                
                # Acquire Transmittance Coefficients into local list
                cloud_transmittance_coeff_local_list.append(transmittance_coeff_buffer_list[0])
                rayleigh_transmittance_coeff_local_list.append(transmittance_coeff_buffer_list[1])
                scattering_by_aerosol_transmittance_coeff_local_list.append(transmittance_coeff_buffer_list[2])
                aerosol_transmittance_coeff_local_list.append(transmittance_coeff_buffer_list[3])
                water_vapor_transmittance_coeff_local_list.append(transmittance_coeff_buffer_list[4])
                mixed_gases_transmittance_coeff_local_list.append(transmittance_coeff_buffer_list[5])
                ozone_transmittance_coeff_local_list.append(transmittance_coeff_buffer_list[6])
        

        # Acquire Cloud Transmittance Coefficient into Data Frame
        cloud_transmittance_coeff_local_df  = pd.DataFrame(cloud_transmittance_coeff_local_list)
        cloud_transmittance_coeff_global_df = pd.concat([cloud_transmittance_coeff_global_df, cloud_transmittance_coeff_local_df], axis=1)

        # Acquire Rayleigh Transimttance Coefficient into Data Frame
        rayleigh_transmittance_coeff_local_df  = pd.DataFrame(rayleigh_transmittance_coeff_local_list)
        rayleigh_transmittance_coeff_global_df = pd.concat([rayleigh_transmittance_coeff_global_df, rayleigh_transmittance_coeff_local_df], axis=1)

        # Acquire Scattering by Aerosol Transmittance Coefficient into Data Frame
        scattering_by_aerosol_transmittance_coeff_local_df  = pd.DataFrame(scattering_by_aerosol_transmittance_coeff_local_list)
        scattering_by_aerosol_transmittance_coeff_global_df = pd.concat([scattering_by_aerosol_transmittance_coeff_global_df, scattering_by_aerosol_transmittance_coeff_local_df], axis=1)

        # Acquire Aerosol Transmittance Coefficient into Data Frame
        aerosol_transmittance_coeff_local_df  = pd.DataFrame(aerosol_transmittance_coeff_local_list)
        aerosol_transmittance_coeff_global_df = pd.concat([aerosol_transmittance_coeff_global_df, aerosol_transmittance_coeff_local_df], axis=1)

        # Acquire Water Vapor Transmittance Coefficient into Data Frame
        water_vapor_transmittance_coeff_local_df  = pd.DataFrame(water_vapor_transmittance_coeff_local_list)
        water_vapor_transmittance_coeff_global_df = pd.concat([water_vapor_transmittance_coeff_global_df, water_vapor_transmittance_coeff_local_df], axis=1)

        # Acquire Mixed Gases Transmittance Coefficient into Data Frame
        mixed_gases_transmittance_coeff_local_df  = pd.DataFrame(mixed_gases_transmittance_coeff_local_list)
        mixed_gases_transmittance_coeff_global_df = pd.concat([mixed_gases_transmittance_coeff_global_df, mixed_gases_transmittance_coeff_local_df], axis=1)

        # Acquire Ozone Transmittance Coefficient into Data Frame
        ozone_transmittance_coeff_local_df  = pd.DataFrame(ozone_transmittance_coeff_local_list)
        ozone_transmittance_coeff_global_df = pd.concat([ozone_transmittance_coeff_global_df, ozone_transmittance_coeff_local_df], axis=1)
        
    # Organize Cloud Transmittance into Global Data Frame
    cloud_transmittance_coeff_global_df = cloud_transmittance_coeff_global_df.transpose()
    cloud_transmittance_coeff_global_df = cloud_transmittance_coeff_global_df.reset_index(drop=True)
    cloud_transmittance_coeff_global_df.columns = cloud_transmittance_coeff_field_list

    # Organize Rayleigh Transmittance into Global Data Frame
    rayleigh_transmittance_coeff_global_df = rayleigh_transmittance_coeff_global_df.transpose()
    rayleigh_transmittance_coeff_global_df = rayleigh_transmittance_coeff_global_df.reset_index(drop=True)
    rayleigh_transmittance_coeff_global_df.columns = rayleigh_transmittance_coeff_field_list

    # Organize Scattering by Aerosol Transmittance into Global Data Frame
    scattering_by_aerosol_transmittance_coeff_global_df = scattering_by_aerosol_transmittance_coeff_global_df.transpose()
    scattering_by_aerosol_transmittance_coeff_global_df = scattering_by_aerosol_transmittance_coeff_global_df.reset_index(drop=True)
    scattering_by_aerosol_transmittance_coeff_global_df.columns = scattering_by_aerosol_transmittance_coeff_field_list

    # Organize Aerosol Transmittance into Global Data Frame
    aerosol_transmittance_coeff_global_df = aerosol_transmittance_coeff_global_df.transpose()
    aerosol_transmittance_coeff_global_df = aerosol_transmittance_coeff_global_df.reset_index(drop=True)
    aerosol_transmittance_coeff_global_df.columns = aerosol_transmittance_coeff_field_list

    # Organize Water Vapor Transmittance into Global Data Frame
    water_vapor_transmittance_coeff_global_df = water_vapor_transmittance_coeff_global_df.transpose()
    water_vapor_transmittance_coeff_global_df = water_vapor_transmittance_coeff_global_df.reset_index(drop=True)
    water_vapor_transmittance_coeff_global_df.columns = water_vapor_transmittance_coeff_field_list

    # Organize Mixed Gases Transmittance into Global Data Frame
    mixed_gases_transmittance_coeff_global_df = mixed_gases_transmittance_coeff_global_df.transpose()
    mixed_gases_transmittance_coeff_global_df = mixed_gases_transmittance_coeff_global_df.reset_index(drop=True)
    mixed_gases_transmittance_coeff_global_df.columns = mixed_gases_transmittance_coeff_field_list

    # Organize Ozone Transmittance into Global Data Frame
    ozone_transmittance_coeff_global_df = ozone_transmittance_coeff_global_df.transpose()
    ozone_transmittance_coeff_global_df = ozone_transmittance_coeff_global_df.reset_index(drop=True)
    ozone_transmittance_coeff_global_df.columns = ozone_transmittance_coeff_field_list

    # Combine All Transmittance Coefficient Data Frames into Global 
    global_transmittance_coeff_df = pd.concat([cloud_transmittance_coeff_global_df, separator_df, rayleigh_transmittance_coeff_global_df, separator_df, scattering_by_aerosol_transmittance_coeff_global_df, separator_df, aerosol_transmittance_coeff_global_df, separator_df, water_vapor_transmittance_coeff_global_df, separator_df, mixed_gases_transmittance_coeff_global_df, separator_df, ozone_transmittance_coeff_global_df], axis=1)
    #print(f'\nGlobal Transmittance Coefficient Data Frame:\n{transmittance_coeff_global_df}')
    
    # Writing Data Frame to CSV File
    date_table_df = global_solar_irradiance_geometry_df['Date']
    julian_date_table_df =global_solar_irradiance_geometry_df['Julian Date']
    sunrise_table_df = global_solar_irradiance_geometry_df['Local Sunrise Time']
    sunset_table_df = global_solar_irradiance_geometry_df['Local Sunset Time']

    new_global_transmittance_coeff_df = pd.concat([building_fields_table_df, date_table_df, julian_date_table_df, sunrise_table_df, sunset_table_df, global_transmittance_coeff_df], axis=1)
    #print(f'new_global_transmittance_coeff_df')
    new_global_transmittance_coeff_df.to_csv(global_transmittance_coeff_csvfile_name, index=False)

    return global_transmittance_coeff_csvfile_name, global_transmittance_coeff_df

# According to Parameterization Model B, iqbal
# Transmittance Coefficient Calculation Function
def transmittance_coeff_function(zenith_angle, meter_above_sea_level, angstrom_turbidity, saturated_vapor_pressure, relative_humidity, ambient_temperature, ozone_layer):

    # Calculation of Mass of Air and Relative Air Mass
    mass_of_air, relative_air_mass =  optical_mass_of_air_function(zenith_angle, meter_above_sea_level)

    # Calculation of Cloud Transmittance
    cloud_transmittance = 0.95

    # Calculation of Rayleigh Scattering Transmittance
    rayleigh_transmittance_coeff = rayleigh_transmittance_coeff_function(mass_of_air)

    # Calculation of Scattering by Aerosol Transnittance
    scattering_by_aerosol_transmittance_coeff = scattering_by_aerosol_transmittance_coeff_funciton(angstrom_turbidity, mass_of_air)

    # Calculation of Aerosol Transmittance
    aerosol_transmittance_coeff = aerosol_transmittance_coeff_function(angstrom_turbidity, mass_of_air)

    # Calculation of Water Vapor Transmittance
    water_vapor_transmittance_coeff = water_vapor_transmittance_coeff_function(saturated_vapor_pressure, relative_humidity, ambient_temperature, relative_air_mass)

    # Calculation of Uniformly Mixed Gases Transmittance
    mixed_gases_transmittance_coeff = mixed_gases_transmittance_coeff_function(mass_of_air)

    # Calculation of Ozone Transmittance
    ozone_transmittance_coeff = ozone_transmittance_coeff_function(ozone_layer, mass_of_air)

    # Transmittance of Absorption of water vapor, aerosol, mixed gases, and ozne
    absorption_transmittance_coeff = (aerosol_transmittance_coeff)*(water_vapor_transmittance_coeff)*(mixed_gases_transmittance_coeff)
    
    #print(f'\nt_aerosol: {aerosol_transmittance_coeff}, t_water_vapor:{water_vapor_transmittance_coeff}, t_mixed_gases: {mixed_gases_transmittance_coeff}, t_ozone: {ozone_transmittance_coeff}')
    #print(f'\nRayleigh Transmittance:{rayleigh_transmittance_coeff}, Scattering by Aerosol Transmittance: {scattering_by_aerosol_transmittance_coeff}, Transmittance: {absorption_transmittance_coeff}')
    return cloud_transmittance, rayleigh_transmittance_coeff, scattering_by_aerosol_transmittance_coeff, aerosol_transmittance_coeff, water_vapor_transmittance_coeff, mixed_gases_transmittance_coeff, ozone_transmittance_coeff

# Transmittance due to Rayleigh Scattering Calculation Function
def rayleigh_transmittance_coeff_function(mass_of_air):
    rayleigh_transmittance_coeff = 0.615958 + 0.375566*(math.exp((-0.221158)*(mass_of_air)))
    return rayleigh_transmittance_coeff

# Transmittance due to Scattering by Aerosol Calculation Function
def scattering_by_aerosol_transmittance_coeff_funciton(angstrom_turbidity, mass_of_air):
    scattering_by_aerosol_transmittance_coeff = ((-0.914000)+((1.909267)*(math.exp((-0.667023)*(angstrom_turbidity)))))**(mass_of_air)
    return scattering_by_aerosol_transmittance_coeff

# Transmittance due to Absorptance by Aerosol Calculation Function
def aerosol_transmittance_coeff_function(angstrom_turbidity, mass_of_air):
    ratio_of_energy_scattered_to_total_attentuation = 0.95 # A value is recommended by Hoyt
    aerosol_aborptance_direct_irradiance = (1 - ratio_of_energy_scattered_to_total_attentuation)*((-0.914000)+((1.909267)*(math.exp((-0.667023)*(angstrom_turbidity)))))**(mass_of_air)
    aerosol_transmittance_coeff = 1 - aerosol_aborptance_direct_irradiance 
    return aerosol_transmittance_coeff

# Transmittance due to Absorptance by Water Vapor Calculation Function
def water_vapor_transmittance_coeff_function(saturated_vapor_pressure, relative_humidity, ambient_temperature, relative_air_mass):
    # Saturated Vapor Pressure (Milibar)
    # Relative Humidity (-)
    # Ambient Temperature (Kelvin)
    precipitable_water = (0.8933)*(math.exp((0.1715*(relative_humidity)*(saturated_vapor_pressure))/(ambient_temperature)))
    u1 =  precipitable_water * relative_air_mass
    water_vapor_absorptance_direct_irradiance = ((0.110)*((u1)+((6.34)*(10**(-4))))**(0.3)) - (0.012)
    water_vapor_transmittance_coeff = 1 - water_vapor_absorptance_direct_irradiance
    return water_vapor_transmittance_coeff

# Transmttamce due to Absorptance by Uniformly Mixed Gases Calcualtion Function
def mixed_gases_transmittance_coeff_function(mass_of_air):
    mixed_gases_absorptance_direct_irradiance = ( ((0.00235*((126*(mass_of_air) + 0.0123)**0.26))) - (0.75*(10**(-4))) + (0.75*(10**(-3))*((mass_of_air)**0.875)) )
    mixed_gases_transmittance_coeff = 1 - mixed_gases_absorptance_direct_irradiance
    return mixed_gases_transmittance_coeff

# Transmittance due to Absorptance by Ozone Calculation Function
def ozone_transmittance_coeff_function(ozone_layer, mass_of_air):
    # According to Manabe and Stricker
    u3 = ozone_layer * mass_of_air
    ozone_absorptance_direct_irradiance = (0.045*(((u3)+(8.34*(10**-4)))**0.38)) - (3.1*(10**-3))
    ozone_transmittance_coeff = 1 - ozone_absorptance_direct_irradiance
    ozone_absorptance_direct_irradiance = positive_interval_feasible_answer_function(ozone_transmittance_coeff)
    return ozone_transmittance_coeff

# Air Mass Calculation
# Relative Air Mass Calculation Empirical Function
def relative_optical_air_mass_function(zenith_angle):
    numpy_error = 93.885-(zenith_angle)
    if numpy_error < 0:
        new_numpy = (zenith_angle) - 93.885 
        product_factor = -1
        relative_air_mass = (1 / ((math.cos(Deg2Rad(zenith_angle))) + (1 / ( (0.15)*(( (product_factor)*((new_numpy)**(1.253)) )) )) ))
    else: 
        relative_air_mass = (1 / ((math.cos(Deg2Rad(zenith_angle))) + (1 / ( (0.15)*(93.885-(zenith_angle)) )**(1.253)) ))
    relative_air_mass = positive_interval_feasible_answer_function(relative_air_mass)
    return relative_air_mass

# Optical Mass of Air Calculation Function
def optical_mass_of_air_function(zenith_angle, meter_above_sea_level):
    relative_air_mass = relative_optical_air_mass_function(zenith_angle)
    mass_of_air = (relative_air_mass)*(1/101.325)*(101.325*(math.exp((-0.0001184)*(meter_above_sea_level))))
    #print(f'\nMass of Air:{mass_of_air}, Relative Air Mass: {relative_air_mass}')
    return mass_of_air, relative_air_mass

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

# Positive Interval Feasible Answer
def positive_interval_feasible_answer_function(answer):
    if isinstance(answer, complex) :
        answer = 0
    elif answer < 0 :
        answer = 0
    else:
        answer = answer

    return answer


def Deg2Rad(deg):
    return deg * (math.pi / 180)
    
def Rad2Deg(rad):
    return rad * (180 / math.pi)


# Create CSV file for storing transmittance Data
def create_csvfile(csvfile_location, csvfile_local_name):
    csvfile_name = str(csvfile_location) + '/' + str(csvfile_local_name) + '.csv'
    with open(csvfile_name, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
    print(f'csv file name: {csvfile_name}')
    return writer, csvfile_name

def create_separator_df_function(end_row):
    separator_list = []
    for i in range(0, end_row):
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
    zenith_angle = Rad2Deg(0.507)
    meter_above_sea_level = 167 # khonKaen above sea level is 167 meters
    angstrom_turbidity = 0.0384
    saturated_vapor_pressure = 99.084
    relative_humidity = 0.000182
    ambient_temperature = 292
    ozone_layer = 260
    steps = 10
    uid = "32430B6CA65169B5-147-0"
    csvfile_location = r"C:\GISTDA\Solarcells_Project\Solar_Efficiency_Analysis_Program2.1\Test_CSV"
    csvfile_name = r"C:\GISTDA\Solarcells_Project\Solar_Efficiency_Analysis_Program2.1\Test_CSV\Solar_Radiation_Geometry_uid_32430B6CA65169B5-147-0.csv"

    transmittance_coeff_global_df = transmittance_coeff_calculation_function(uid, csvfile_location, csvfile_name, steps, meter_above_sea_level, angstrom_turbidity, saturated_vapor_pressure, relative_humidity, ambient_temperature, ozone_layer)

#main()

def main2():
    uid = "32430B6CA65169B5-147-0"
    csvfile_location = r"C:\GISTDA\Solarcells_Project\Solar_Efficiency_Analysis_Program2.1\Test_CSV"
    csvfile_name = r"C:\GISTDA\Solarcells_Project\Solar_Efficiency_Analysis_Program2.1\Test_CSV\Solar_Radiation_Geometry_uid_32430B6CA65169B5-147-0.csv"

    global_solar_irradiance_geometry_df = pd.read_csv(csvfile_name)
    zenith_angle_df = global_solar_irradiance_geometry_df.iloc[0,263:]

    meter_above_sea_level = 167 # Khon-Kaen height above sea level is 167 meters
    angstrom_turbidity = 0.0384
    saturated_vapor_pressure = 99.084
    relative_humidity = 0.000182
    ambient_temperature = 292
    ozone_layer = 260
    steps = 10

    transmittance_coeff_global_df = transmittance_coeff_calculation_function(uid, csvfile_location, csvfile_name, steps, meter_above_sea_level, angstrom_turbidity, saturated_vapor_pressure, relative_humidity, ambient_temperature, ozone_layer)

#main2()

def main3():
    csvfile_name = r"C:\GISTDA\Solarcells_Project\Solar_Efficiency_Analysis_Program2.1\Test_CSV\Solar_Radiation_Geometry_uid_32430B6CA65169B5-147-0.csv"

    global_solar_irradiance_geometry_df = pd.read_csv(csvfile_name)
    zenith_angle_df = global_solar_irradiance_geometry_df.iloc[0,263:]

    meter_above_sea_level = 167 # khonKaen above sea level is 167 meters
    angstrom_turbidity = 0.0384
    saturated_vapor_pressure = 99.084
    relative_humidity = 0.000182
    ambient_temperature = 292
    ozone_layer = 260
    steps = 10

    for zenith_angle in zenith_angle_df:
        zenith_angle = float(zenith_angle)
        print(f'Zenith Angle: {zenith_angle}')
        mass_of_air, relative_air_mass = optical_mass_of_air_function(zenith_angle, meter_above_sea_level)
        print(f'mass of air: {mass_of_air}, relative air mass: {relative_air_mass}')
        
        transmittance_coeff_function(zenith_angle, meter_above_sea_level, angstrom_turbidity, saturated_vapor_pressure, relative_humidity, ambient_temperature, ozone_layer)

#main3()