from os.path import abspath, join, pardir
import sys
from numpy.testing import assert_almost_equal

dp = abspath(join(__file__, pardir, pardir))
sys.path.insert(0, dp)

from pyMPM import MPM

def Amax(fmin, fmax, RH=0):
    """ returns the max attenuation between two freq at given RH """
    A_max = 0
    f_max = 0
    #RH = 100  # Relative humidity in %
    T = 15  # Air temperature in degree Celcius
    P = 1013  # Air pressiure in mbar

    for f in range(fmin, fmax+1):
        A = MPM(f, P, T, RH, 0, 0, 0, 'att')
        if A > A_max:
            f_max = f
            A_max = A[0]
    return f_max, A_max


def Amin(fmin, fmax, RH=100):
    """ returns the minimum attenuation between two freq at given RH """
    A_min = 1e5
    f_min = 0
    #RH = 100  # Relative humidity in %
    T = 15  # Air temperature in degree Celcius
    P = 1013  # Air pressiure in mbar

    for f in range(fmin, fmax+1):
        A = MPM(f, P, T, RH, 0, 0, 0, 'att')
        if A < A_min:
            f_min = f
            A_min = A[0]
    return f_min, A_min
    
def test_Amin():
    """ verifies the min attenuation between 20GHz and 100GHz
    when RH=100% """
    f, A = Amin(20,100,100)
    assert f == 31
    assert_almost_equal(A, 0.1711905)  # 0960372795

def test_Amax():
    """ verifies the max attenuation between 100GHz and 150GHz
    when RH=0% """
    f, A = Amax(100,150,0)
    assert f == 119
    assert_almost_equal(A,1.3475992)  # 227523178
