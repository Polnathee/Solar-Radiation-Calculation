import pandas as pd
import csv

import Phase1_Solar_Efficiency_Analysis_Program.EarthDeclinationCal as declination

fn = r'C:/Nay/SolarCells_Project/Data/TestData/Set2_QGIS_Data/FlatRoof2_SolarInsolation/Pl1_20231210_Gov_buildings_LOD2_att_geo.shp'

layer = QgsVectorLayer(fn, '', 'org')
pv = layer.dataProvider()

for field in layer.fields():
    print(field.name())

day = 365

for d in range (1, day+1):
    #print(f'Day: {d + 1}')
    n = d-1
    
    # Earth Declination Calculation
    dDelta = declination.declination_function(d)
    # dDelta = declination.Rad2Deg(dDelta)
    print(f'Day: {d}, Declination: {dDelta}')
    
    # reading the csv file 
    df = pd.read_csv(r"C:\Nay\SolarCells_Project\Data\TestData\Set2_QGIS_Data\FlatRoof2_SolarInsolation\FlatRoof_Declination\FlatRoof2_Declination.csv")
    
    #updating the column value/data
    df.loc[n, 'Day'] = d
    df.loc[n, 'Declination'] = dDelta

    # writing into the file
    df.to_csv(r"C:\Nay\SolarCells_Project\Data\TestData\Set2_QGIS_Data\FlatRoof2_SolarInsolation\FlatRoof_Declination\FlatRoof2_Declination.csv", index=False)
    