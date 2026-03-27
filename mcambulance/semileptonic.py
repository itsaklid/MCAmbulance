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
from scipy.integrate import quad, dblquad
from scipy.interpolate import CubicSpline
from .misc import lam, BlattWeisskopf2, ThreeBodyPS

class BtoDstarstarlnu:
    def __init__(self, conf):
        self.m_1 = conf.m_1
        self.m_2 = conf.m_2
        self.m_3 = conf.m_3
        self.m_4 = conf.m_4
        self.m_l = conf.m_l
        self.m_nom = conf.m_nom
        self.g_nom = conf.g_nom
        self.RBW = conf.RBW
        self.l = conf.l
        self.subthreshold = conf.subthreshold
        self.threebody = conf.threebody

        self.q2p = (self.m_l) ** 2
        self.q2m = (self.m_1 - self.m_2 - self.m_3 - self.m_4) ** 2
        self.k2p = (self.m_2 + self.m_3 + self.m_4) ** 2
        self.k2m = (self.m_1 - self.m_l) ** 2

        self._helperv = np.vectorize(self._helper)
        self._norm = CubicSpline(np.linspace(self.k2p, self.k2m, 1000), self._helperv(np.linspace(self.k2p + 1e-6,self.k2m - 1e-6,1000)))
        self.gamma = self._Gamma()
        self.gamma_wrong = self._Gamma_wrong()

    def _LS2(self, M2, l):
        if self.subthreshold:
            p = np.sqrt(lam(M2, self.m_2 ** 2, self.m_3 ** 2)) / 2. / np.sqrt(M2)
            pp = 1.
        elif self.threebody:
            # Treat the pi^+ pi^0 cases as equal-mass case
            if abs(self.m_3 - self.m_4) < 0.01:
                m = min(self.m_3, self.m_4)
                M = self.m_2
            else:
                raise Exception("Mass configuration not supported")
            p = ThreeBodyPS(M2, M, m)
            pp = 1.
        else:
            p = np.sqrt(lam(M2, self.m_2 ** 2, self.m_3 ** 2)) / 2. / np.sqrt(M2)
            pp = np.sqrt(lam(self.m_nom ** 2, self.m_2 ** 2, self.m_3 ** 2)) / 2. / self.m_nom

        momratio = (p/pp) ** (2 * l + 1)
        if self.subthreshold or self.threebody:
            factor = 1.
        else:
            factor = momratio * self.m_nom / np.sqrt(M2) * BlattWeisskopf2(p, pp, self.RBW, self.l)
        gam = factor * self.g_nom
        return momratio / ((M2 - self.m_nom ** 2) ** 2 + self.m_nom ** 2 * gam ** 2) * BlattWeisskopf2(p, pp, self.RBW, self.l)

    def _LS2_NR(self, M2): 
        return self.g_nom / 2. / np.pi / ( (np.sqrt(M2) - self.m_nom) ** 2 + self.g_nom ** 2 / 4. )

    def _helper(self, M2):
        def vertex(t):
            lamD = lam(t, self.m_1 ** 2, M2)
            mlhat2 = self.m_l ** 2 / t
            pskin = (1. - mlhat2) ** 2 * np.sqrt(lamD)
            h0, ht, hp, hm = self._helamps(t, M2)
            return t * pskin * ((h0 ** 2 + hp ** 2 + hm ** 2) * (2. + mlhat2) + 3. * mlhat2 * ht ** 2) / 2.

        return quad(vertex, self.m_l ** 2, (self.m_1 - np.sqrt(M2)) ** 2)[0]

    def _dGamma2D_wrong(self, q2, M2):
        def vertex(t):
            lamD = lam(t, self.m_1 ** 2, M2)
            mlhat2 = self.m_l ** 2 / t
            pskin = t * (1. - mlhat2) ** 2 * np.sqrt(lamD)
            h0, ht, hp, hm = self._helamps(t, M2)
            return pskin * ((h0 ** 2 + hp ** 2 + hm ** 2) * (2. + mlhat2) + 3. * mlhat2 * ht ** 2) / 2.

        if self.subthreshold or self.threebody:
            return 1./ np.sqrt(M2) * vertex(q2) * self._LS2_NR(M2) / self._norm(M2)
        else:        
            return 1./ np.sqrt(M2) * vertex(q2) * self._LS2(M2, self.l) / self._norm(M2)

    def _dGamma2D(self, q2, M2):
        def vertex(t):
            lamD = lam(t, self.m_1 ** 2, M2)
            mlhat2 = self.m_l ** 2 / t
            pskin = t * (1. - mlhat2) ** 2 * np.sqrt(lamD)
            h0, ht, hp, hm = self._helamps(t, M2)
            return pskin * ((h0 ** 2 + hp ** 2 + hm ** 2) * (2. + mlhat2) + 3. * mlhat2 * ht ** 2) / 2.

        return vertex(q2) * self._LS2(M2, self.l)

    def _Gamma(self):
        upper = lambda x : (self.m_1 - np.sqrt(x)) ** 2 
        return dblquad(self._dGamma2D, self.k2p, self.k2m, self.m_l ** 2, upper)[0]

    def _Gamma_wrong(self):
        upper = lambda x : (self.m_1 - np.sqrt(x)) ** 2 
        return dblquad(self._dGamma2D_wrong, self.k2p, self.k2m, self.m_l ** 2, upper)[0]

    def CorrectionWeight(self, M):
        if self.subthreshold or self.threebody:
            return M * self._norm(M ** 2) * self.gamma_wrong / self.gamma * self._LS2(M ** 2, self.l) / self._LS2_NR(M ** 2)
        else:
            return M * self._norm(M ** 2) * self.gamma_wrong / self.gamma
