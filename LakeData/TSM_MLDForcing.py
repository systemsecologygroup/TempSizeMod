"""
Generate MLD forcing from observation data of Greifensee
"""
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

wd = 'your wd'

data_mld = pd.read_csv(wd+'/Original_MLD.csv')

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

#---------------------------------------------------------------------
"""
Mixed Layer Depth (MLD)
1. taking the mean for each julian day
2. taking the mean for each month
3. interpolate a function based on 12-month data points
"""
mld_GR = data_mld.groupby('Julian day', as_index=False)['thermocl'].median().to_numpy()

condlist = [0., 32., 70., 90., 121., 152., 182., 213., 244., 274., 305., 330., 345, 365]

# there are noise in MLD data, so we did some manipulation from visual inspection
extrct_GR_mld = np.zeros((len(condlist), 2))
extrct_GR_mld[:, 0] = condlist
extrct_GR_mld[0:2, 1] = np.repeat(30, 2)
extrct_GR_mld[2:, 1] = np.array([12, 3, 4, 5, 6, 7, 8, 9, 12, 18, 30, 30])


## Quick plot
fig, axs = plt.subplots(1, 1, figsize=(7, 4), sharex='all')
fig.subplots_adjust(wspace=0.3, hspace=0.12, left=0.1, right=0.96, top=0.9, bottom=0.2)
axs.scatter(mld_GR[:, 0], mld_GR[:, 1], s=15, color='gray')
axs.scatter(extrct_GR_mld[:, 0], extrct_GR_mld[:, 1], s=25, color='r')
axs.axis([0, 365, 35, -1])
axs.set_xlabel('day', labelpad=10)
axs.set_ylabel('MLD', labelpad=10)

from scipy.interpolate import PchipInterpolator
MLD_pchip_GR = PchipInterpolator(extrct_GR_mld[:, 0], extrct_GR_mld[:, 1], axis=0)
MLD_pchip_GR_spl = MLD_pchip_GR(np.arange(365))

# Detailed plot
fig, axs = plt.subplots(figsize=(8, 4))
fig.subplots_adjust(wspace=0.2, hspace=0.1, left=0.1, right=0.95, top=0.95, bottom=0.15)

axs.plot(np.arange(365), MLD_pchip_GR_spl, color='r', lw=2.5, zorder=2, label='forcing')
axs.scatter(mld_GR[:, 0], mld_GR[:, 1], s=15, facecolor='steelblue', edgecolor='k', lw=0.25, zorder=1, label='data')
# axs.scatter(extrct_GR_mld[:, 0], extrct_GR_mld[:, 1], s=50, color='r', lw=1, edgecolor='k', zorder=3,
#             label='Extracted lake median')
axs.axis([0, 365, 35, -1])
axs.set_ylabel('Mixed layer depth, MLD (m)\nGreifen', fontsize=12, labelpad=10)
axs.set_xlabel('Month', fontsize=12, labelpad=10)
axs.legend(loc=4, fontsize=9, ncol=1, bbox_to_anchor=(0.9, 0))
axs.set_xticks([1., 32., 60., 91., 121., 152., 182., 213., 244., 274., 305., 335])
axs.set_xticklabels(['J', 'F', 'M', 'A', 'M', 'J', 'J', 'A', 'S', 'O', 'N', 'D'], fontsize=12)

plt.savefig(fname=wd + '/MLD_final.png', dpi=800)

## save csv, save points and interpolate again in the run script
MLD_pt = np.vstack((extrct_GR_mld[:, 0], extrct_GR_mld[:, 1])).T
np.savetxt(wd+"/MLD_final.csv", MLD_pt, delimiter=",")
