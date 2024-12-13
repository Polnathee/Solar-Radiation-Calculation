import numpy as np

def Deg2Rad(deg):
    return deg * (np.pi / 180)
    
def Rad2Deg(rad):
    return rad * (180 / np.pi)


earth_radius  = 6373.0 # Kilometers

uid_building_latitude1 = 16.4421
uid_building_longitude1 = 102.84

uid_building_latitude2 = 16.4414
uid_building_longitude2 = 102.834




difference_longitude_df = Deg2Rad(uid_building_longitude2 - uid_building_longitude1)
difference_latitude_df  = Deg2Rad(uid_building_latitude2 - uid_building_latitude1)
print("difference long: ", difference_longitude_df)
print("difference lat: ", difference_latitude_df)
a = (np.sin(difference_latitude_df/2))**2 + np.cos(Deg2Rad(uid_building_latitude1)) * np.cos(Deg2Rad(uid_building_latitude2)) * (np.sin(difference_longitude_df/2))**2
c = 2 * np.atan2(np.sqrt(a), np.sqrt(1-a))
distance_series = earth_radius * c * 1000

print(distance_series)
