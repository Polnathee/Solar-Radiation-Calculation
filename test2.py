import math

import csv
import numpy as np
import pandas as pd

def Deg2Rad(deg):
    return deg * (math.pi / 180)
    
def Rad2Deg(rad):
    return rad * (180 / math.pi)
'''
y_df = pd.DataFrame([1,2,3,4,5])
print(y_df.values.tolist())
x_df = pd.DataFrame((y_df.values.tolist())*4)

print(x_df)
'''

azimuth_angle_field_df = pd.DataFrame([45, 135, 225, 315])

a_df = pd.DataFrame([[2,3,4,5,36,7]])
b_df = pd.DataFrame([[-1,0,1]])

#print(a_df,'\n',b_df)

c_df = a_df * b_df
#print(c_df)

list1 = [[1,1],[1,1]]
list2 = [[2,3,7],[4,5,8]]
radius = 5


df2 = pd.DataFrame(list2)
print(df2)
df2_column_level_zero_list1 = [1]
df2_column_level_one_list1 = list(range(1,radius+1))
df2_column_index_iterables1 = [df2_column_level_zero_list1,df2_column_level_one_list1]
df2_column_index1 = pd.MultiIndex.from_product(df2_column_index_iterables1, names=['first', 'second'])

#print(df2_column_index1)
#print(df2.stack(future_stack=True))
#df21_df =pd.DataFrame(pd.DataFrame((pd.DataFrame(df2.stack(future_stack=True)).values.transpose().tolist())*radius).transpose().stack(future_stack=True)).transpose()
df21_df =pd.DataFrame((pd.DataFrame(pd.DataFrame((pd.DataFrame(df2.stack(future_stack=True)).values.transpose().tolist())*radius).transpose().stack(future_stack=True)).transpose()).values.tolist()*radius)
print("\ndf222",df21_df)

df21_column_level_zero_list2 = list(range(1,(df2.shape[0])+1))
df21_column_level_one_list2 = list(range(1,(df2.shape[1]*radius)+1))
df21_column_index_iterables2 = [df21_column_level_zero_list2,df21_column_level_one_list2]
df21_column_index2 = pd.MultiIndex.from_product(df21_column_index_iterables2, names=['first', 'second'])

df21_row_level_zero_list2 = list(range(1,2))
df21_row_level_one_list2 = list(range(1,radius+1))
df21_row_index_iterables2 = [df21_row_level_zero_list2,df21_row_level_one_list2]
df21_row_index2 = pd.MultiIndex.from_product(df21_row_index_iterables2, names=['row1', 'row2'])
#print(df21_column_index2)

df21_df.columns = df21_column_index2
df21_df = df21_df.set_index(df21_row_index2)
print("\ndf21",df21_df,"\n")
df21_df = df21_df.transpose().stack(future_stack=True).transpose().stack(1,future_stack=True).transpose()
print("\nlast df21",df21_df)

def test3():
    df1 = pd.DataFrame(list1)
    #print(df1)
    # Sample DataFrame
    df = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})

    # Using len()
    columns = df1.shape[1]

    # Using shape
    rows = df1.shape[0]

    #print("Number 0f columns:", columns)
    #print("Number of rows:", rows)


