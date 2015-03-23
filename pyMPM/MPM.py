# -*- coding: utf-8 -*-
"""
Created on Fri Mar 20 13:20:49 2015

@author: chwala-c
"""

import numpy as np


def MPM93(f, P, T, U, wa, wae, R, output_type='ref'):
    param = inputconv(P, T, U)
    
    NV = watervapormodule(f, param.e, param.pd, param.th)
    ND = dryairmodule(f, param.e, param.pd, param.th)
    
    # Sum up all refractivities
    N = NV + ND
    
    return outconv(f, N, output_type)
    
def inputconv(P, T, U):
    """
    Convert input parameters P, T, U to e, pd, th
    
    Parameters
    ----------
    
    P : float
        Air pressure in mbar
    T : float
        Air temperature in degree Celcius
    U : Relative humidity in %
    
    Returns
    -------
    
    a : namedtuple
        Namedtuple of 
         * e (Partial water vapor pressure)
         * pd (Partial pressure of dry air)
         * th (Reciprocal temperature)
    """
    
    from collections import namedtuple
    a = namedtuple('a', ['e', 'pd', 'th'])
    
    TK = T + 273.15
    # Reciprocal temperature theta
    th = 300.0/TK
    # Water wapor saturation pressure
    es = 2.408e11*th**5*np.exp(-22.644*th)
    # Partial pressuer of water vapor
    e = es*U/100.0;
    # Partial pressure of dry air
    pd = P - e
    # water vapor density in g/m3
    Rs = 461.25; # Specifice gas constant for water vapor (Stöcker, Taschenbuch der Physik)
    rhogas = 100000*e/(Rs*TK)
    
    return a(e=e, pd=pd, th=th)
    
def outconv(f, N, output_type):
    """ 
    Convert complex refractivity N to desired output 
    
    Parameters
    ----------
    
    f : float, np.array of float
        Frequency in GHz
    N : complex, np.array of complex
        Refractivity
    output_type: str
        Desired output tpye. Supporte types are:
        'ref' = Refractivity
        'att' = Attenuation in db/km
        'dis' = Phase dispersion in deg/km
        'del' = Group delay in ps/km
        'abs' = Absorption coefficients in 1/m
    
    Returns
    -------
    
    out : float, np.array
        The desired conversion of the refractiviy
    """
    
    c=299792458
    
    if len(N) == 0:
        return 0
    else:
        if output_type == 'ref':
            # Refractivity
            out = N
        elif output_type == 'att':
            # Attenuation in db/km
            out = 0.1820*f*np.imag(N)
        elif output_type == 'dis':
            # Phase dispersion beta in deg/km
            out = 1.2008*f*np.real(N)
        elif output_type == 'del':
            # Group delay tay in ps/km
            out = 3.3356 * np.real(N)
        elif output_type == 'abs':
            # Absorption coefficients in 1/m
            out = 4*np.pi*1000/c*f*np.imag(N)
        else:
            raise ValueError('output_type not supported')
        return out
          
def dryairmodule(f_vec, e, pd, th):
    """
    Calculate refractivity for oxygen lines
    
    Parameters
    ----------
    
    blabla
    
    """
    
    # Make sure f_vec is an iterabel array
    if type(f_vec) == float or type(f_vec) == int:
        f_vec = np.array([f_vec,])
    
    ND = []
    oxygen_lines = np.loadtxt('oxygen93.txt')
    
    for f in f_vec:
        # Non dispersive part
        nd = 0.2588*pd*th
        # Loop over lines
        for line in oxygen_lines:
            f_line = line[0]
            # Line strength (with correction factor 1e-6)
            S =  1e-6*line[1]/f_line*pd*th**3*np.exp(line[2]*(1-th))
            # Line width
            gamma = line[3]/1000.0*(pd*th**line[4] + 1.1*e*th)
            # Zeeman effect
            gamma = np.sqrt(gamma**2 + 2.25e-6)
            # Overlap parameter (with correction factor 1e-3)
            delta = 1e-3*(line[5] + line[6]*th)*(pd+e)*th**0.8
            # Line form function
            F = f*((1-1j*delta)/(f_line-f-1j*gamma) - (1+1j*delta)/(f_line+f+1j*gamma))
            nd = nd + S*F
        # Non resonant part
        So = 6.14e-5*pd*th**2
        Fo = -f/(f+1j*0.56e-3*(pd+e)*th**0.8)
        Sn = 1.4e-12*pd**2*th**3.5
        Fn = f/(1 + 1.93e-5*f**1.5) # Correction 1.9 -> 1.93
        nd = nd + So*Fo + 1j*Sn*Fn
        ND.append(nd)
    return np.array(ND)

        
def watervapormodule(f_vec, e, pd, th):
    """ 
    Calcualte refractivity for water vapor lines 
    
    Parameters
    ----------
    
    f_vec : float, or array of floats
        Frequency in GHz
        
        ....
        
    """
    
    # Make sure f_vec is an iterabel array
    if type(f_vec) == float or type(f_vec) == int:
        f_vec = np.array([f_vec,])
    
    NV = []
    water_lines = np.loadtxt('water93.txt')
    # Loop over frequencies
    for f in f_vec:
        nv = (4.163*th + 0.239)*e*th
        # Loop over lines
        for line in water_lines:
            f_line = line[0]
            # Line strength
            S = line[1]/f_line*e*th**(3.5)*np.exp(line[2]*(1 - th))
            # Line width
            gamma = line[3]/1000 * (line[4]*e*th**line[6] + pd*th**line[5])
            # Doppler broadening
            #i_dopp = np.where(pd + e < 0.7)
            if pd + e < 0.7:
                gamma = 0.535*gamma + np.sqrt(0.217*gamma**2 + (1.46e-6*gamma*np.sqrt(th))**2)
            # Line form function
            F = f*(1/(f_line - f - 1j*gamma) - 1/(f_line + f + 1j*gamma))
            nv = nv + S*F
        NV.append(nv)
    return np.array(NV)
