import math

# Declination (delta)
def declination_function(n):
    rDelta = (Deg2Rad(23.45)) * math.sin(((2 * math.pi)/365)*(n + 284))
    dDelta = Rad2Deg(rDelta)
    
    # print(f'Day: {n}, Earth Decilnation Angle : {dDelta}')
    
    return dDelta

def Deg2Rad(deg):
    return deg * (math.pi / 180)
    
def Rad2Deg(rad):
    return rad * (180 / math.pi)