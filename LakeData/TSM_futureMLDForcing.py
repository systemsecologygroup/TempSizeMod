"""
Produce environmental forcing for a hypothesized future MLD
"""
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

wd = 'your wd'

data_mld = pd.read_csv(wd+'/RawData_MLD.csv')

#---------------------------------------------------------------------
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
for i in range(len(data_mld)):
    jday = np.append(jday, datestdtojd(data_mld['date'][i]))
data_mld.insert(1, 'Julian day', pd.DataFrame(jday))                             # phychem data


"""
Mixed Layer Depth (MLD)
1. taking the mean for each julian day
2. taking the mean for each month
3. interpolate a function based on 12-month data points
"""
mld_GR = data_mld.groupby('Julian day', as_index=False)['thermocl'].median().to_numpy()

condlist = [0., 32., 75., 100., 121., 152., 182., 213., 244., 274., 305., 330., 345, 365]
condlist_future = [0., 32., (75.-22.), (100.-22.), 121., 152., 182., 213., 244., 274., 305, (330.+11.), (345.+11.), 365]
# approximated julian day of the first day of each month*

# there are more noise in MLD, so we did some manipulation from visual inspection
extrct_GR_mld = np.zeros((len(condlist), 2))
extrct_GR_mld[:, 0] = condlist
extrct_GR_mld[0:3, 1] = np.repeat(30, 3)
extrct_GR_mld[3:, 1] = np.array([3, 4, 5, 6, 7, 8, 9, 12, 18, 30, 30])

extrct_GR_futmld = np.zeros((len(condlist_future), 2))
extrct_GR_futmld[:, 0] = condlist_future
extrct_GR_futmld[0:3, 1] = np.repeat(30, 3)
extrct_GR_futmld[3:, 1] = np.array([3, 4, 5, 6, 7, 8, 9, 10, 18, 30, 30])


from scipy.interpolate import PchipInterpolator
MLD_pchip_GR = PchipInterpolator(extrct_GR_mld[:, 0], extrct_GR_mld[:, 1], axis=0)
MLD_pchip_GR_spl = MLD_pchip_GR(np.arange(365))

futMLD_pchip_GR = PchipInterpolator(extrct_GR_futmld[:, 0], extrct_GR_futmld[:, 1], axis=0)
futMLD_pchip_GR_spl = futMLD_pchip_GR(np.arange(365))


# Detailed plot
fig, axs = plt.subplots(figsize=(8, 4))
fig.subplots_adjust(wspace=0.2, hspace=0.1, left=0.1, right=0.95, top=0.95, bottom=0.15)

axs.plot(np.arange(365), MLD_pchip_GR_spl, color='k', lw=2.5, zorder=2, label='Standard MLD')
axs.plot(np.arange(365), futMLD_pchip_GR_spl, color='r', lw=2.5, zorder=2, label='Hypothesized MLD')
axs.axis([0, 365, 35, 0])
axs.set_ylabel('Mixed layer depth, MLD (m)', fontsize=12, labelpad=10)
axs.set_xlabel('Month', fontsize=12, labelpad=10)
axs.legend(loc=4, fontsize=12, ncol=1, bbox_to_anchor=(0.9, 0))
axs.set_xticks([1., 32., 60., 91., 121., 152., 182., 213., 244., 274., 305., 335])
axs.set_xticklabels(['J', 'F', 'M', 'A', 'M', 'J', 'J', 'A', 'S', 'O', 'N', 'D'], fontsize=12)


## save to csv
futMLD_pt = np.vstack((extrct_GR_futmld[:, 0], extrct_GR_futmld[:, 1])).T
np.savetxt(wd+"TempSizeMod_TSM/Forcing/Final/futMLD_final.csv", futMLD_pt, delimiter=",")
