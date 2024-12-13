import pandas as pd
import csv

import Phase1_Solar_Efficiency_Analysis_Program.HourAngleCal as HourAngleCal
import SolarInsolationCal as insolation

fn = r'C:/Nay/SolarCells_Project/Data/TestData/Set2_QGIS_Data/FlatRoof2_SolarInsolation/Pl1_20231210_Gov_buildings_LOD2_att_geo.shp'

layer = QgsVectorLayer(fn, '','ogr')
pv = layer.dataProvider()

# for field in layer.fields():
#     print(field.name())
decli_csv = r"C:\Nay\SolarCells_Project\Data\TestData\Set2_QGIS_Data\FlatRoof2_SolarInsolation\FlatRoof_Declination\FlatRoof2_Declination.csv"
hra_csv = r"C:\Nay\SolarCells_Project\Data\TestData\Set2_QGIS_Data\FlatRoof2_SolarInsolation\FlatRoof_HRA\FlatRoof2_D1HRA.csv"
zenith_csv = r"C:\Nay\SolarCells_Project\Data\TestData\Set2_QGIS_Data\FlatRoof2_SolarInsolation\FlatRoof2_ZenithAngle\FlatRoof2_D1ZenithAngle.csv"
#DHI_csv = r"C:\Nay\SolarCells_Project\Data\TestData\Set2_QGIS_Data\FlatRoof2_SolarInsolation\FlatRoof2_SolarEnergy\FlatRoof2_SolarEnergyD1.csv"

# reading the csv file: FlatRoof2_D1HRA
df_hra = pd.read_csv(hra_csv)

day = 1
step = 30

min_rise_hra = df_hra['Sunrise HRA'].min()
max_set_hra = df_hra['Sunset HRA'].max()
# min_rise_hra = 6
# max_set_hra = 18

start_time = HourAngleCal.hra2st(min_rise_hra)
stop_time = HourAngleCal.hra2st(max_set_hra)

with edit (layer):
    for d in range(day, day+1):
        # reading the csv file: FlatRoof2_Declination
        df_decli = pd.read_csv(decli_csv)
        dn = day-1
        dDelta = df_decli.loc[dn, 'Declination']
        # print(f'Index: {dn}, Declination: {dDelta}')
        for h in range(start_time, stop_time+1, 1):
            for m in range(0, 60, step):
                for f in layer.getFeatures():
                    uid = f[0]
                    # print(f'uid: {uid}')
                    
                    lat = f[20]
                    # print(f'latitude: {lat}')
                    
                    # find uid in csv file: FlatRoof2_SolarInsolationD1
                    desired_row = df_hra[df_hra['uid'] == f'{uid}']
                    n = desired_row.index[0]
                    # print(f'index: {n}')
                    
                    if m == 0:
                        hra1 = df_hra.loc[n,f'D{d},T{h}:{m}']
                        hra2 = df_hra.loc[n,f'D{d},T{h}:30']
                    elif m == 30:
                        hra1 = df_hra.loc[n,f'D{d},T{h}:{m}']
                        hra2 = df_hra.loc[n,f'D{d},T{h+1}:0']
                    
                    # print(f'hra1: {hra1}, hra2: {hra2}')

                    # Power Factor, KW/m^2/h
                    power_factor = 60/step

                    # DirectNormalIrradiance_function(day, dDelta, lat, hra1, hra2)
                    # i_o, zenith_angle = insolation.normal_solarInsolation_function(day, dDelta, lat, hra1, hra2)
                    # i_o = (i_o) * (power_factor)

                    # DiffuseHorizontalIrradiance_function(day, dDelta, lat, hra1, hra2)
                    i_d = insolation.diffuse_solarInsolation_function(day, dDelta, lat, hra1, hra2)
                    i_d = (i_d) * (power_factor)

                    # Global Horizontal Irradiance (GHI)
                    # i = i_o + i_d

                    # reading the csv file: FlatRoof2_SolarEnergyD1
                    df_solarEner = pd.read_csv(DHI_csv)
                    # updating the solarEner csv file
                    if h==start_time and m==0:
                        df_solarEner.loc[n, 'uid'] = uid
                        if i_d <= 0 :
                            df_solarEner.loc[n, f'D{d},T{h}:0'] = 0
                            df_solarEner.loc[n, f'D{d},T{h}:30'] = 0
                        else:
                            df_solarEner.loc[n, f'D{d},T{h}:30'] = i_d
                    else:
                        if uid == df_hra.loc[n,'uid']:
                            if m==30:
                                df_solarEner.loc[n, f'D{d},T{h+1}:0'] = i_d
                            elif m==0:
                                df_solarEner.loc[n, f'D{d},T{h}:30'] = i_d
                    # writing into the file
                    df_solarEner.to_csv(DHI_csv, index=False)


