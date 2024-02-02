"""
Generate temperature forcing from observation data of Greifensee
"""
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

wd = 'your wd'

data = pd.read_csv(wd+'/Original_forc_data.csv')
data_temp = data[['date', 'water_temp']]


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
for i in range(len(data_temp)):
    jday = np.append(jday, datestdtojd(data_temp['date'][i]))
data_temp.insert(1, 'Julian day', pd.DataFrame(jday))

#---------------------------------------------------------------------
data['month'] = pd.DatetimeIndex(data['date']).month
dayno = np.array([1., 32., 60., 91., 121., 152., 182., 213., 244., 274., 305., 335])
dayno_used = np.array([16,  47,  75, 106, 136, 167, 197, 228, 259, 289, 320, 350])

"""
Temperature
1. taking the mean from each julian day
2. taking the mean from each month
3. interpolate a function based on 12-month data points
"""

temp = data_temp.groupby(['Julian day'], as_index=False)['water_temp'].mean()

# adding the column month from julian day
temp.insert(1, 'year_fool', np.repeat(2000, len(temp)))
temp['date_fool'] = pd.to_datetime(temp['year_fool'], format='%Y') + pd.to_timedelta(temp['Julian day'], unit='D') - pd.Timedelta('1D')
temp['month'] = pd.DatetimeIndex(temp['date_fool']).month

temp_mean = temp.groupby(['month'], as_index=False)['water_temp'].mean().to_numpy()

#### Interpolation ####
from scipy.interpolate import make_interp_spline
ext_time = np.append(np.append(dayno+15, 365+dayno+15), 365*2+dayno+15)
Temp_pchip = make_interp_spline(ext_time, np.tile(temp_mean[:, 1], 3), k=3)
Temp_pchip_spl = Temp_pchip(np.arange(365*3))
Temp_pchip_spl = Temp_pchip_spl[365:730]        # we select the middle year for a smoother forcing

temp_val = []
for i in range(len(dayno_used)):
    temp_val = np.append(temp_val, Temp_pchip_spl[dayno_used[i]])

###################
fig, axs = plt.subplots(figsize=(8, 4))
fig.subplots_adjust(wspace=0.2, hspace=0.1, left=0.1, right=0.95, top=0.95, bottom=0.15)

axs.scatter(x=data_temp['Julian day'], y=data_temp['water_temp'], s=15, color='steelblue', lw=0.25, ec='k', label='data')
axs.plot(np.arange(365), Temp_pchip_spl, color='r', lw=2.5, label='forcing')
# axs.plot(dayno+15, temp_mean[:, 1], color='r', lw=2)
axs.set_ylabel('Photic zone water temperature', fontsize=12)
axs.set_xlim(0, 365)
axs.set_ylim(0, 25)
axs.set_xticks([1., 32., 60., 91., 121., 152., 182., 213., 244., 274., 305., 335])
axs.set_xticklabels(['J', 'F', 'M', 'A', 'M', 'J', 'J', 'A', 'S', 'O', 'N', 'D'])
axs.set_xlabel('Month', fontsize=12, labelpad=10)
axs.legend(loc=2)

plt.savefig(fname=wd + '/Temp_final.png', dpi=800)

## save csv, save points and interpolate again in the run script
Temp_pt = np.vstack((dayno_used, temp_val)).T
np.savetxt(wd+"/Temp_final.csv", Temp_pt, delimiter=",")
