import csv
import pandas as pd

# Custom Program
import Phase32_Input_dedrived_data_function         as input_data_program
import Phase32_Solar_Irradiance_Geometry_function   as solar_irradiance_geometry_program
import Phase32_Shading_Angle_Geometry_function      as shading_factor_program
import Phase32_Transmittance_Coefficient_function   as transmittance_coefficient_program
import Phase34_SolarIrradianceAndRadiation_function as solar_irradiance_and_irradiation_program


def solar_efficiency_analysis_program_function():
    # Select Attribute Table csv File (.csv)
    attribute_table_csvfile_name                        = r"C:\GISTDA\Solarcells_Project\Solar_Efficiency_Analysis_Program3\Attribute_Table_Data\Building_Attribute_Table_LOD200_Draft2.2.csv"
    # Read Attribute Table csv File
    attribute_table_csv_df                              = pd.read_csv(attribute_table_csvfile_name)

    # Select Vertices Attribute Table csv File (.csv)
    vertices_attribute_csvfile_name                     = r"C:\GISTDA\Solarcells_Project\Solar_Efficiency_Analysis_Program3\Attribute_Table_Data\Building_Attribute_Table_LOD200_Vertices_Draft2.3.csv"
    # Read Vertices Attribute Table csv File
    vertices_attribute_df                               = pd.read_csv(vertices_attribute_csvfile_name, usecols=['uid', 'heightmax', 'rooftop', 'rooftype', 'area', 'vertex_index', 'distance', 'lat', 'long'])
   
    # Select Point DEM Attribute Table csv File (.csv)
    point_dem_gov_building_csvfile_name                 = r"C:\GISTDA\Solarcells_Project\Solar_Efficiency_Analysis_Program3\Attribute_Table_Data\Point_dem.csv"
    # Read Point DEM Gov Building Table csv File
    point_dem_gov_building_df                           = pd.read_csv(point_dem_gov_building_csvfile_name, usecols=['uid','DEM'])

    # Setup file location for output files
    # Global Solar Irradiance Geometry Output File Location
    global_solar_irradiance_geometry_csvfile_location   = r"C:\GISTDA\Solarcells_Project\Solar_Efficiency_Analysis_Program3\Phase3.1_CalResult_Solar_Efficiency\GOV_Building_Solar_Radiation_Geometry_Data"
    # Global Shading Factor Output File Location
    global_shading_factor_csvfile_location              = r"C:\GISTDA\Solarcells_Project\Solar_Efficiency_Analysis_Program3\Phase3.1_CalResult_Solar_Efficiency\GOV_Building_Shading_Factor_Data"

    # Global Solar Transimttance Coefficient Output File Location
    global_transmittance_coeff_csvfile_location         = r"C:\GISTDA\Solarcells_Project\Solar_Efficiency_Analysis_Program3\Phase3.1_CalResult_Solar_Efficiency\GOV_Building_Transmittance_Coefficient_Data"
    
    # Global Solar Irradiance Analysis Output File Location
    global_solar_irradiance_csvfile_location            = r"C:\GISTDA\Solarcells_Project\Solar_Efficiency_Analysis_Program3\Phase3.1_CalResult_Solar_Efficiency\GOV_Building_Solar_Irradiance_Data"
    global_solar_irradiation_csvfile_location           = r"C:\GISTDA\Solarcells_Project\Solar_Efficiency_Analysis_Program3\Phase3.1_CalResult_Solar_Efficiency\GOV_Building_Solar_Irradiation_Data"
    
    # Global Analysis For All Building in Desired Calculation Area File Location
    global_solar_irradiance_analysis_csvfile_location   = r"C:\GISTDA\Solarcells_Project\Solar_Efficiency_Analysis_Program3\Phase3.1_CalResult_Solar_Efficiency\Solar_Irradiance_Data"
    global_solar_irradiation_analysis_csvfile_location  = r"C:\GISTDA\Solarcells_Project\Solar_Efficiency_Analysis_Program3\Phase3.1_CalResult_Solar_Efficiency\Solar_Irradiation_Data"
    global_shading_factor_analysis_csvfile_location     = r"C:\GISTDA\Solarcells_Project\Solar_Efficiency_Analysis_Program3\Phase3.1_CalResult_Solar_Efficiency\Shading_Factor_Data"
    
    global_solar_analysis_csvfile_location = r"C:\GISTDA\Solarcells_Project\Solar_Efficiency_Analysis_Program3\Phase3.1_CalResult_Solar_Efficiency\Solar_Analysis_Data"
    
    # Parameters and Data
    start_time                  = 5   # Start solar irradiance calculation time is 05.00 a.m.
    stop_time                   = 18  # Stop solar irradiance calculation time is 18.00 p.m.
    steps                       = 15  # Step 10 minutes for calculation results
    desired_interval_steps      = 30  # Step 30 minutes for analysis results

    std_longitude               = 105        # Bangkok UTC longitude (Ubon Ratchathani)
    angstrom_turbidity          = 0.138      # Mean Angstrom's Turbidity at KhonKaen over year
    saturated_vapor_pressure    = 99.084     # Kilo Pascals
    relative_humidity           = 0.000182
    ambient_temperature         = 292        # Kilo Pascals
    ozone_layer_thickness       = 260        # Centimeters
    barometric_pressure         = 990
    angstrom_turbidity          = 0.138


    # Calculation of Rooftop Geometry
    global_rooftop_geometry_df = solar_irradiance_geometry_program.rooftop_geometry_function(attribute_table_csv_df, vertices_attribute_df)
    
    # Julian Date Data Frame
    julian_date_df          = solar_irradiance_geometry_program.date_function()
    local_standard_time_df  = pd.DataFrame([list(hour_time+(minute_time/60) for hour_time in range(start_time,stop_time+1) for minute_time in range(0,60,steps))]*julian_date_df.shape[0]).round(6)
    
    #"""
    n = 0
    uid = attribute_table_csv_df.loc[0, 'uid']
    #uid = '2D264B6CA65169B5-41-0'
    #for uid in attribute_table_csv_df['uid']:
    n+=1
    print('\n----------------------------------------------------------------------------------',
        f'\nno.{n} uid: {uid}')

    # Solar Irradiance Geometry Calculation Function:
    # Input dedrived data Function:
    building_fields_table_df                                = input_data_program.input_dedrived_data(attribute_table_csvfile_name, uid)
    print(building_fields_table_df)
    # Processing Solar Irradiance Geometry Parameters:
    date_field_df, solar_hour_angle_df, altitude_angle_df, azimuth_angle_df, zenith_angle_df = solar_irradiance_geometry_program.solar_irradiance_geometry_function(uid, building_fields_table_df, julian_date_df, local_standard_time_df, global_rooftop_geometry_df, global_solar_irradiance_geometry_csvfile_location, steps, std_longitude, start_time, stop_time)
    
    uid_building_digital_elevation_model_height             = point_dem_gov_building_df.loc[point_dem_gov_building_df['uid']==uid, 'DEM'].values[0]
    
    # Shading Angle Geometry Calculation Function:
    # Processing Shading Factor
    shading_factor_df                                       = shading_factor_program.shading_geometry_function(uid, attribute_table_csv_df, global_shading_factor_csvfile_location, building_fields_table_df, global_rooftop_geometry_df, uid_building_digital_elevation_model_height, point_dem_gov_building_df, date_field_df, altitude_angle_df, azimuth_angle_df, steps, start_time, stop_time)

    # Transmittance Coefficient Calculation Function:
    global_transmittance_coeff_df_list                      = transmittance_coefficient_program.transmittance_coeff_calculation_function(uid, building_fields_table_df, date_field_df, julian_date_df, zenith_angle_df, global_transmittance_coeff_csvfile_location, steps, uid_building_digital_elevation_model_height, angstrom_turbidity, saturated_vapor_pressure, relative_humidity, ambient_temperature, ozone_layer_thickness, start_time, stop_time)

    # Processing Solar Irradiation And Irradiance
    global_solar_irradiance_df, global_solar_irradiation_df = solar_irradiance_and_irradiation_program.global_solar_irradiance_calculation_function(uid, building_fields_table_df, date_field_df, global_rooftop_geometry_df, solar_hour_angle_df, azimuth_angle_df, altitude_angle_df, shading_factor_df, global_transmittance_coeff_df_list, global_solar_irradiance_csvfile_location, global_solar_irradiation_csvfile_location, steps, barometric_pressure, angstrom_turbidity, start_time, stop_time)
    
    #"""
    
    # Preparing Data for Qgis
    #solar_irradiance_and_irradiation_program.loading_and_prepareing_data_for_qgis341(attribute_table_csvfile_name, global_solar_irradiance_csvfile_location, global_solar_irradiation_csvfile_location, global_solar_analysis_csvfile_location, steps, start_time, stop_time)
    solar_irradiance_and_irradiation_program.loading_and_prepareing_data_for_qgis331(attribute_table_csvfile_name, date_field_df, global_solar_irradiance_csvfile_location, global_solar_irradiation_csvfile_location, global_shading_factor_csvfile_location, global_solar_irradiance_analysis_csvfile_location, global_solar_irradiation_analysis_csvfile_location, global_shading_factor_analysis_csvfile_location, steps, desired_interval_steps, start_time, stop_time)

solar_efficiency_analysis_program_function()

