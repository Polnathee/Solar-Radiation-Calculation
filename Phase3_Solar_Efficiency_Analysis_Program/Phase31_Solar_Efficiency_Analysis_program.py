import csv
import pandas as pd

# Custom Program
import Phase3_Solar_Efficiency_Analysis_Program.Phase31_Input_dedrived_data_function as input_data_program
import Phase3_Solar_Efficiency_Analysis_Program.Phase31_SolarIrradianceGeometry_function as solar_irradiance_geometry_program
import Phase3_Solar_Efficiency_Analysis_Program.Phase32_Solar_IrradianceAndRadiation_function as solar_irradiance_geometry_program2
import Phase3_Solar_Efficiency_Analysis_Program.Phase31_Transmittance_Coefficient_function as transmittance_coeff_program
import Phase3_Solar_Efficiency_Analysis_Program.Phase31_SolarIrradianceAndRadiation_function as solar_irradiance_program

import Phase33_SolarIrradianceAndRadiation_function as solar_irradiance_and_irradiation_program


def main():
    #Select Attribute Table File (.csv)
    attribute_table_csvfile_name = r"C:\GISTDA\Solarcells_Project\Solar_Efficiency_Analysis_Program2.1\Attribute_Table_Data\Building_Attribute_Table_LOD200_Draft2.2.csv"
    # Selecr Vertices Attribute Table File (.csv)
    vertices_attribute_csvfile_name = r"C:\GISTDA\Solarcells_Project\Solar_Efficiency_Analysis_Program2.1\Attribute_Table_Data\Building_Attribute_Table_LOD200_Vertices_Draft2.3.csv"
    
    # Read Attribute Table File
    attribute_table_csv_df = pd.read_csv(attribute_table_csvfile_name)
    
    n = 0
    #uid = attribute_table_csv_df.loc[0, 'uid']

    # Calculation of Rooftop Geometry
    #global_rooftop_geometry_df = solar_irradiance_geometry_program.rooftop_geometry_function(vertices_attribute_csvfile_name)

    for uid in attribute_table_csv_df['uid']:
        n+=1
        #print(f'no.{n} uid: {uid}')

        # Solar Irradiance Geometry Function: Processing and Calculation
        # Setup file location for output files
        #global_solar_irradiance_geometry_csvfile_location = r"C:\GISTDA\Solarcells_Project\Solar_Efficiency_Analysis_Program2.1\Test_CSV"
        global_solar_irradiance_geometry_csvfile_location = r"C:\GISTDA\Solarcells_Project\Solar_Efficiency_Analysis_Program2.1\Phase2.2_CalResult_Solar_Efficiency\Gov_Building_Solar_Irradiance_Geometry_Data_Phase2.2"
    
        # Input dedrived data Function: Processing and  Organizing
        #building_fields_table_df = input_data_program.input_dedrived_data(attribute_table_csvfile_name, uid)
        #building_fields_table_df.head()
        # Acquire Data
        steps = 10
        std_longitude = 105 # bangkok UTC longitude (Ubon Ratchathani)
        #longitude = building_fields_table_df.iloc[0,2]
        #latitude  = building_fields_table_df.iloc[0,1]

        #Processing and Writing Solar Irradiance Geometry CSV file
        #global_solar_irradiance_geometry_csvfile_name, global_solar_irradiance_geometry_df = solar_irradiance_geometry_program.solar_radiation_geometry_funciton(uid, building_fields_table_df, global_rooftop_geometry_df, global_solar_irradiance_geometry_csvfile_location, steps, std_longitude, longitude, latitude)
                                                                                                                                
        # Transmittance Coefficient Function: Processing and Calculation
        # Setup file location for output files
        #global_transmittance_coeff_csvfile_location = r"C:\GISTDA\Solarcells_Project\Solar_Efficiency_Analysis_Program2.1\Test_CSV"
        global_transmittance_coeff_csvfile_location = r"C:\GISTDA\Solarcells_Project\Solar_Efficiency_Analysis_Program2.1\Phase2.2_CalResult_Solar_Efficiency\Gov_Building_Transmittance_Coefficient_Data_Phase2.2"
        # Acquire Data
        meter_above_sea_level    = 167        # KhonKaen height above sea level is 167 meters
        angstrom_turbidity       = 0.138      # Mean Angstrom's Turbidity at KhonKaen over year
        saturated_vapor_pressure = 99.084     # kilo Pascals
        relative_humidity        = 0.000182
        ambient_temperature      = 292        # kilo Pascals
        ozone_layer              = 260        # Centimeters

        # Processing and Writing Transmittance Coefficient CSV File
        #global_transmittance_coeff_csvfile_name, global_transmittance_coeff_df = transmittance_coeff_program.transmittance_coeff_calculation_function(uid, building_fields_table_df, global_transmittance_coeff_csvfile_location, global_solar_irradiance_geometry_csvfile_name, steps, meter_above_sea_level, angstrom_turbidity, saturated_vapor_pressure, relative_humidity, ambient_temperature, ozone_layer)

        #global_solar_irradiance_csvfile_location = r"C:\GISTDA\Solarcells_Project\Solar_Efficiency_Analysis_Program2.1\Test_CSV"
        #global_solar_irradiation_csvfile_location = r"C:\GISTDA\Solarcells_Project\Solar_Efficiency_Analysis_Program2.1\Test_CSV"
        #global_solar_building_analysis_csvfile_location = r"C:\GISTDA\Solarcells_Project\Solar_Efficiency_Analysis_Program2.1\Test_CSV"
        #globla_solar_daily_irradiance_analysis_csvfile_location = r"C:\GISTDA\Solarcells_Project\Solar_Efficiency_Analysis_Program2.1\Test_CSV"
        
        global_solar_irradiance_csvfile_location = r"C:\GISTDA\Solarcells_Project\Solar_Efficiency_Analysis_Program2.1\Phase2.2_CalResult_Solar_Efficiency\Gov_Building_Solar_Irradiance_Data_Phase2.2"
        global_solar_irradiation_csvfile_location = r"C:\GISTDA\Solarcells_Project\Solar_Efficiency_Analysis_Program2.1\Phase2.2_CalResult_Solar_Efficiency\Gov_Building_Solar_Irradiation_Data_Phase2.2"
        global_solar_building_analysis_csvfile_location = r"C:\GISTDA\Solarcells_Project\Solar_Efficiency_Analysis_Program2.1\Phase2.2_CalResult_Solar_Efficiency\Gov_Solar_Building_Analysis_Data_Phase2.2"
        global_solar_daily_irradiation_analysis_csvfile_location = r"C:\GISTDA\Solarcells_Project\Solar_Efficiency_Analysis_Program2.1\Phase2.2_CalResult_Solar_Efficiency\Gov_Daily_Irradiation_Analysis_Data_Phase2.2"
        barometric_pressure = 990
        angstrom_turbidity = 0.138
        steps = 10
        # Processing Solar Irradiation And Irradiance
        #global_solar_irradiance_csvfile_name, global_solar_irradiation_csvfile_name = solar_irradiance_program. global_solar_irradiance_calculation_function(uid, building_fields_table_df, global_solar_irradiance_csvfile_location, global_solar_irradiation_csvfile_location, global_solar_building_analysis_csvfile_location, global_solar_irradiance_geometry_csvfile_location, global_transmittance_coeff_csvfile_location, steps, barometric_pressure, angstrom_turbidity)

    start_time = 5
    stop_time = 18
    steps = 10
    date_field_df = 1
    global_solar_irradiance_analysis_csvfile_location = 1
    global_solar_irradiation_analysis_csvfile_location = 1

    # Preparing Data for Qgis
    desired_interval_steps = 30
    #solar_irradiance_program.loading_and_prepareing_data_for_qgis( attribute_table_csvfile_name, global_solar_irradiance_geometry_csvfile_location, global_solar_building_analysis_csvfile_location, global_solar_irradiation_csvfile_location, global_solar_daily_irradiation_analysis_csvfile_location, steps, desired_interval_steps)
    #solar_irradiance_geometry_program2.loading_and_prepareing_data_for_qgis(attribute_table_csvfile_name, global_solar_irradiance_geometry_csvfile_location, global_solar_irradiation_csvfile_location, globla_solar_daily_irradiance_analysis_csvfile_location, steps)
    #solar_irradiance_and_irradiation_program.loading_and_prepareing_data_for_qgis(attribute_table_csvfile_name, date_field_df, global_solar_irradiance_csvfile_location, global_solar_irradiation_csvfile_location, global_solar_irradiance_analysis_csvfile_location, global_solar_irradiation_analysis_csvfile_location, steps, desired_interval_steps, start_time, stop_time)
#main()

