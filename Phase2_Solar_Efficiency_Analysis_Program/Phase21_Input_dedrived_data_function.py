import csv
import pandas as pd

def input_dedrived_data(attribute_table_csv, uid):
    # Stores Building Chracteristic Data
    building_characteristic_df = get_data(attribute_table_csv)

    # Finding UID in Attribute Data Table
    desired_row_df = building_characteristic_df.loc[building_characteristic_df['uid'] == f'{uid}']
    print(f'Desired Row Data Frame:\n{desired_row_df}')
    
    # Desired Fields
    #fields_index = ["uid", "lat", "long", "height", "rooftype", "rooftop", "shax1", "shay1", "shax2", "shay2"]
    order_column = pd.Series({'uid':'uid', 'lat':'lat', 'long':'long', 'height':'height', 'rooftype':'rooftype', 'rooftop':'rooftop', 'shax1':'shax1', 'shay1':'shay1', 'shax2':'shax2', 'shay2':'shay2'})
    desired_row_df = pd.concat([desired_row_df, order_column.to_frame(0).T], ignore_index=True)
    desired_row_df = desired_row_df.reindex([1,0])
    desired_row_df.index = range(len(desired_row_df))
    #print(f'Desired Row Data Frame:\n{desired_row_df}')

    # Acquire Data from Attribute Table
    desired_row_df = desired_row_df.transpose()
    desired_row_df.index = range(len(desired_row_df))

    #print(new_desired_row_df.shape)

    desired_row_df.columns = ['Fields','Descriptions']
    #print(desired_row_df.head())
    #print(desired_row_df.columns)
    #print(desired_row_df.index)

    # Writing Data into Data Frame
    fields_table_df = desired_row_df
    
    return fields_table_df


def get_data(attribute_table_csvfile_name):
    # Acquire data from the Attribute Table.csv
    building_characteristic_df = pd.read_csv(attribute_table_csvfile_name, usecols=['uid', 'lat', 'long', 'height', 'rooftype', 'rooftop', 'shax1', 'shay1', 'shax2', 'shay2'])

    # Re-order and filter data column
    reorder_column = ['uid', 'lat', 'long', 'height', 'rooftype', 'rooftop', 'shax1', 'shay1', 'shax2', 'shay2']
    building_characteristic_df = building_characteristic_df[reorder_column]

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

