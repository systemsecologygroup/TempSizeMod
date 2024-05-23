import numpy as np
import time

import pandas as pd
import xarray as xr
from scipy.interpolate import make_interp_spline

Pnum = 10      # specify the nos of phytoplankton size groups
Ynum = 10       # no. of modeling year
mod_name = 'Mod_proj'

# Import forcing data
wd = 'wd'

LWST = np.genfromtxt(wd+'Final/Temp_final.csv', delimiter=',')
PAR = np.genfromtxt(wd+'Final/PAR_final.csv', delimiter=',')
MLD = np.genfromtxt(wd+'Final/MLD_final.csv', delimiter=',')
PO4 = np.genfromtxt(wd+'Final/PO4_final.csv', delimiter=',')
PO4[:, 1] = PO4[:, 1]*0.010529               # convert from µg L-1 to µmol L-1

"""
Interpolation
"""
LWST_spl = make_interp_spline(LWST[:, 0], LWST[:, 1], k=3)
LWST_spl = LWST_spl(np.arange(365))

PAR_spl = make_interp_spline(PAR[:, 0], PAR[:, 1], k=3)
PAR_spl = PAR_spl(np.arange(365))

from scipy.interpolate import PchipInterpolator
MLD_pchip_spl = PchipInterpolator(MLD[:, 0], MLD[:, 1], axis=0)
MLD_pchip_spl = MLD_pchip_spl(np.arange(365))
MLD_pchip_spl[364] = MLD_pchip_spl[0]

PO4_spl = make_interp_spline(PO4[:, 0], PO4[:, 1], k=3)
PO4_spl = PO4_spl(np.arange(365))


"""
dmdt
"""
dmdt = np.zeros((365))
dmdt[0:364] = np.diff(MLD_pchip_spl)  # dmdt (364,)
dmdt[364] = dmdt[0]

#######
## Setting up temperature increase for different RCP scenarios
temp_incr = [0, 1.4, 2.5, 4.2]
LWST_rcp = np.zeros((365, len(temp_incr)))

for i in range(len(temp_incr)):
    LWST_rcp[:, i] = LWST_spl + temp_incr[i]


#######

LWST_run = np.tile(LWST_rcp, (Ynum, 1))              # change this line for RCP scenarios
PAR_run = np.tile(PAR_spl, Ynum)
mld_run = np.tile(MLD_pchip_spl, Ynum)  # multiplicating physical forcing arrays
dmdt_run = np.tile(dmdt, Ynum)
PO4_run = np.tile(PO4_spl, Ynum)
NO3_run = np.tile(NO3_spl, Ynum)

N0 = np.repeat(0.65, Ynum*365)

sol = np.zeros((Ynum*365, Pnum + 4, len(temp_incr)))  # time; no. var; RCP scenarios


from TSM1_v0_PO4_Q10_final import SizeModLogspace

# Run solution
starttime = time.ctime()        # save it for documentation purposes
print(mod_name, str(Pnum), "start:", starttime)
start = time.time()             # start the timer

for i in range(len(temp_incr)):
    sol[:, :, i] = SizeModLogspace(mld=mld_run, par=PAR_run, sst=LWST_run[:, i], dmdt=dmdt_run, N0=N0, numP=Pnum,
                                   numYears=Ynum, minZ=15, maxZ=200).solution

# Complete
end = time.time()  # stop the timer
endtime = time.ctime()  # save it for documentation purposes
print(mod_name, str(Pnum), "complete:", endtime)
runtime = (end - start) / 3600  # calculate run time (hour)
print(mod_name, str(Pnum), "run time(hour):", runtime)
print(mod_name, str(Pnum), "run time(day):", runtime/24)


# Storing output
out = xr.Dataset(
    {'Nut': (['time', 'RCP'], sol[:, 0, :]),
     'Zoo': (['time', 'ZooSize', 'RCP'], sol[:, 1:3, :]),
     'Phy': (['time', 'PhySize', 'RCP'], sol[:, 4:4+Pnum*1, :])},
    coords={'time': np.arange(Ynum*365),
            'ZooSize': [20, 400],
            'PhySize': np.logspace(0, np.log10(150), Pnum),
            'RCP': [0, 1.4, 2.5, 4.2]},
    attrs={'Title': 'This file contains sol output with different nutrient and mixing regimes',
           'No. phytoplankton size group': Pnum,
           'LWST units': 'Degree celcius',
           'PAR units': 'Ein m$^{-2}$ d$^{-1}$',
           'MLD units': 'Meters',
           'Variable units': 'µmol P L$^{-1}$',
           'Size units': 'µm ESD',
           'Phyto size range': '1 - 150',
           'Zoo size range': '20 - 400'})
out.to_netcdf(wd + 'output_proj.nc')  # export



