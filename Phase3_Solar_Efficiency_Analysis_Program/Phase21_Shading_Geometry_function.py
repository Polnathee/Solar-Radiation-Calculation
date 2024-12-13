import math

import csv
import numpy as np
import pandas as pd

def Deg2Rad(deg):
    return deg * (math.pi / 180)
    
def Rad2Deg(rad):
    return rad * (180 / math.pi)

uid_building_latitude = 16.348
uid_building_longitude = 102.839

shading_calculation_radius = 5
latitude_interval = shading_calculation_radius
longitude_interval = shading_calculation_radius

# Coordinate Plane (Quadrant1-4)
coordinate_plane_list       = list(range(-latitude_interval,(latitude_interval+1),1) for x in range (-longitude_interval,(longitude_interval+1),1))
coordinate_plane_list       = zip(*coordinate_plane_list)
coordinate_plane_df         = pd.DataFrame(coordinate_plane_list)
coordinate_plane_df         = pd.DataFrame(np.where(coordinate_plane_df==0, 1, coordinate_plane_df))
coordinate_plane_df.columns = list(range(-latitude_interval,latitude_interval+1,1))
coordinate_plane_df         = coordinate_plane_df.set_index([pd.Index(list(range(-latitude_interval,latitude_interval+1,1)))])

# Filter only Latitude that is feasible with calculation radius
coordinate_plane_df         = pd.DataFrame(np.where(abs(coordinate_plane_df)<(((latitude_interval**2)-(coordinate_plane_df.columns**2))**(1/2)), coordinate_plane_df, 0))
coordinate_plane_df.columns = list(range(-longitude_interval,longitude_interval+1,1))

azimuth = 45 # Degree
azimuth_upper_bound = azimuth+15
azimuth_lower_bound = azimuth-15
if azimuth_upper_bound >360:
    azimuth_upper_bound = azimuth_upper_bound - 360
if azimuth_lower_bound < 0:
    azimuth_lower_bound = azimuth_lower_bound + 360
azimuth_upper_bound_factor = math.tan(Deg2Rad(azimuth_upper_bound))
azimuth_lower_bound_factor = math.tan(Deg2Rad(azimuth_lower_bound))
#print(f"Condition1: {(90>azimuth_upper_bound>=0 or 360>=azimuth_upper_bound>270) and (90>azimuth_lower_bound>=0 or 360>=azimuth_lower_bound>270)}")
#print(f"Condition2: {270>azimuth_upper_bound>90 and 270>azimuth_lower_bound>90}")
#print(f"Condition3: {azimuth_upper_bound>=90 and azimuth_lower_bound<=90}")
#print(f"Condition4: {azimuth_upper_bound>=270 and azimuth_lower_bound<=270}")
if (90>azimuth_upper_bound>=0 or 360>=azimuth_upper_bound>270) and (90>azimuth_lower_bound>=0 or 360>=azimuth_lower_bound>270):
    print("Condition 1")
    coordinate_plane_df         = pd.DataFrame(np.where(coordinate_plane_df <= ((coordinate_plane_df.columns)*(azimuth_upper_bound_factor)), coordinate_plane_df, 0))
    coordinate_plane_df.columns = list(range(-latitude_interval,latitude_interval+1,1))
    coordinate_plane_df         = pd.DataFrame(np.where(coordinate_plane_df >= ((coordinate_plane_df.columns)*(azimuth_lower_bound_factor)), coordinate_plane_df, 0))
    coordinate_plane_df.columns = list(range(-latitude_interval,latitude_interval+1,1)) 
elif 270>azimuth_upper_bound>90 and 270>azimuth_lower_bound>90:
    print("Condition 2")
    coordinate_plane_df         = pd.DataFrame(np.where(coordinate_plane_df >= ((coordinate_plane_df.columns)*(azimuth_upper_bound_factor)), coordinate_plane_df, 0))
    coordinate_plane_df.columns = list(range(-latitude_interval,latitude_interval+1,1))
    coordinate_plane_df         = pd.DataFrame(np.where(coordinate_plane_df <= ((coordinate_plane_df.columns)*(azimuth_lower_bound_factor)), coordinate_plane_df, 0))
    coordinate_plane_df.columns = list(range(-latitude_interval,latitude_interval+1,1))
