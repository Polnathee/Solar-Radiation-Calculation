import math
import Phase1_Solar_Efficiency_Analysis_Program.Atmospheric_coeffCal as atm_coeff

#i_sc = 4917.96*(10**3) # Joules per hour per square meter 
i_sc = 1.3667 # Kilowatts per square meter

def normal_solarInsolation_function(day, dDelta, lat, hra1, hra2, step):
    #E0 for solar insolation Cal
    e_0 = extraterrestial_function(day)
    # Zenith Angle for atmos_coeff
    theta_z = zenith_angle_function(dDelta, lat, hra1)
    # Integrate theta Z for Solar Insolation Cal
    int_theta_z = intzenith_angle_function(dDelta, lat, hra1, hra2)

    # Atmospheric Pressure at Khon Kaen is 108 kilo pascal
    pressure = 100.8 #(kilo Pascal)

    normal_atmos_coeff = normal_atmos_coeff_function(pressure, theta_z)
    #print(f'Normal Atmospheric Coefficient: {normal_atmos_coeff}')

    # Power Factor for kWh/m^2/h (Global insolation)
    power_factor = 60/step

    # Irradiance Calculation
    # Extraterrestial Irradiance in degree, ir_no
    ir_no = (i_sc) * (e_0) * (math.cos(Deg2Rad(theta_z)))
    if ir_no < 0:
        ir_no = 0
    else:
        ir_no = ir_no
    #print(f'ir_no: {ir_no} kW/m^2')

    t_cloud = 0.03

    t_r, t_rn = atm_coeff.tr_function(pressure, theta_z)

    # Test Global Insolation with Cloud
    i_b = (i_sc) * (e_0) * (math.cos(Deg2Rad(theta_z))) * t_cloud
    print(f'I_b: {i_b}')

    i_d = (i_sc) * (e_0) * (math.cos(Deg2Rad(theta_z))) * (0.4) * (1-t_cloud)
    print(f'I_d: {i_d}')

    i_dr = (i_sc) * (e_0) * (math.cos(Deg2Rad(theta_z))) * ((1-t_rn)*0.1)
    print(f'I_dr: {i_dr}')

    i_global = i_b + i_d + i_dr
    print(f'I_Global: {i_global}')

    # Global Irradiance in degree, ir_o
    ir_o = ir_no * (normal_atmos_coeff)
    print(f'ir_o: {ir_o} kW/m^2')

    # Insolation Calculation
    # Extraterrestial Insolation Calculation in degree, I_no (kWh/m^2/hr)
    i_no = (12/math.pi) * (i_sc) * (e_0) * (int_theta_z)
    if i_no < 0:
        i_no = 0
    else:
        i_no = i_no
    #print(f'i_no: {i_no} kW/m^2/0.5h')

    # Global Insolation Calculation in degree,I_o (kWh/m^2/hr)
    i_o = i_no * (normal_atmos_coeff)
    #print(f'i_o: {i_o} kW/m^2/0.5h')

    return i_o, ir_o, theta_z

def diffuse_solarInsolation_function(day, dDelta, lat, hra1, hra2):
    #E0 for solar insolation Cal
    e_0 = extraterrestial_function(day)
    # Zenith Angle for atmos_coeff
    theta_z = zenith_angle_function(dDelta, lat, hra1)
    # Integrate theta Z for Solar Insolation Cal
    int_theta_z = intzenith_angle_function(dDelta, lat, hra1, hra2)

    # Atmospheric Pressure at Khon Kaen is 108 kilo pascal
    pressure = 99 #(kilo Pascal)

    t_r = atm_coeff.tr_function(pressure, theta_z)
    t_o = atm_coeff.t_o_function(theta_z)
    t_g = atm_coeff.t_g_function(pressure, theta_z)
    t_w = atm_coeff.t_w_function(theta_z)
    t_aer = atm_coeff.t_aer_function(pressure, theta_z)
    t_aera = atm_coeff.t_aera_function(pressure, theta_z, t_aer)
    t_aers = 0.9
    m_a = atm_coeff.m_a_function(pressure, theta_z)
    f_c = 1

    # Calculation in degree
    i_dr = i_dr_function(i_sc, e_0, int_theta_z, t_r, t_o, t_g, t_w, t_aera, m_a)
    i_daer = i_daer_function(i_sc, e_0, int_theta_z, t_o, t_g, t_w, t_aers, f_c, m_a)
    
    if i_dr < 0:
        i_dr = 0
    
    if i_daer < 0:
        i_daer = 0

    i_d = i_dr + i_daer
    #print(f'i_d: {i_d}, i_dr: {i_dr}, i_daer: {i_daer}')
    return i_d

