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
from .misc import wcalc, lam
from .semileptonic import BtoDstarstarlnu

class BtoD0lnu_HQET(BtoDstarstarlnu):
    def __init__(self, kin_conf, hqet_conf):
        self.params = hqet_conf.params
        self.m_b = hqet_conf.m_b
        self.m_c = hqet_conf.m_c
        self.tau_w1 = self.params[0]
        self.tau_wp = self.params[1]
        self.L = hqet_conf.L
        self.Lps = hqet_conf.Lps
        self.zt_1 = self.params[2]
        self.zt_2 = hqet_conf.zt_2
        self.ce_1 = hqet_conf.ce_1
        self.ce_2 = hqet_conf.ce_2
        self.ce_3 = hqet_conf.ce_3
        self.ce_b = hqet_conf.ce_b
        BtoDstarstarlnu.__init__(self, kin_conf)
        
    def _helamps(self, q2, M2):
        gp, gm = self._ffs(q2, M2)
        
        M = np.sqrt(M2)
        sqrtlam = np.sqrt(lam(M2, q2, self.m_1**2))
        sqrtq2 = np.sqrt(q2)

        fp = ((self.m_1 + M) * gp - (self.m_1 - M) * gm) / (2. * np.sqrt(self.m_1 * M))
        f0 = ((self.m_1 - M) * ((self.m_1 + M) ** 2 - q2) * gp - (self.m_1 + M) * ((self.m_1 - M) ** 2 - q2) * gm) / (2. * (self.m_1 ** 2 - M2) * np.sqrt(self.m_1 * M))

        h0 = sqrtlam * fp / sqrtq2
        ht = (self.m_1 ** 2 - M2) * f0 / sqrtq2
        hp = 0.
        hm = 0.
                          
        return h0, ht, hp, hm

    def _ffs(self, q2, M2):
        w = wcalc(q2, self.m_1, np.sqrt(M2))
        z12 = self.tau_w1 * (1. + self.tau_wp * (w - 1.))
        ec = 0.5 / self.m_c
        eb = 0.5 / self.m_b

        gp = ec * (2. * (w - 1.) * self.zt_1 - 3. * (w * self.Lps - self.L) / (w + 1.)) - eb * ((self.Lps * (2. * w + 1.) - self.L * (w + 2.)) / (w + 1.) - 2. * (w - 1.) * self.zt_1)
        gm = 1. + ec * (6. * self.ce_1 - 2. * (w + 1.) * self.ce_2) + eb * self.ce_b

        return z12 * gp, z12 * gm

class BtoD1plnu_HQET(BtoDstarstarlnu):
    def __init__(self, kin_conf, hqet_conf):
        self.params = hqet_conf.params
        self.m_b = hqet_conf.m_b
        self.m_c = hqet_conf.m_c
        self.tau_w1 = self.params[0]
        self.tau_wp = self.params[1]
        self.L = hqet_conf.L
        self.Lps = hqet_conf.Lps
        self.zt_1 = self.params[2]
        self.zt_2 = hqet_conf.zt_2
        self.ce_1 = hqet_conf.ce_1
        self.ce_2 = hqet_conf.ce_2
        self.ce_3 = hqet_conf.ce_3
        self.ce_b = hqet_conf.ce_b
        BtoDstarstarlnu.__init__(self, kin_conf)

    def _helamps(self, q2, M2):
        gAD1, gV1D1, gV2D1, gV3D1 = self._ffs(q2, M2)
        
        M = np.sqrt(M2)
        sqrtlam = np.sqrt(lam(M2, q2, self.m_1**2))
        sqrtq2 = np.sqrt(q2)

        V = 0.5 * gAD1 * (self.m_1 + M) / np.sqrt(self.m_1 * M)
        A1 = gV1D1 * np.sqrt(self.m_1 * M) / (self.m_1 + M)
        A2 = -0.5 * (self.m_1 + M) * (gV3D1 + M / self.m_1 * gV2D1) / np.sqrt(self.m_1 * M)
        a3f = 0.5 * ((self.m_1 + M) * A1 - (self.m_1 - M) * A2) / M
        A0 = a3f - q2 * (gV3D1 - M / self.m_1 * gV2D1) / (4. * M * np.sqrt(self.m_1 * M))

        h0 = (A1 * (self.m_1 + M) ** 2 * (self.m_1 ** 2 - M2 - q2) - A2 * sqrtlam ** 2) / (2. * M * (self.m_1 + M) * sqrtq2)
        ht = A0 * sqrtlam / sqrtq2
        hp = (A1 * (self.m_1 + M) ** 2 - sqrtlam * V) / (self.m_1 + M)
        hm = (A1 * (self.m_1 + M) ** 2 + sqrtlam * V) / (self.m_1 + M)
                          
        return h0, ht, hp, hm

    def _ffs(self, q2, M2):
        w = wcalc(q2, self.m_1, np.sqrt(M2))
        z12 = self.tau_w1 * (1. + self.tau_wp * (w - 1.))
        ec = 0.5 / self.m_c
        eb = 0.5 / self.m_b

        gAD1p = 1. + ec * ((w * self.Lps - self.L) / (w + 1.) - 2. * self.ce_1) + eb * (self.ce_b + 2. * (w - 1.) * self.zt_1 - (self.Lps * (2. * w + 1.) - self.L * (w + 2.)) / (w + 1.))
        gV1D1p = (w - 1.) + ec * ((w * self.Lps - self.L) - 2. * self.ce_1 * (w - 1.)) - eb * ((self.Lps * (2. * w + 1) - self.L * (w + 2.)) - 2. * self.zt_1 * (w ** 2 - 1.) - self.ce_b * (w - 1.))
        gV2D1p = 2. * ec * (self.zt_1 - self.ce_2)
        gV3D1p = -1. - ec * ((w * self.Lps - self.L) / (w + 1.) + 2. * self.zt_1 - 2. * self.ce_1 + 2. * self.ce_2) + eb * ((self.Lps * (2. * w + 1) - self.L * (w + 2.)) / (w + 1.) - 2. * (w - 1.) * self.zt_1 - self.ce_b)

        return z12 * gAD1p, z12 * gV1D1p, z12 * gV2D1p, z12 * gV3D1p
