import csv
import pandas as pd

# Custom Program
import Phase21_Input_dedrived_data_function as input_data_program
import Phase21_SolarIrradianceGeometry_function as solar_irradiance_geometry_program
import Phase21_Transmittance_Coefficient_function as transmittance_coeff_program
import Phase21_SolarIrradianceAndRadiation_function as solar_irradiance_program


def main():
    #Select Attribute Table File (shape file, .shp)
    attribute_table_csv = r"C:\GISTDA\Solarcells_Project\Solar_Efficiency_Analysis_Program2.1\Attribute_Table_Data\Building_Attribute_Table_LOD200_Draft2.1.csv"
    attribute_table_csvfile_name = r"C:\GISTDA\Solarcells_Project\Solar_Efficiency_Analysis_Program2.1\Attribute_Table_Data\Building_Attribute_Table_LOD200_Draft2.1.csv"
    # Read Attribute Table File
    attribute_table_csv_df = pd.read_csv(attribute_table_csv)
    
    n = 0
    #uid = attribute_table_csv_df.loc[0, 'uid']

    for uid in attribute_table_csv_df['uid']:
        n+=1
        print(f'no.{n} uid: {uid}')

        # Solar Irradiance Geometry Function: Processing and Calculation
        # Setup file location for output files
        #global_solar_irradiance_geometry_csvfile_location = r"C:\GISTDA\Solarcells_Project\Solar_Efficiency_Analysis_Program2.1\Test_CSV"
        global_solar_irradiance_geometry_csvfile_location = r"C:\GISTDA\Solarcells_Project\Solar_Efficiency_Analysis_Program2.1\Phase2.1_CalResult_Solar_Efficiency\Gov_Building_Solar_Radiation_Geometry_Data"
        

        # Input dedrived data Function: Processing and  Organizing
        #building_fields_table_df = input_data_program.input_dedrived_data(attribute_table_csv, uid)
        #building_fields_table_df.head()
        # Acquire Data
        steps = 10
        std_longitude = 105 # bangkok UTC longitude (Ubon Ratchathani)
        #longitude = building_fields_table_df.loc[2,'Descriptions']
        #latitude  = building_fields_table_df.loc[1,'Descriptions']

        #Processing and Writing Solar Irradiance Geometry CSV file
        #global_solar_irradiance_geometry_csvfile_name, global_solar_irradiance_geometry_df = solar_irradiance_geometry_program.solar_radiation_geometry_funciton(uid, building_fields_table_df, global_solar_irradiance_geometry_csvfile_location, steps, std_longitude, longitude, latitude)


        # Transmittance Coefficient Function: Processing and Calculation
        # Setup file location for output files
        #global_transmittance_coeff_csvfile_location = r"C:\GISTDA\Solarcells_Project\Solar_Efficiency_Analysis_Program2.1\Test_CSV"
        global_transmittance_coeff_csvfile_location = r"C:\GISTDA\Solarcells_Project\Solar_Efficiency_Analysis_Program2.1\Phase2.1_CalResult_Solar_Efficiency\Gov_Building_Transmittance_Coefficient_Data"
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

        global_solar_irradiance_csvfile_location = r"C:\GISTDA\Solarcells_Project\Solar_Efficiency_Analysis_Program2.1\Phase2.1_CalResult_Solar_Efficiency\Gov_Building_Solar_Irradiance_Data"
        global_solar_irradiation_csvfile_location = r"C:\GISTDA\Solarcells_Project\Solar_Efficiency_Analysis_Program2.1\Phase2.1_CalResult_Solar_Efficiency\Gov_Building_Solar_Irradiation_Data"
        global_solar_building_analysis_csvfile_location = r"C:\GISTDA\Solarcells_Project\Solar_Efficiency_Analysis_Program2.1\Phase2.1_CalResult_Solar_Efficiency\Gov_Solar_Building_Analysis_Data"
        globla_solar_daily_irradiance_analysis_csvfile_location = r"C:\GISTDA\Solarcells_Project\Solar_Efficiency_Analysis_Program2.1\Phase2.1_CalResult_Solar_Efficiency\Gov__Daily_Irradiance_Anslysis_Data"
        
        barometric_pressure = 990
        angstrom_turbidity = 0.138
        steps = 10
        # Processing Solar Irradiation And Irradiance
        #global_solar_irradiance_csvfile_name, global_solar_irradiation_csvfile_name = solar_irradiance_program.global_solar_irradiance_calculation_funciton(attribute_table_csvfile_name, uid, building_fields_table_df, global_solar_irradiance_csvfile_location, global_solar_irradiation_csvfile_location, global_solar_building_analysis_csvfile_location, globla_solar_daily_irradiance_analysis_csvfile_location, global_solar_irradiance_geometry_csvfile_name, global_transmittance_coeff_csvfile_name, steps, barometric_pressure, angstrom_turbidity)
        
    # Preparing Data for Qgis
    solar_irradiance_program.loading_and_prepareing_data_for_qgis(attribute_table_csvfile_name, global_solar_building_analysis_csvfile_location, globla_solar_daily_irradiance_analysis_csvfile_location)


main()

