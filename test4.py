import csv
import numpy as np
import pandas as pd
import geopandas as pgd

import pandas as pd
from geopy.distance import geodesic
from itertools import combinations
import multiprocessing as mp

from multiprocessing import Pool

def Deg2Rad(deg):
    return deg * (np.pi / 180)
    
def Rad2Deg(rad):
    return rad * (180 / np.pi)

def test41():
    sun_azimuth_angle = pd.DataFrame([30,45])
    radius_of_shading_calculation = 2 # 0.050 degree of latitude and longitude
    horizontal_angle_interval_of_shading_calculation = 7.5 # +-7.5 degree of horizontal plane angle
    latitude_interval             = radius_of_shading_calculation
    longitude_interval            = radius_of_shading_calculation

    coordinate_plane_list                        = list(range(-latitude_interval,(latitude_interval+1),1) for x in range (-longitude_interval,(longitude_interval+1),1))
    coordinate_plane_list                        = zip(*coordinate_plane_list)
    feasible_shading_coordinate_plane_df         = pd.DataFrame(coordinate_plane_list)
    feasible_shading_coordinate_plane_df         = pd.DataFrame(np.where(feasible_shading_coordinate_plane_df==0, 1, feasible_shading_coordinate_plane_df))
    feasible_shading_coordinate_plane_df.columns = list(range(-latitude_interval,latitude_interval+1,1))
    feasible_shading_coordinate_plane_df         = feasible_shading_coordinate_plane_df.set_index([pd.Index(list(range(-latitude_interval,latitude_interval+1,1)))])
    print("\nData Frame1\n",feasible_shading_coordinate_plane_df)

    feasible_shading_coordinate_plane_df         = pd.DataFrame(np.where(abs(feasible_shading_coordinate_plane_df)<(((latitude_interval**2)-(feasible_shading_coordinate_plane_df.columns**2))**(1/2)), feasible_shading_coordinate_plane_df, 0))
    feasible_shading_coordinate_plane_df.columns = list(range(-longitude_interval,longitude_interval+1,1))

    # Computing uid Building Azimuth Angle
    azimuth_angle_upper_bound = sun_azimuth_angle + horizontal_angle_interval_of_shading_calculation
    azimuth_angle_lower_bound = sun_azimuth_angle - horizontal_angle_interval_of_shading_calculation
    print('Upper Bound', azimuth_angle_upper_bound)
    azimuth_angle_upper_bound_df = pd.DataFrame(np.where(azimuth_angle_upper_bound>360, azimuth_angle_upper_bound-360, azimuth_angle_upper_bound))
    azimuth_angle_lower_bound_df = pd.DataFrame(np.where(azimuth_angle_lower_bound<0, azimuth_angle_lower_bound+360, azimuth_angle_lower_bound))
    azimuth_angle_upper_bound_factor = np.tan(Deg2Rad(azimuth_angle_upper_bound))
    azimuth_angle_lower_bound_factor = np.tan(Deg2Rad(azimuth_angle_lower_bound))
    print('Upper Bound Factor', azimuth_angle_upper_bound_factor)

    global_feasible_shading_coordinate_plane_df = pd.DataFrame([[feasible_shading_coordinate_plane_df],[feasible_shading_coordinate_plane_df]])

    global_feasible_shading_coordinate_plane_df = pd.DataFrame(np.where(global_feasible_shading_coordinate_plane_df.iloc[0,:]>0,5,9))

    '''
    def condition1(feasible_shading_coordinate_plane_df, azimuth_angle_upper_bound_factor, azimuth_angle_lower_bound_factor):
        feasible_shading_coordinate_plane_df             = pd.DataFrame(np.where(feasible_shading_coordinate_plane_df <= ((feasible_shading_coordinate_plane_df.columns)*(azimuth_angle_upper_bound_factor)), feasible_shading_coordinate_plane_df, 0))
        feasible_shading_coordinate_plane_df.columns     = list(range(-latitude_interval,latitude_interval+1,1))
        feasible_shading_coordinate_plane_df             = pd.DataFrame(np.where(feasible_shading_coordinate_plane_df >= ((feasible_shading_coordinate_plane_df.columns)*(azimuth_angle_lower_bound_factor)), feasible_shading_coordinate_plane_df, 0))
        feasible_shading_coordinate_plane_df.columns     = list(range(-latitude_interval,latitude_interval+1,1)) 


    if (90>azimuth_angle_upper_bound>=0 or 360>=azimuth_angle_upper_bound>270) and (90>azimuth_angle_lower_bound>=0 or 360>=azimuth_angle_lower_bound>270):
    '''


    #print([[feasible_shading_coordinate_plane_df]], "\n")
    print("\nGlobal Data Frame\n",global_feasible_shading_coordinate_plane_df)

    print('\nGlobal Data Frame[0,0]\n',global_feasible_shading_coordinate_plane_df.iloc[0,0])

