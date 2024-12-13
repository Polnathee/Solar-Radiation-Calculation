import pandas as pd

def group_test():
        df = pd.DataFrame({'Animal': ['Falcon', 'Falcon',
                                'Parrot', 'Parrot'],
                        'Max Speed': [380., 370., 24., 26.]})

        print(df)
        new_df = df.groupby("Animal", group_keys=True)[['Max Speed']].apply(lambda x: x)
        new_df2 = df.groupby("Animal", group_keys=True)[['Max Speed']].apply(lambda x: x)

        print(new_df)
        print(new_df2)

        from datetime import date
        import calendar

        today = date.today()
        year = today.year
        print(calendar.isleap(year))


from datetime import datetime

date_object = datetime.strptime("06-09-2020", '%d-%m-%Y')
x = date_object.strftime('%Y%m%d')
print(x)

