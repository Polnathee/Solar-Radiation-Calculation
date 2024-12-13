import csv
import pandas as pd

def input_dedrived_data(attribute_table_csv, uid):
    # Stores Building Chracteristic Data
    building_characteristic_df = get_data(attribute_table_csv)

    # Finding UID in Attribute Data Table
    desired_row_df = building_characteristic_df.loc[building_characteristic_df['uid'] == f'{uid}']
    #print(f'Desired Row Data Frame:\n{desired_row_df}')

    # Writing Data into Data Frame
    building_fields_table_df = desired_row_df
    building_fields_table_df = building_fields_table_df.reset_index(drop=True)
    
    return building_fields_table_df

def get_data(attribute_table_csvfile_name):
    # Acquire data from the Attribute Table.csv
    building_characteristic_df = pd.read_csv(attribute_table_csvfile_name, usecols=['uid', 'lat', 'long', 'height', 'rooftype', 'rooftop', 'area'])

    # Re-order and filter data column
    reorder_column = ['uid', 'lat', 'long', 'height', 'area', 'rooftype', 'rooftop']
    building_characteristic_df = building_characteristic_df[reorder_column]
    building_characteristic_df = building_characteristic_df.reset_index(drop=True)

    #print(len(building_characteristic_df))
    #print(type(building_characteristic_df))
    #print(building_characteristic_df)
    return building_characteristic_df

def create_csvfile(csvfile_location, csvfile_local_name):
    csvfile_name = str(csvfile_location) + '/' + str(csvfile_local_name) + '.csv'
    with open(csvfile_name, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
    #print(f'csv file name: {csvfile_name}')
    return writer, csvfile_name

