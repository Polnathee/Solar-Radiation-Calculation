import pandas as pd
import csv

import Phase1_Solar_Efficiency_Analysis_Program.HourAngleCal as HourAngleCal

fn = r"C:/GISTDA/Solarcells_Project/Data/TestData/Set2_QGIS_Data/FlatRoof2_SolarInsolation/Pl1_20231210_Gov_buildings_LOD2_att_geo.shp"

gov_building_solar_irradiance_csvfile_name = r"C:\GISTDA\Solarcells_Project\Solar_Efficiency_Analysis_Program2.1\Test_CSV\Building_Solar_Analysis_uid_32430B6CA65169B5-147-0.csv"

layer = iface.addVectorLayer(fn, 'Test22','ogr')
# layer = QgsVectorLayer(fn, '','ogr')
pv = layer.dataProvider()
caps = layer.dataProvider().capabilities()

# for field in layer.fields():
#     print(field.name())
# layer.startEditing()

gov_building_irradiance_df = pd.read_csv(gov_building_solar_irradiance_csvfile_name)

sunrise_local_time = (gov_building_irradiance_df['Local Sunrise Time'].max())
sunset_local_time  = (gov_building_irradiance_df['Local Sunset Time'].min())

global_sunrise_local_time_list = []
global_sunrise_local_time_list.append(sunrise_local_time)
global_sunset_local_time_list = []
global_sunset_local_time_list.append(sunset_local_time)

steps = 10

global_sunrise_local_time = max(global_sunrise_local_time_list)
global_sunset_local_time = min(global_sunset_local_time_list)

start_time = int(global_sunrise_local_time)
stop_time  = int(global_sunset_local_time)

with edit(layer):
    for julian_date in range (1,2):
        for hour in range (start_time, stop_time+1):
            if hour < 10:
                hour_time = "0"+str(hour)
            else:
                hour_time = str(hour)
                
            if caps & QgsVectorDataProvider.AddAttributes:
                res = layer.dataProvider().addAttributes([QgsField(f'{hour_time}', QVariant.Double)])
                layer.updateFields()
    
    for feature in layer.getFeatures():
        for julian_date in range (1,2):
            for hour in range (start_time, stop_time+1):
                if hour < 10:
                    hour_time = "0"+str(hour)
                else:
                    hour_time = str(hour)
                    
                direct_hourly_irradiance = gov_building_irradiance_df.loc[julian_date, f"Hourly Direct Normal Irradiance-{hour_time}:00"]
                diffuse_hourly_irradiance = gov_building_irradiance_df.loc[julian_date, f"Hourly Diffuse Irradiance-{hour_time}:00"]
                
                total_hourly_irradiance = direct_hourly_irradiance + diffuse_hourly_irradiance
                
                feature.setAttribute(f'{hour_time}', total_hourly_irradiance)
                
                layer.updateFeature(feature)

    


