#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2026 Florian Herren
# Copyright (c) 2026 Raynette van Tonder
#
# This file is part of MCAmbulance.
# 
# MCAmbulance is free software: you can redistribute it and/or modify it under the terms of the
# GNU General Public License as published by the Free Software Foundation, either version 3
# of the License, or (at your option) any later version.
#
# MCAmbulance is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
# without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. 
# See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with MCAmbulance.
# If not, see <https://www.gnu.org/licenses/>. 

import numpy as np

def lam(x, y, z):
    return x ** 2 + y ** 2 + z ** 2 - 2. * (x * y + y * z + z  * x)

def wcalc(q2, m1, m2):
    return (m1 ** 2 + m2 ** 2 - q2) / (2. * m1 * m2)
    
def BlattWeisskopf2(p, pp, R, l):
    if l == 0:
        return 1.
    elif l == 1:
        zR2 = R ** 2 * p ** 2
        zR2p = R ** 2 * pp ** 2
        return ( zR2p + 1. ) / ( zR2 + 1. )
    else:
        return 1.

def ThreeBodyPS(M2, M, m):
    delta = (1. - (M + 2. * m) ** 2 / M2) / 8. / m / M
    pref = 32. * np.pi / np.sqrt(M / (M + 2. * m)) * (m * M) ** 3
    coefflist = np.array([0,0,1,m**2 + 8*m*M + M**2,(-5*m**4 + 100*m**3*M + 510*m**2*M**2 + 92*m*M**3 - M**4)/8., \
     (7*m**6 - 84*m**5*M + 987*m**4*M**2 + 4064*m**3*M**3 + 861*m**2*M**4 - 12*m*M**5 + M**6)/8., \
     (-105*m**8 + 1176*m**7*M - 7980*m**6*M**2 + 71624*m**5*M**3 + 259210*m**4*M**4 + 60200*m**3*M**5 - 876*m**2*M**6 + 120*m*M**7 - 9*M**8)/64., \
     (231*m**10 - 2640*m**9*M + 16335*m**8*M**2 - 82320*m**7*M**3 + 623550*m**6*M**4 + 2067696*m**5*M**5 + 509830*m**4*M**6 - 7280*m**3*M**7 + 1275*m**2*M**8 - \
      160*m*M**9 + 11*M**10)/64.,(-9009*m**12 + 108108*m**11*M - 671814*m**10*M**2 + 3031380*m**9*M**3 - 12615075*m**8*M**4 + 84849336*m**7*M**5 + \
      264017628*m**6*M**6 + 67908456*m**5*M**7 - 928935*m**4*M**8 + 189500*m**3*M**9 - 30774*m**2*M**10 + 3588*m*M**11 - 229*M**12)/1024., \
     (23595*m**14 - 300300*m**13*M + 1936935*m**12*M**2 - 8664656*m**11*M**3 + 31814783*m**10*M**4 - 115535420*m**9*M**5 + 711096155*m**8*M**6 + 2107726720*m**7*M**7 + \
      559484849*m**6*M**8 - 7258692*m**5*M**9 + 1646085*m**4*M**10 - 314160*m**3*M**11 + 47845*m**2*M**12 - 5236*m*M**13 + 313*M**14)/1024., \
     (-1042899*m**16 + 14119248*m**15*M - 95742504*m**14*M**2 + 440231792*m**13*M**3 - 1585315732*m**12*M**4 + 5018469456*m**11*M**5 - 16440191768*m**10*M**6 + \
      94415292400*m**9*M**7 + 269302755150*m**8*M**8 + 73253524080*m**7*M**9 - 897871128*m**6*M**10 + 220263120*m**5*M**11 - 47055764*m**4*M**12 + 8480752*m**3*M**13 - \
      1221672*m**2*M**14 + 126416*m*M**15 - 7123*M**16)/16384.,(3002285*m**18 - 43232904*m**17*M + 309697245*m**16*M**2 - 1485777696*m**15*M**3 + \
      5454036900*m**14*M**4 - 16778885760*m**13*M**5 + 47429549076*m**12*M**6 - 143253021600*m**11*M**7 + 778051467414*m**10*M**8 + 2151041754160*m**9*M**9 + \
      596651584230*m**8*M**10 - 6902314848*m**7*M**11 + 1799947380*m**6*M**12 - 418283712*m**5*M**13 + 84842820*m**4*M**14 - 14546400*m**3*M**15 + 1994661*m**2*M**16 - \
      196200*m*M**17 + 10469*M**18)/16384.])
    res = 0
    for i, coeff in enumerate(coefflist):
        res += coeff * (delta ** i)

    res *= pref
    return res
    
    
