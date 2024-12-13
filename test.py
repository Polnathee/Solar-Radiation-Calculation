import math
import numpy as np
import pandas as pd

def Deg2Rad(deg):
    return deg * (np.pi / 180)
    
def Rad2Deg(rad):
    return rad * (180 / np.pi)

radius = 50
azimuth_angle_field_df = pd.DataFrame([45, 135, 225, 315, 53, 37, 115])
azimuth_angle_df = pd.DataFrame(azimuth_angle_field_df.values.tolist() * len(list(range(-radius, radius+1,1))))
azimuth_angle_df = pd.DataFrame(azimuth_angle_df.stack(future_stack=True).reset_index(drop=True))
azimuth_angle_df = azimuth_angle_df.sort_values(by=0, ascending=True).reset_index(drop=True)
azimuth_angle_df = azimuth_angle_df.transpose()

azimuth_angle_upper_bound_factor_df = np.tan(Deg2Rad(azimuth_angle_df))

column_minor_index_list         = (((pd.DataFrame(list(range(-radius,radius+1)))))).transpose().values.tolist()
column_minor_display_index_list = (((pd.DataFrame(list(range(-radius,radius+1)))/1000)+102.8)).transpose().values.tolist()
row_minor_latitude_list         = (((pd.DataFrame(list(range(-radius,radius+1)))/1000)+16.4)).transpose().values.tolist()
print(column_minor_index_list)
column_major_index_list = list(range(1,len(azimuth_angle_field_df)+1))

iterables = [column_major_index_list, column_minor_index_list[0]]
display_iterables = [column_major_index_list, column_minor_display_index_list[0]]
#print(iterables)
calculation_index = pd.MultiIndex.from_product(iterables, names=["first", "second"])
display_index     = pd.MultiIndex.from_product(display_iterables, names=["first", "second"])
#print(index)

local_list = list(range(-radius,radius+1) for x in range (-radius,radius+1))
#print(pd.DataFrame(zip(*(local_list*2))))

azimuth_angle_upper_bound_factor_df.columns = calculation_index
df1 = pd.DataFrame(zip(*(local_list*len(azimuth_angle_field_df))), index=list(range(-radius,radius+1)), columns=calculation_index)
#print(df1.columns.get_level_values(1))

df1         = pd.DataFrame(np.where(abs(df1)<(((radius**2)-(df1.columns.get_level_values(1)**2))**(1/2)), df1, 0))
df1.columns = calculation_index
#print('radius check\n',df1)

check_df = pd.DataFrame(df1.columns.get_level_values(1)*azimuth_angle_upper_bound_factor_df)
print(azimuth_angle_upper_bound_factor_df)
print(df1.columns.get_level_values(1)*azimuth_angle_upper_bound_factor_df)
check_list = check_df.values.tolist()
check1 = pd.DataFrame([check_list[0]]*101)
check1.columns = calculation_index
print("check\n",check1)

conditions = [(((90>azimuth_angle_df)&(azimuth_angle_df>=0))|((360>=azimuth_angle_df)&(azimuth_angle_df>270))), (((270>azimuth_angle_df)&(azimuth_angle_df>90)))]
choices = [pd.DataFrame((np.where(df1>check1,df1,0)), index=row_minor_latitude_list, columns=calculation_index), pd.DataFrame((np.where(df1<check1,df1,0)), index=row_minor_latitude_list, columns=calculation_index)]

df1 = pd.DataFrame(np.select(conditions, choices, default=np.nan))

'''
df1 = pd.DataFrame((np.where(abs(df1)>check1,1,0)), index=row_minor_latitude_list, columns=index)
'''

df1 = df1.sort_index(ascending=False)
df1.columns = calculation_index
df1 = pd.DataFrame(np.where(df1!=0,(df1/1000)+16.4, 0),index=row_minor_latitude_list, columns=display_index)

df1 = df1.stack(future_stack=True).reset_index()

df1.columns = ['lat','long'] + list(range(1,len(azimuth_angle_field_df)+1))
df2 = df1.loc[np.count_nonzero(df1.loc[:,2:],axis=1)>0]
print(df2)
print('Length of Feasible Coordinates:',len(df2))