def zenith_angle_function(dDelta, lat, hra):
    theta_z = Rad2Deg(math.acos(math.sin(Deg2Rad(dDelta))*math.sin(Deg2Rad(lat)) + math.cos(Deg2Rad(dDelta))*math.cos(Deg2Rad(lat))*math.cos(Deg2Rad(hra))))
    #print(f'Zenith: {theta_z}')
    return theta_z

def intzenith_angle_function(dDelta, lat, hra1, hra2):
    int_theta_z = (((math.sin(Deg2Rad(dDelta)))*(math.sin(Deg2Rad(lat)))*(Deg2Rad(hra2) - Deg2Rad(hra1))) + ((math.cos(Deg2Rad(dDelta)))*(math.cos(Deg2Rad(lat)))*((math.sin(Deg2Rad(hra2)))-(math.sin(Deg2Rad(hra1))))))
    #print(f'Int_Zenith: {int_theta_z}')
    return int_theta_z

def normal_atmos_coeff_function(pressure, theta_z):
    # Coefficient of radiation due to scattering in air molecule 
    t_r, t_rn = atm_coeff.tr_function(pressure, theta_z)
    # Coeffcient of radiation due to scattering and absorbtion in air molecule
    t_aer = atm_coeff.t_aer_function(pressure, theta_z)
    # Coefficient of radiation due to vapor
    t_w = atm_coeff.t_w_function(theta_z)
    # Coefficient of radiation due to Ozone
    t_o = atm_coeff.t_o_function(theta_z)
    # Coefficient of radiation due to ambient gases
    t_g = atm_coeff.t_g_function(pressure, theta_z)

    # Product of coefficient that affects solar radiation
    atmos_coeff = (t_r)*(t_aer)*(t_w)*(t_o)*(t_g)
    return atmos_coeff

def extraterrestial_function(day):
    e_0 = 1 + 0.033*(math.cos(((2*math.pi)*(day))/365))
    #print(f'E0: {e_0}')
    return e_0

def i_dr_function(i_sc, e_0, int_theta_z, t_r, t_o, t_g, t_w, t_aera, m_a):
    diffuse_atmos_coeff = (t_o)*(t_g)*(t_w)*(t_aera)*((1-t_r)/2*(1-(m_a)-(m_a**1.02)))
    #print(f'Diffuse IDR Coeff:{diffuse_atmos_coeff}')
    i_dr = (12/math.pi) * (i_sc) * (e_0) * (int_theta_z) * (diffuse_atmos_coeff) 
    return i_dr

def i_daer_function(i_sc, e_0, int_theta_z, t_o, t_g, t_w, t_aers, f_c, m_a):
    diffuse_atmos_coeff = (t_o)*(t_g)*(t_w)*(t_aers)*((f_c*(1-t_aers))/(1-(m_a)+(m_a**1.02)))
    #print(f'Diffuse SIDAER Coeff:{diffuse_atmos_coeff}')
    i_daer = (12/math.pi) * (i_sc) * (e_0) * (int_theta_z) * (diffuse_atmos_coeff)
    return i_daer

def Deg2Rad(deg):
    return deg * (math.pi / 180)
    
def Rad2Deg(rad):
    return rad * (180 / math.pi)

def main():
#     #d = 1
#     #dDelta = -23.0116367278692
#     #lat = 16.4425
#     #hra1 = -2.89004224
#     #hra2 = 4.607620158

    d = 1
    dDelta = 23.42372933046904
    lat = 13.9789
    hra1 = -65.3167561038434
    hra2 = -50.31902590805204
    step = 30
    
    #zenith_angle_function(dDelta, lat, hra1)
    i = normal_solarInsolation_function(d, dDelta, lat, hra1, hra2, step)

main()
