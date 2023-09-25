import os
import numpy as np
import time
import xarray as xr
from scipy.interpolate import make_interp_spline

Pnum = 30       # specify the nos of phytoplankton size groups
Ynum = 10       # no. of modeling year

# Import forcing data
wd = '/Users/szewing/Desktop/PhD_work/3. ThermalTrait/TempSizeMod_TSM'  # '/people/home/sto/SizeMod'
os.chdir(wd)

# Temperature and PAR data
LWST_CTD = np.genfromtxt('Forcing/TempForc_CTD.csv', delimiter=',')
# LWST_8 = np.genfromtxt('Forcing/TempForc.csv', delimiter=',')
nSSI = np.genfromtxt('Forcing/nSSI_13p_syn.csv', delimiter=',')
MLD = np.genfromtxt('Forcing/MLDForc_Theoretical.csv', delimiter=',')

for a in range(8):  # To synchonized the initial and end forcing value
    nSSI[0, a + 1] = nSSI[12, a + 1]


# Converting nSSI into PAR
def nSSI2PAR(netSSI):
    """
    This function is to convert nSSI (W m-2) into PAR (Ein m-2 d-1)
    PAR is a term used to describle radiation in wavelengths usedful for photosynthesis [1]
    PAR is generally accepted to be wavelengths between 400 and 700 nm [1]
    Procedure:
    1. extr = extraction factor (only about 45% of the nSSI is in the 400-700nm range, Howell et al. 1983)
    2. conv = conversion factor from W m-2 to Ein m-2 d-1 (Lampert and Sommer, 2007, pp.20)**
    ** see PAR_UnitConversion.docx
    """
    extr = 0.45
    conv = 0.432
    return netSSI * extr * conv


PAR = nSSI2PAR(nSSI)
PAR[:, 0] = nSSI[:, 0]

# Creating forcing curves
PAR_spl = make_interp_spline(PAR[:, 0], PAR[:, 5], k=2)
PAR_spl = PAR_spl(np.arange(365))
PAR_spl[364] = PAR_spl[0]

# generate dmdt arrays
dmdt = np.zeros(365)
dmdt[0:364] = np.diff(MLD[:])
dmdt[364] = dmdt[0]

MLD_run = np.tile(MLD, Ynum)
dmdt_run = np.tile(dmdt, Ynum)
LWST_CTD_spl = np.tile(LWST_CTD, Ynum)
PAR_spl = np.tile(PAR_spl, Ynum)

# Runs - loop
N0_list = np.array([0.01, 0.1, 1])         # equivalent to 0.03, 0.3, 3 µmol PO4 L-1 ( x 95 to convert to µg)
Z1_size = np.array([5, 20, 150])
Z1_GrazStrtgy = np.array([0.2, 0.5])      # specialist or generalist
########################################################
sol = np.zeros((Ynum*365, 4 + Pnum + (5*Pnum), len(N0_list), len(Z1_size), len(Z1_GrazStrtgy)))

mod_name = 'TSM_flux_theor' + str(Ynum) + 'yr'

from TheoMod import SizeModLogspace

# Run solution
starttime = time.ctime()  # save it for documentation purposes
print(mod_name, "start:", starttime)
start = time.time()  # start the timer
for i in range(len(N0_list)):  # nutrient level
    for j in range(len(Z1_size)):
        for k in range(len(Z1_GrazStrtgy)):
            sol[:, :, i, j, k] = SizeModLogspace(mld=MLD_run, par=PAR_spl, sst=LWST_CTD_spl, dmdt=dmdt_run, N0=N0_list[i],
                                                 numP=Pnum, numYears=Ynum, minZ=Z1_size[j], SizeTol=[Z1_GrazStrtgy[k], 0.5]).solution

end = time.time()  # stop the timer
endtime = time.ctime()  # save it for documentation purposes
print(mod_name, "complete:", endtime)
