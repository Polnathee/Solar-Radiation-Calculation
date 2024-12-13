import pandas as pd
import csv

import Phase1_Solar_Efficiency_Analysis_Program.HourAngleCal as HourAngleCal
import Phase1_Solar_Efficiency_Analysis_Program.SolarInsolationCal as insolation

fn = r"C:/GISTDA/Solarcells_Project/Data/TestData/Set2_QGIS_Data/FlatRoof2_SolarInsolation/Pl1_20231210_Gov_buildings_LOD2_att_geo.shp"

layer = QgsVectorLayer(fn, '','ogr')
pv = layer.dataProvider()

# for field in layer.fields():
#     print(field.name())

decli_csv         = r"C:\GISTDA\Solarcells_Project\Data\TestData\Set2_QGIS_Data\FlatRoof2_SolarInsolation\FlatRoof_Declination\FlatRoof2_Declination.csv"
hra_csv           = r"C:\GISTDA\Solarcells_Project\Data\TestData\Set2_QGIS_Data\FlatRoof2_SolarInsolation\FlatRoof_HRA\FlatRoof2_D261HRA.csv"
zenith_csv        = r"C:\GISTDA\Solarcells_Project\Data\TestData\Set2_QGIS_Data\FlatRoof2_SolarInsolation\FlatRoof2_ZenithAngle\FlatRoof2_D261ZenithAngle.csv"
DNI_csv           = r"C:\GISTDA\Solarcells_Project\Data\TestData\Set2_QGIS_Data\FlatRoof2_SolarInsolation\FlatRoof2_SolarEnergy\FlatRoof2_SolarEnergyD261\FlatRoof2_DNI_D261.csv"
FR_insolation_csv = r"C:\GISTDA\Solarcells_Project\Data\TestData\Set2_QGIS_Data\FlatRoof2_SolarInsolation\FlatRoof2_SolarEnergy\FlatRoof2_SolarEnergyD261\FlatRoof2_GlobalInsolation_D261.csv"

# reading the csv file: FlatRoof2_D1HRA
df_hra = pd.read_csv(hra_csv)

day = 261
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
        for f in layer.getFeatures():
            for h in range(start_time, stop_time+1, 1):
                for m in range(0, 60, step):
                    uid = f[0]
                    #print(f'uid: {uid}')
                    
                    lat = f[20]
                    # print(f'latitude: {lat}')
                    
                    # find uid in csv file: FlatRoof2_SolarInsolationD1
                    desired_row = df_hra[df_hra['uid'] == f'{uid}']
                    n = desired_row.index[0]
                    print(f'index: {n}')
                    
                    if m == 0 & h <= stop_time:
                        hra1 = df_hra.loc[n,f'D{d},T{h}:{m}']
                        hra2 = df_hra.loc[n,f'D{d},T{h}:30']
                    elif m == 30 & h < stop_time:
                        hra1 = df_hra.loc[n,f'D{d},T{h}:{m}']
                        hra2 = df_hra.loc[n,f'D{d},T{h+1}:0']
                    elif m == 0 & h >= stop_time:
                        hra1 = df_hra.loc[n,f'D{d},T{h}:{m}']
                        hra2 = df_hra.loc[n,f'D{d},T{h}:30']
                    elif m == 30 & h >= stop_time:
                        hra1 = max_set_hra
                        hra2 = max_set_hra
                        
                    # print(f'hra1: {hra1}, hra2: {hra2}')

                    # DirectNormalIrradiance_function(day, dDelta, lat, hra1, hra2)
                    i_o, ir_o, zenith_angle = insolation.normal_solarInsolation_function(day, dDelta, lat, hra1, hra2, step)

                    ### Global Horizontal Irradiance (GHI) ###
                    # FlatRoof: GHI = DNI (Direct Normal Irradiance)

                    # reading the csv file: FlatRoof2_SolarEnergyD1
                    df_DNI = pd.read_csv(DNI_csv)
                    # updating the solarEner csv file
                    if h==start_time and m==0:
                        df_DNI.loc[n, 'uid'] = uid
                        if ir_o <= 0 :
                            df_DNI.loc[n, f'D{d},T{h}:0'] = 0
                            df_DNI.loc[n, f'D{d},T{h}:30'] = 0
                        else:
                            df_DNI.loc[n, f'D{d},T{h}:30'] = ir_o
                    else:
                        if uid == df_insol.loc[n,'uid']:
                            if m==30:
                                df_DNI.loc[n, f'D{d},T{h+1}:0'] = ir_o
                            elif m==0:
                                df_DNI.loc[n, f'D{d},T{h}:30'] = ir_o
                    # writing into the file
                    df_DNI.to_csv(DNI_csv, index=False)


                    ### Global Insolation (surface) ###
                    # reading the csv file: FlatRoof2_SolarEnergyD1
                    df_insol = pd.read_csv(FR_insolation_csv)
                    # updating the solarEner csv file
                    if h==start_time and m==0:
                        df_insol.loc[n, 'uid'] = uid
                        if ir_o <= 0 :
                            df_insol.loc[n, f'D{d},T{h}:0'] = 0
                            df_insol.loc[n, f'D{d},T{h}:30'] = 0
                        else:
                            df_insol.loc[n, f'D{d},T{h}:30'] = i_o
                    else:
                        if uid == df_insol.loc[n,'uid']:
                            if m==30:
                                df_insol.loc[n, f'D{d},T{h+1}:0'] = i_o
                            elif m==0:
                                df_insol.loc[n, f'D{d},T{h}:30'] = i_o
                    # writing into the file
                    df_insol.to_csv(FR_insolation_csv, index=False)


                    # reading the csv file: FlatRoof2_ZenithAngle
                    df_zenith = pd.read_csv(zenith_csv)
                    # updating the Zenith Angle csv file
                    if h==0 and m==0:
                        df_zenith.loc[n, 'uid'] = uid
                        df_zenith.loc[n, f'D{d},T{h}:{m}'] = zenith_angle
                    else:
                        if uid == df_zenith.loc[n, 'uid']:
                            df_zenith.loc[n, f'D{d},T{h}:{m}'] = zenith_angle
                    # writing into the file
                    df_zenith.to_csv(zenith_csv, index=False)