def test42():
    arrays = [
        np.array(["bar", "bar", "baz", "baz", "foo", "foo", "qux", "qux"]),
        np.array(["one", "two", "one", "two", "one", "two", "one", "two"]),
    ]

    tuples = list(zip(*arrays))
    index = pd.MultiIndex.from_tuples(tuples, names=["first", "second"])

    s = pd.Series(np.random.randn(8), index=arrays)
    df = pd.DataFrame(np.random.randn(8, 4), index=arrays)
    df2 = pd.DataFrame(np.random.randn(3, 8), index=["A", "B", "C"], columns=index)

    print("s\n",s,"\n DF\n",df)
    df_columns_index_df = df.index.get_level_values(0)
    print(df_columns_index_df[0])
    print("\nDF Index:\n",df.loc[(slice(df_columns_index_df[0]),),1].index.get_level_values(1))

    bar_df = df[0]
    print("\nDF df['0']\n:", bar_df)

    bar_df = df.loc[('bar')]
    print("\nDF df['555']\n:", bar_df)

    df_index = df.index.get_level_values(0)
    print("666\n", df.loc[df_index[1]])


    df_bar_two_df = df.loc[('bar','two')]
    print("\n DF df.loc[('bar','two)]:\n",df_bar_two_df)


    print("\nDF2:\n",df2)
    bar_df2 = df2['bar']
    print("\nDF2 df2['bar']\n:", bar_df2)

    df2_columns_index_df = df2.columns.get_level_values(0)
    print("\nDF2 columns index:\n", df2_columns_index_df)
    print("\nDF2 columns index:\n", df2_columns_index_df[[4,7]])
    df2_columns_level_values = df2[df2_columns_index_df[[4,7]]].columns.remove_unused_levels()
    print("\nDF2 Columns level:\n", df2_columns_level_values)


def testtest(group):
    
    def test43(group):
        group_df = pd.DataFrame(group)
        processed_df = group_df+2
        return processed_df
    
    return [test43(group)] 


    if __name__ == '__main__':
        # Create a pool of workers
        pool = Pool(processes=4)
        # Apply the function to each group using multiprocessing
        results = pool.imap(testtest, sun_altitude_angle_df)
        pool.close()
        pool.join()
        # Convert the results to a DataFrame
        print("result:\n", results)
        processed_df = pd.DataFrame(results)
        # Print the processed DataFrame
        print("processed df:\n",processed_df)


def test5():
    import pandas as pd
    from geopy.distance import geodesic
    from itertools import combinations
    import multiprocessing as mp

    df = pd.DataFrame(
        {
            "serial_number": [1, 2, 3, 4, 5, 6, 7, 8, 9, 0],
            "column_name": ["aa", "aa", "aa", "bb", "bb", "bb", "bb", "cc", "cc", "cc"],
            "lat": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
            "lon": [21, 22, 23, 24, 25, 26, 27, 28, 29, 30],
        }
    )

    grp_lst_args = list(df.groupby("column_name").groups.items())
    print(grp_lst_args)
    # [('aa', [0, 1, 2]), ('cc', [7, 8, 9]), ('bb', [3, 4, 5, 6])]


    def calc_dist(arg):
        grp, lst = arg
        return pd.DataFrame([[grp,df.loc[c[0]].serial_number,df.loc[c[1]].serial_number,geodesic(df.loc[c[0], ["lat", "lon"]], df.loc[c[1], ["lat", "lon"]]),]for c in combinations(lst, 2) ],columns=["column_name", "machine_A", "machine_B", "Distance"],)

    if __name__ == '__main__':

        pool = mp.Pool(processes=(mp.cpu_count() - 1))
        results = pool.map(calc_dist, grp_lst_args)
        pool.close()
        pool.join()
        results_df = pd.concat(results)

        results_df
        print(results_df)

test42()