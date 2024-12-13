import pandas as pd
import csv

import Phase1_Solar_Efficiency_Analysis_Program.HourAngleCal as HourAngleCal

fn = r"C:/GISTDA/Solarcells_Project/Data/TestData/Set2_QGIS_Data/FlatRoof2_SolarInsolation/Pl1_20231210_Gov_buildings_LOD2_att_geo.shp"

layer = QgsVectorLayer(fn, '','ogr')
pv = layer.dataProvider()

# for field in layer.fields():
#     print(field.name())

day = 261
TZ = 7.0
n = 0

hra_csv = r"C:\GISTDA\Solarcells_Project\Data\TestData\Set2_QGIS_Data\FlatRoof2_SolarInsolation\FlatRoof_HRA\FlatRoof2_D261HRA.csv"
decli_csv = r"C:\GISTDA\Solarcells_Project\Data\TestData\Set2_QGIS_Data\FlatRoof2_SolarInsolation\FlatRoof_Declination\FlatRoof2_Declination.csv"

with edit (layer):
    # reading the declination csv file:
    df_decli = pd.read_csv(decli_csv)
    dDelta =  df_decli.loc[day-1,f'Declination']
    for f in layer.getFeatures():
        # reading the csv file 
        df = pd.read_csv(hra_csv)
        
        uid = f[0]
        lad = f[20]
        rise_hra = HourAngleCal.rise_hra_function(dDelta, lad)

        #updating the column value/data
        df.loc[n, 'uid'] = uid
        
        if uid == df.loc[n,'uid']:
                df.loc[n, 'Sunrise HRA'] = -(rise_hra)
                df.loc[n, 'Sunset HRA']  = (rise_hra)
        # writing into the file
        df.to_csv(hra_csv, index=False)
        
        n+=1
        layer.updateFeature(f)


# finding min sunrise hra and max sunset hra
df = pd.read_csv(hra_csv)
min_rise_hra = df['Sunrise HRA'].min()
max_set_hra = df['Sunset HRA'].max()

start_time = HourAngleCal.hra2st(min_rise_hra)
stop_time = HourAngleCal.hra2st(max_set_hra)

# start_time = 6
# stop_time = 18

with edit (layer):
    for d in range (day, day+1):
        # print(f'Day: {d + 1}')
                n=0
                for f in layer.getFeatures():
                    
                    for h in range (start_time, stop_time+1, 1):
                        # print(f'time: {t}')
                        for m in range (0, 60, 30):
                            t = h + (m/60)
                    
                            uid = f[0]
                            long = f[21]
                        
                            hra = HourAngleCal.solarHourAngle_function(d, t, long, TZ)
                            
                            # reading the csv file 
                            df = pd.read_csv(hra_csv)
                            #updating the column value/data
                            if t>0:
                                if uid == df.loc[n,'uid']:
                                    df.loc[n, f'D{d},T{h}:{m}'] = hra
                            else:
                                df.loc[n, f'D{d},T{h}:{m}'] = hra
                            # writing into the file
                            df.to_csv(hra_csv, index=False)

                            layer.updateFeature(f)
                            
                    n+=1
