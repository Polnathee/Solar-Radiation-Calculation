
import pandas as pd
import csv

#os.listfir()
a=1
day = 1
time = 24

if 10>5:
    print(0)

#print("Running")
# reading the csv file 
#fieldName = str(f'Day {d}, {t}:00')
df = (pd.read_csv(r"C:\Nay\SolarCells_Project\QGIS\Py_Code\TestCSV\FlatRoof2_SolarInsolation.csv")).assign(Table2=a)

for d in range (0,1):
    for t in range (0,24,2):
        for i in range (0,5):
            #updating the column value/data
            df.loc[i, f'D{d},T{t}:00'] = t+i+1
            #df.loc[f, 'uid'] = uid


# writing into the file
df.to_csv(r"C:\Nay\SolarCells_Project\QGIS\Py_Code\TestCSV\FlatRoof2_SolarInsolation.csv", header=True, index=False)
print(df)

if 10>5:
    print(0)
