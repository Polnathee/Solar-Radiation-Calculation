import math

def tr_function(pressure,zenith_angle):
    # (pressure) Atmospheric Pressure in Kilopascal
    m_a =  m_a_function(pressure, zenith_angle)
    print(f'Ma: {m_a}')
    t_r = math.exp((-0.0903)*(m_a**0.84)*(1.0+m_a-(m_a**1.01)))
    t_rn = 0.615958 + 0.375566 * (math.exp(-0.221185*(m_a)))
    #print(f'tr: {t_r}')
    print(f'tr: {t_rn}')
    return t_r, t_rn

def t_aer_function(pressure, zenith_angle):
    # mean of alpha is 1.3, mean og beta is 0.138
    alpha = 1.3
    beta = 0.138
    m_a =  m_a_function(pressure, zenith_angle)

    # Machler Model, Note: Beta < 0.5
    t_aer = ((0.12445*(alpha))-0.0162) + (1.003-(0.1252*(alpha)))*(math.exp((-beta*m_a)*(1.089*(alpha)+0.5123)))
    #print(f'taer: {t_aer}')
    return t_aer

def t_aera_function(pressure, zenith_angle, t_aer):
    #(pressure) Atmospheric Pressure in Kilopascal
    m_a =  m_a_function(pressure, zenith_angle)
    ssa = 1.0

    t_aera = 1.0-(1.0-(ssa))*((1.0)-(m_a)+(m_a**1.06))*(1.0-(t_aer))
    #print(f'taera: {t_aera}')
    return t_aera

def t_w_function(zenith_angle):
    rh = 0.000182
    T = 292
    p_sv = 990.84

    w = 0.8933*(math.exp(0.1715*(rh)*(p_sv)*(1/T)))
    m_r = 1/(abs(math.cos(Deg2Rad(zenith_angle))))
    u1 = (w)*(m_r)
    # Lacis and Hansen Model
    alpha_w = (2.9*(u1))/(((1+141.5*u1)**0.635)+(5.92*u1))
    #print(f'AlphaW1 : {alpha_w}')
    t_w = 1 - alpha_w
    #print(f'tw: {t_w}')
    return t_w

def  t_o_function(zenith_angle):
    l = 0.260
    m_r = 1/(abs(math.cos(Deg2Rad(zenith_angle))))
    u3 = (l)*(m_r)
    alpha_o = ((0.02118*u3) / (1+(0.042*u3)+((3.23*10**-4)*(u3**2)))) + ((1.082*u3)/(1+(138.6*u3)**0.805)) + ((0.0658*u3)/(1+(103.6*u3)**3))
    #print(f'alpha: {alpha_o}')
    t_o = 1 - alpha_o
    #print(f'to: {t_o}')
    return t_o
                             
def t_g_function(pressure, zenith_angle):
    m_a = m_a_function(pressure, zenith_angle)
    t_g = math.exp(-0.01278*((m_a))**0.26)
    #print(f'tg: {t_g}')
    return t_g

def m_a_function(pressure, zenith_angle):
    # Relative Air Mass, zenith angle in radian
    m_r = 1/(abs(math.cos(Deg2Rad(zenith_angle))))
    #print(f'Mr: {m_r}')
    # (pressure) Atmospheric Pressure in Kilopascal
    m_a =  m_r * (pressure/101.325)
    #print(f'Ma: {m_a}')
    return m_a

def t_aer_p_funtion(a_lambda):
    # Angstrom's Turbidity Coefficient at Khonkaen is 0.138 (mean)
    beta = 0.138
    # Angstrom's Wavelenght Exponent is 1.3 (mean)
    alpha = 1.3
    t_aer_p = (beta)*(a_lambda**(-alpha))
    #print(f'taer_p: {t_aer_p}')
    return t_aer_p

def Deg2Rad(deg):
    return deg * (math.pi / 180)
    
def Rad2Deg(rad):
    return rad * (180 / math.pi)

def main():

    pressure = 99
    zenith_angle = 39.55526311
    t_r = tr_function(pressure, zenith_angle)
    t_aer = t_aer_function(pressure, zenith_angle)
    t_o = t_o_function(zenith_angle)
    t_w = t_w_function(zenith_angle)
    t_g = t_g_function(pressure, zenith_angle)

    t = t_r * t_aer * t_o * t_w * t_g
    print(f't: {t}')

#main()