elif azimuth_upper_bound>=90 and azimuth_lower_bound<=90:
    print("Condition 3")
    if azimuth_upper_bound == 90:
        coordinate_plane_df = pd.DataFrame(np.where(coordinate_plane_df <= ((coordinate_plane_df.columns)*(azimuth_upper_bound_factor)), coordinate_plane_df, 0))
        coordinate_plane_df.columns = list(range(-latitude_interval,latitude_interval+1,1))
        coordinate_plane_df = pd.DataFrame(np.where(coordinate_plane_df >= ((coordinate_plane_df.columns)*(azimuth_lower_bound_factor)), coordinate_plane_df, 0))
        coordinate_plane_df.columns = list(range(-latitude_interval,latitude_interval+1,1))
    else:
        coordinate_plane_df = pd.DataFrame(np.where(coordinate_plane_df >= ((coordinate_plane_df.columns)*(azimuth_upper_bound_factor)), coordinate_plane_df, 0))
        coordinate_plane_df.columns = list(range(-latitude_interval,latitude_interval+1,1))
        coordinate_plane_df = pd.DataFrame(np.where(coordinate_plane_df >= ((coordinate_plane_df.columns)*(azimuth_lower_bound_factor)), coordinate_plane_df, 0))
        coordinate_plane_df.columns = list(range(-latitude_interval,latitude_interval+1,1))
elif azimuth_upper_bound>=270 and azimuth_lower_bound<=270:
    print("Condition 4")
    if azimuth_upper_bound == 270:
        coordinate_plane_df = pd.DataFrame(np.where(coordinate_plane_df >= ((coordinate_plane_df.columns)*(azimuth_upper_bound_factor)), coordinate_plane_df, 0))
        coordinate_plane_df.columns = list(range(-latitude_interval,latitude_interval+1,1))
        coordinate_plane_df = pd.DataFrame(np.where(coordinate_plane_df <= ((coordinate_plane_df.columns)*(azimuth_lower_bound_factor)), coordinate_plane_df, 0))
        coordinate_plane_df.columns = list(range(-latitude_interval,latitude_interval+1,1))
    else:
        coordinate_plane_df = pd.DataFrame(np.where(coordinate_plane_df <= ((coordinate_plane_df.columns)*(azimuth_upper_bound_factor)), coordinate_plane_df, 0))
        coordinate_plane_df.columns = list(range(-latitude_interval,latitude_interval+1,1))
        coordinate_plane_df = pd.DataFrame(np.where(coordinate_plane_df <= ((coordinate_plane_df.columns)*(azimuth_lower_bound_factor)), coordinate_plane_df, 0))
        coordinate_plane_df.columns = list(range(-latitude_interval,latitude_interval+1,1))

#print(coordinate_plane_df)
coordinate_plane_df = pd.DataFrame(np.where(coordinate_plane_df != 0, (coordinate_plane_df/1000)+uid_building_latitude, 0))
#new_coordinate_plane_df = coordinate_plane_df.stack().reset_index()

coordinate_plane_column_df = (pd.DataFrame(list(range(-longitude_interval,(longitude_interval+1),1)))/10000)+uid_building_longitude
coordinate_plane_column_df = coordinate_plane_column_df.transpose()
coordinate_plane_column_list = coordinate_plane_column_df.values.tolist()
coordinate_plane_df.columns = coordinate_plane_column_list[0]

coordinate_plane_df = coordinate_plane_df.set_index([pd.Index(list(range(-latitude_interval,latitude_interval+1,1)))])
coordinate_plane_df = coordinate_plane_df.sort_index(ascending=False)
print(coordinate_plane_df,"\n")

new_coordinate_plane_df = coordinate_plane_df
new_coordinate_plane_df = new_coordinate_plane_df.stack().reset_index()
new_coordinate_plane_filter = (new_coordinate_plane_df[0]!=0)
new_coordinate_plane_df = new_coordinate_plane_df[new_coordinate_plane_filter]

print("200",new_coordinate_plane_df,"\n")


