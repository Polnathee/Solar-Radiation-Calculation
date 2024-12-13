import math
import Phase1_Solar_Efficiency_Analysis_Program.EarthDeclinationCal as declication

# HourAngle(HRA) is used for calculate daily solar radiation
def solarHourAngle_function(n, time, long, TZ):
    st = lst_function(n, time, long, TZ)
    hra = 15.0 * (st - 12.0)
    print(f'Day : {n}, Time: {time}, ST : {st} Hour Angle : {hra}')
    return hra

def lst_function(n, time, long, TZ):
    offset = offset_function(n, time, long, TZ)
    return float(time) + (offset/60)

def offset_function(n, time, long, TZ):
    eot = eot_function(n, time)
    return eot + (4 * (long - (15.0 * float(TZ))))

def eot_function(n, time):
    gramma = fractionYear_function(n, time)
    eot = 229.18 * (0.000075 + ((0.001868)*math.cos(gramma)) - (0.032077*(math.sin(gramma))) - (0.014615*(math.cos(2*gramma))) - (0.040849*(math.sin(2 * gramma))) )
    return eot

def fractionYear_function(n, time):
    gramma = ((2 * math.pi)/365) * (float(n-1) + ((time-12)/24))
    return gramma

def rise_hra_function(dDelta, lad):
    hra_rise = Rad2Deg(math.acos((-1)*(math.tan(Deg2Rad(dDelta)))*(math.tan(Deg2Rad(lad)))))
    print(f'Rise HRA: {hra_rise}')
    return  hra_rise

def hra2st (hra):
    st = (hra/15) + 12
    time = int(st)
    diff_time = st - time
    if diff_time >= 0.5:
        time += 1
    else:
        time = int(st)
    print(f' Time: {time}, Suntime: {st}')
    return time

def Deg2Rad(deg):
    return deg * (math.pi / 180)
    
def Rad2Deg(rad):
    return rad * (180 / math.pi)


def main():
    for day in range (175,176):
        longitude = 100.1703
        ladtitude = 13.9789
        dDelta = declication.declination_function(175)
        print(f'Ddelta: {dDelta}')
        pacificSTDT = 7.0
        rise_hra = rise_hra_function(dDelta, ladtitude )
        rise_time = hra2st(-rise_hra)
        for hour in range (7, 12):
            for minute in range (0, 60, 30):
                time = hour + (minute / 60)
                hra = solarHourAngle_function(day, time, longitude, pacificSTDT)
    return hra

main()