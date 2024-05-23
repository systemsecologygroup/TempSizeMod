import pdb

import numpy as np
from scipy.integrate import odeint


class SizeModLogspace:
    """
    Size-based model
    Model has multiple groups of phytoplankton, two groups of zooplankton in different sizes, one nutrient source,
    and a detritus community.

    Model assumption:
    - thermal response of the phytoplankton follows a unimodal curve adapted from Norberg (2004)
    - the maximum growth of phytoplankton follows an allometric relationship taken from data compilations of Edwards et al. (2012)
    - phytoplankton nutrient uptake follows Michelis-Menton kinetics
    - the half-saturation constant of the uptake kinetics derived from a community mean value and is not size-dependent
    - phytoplankton are grazed by size-selective zooplankton, small phytoplankton are grazed more intensively
    - zooplankton graze on a wide size-feeding range; small zooplankton has a narrower range than large zooplankton in absolute values
    - zooplankton grazing is scaled by a Q10 factor
    -------
    Flexible parameters:
        - n0
        - prey tolerance
        - P size range
        - Z size range
        - no. of P size classes
        - no. of years for model running

    Fixed parameters:
        - Community mean Kn
        - Allometric parameters for Mu
        - Allometric parameters for Topt
        - Allometric parameters for Imax
        - Allometric parameters for grazing size preference
        - Model params
    """

    def __init__(self, mld, par, sst, dmdt, N0, minP=0, maxP=np.log10(200), numP=15, minZ=20, maxZ=600, numZ=2, numYears=5,
                 Zsmall0=6.25e-4, Zlarge0=6.25e-4, D0=6.25e-4, Mz2S0=0, Mz2L0=0,
                 Pmax=1.1, Kpar=0.1, alpha=0.02, Mz=0.1, Mp=0.1, Mz2=0.34,
                 Ieff=0.75, beta=0.69, Kp=0.19, Rem=0.15, k=0.1,
                 mu_alpha=-0.36, mu_beta=10 ** 0.69, Kn=0.06,
                 sig_T=12.5, topt=13, graz_Q10=2.8,   #sig_T=12.5, topt=16.5
                 graz_alpha=-0.28, graz_beta=23, ops_alpha=0.7, ops_beta=0.45,
                 SizeTol=[0.435, 0.6]):
        self.mld = mld
        self.par = par  # photosynethically activated radiation (E*m^-2*d^-1)
        self.sst = sst  # sea surface temperature/lake surface water temperature (LSWT)
        self.dmdt = dmdt  # dmdt
        self.N0 = N0  # Initial nutrient concentrations (µmol P*L^-1)
        self.minP = minP  # min. size of P size range
        self.maxP = maxP  # max. size of P size range
        self.numP = numP  # number of phytoplankton size class
        self.minZ = minZ  # min. size of Z size range
        self.maxZ = maxZ  # max. size of Z size range
        self.numZ = numZ  # number of zooplankton size class
        self.numYears = numYears  # Number of years for model run
        self.Zsmall0 = Zsmall0  # Initial Zsmall concentration (µmol P*L^-1)
        self.Zlarge0 = Zlarge0  # Initial Zlarge concentration (µmol P*L^-1)
        self.D0 = D0  # Initial detritus concentration (µmol P*L^-1)
        self.Ps0 = np.repeat(6.25e-4, self.numP, axis=0)  # Initial P concentration (µmol P*L^-1)
        self.muP0 = np.repeat(0, self.numP, axis=0)  # Initial concentration for growth fluxes (µmol P*L^-1)
        self._2ZS0 = np.repeat(0, self.numP, axis=0)  # Initial concentration for Z1 grazing fluxes (µmol P*L^-1)
        self._2ZL0 = np.repeat(0, self.numP, axis=0)  # Initial concentration for Z2 grazing fluxes (µmol P*L^-1)
        self.Mz2S0 = Mz2S0
        self.Mz2L0 = Mz2L0
        self.Pmax = Pmax  # Max photosynthesis rate
        self.Kpar = Kpar  # Water attenuation coefficient
        self.alpha = alpha  # Initial slope of P-I curve
        self.Mz = Mz  # Natural mortality - Zooplankton
        self.Mp = Mp  # Natural mortality - Phytoplankton
        self.Mz2 = Mz2  # Mortality from upper predators
        self.Ieff = Ieff  # Ingestion efficiency
        self.beta = beta  # Assimlation efficiency
        self.Kp = Kp  # Phytoplankton half-saturation constant (µmol P*L^-1)
        self.Rem = Rem  # Remineralization rate (day^-1)
        self.k = k  # Cross thermocline mixing factor (m/day)
        self.mu_alpha = mu_alpha  # Slope of allometric max. uptk rate
        self.mu_beta = mu_beta  # Intercept of allometric max. uptk rate
        self.Kn = Kn  # nutrient half-saturation constant for phytoplankton
        self.sig_T = sig_T  # community mean thermal tolerance breadth width as per Thomas et al. (2015)
        self.topt = topt    # optimal growth temperature
        self.graz_alpha = graz_alpha  # Slope of allometric max. grazing rate (day^-1)
        self.graz_beta = graz_beta  # Intercept of allometric max.grazing rate (day^-1)
        self.ops_alpha = ops_alpha  # Slope of allometric optimum prey size
        self.ops_beta = ops_beta  # Intercept of allometric optimum prey size
        self.SizeTol = SizeTol  # Prey size tolerance (should be an array)
        self.graz_Q10 = graz_Q10  # Q10 temperature for grazing
        self.init_con = np.concatenate(([self.N0[0]],  # N0
                                        [self.Zsmall0],  # Zsmall0
                                        [self.Zlarge0],  # Zlarge0
                                        [self.D0],      # D0
                                        [self.Ps0],     # Ps0
                                        [self.muP0],
                                        [self._2ZS0],
                                        [self._2ZL0],
                                        [self.Mz2S0],
                                        [self.Mz2L0]), axis=None)
        self.t_array = np.arange(0, 365 * self.numYears)  # Time array
        self.Psize_array = np.logspace(self.minP, self.maxP, num=self.numP, base=10)  # Size array for phytoplankton
        self.Zsize_array = np.linspace(self.minZ, self.maxZ, self.numZ)  # Size array for zooplankton
        self.solution = odeint(self.AlloNPsZD, self.init_con, self.t_array, rtol=1.e-10, atol=1.e-10)   #, hmax=1, hmin=1)

    def Vol2ESD(self, v):  # Vol2ESD(1) = 1.2407
        esd = ((v * 6) / np.pi) ** (1 / 3)
        return esd

    def Allo_mumax(self, PhySize):
        return self.mu_beta * ((PhySize / self.Vol2ESD(1)) ** self.mu_alpha)

    def NU(self, nut):
        """
        Michelis-Menton uptake
        :param nut:
        :return:
        """
        return nut / (nut + self.Kn)

    def temp_dependence(self, time):
        """
        Eppley-Norberg formulation
        :param time: timestep to derive temperature
        :return:
        """
        b_eppley = 0.0633
        thermtol = (1 - ((time - self.topt) / self.sig_T) ** 2) * np.exp(b_eppley * time)
        return thermtol

    def LightLim(self, I, Z):
        """
        Light limitation function on photosynthesis based on Smith's function,
        illustrated by a P-I curve
        """
        I0 = I
        Iz = I0 * np.exp(-self.Kpar * Z)
        LL = (((self.Pmax / (self.Kpar * Z)) * np.log((self.alpha * I0 + np.sqrt((self.Pmax ** 2) +
                                                                                 (self.alpha * I0) ** 2)) / ((self.alpha * Iz) +
                                                                                                             np.sqrt(self.Pmax ** 2 + (self.alpha * Iz) ** 2)))))
        return LL

    def Imax_Q10(self, time):
        """
        Q10 method based on Sherman et al. (2016) Global Biogeochemical Cycles, 30(4)
        -----------------------------------------------------------------------------------
        T0: reference temperature, adopted as 303.15K (30 degree Celcius)
        Q10: the factor change in growth rate for a 10 degree change in temperature
        :param time: timestep
        :return: size- and temperature- dependent grazing rates
        """
        ref_temp = 15          # reference temperature
        # G0 = 0.57             # (marine zooplankton: Sherman et al., 2016):: we use size-dependent grazing rates
        # Q10 = 1.47           # (marine zooplankton: Sherman et al., 2016)
        # Q10 = 2.4             # Durbin and Durbin (1992)
        # Q10 = 3.9             # Kiørboe et al. (1982)
        # Q10 = 2.8             # Hansen et al. (1997) & Gosselain et al. (1996)
        return self.graz_Q10 ** ((time - ref_temp) / 10)

    def AlloImax(self, ZooSize, time):
        """
        Max. ingestion rate also depends on the size of the zooplankton
        ----------
        graz_alpha = -0.4  # Hansen et al. 1994, Banas, 2011
        graz_beta = 26  # Hansen et al. 1994, Banas, 2011 [day^-1]
        """
        imax = self.graz_beta * ((ZooSize / 1) ** self.graz_alpha)
        return self.Imax_Q10(time) * imax

    def AllogpP(self, PhySize, ZooSize, SizeTol):
        """
        Selected zooplankton size class of 10 & 200[µm]
        """
        OPS = self.ops_beta * ((ZooSize / 1) ** self.ops_alpha)                             # µm ESD
        gpP = np.exp(-((np.log10(PhySize) - np.log10(OPS)) / SizeTol) ** 2)
        return gpP

    def AlloGraz(self, PhySize, ZooSize, Pi, SizeTol, denom, time):
        """
        PhySize  = Size class/array of phytoplankton population;
        ZooSize = Size class/array of zooplankton population;
        Pi 	 	 = Phytoplankton biomass
        """
        graz = self.AlloImax(ZooSize, time) * ((self.AllogpP(PhySize, ZooSize, SizeTol) * Pi) / (self.Kp + denom))
        return graz

    def mixing(self, time):
        """k refers to the cross thermocline mixing factor"""
        return (self.k + max(self.dmdt[time], 0.)) / self.mld[time]

    def AlloNPsZD(self, y, t):
        """
        A size-based trophic model with multiple phytoplankton and zooplankton size class
        ----------
        y: array of initial conditions of state variables (var)
        t: time array
        """
        # Initialization
        N = y[0]
        Zsmall = y[1]
        Zlarge = y[2]
        D = y[3]
        Ps = y[4:4+self.numP*1]
        flux_muP = y[4+self.numP*1:4+self.numP*2]
        flux_2ZS = y[4+self.numP*2:4+self.numP*3]
        flux_2ZL = y[4 + self.numP * 3:4 + self.numP * 4]
        Mz2_ZS = y[4 + self.numP * 4 + 0]
        Mz2_ZL = y[4 + self.numP * 4 + 1]
        var = np.zeros(len(y))
        t = int(t)

        # non-P dependent equations
        """
        Zsmall = specialist, narrower size tolerance factor;
        Zlarge = generalist, wider size tolerance factor.
        """
        Graz_denomZsmall = np.sum(self.AllogpP(self.Psize_array, self.Zsize_array[0], self.SizeTol[0]) * Ps)
        Graz_denomZlarge = np.sum(self.AllogpP(self.Psize_array, self.Zsize_array[1], self.SizeTol[1]) * Ps)
        Mz2_ZS = self.Mz2 * (Zsmall ** 2)
        Mz2_ZL = self.Mz2 * (Zlarge ** 2)

        # [dNdt]
        var[0] = (self.Rem * D  # Remineration
                  + self.mixing(t) * (self.N0[t] - N))  # MixingN

        # [dZ1dt]
        var[1] = (- self.Mz * Zsmall  # Natural mortality Z1
                  - Mz2_ZS  # density-dependent top predator grazing Z1
                  - (self.dmdt[t] / self.mld[t]) * Zsmall)  # Mixing loss Z1

        # [dZ2dt]
        var[2] = (- self.Mz * Zlarge  # Natural mortality Z2
                  - Mz2_ZL  # Top predator grazing Z2
                  - (self.dmdt[t] / self.mld[t]) * Zlarge)  # Mixing loss Z2

        # [dDdt]
        var[3] = (self.Mz * (Zsmall + Zlarge)  # MortalityZsmall+Zlarge
                  - self.Rem * D  # Remineration
                  - self.mixing(t) * D)  # Mixing loss D

        # P-dependent (loop)
        for i in range(len(Ps)):
            """
            Psize = Size class/array of phytoplankton population;
            """
            P = Ps[i]  # define P in the loop
            Psize = self.Psize_array[i]     # define Psize in the loop
            flux_muP = (self.Allo_mumax(Psize) * self.temp_dependence(self.sst[t])) * self.NU(N) * self.LightLim(self.par[t], self.mld[t]) * P
            # flux_mu_temp = self.temp_dependence(self.sst[t])
            # flux_mu_nut = self.NU(N)
            flux_2ZS = self.beta * self.Ieff * self.AlloGraz(Psize, self.Zsize_array[0], P, self.SizeTol[0], Graz_denomZsmall, self.sst[t]) * Zsmall
            flux_2ZL = self.beta * self.Ieff * self.AlloGraz(Psize, self.Zsize_array[1], P, self.SizeTol[1], Graz_denomZlarge, self.sst[t]) * Zlarge

            # [dNdt]
            var[0] = (var[0]
                      - flux_muP
                      + (self.beta * (1. - self.Ieff) * self.AlloGraz(Psize, self.Zsize_array[0], P, self.SizeTol[0], Graz_denomZsmall, self.sst[t])) * Zsmall
                      # Excretion from grazing(Zsmall))
                      + (self.beta * (1. - self.Ieff) * self.AlloGraz(Psize, self.Zsize_array[1], P, self.SizeTol[1], Graz_denomZlarge, self.sst[t])) * Zlarge)
                      # Excretion from grazing(Zlarge))

            # [dZ1dt]
            var[1] = (var[1]
                      + flux_2ZS)  # GrazingP from Zsmall

            # [dZ2dt]
            var[2] = (var[2]
                      + flux_2ZL)  # GrazingP from Zlarge

            # [dDdt]
            var[3] = (var[3]
                      + ((1. - self.beta) * self.AlloGraz(Psize, self.Zsize_array[0], P, self.SizeTol[0], Graz_denomZsmall, self.sst[t])) * Zsmall  # SloppyfeedP - Zsmall
                      + ((1. - self.beta) * self.AlloGraz(Psize, self.Zsize_array[1], P, self.SizeTol[1], Graz_denomZlarge, self.sst[t])) * Zlarge  # SloppyfeedP - Zlarge
                      + self.Mp * P)

            # [dPsdt]
            var[4 + i] = (var[4 + i]
                          + flux_muP  # Uptk
                          - self.Mp * P  # MortalityP
                          - self.AlloGraz(Psize, self.Zsize_array[0], P, self.SizeTol[0], Graz_denomZsmall, self.sst[t]) * Zsmall  # GrazingP from Zsmall
                          - self.AlloGraz(Psize, self.Zsize_array[1], P, self.SizeTol[1], Graz_denomZlarge, self.sst[t]) * Zlarge  # GrazingP from Zlarge
                          - self.mixing(t) * P)  # Mixing

            # growth fluxes
            var[4 + self.numP*1 + i] = var[4 + self.numP*1 + i] + flux_muP

            # grazing fluxes
            var[4 + self.numP*2 + i] = var[4 + self.numP*2 + i] + flux_2ZS
            var[4 + self.numP*3 + i] = var[4 + self.numP*3 + i] + flux_2ZL

            # predatory fluxes
            var[4 + self.numP*4 + 0] = Mz2_ZS
            var[4 + self.numP * 4 + 1] = Mz2_ZL
        #pdb.set_trace()
        return var
