"""
Generate PAR (irradiance) forcing from observation data of Greifensee
irradiance is measured by the unit of W m-2
"""
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

wd = 'your wd'

data = pd.read_csv(wd+'/Original_Temp+PAR.csv')
data_nSSI = data[['date', 'global_radiation']]


# convert real data to julian day (0-365)
import datetime

def datestdtojd(stddate):
    """
    source: https://rafatieppo.github.io/post/2018_12_01_juliandate/
    :param stddate: standard date for input
    :return:
    """
    fmt = '%Y-%m-%d'
    sdtdate = datetime.datetime.strptime(stddate, fmt)
    sdtdate = sdtdate.timetuple()
    jdate = sdtdate.tm_yday
    return jdate

jday = np.array([])
for i in range(len(data_nSSI)):
    jday = np.append(jday, datestdtojd(data_nSSI['date'][i]))
data_nSSI.insert(1, 'Julian day', pd.DataFrame(jday))                             # phychem data


#---------------------------------------------------------------------
data['month'] = pd.DatetimeIndex(data['date']).month
dayno = np.array([1., 32., 60., 91., 121., 152., 182., 213., 244., 274., 305., 335])
dayno_used = np.array([16,  47,  75, 106, 136, 167, 197, 228, 259, 289, 320, 350])


"""
Irradiance
1. taking the interquartile range at 75% for each julian day
2. taking the monthly mean of the daily interquantile
3. calculating PAR
5. interpolate a function based on 12-month data points
"""
nSSI_quart = data.groupby(['Julian day'], as_index=False)['global_radiation'].quantile(0.75)

# adding the column month from julian day
nSSI_quart.insert(1, 'year_fool', np.repeat(2000, len(nSSI_quart)))
nSSI_quart['date_fool'] = pd.to_datetime(nSSI_quart['year_fool'], format='%Y') + pd.to_timedelta(nSSI_quart['Julian day'], unit='D') - pd.Timedelta('1D')
nSSI_quart['month'] = pd.DatetimeIndex(nSSI_quart['date_fool']).month
nSSI_quart_month = nSSI_quart.groupby(['month'], as_index=False)['global_radiation'].mean().to_numpy()


def nSSI2PAR(netSSI):
    """
    This function is to convert nSSI (W m-2) into PAR (E m-2 d-1)
    Procedure:
    1. extr = extraction factor (only about 45% of the nSSI is in the 400-700nm range, Howell et al. 1983)
    2. conv = conversion factor from W m-2 to Ein m-2 d-1 (Lampert and Sommer, 2007, pp.20)**
    ** further details please see PAR_UnitConversion.docx
    """
    extr = 0.45
    conv = 0.432
    return netSSI * extr * conv

#### Interpolation ####
from scipy.interpolate import make_interp_spline
PAR_pchip = make_interp_spline(dayno+15, nSSI2PAR(nSSI_quart_month[:, 1]), k=3)
PAR_pchip_spl = PAR_pchip(np.arange(365))
###################

fig, axs = plt.subplots(figsize=(8, 4))
fig.subplots_adjust(wspace=0.2, hspace=0.1, left=0.1, right=0.95, top=0.95, bottom=0.15)

axs.scatter(x=data_nSSI['Julian day'], y=nSSI2PAR(data_nSSI['global_radiation']), s=15, color='steelblue', lw=0.25, ec='k')
axs.set_ylabel('PAR (Ein m$^{-2}$ d$^{-1}$)', fontsize=12)
axs.plot(np.arange(365), PAR_pchip_spl, color='r', lw=2.5, label='forcing')
axs.set_xlim(0, 365)
axs.set_ylim(0, 80)
axs.set_xticks([1., 32., 60., 91., 121., 152., 182., 213., 244., 274., 305., 335])
axs.set_xticklabels(['J', 'F', 'M', 'A', 'M', 'J', 'J', 'A', 'S', 'O', 'N', 'D'])
axs.set_xlabel('Month', fontsize=12, labelpad=10)
axs.legend(loc=1, fontsize=12)

plt.savefig(fname=wd + '/PAR_final.png', dpi=800)

## save csv, save points and interpolate again in the run script
PAR_pt = np.vstack((dayno+15, nSSI2PAR(nSSI_quart_month[:, 1]))).T
np.savetxt(wd+"TempSizeMod_TSM/Forcing/Final/PAR_final.csv", PAR_pt, delimiter=",")



