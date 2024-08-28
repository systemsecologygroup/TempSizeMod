"""
[Include colonial large species]
Plotting selected plankton data in Greifensee (data source: Eawag)
- annual composite
"""
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib import cm

wd = 'your wd'

#### Selection of zooplantkon data ####
# We chose the more abundant zooplantkon species that are
# 1. mostly herbivores (non-carnivores and consume autotrophs)
# 2. non-predatory species
# p.s. The model does not consider intra-guild predation; there are certain trophic links unable to capture.

## For phytoplankton, we use only the ROIs and the bio-area data (see flow chart)
phydata = pd.read_csv(wd + '/raw_NPdata.csv', sep=',',
                      usecols=['date',
                   'dinobryon_ROIs', 'dinobryon_area_log10_mm2',
                   'uroglena_ROIs', 'uroglena_area_log10_mm2',
                   'centric_diatom_ROIs', 'centric_diatom_area_log10_mm2',
                   'cryptophyceae_ROIs', 'cryptophyceae_area_log10_mm2',
                   'rhodomonas_ROIs', 'rhodomonas_area_log10_mm2',
                   'chlorophytes_ROIs', 'chlorophytes_area_log10_mm2'])

## For zooplankton, we use major axis length and minor axis length for ciliates and major axis length for daphnia
zoodata_used = pd.read_csv(wd + '/raw_NPdata.csv', sep=',',
                           usecols=['date', 'daphnia_ROIs', 'daphnia_area_log10_mm2', 'daphnia_MaL_mm', 'daphnia_MiL_mm',
                                    'ciliates_ROIs', 'ciliates_area_log10_mm2', 'ciliates_MaL_mm', 'ciliates_MiL_mm'])

## set name
physpecies = ['dinobryon', 'uroglena', 'centric_diatom', 'cryptophyceae', 'rhodomonas', 'chlorophytes']
zoospecies_used = ['daphnia', 'ciliates']


## bio-area unit conversion
def logArea2μmArea(LnArea):
    """
    The conversion of raw data from the underwater camera to μm ESD
    :param LnArea: log10 cell area (mm2)
    :return: μm2 bio-area
    """
    mm_sq2μm_sq = 1e6
    return (10 ** LnArea) * mm_sq2μm_sq


# adjusting the data units
for i in range(len(physpecies)):
    phydata.insert(1 + i, physpecies[i] + '_area_μm2', logArea2μmArea(phydata[physpecies[i] + '_area_log10_mm2']))

for i in range(len(zoospecies_used)):
    zoodata_used.insert(1 + i, zoospecies_used[i] + '_area_μm2', logArea2μmArea(zoodata_used[zoospecies_used[i] + '_area_log10_mm2']))

for i in range(len(zoospecies_used)):
    zoodata_used.insert(1+len(zoospecies_used) + i, zoospecies_used[i] + '_MaL_μm', zoodata_used[zoospecies_used[i] + '_MaL_mm'] * 1e3)

for i in range(len(zoospecies_used)):
    zoodata_used.insert(1+len(zoospecies_used)*2 + i, zoospecies_used[i] + '_MiL_μm', zoodata_used[zoospecies_used[i] + '_MiL_mm'] * 1e3)



# The ROIs data refers to region of interest (ROI), it is taken by the underwater imaging camera, and the unit is objects capture or
# detected per second [For details please refer to Merz et al. (2021)]
def ROI_0p5x(roi):
    """
    0p5x is for cells or individuals that are in large size (100μm-7mm).
    All phytoplankton >100μm ESD, dinobryon and uroglena, and large zooplankton e.g. daphnia are measured in this magnification.
    This linear log-log relationship of transforming ROI to count/mL is verified by field measurement data in Merz et al. (2021).
    :param roi: region of interest; basically refer to counts/identification by the camera
    :return: count per mL per day
    """
    x = 10 ** (0.91 / 1.3) * roi ** (1 / 1.3)
    return x

def ROI_5p0x(roi):
    """
    5p0x is for cells or individuals that are in sMaLler size (~10-150μm).
    All phytoplankton <100μm ESD and ciliates are measured in this magnification.
    This linear log-log relationship of transforming ROI to count/mL is verified by field measurement data in Merz et al. (2021).
    :param roi: region of interest; basically refer to counts/identification by the camera
    :return: count per mL per day
    """
    x = 10 ** (2.9 / 0.71) * roi ** (1 / 0.71)
    return x


### converting to phyto abundance
phydata.insert(2, 'dinobryon_count/mL', ROI_0p5x(phydata['dinobryon_ROIs']))  # large phyto
phydata.insert(3, 'uroglena_count/mL', ROI_0p5x(phydata['uroglena_ROIs']))  # large phyto
phydata.insert(4, 'centric_diatom_count/mL', ROI_5p0x(phydata['centric_diatom_ROIs']))  # small cells
phydata.insert(5, 'cryptophyceae_count/mL', ROI_5p0x(phydata['cryptophyceae_ROIs']))  # small cells
phydata.insert(6, 'rhodomonas_count/mL', ROI_5p0x(phydata['rhodomonas_ROIs']))  # small cells
phydata.insert(7, 'chlorophytes_count/mL', ROI_5p0x(phydata['chlorophytes_ROIs']))  # small cells

zoodata_used.insert(2, 'daphnia_count/mL', ROI_0p5x(zoodata_used['daphnia_ROIs']))
zoodata_used.insert(4, 'ciliates_count/mL', ROI_5p0x(zoodata_used['ciliates_ROIs']))


### Bio-area to biovolume
def bioArea2Vol(Area):
    """
    Based on the scaling provided in Ryabov et al. (2021)
    :param Area:
    :return: Biovolume (μm3)
    """
    v = ((1 / (10**0.25)) * Area) ** (1/0.68)              # calibrated
    return v

### Ellipsoidal ciliates
def Length2Vol(aa, bb, cc):
    """
    Calculting biovolume assuming ellipsoidal ciliates, following Hillebrand et al. (1999)
    :param aa: minor axis length (μm)
    :param bb: depth (μm)
    :param cc: major axis length (μm)
    :return: biovolume (μm3)
    """
    v = (np.pi/6) * aa * bb * cc
    return v


### Deriving phytoplankton biomass
# calculating the biovolume from area using the scaling function from Ryabov et al. (2021)
for i in range(len(physpecies)):
    phydata.insert(1 + i, physpecies[i] + '_biov', bioArea2Vol(phydata[physpecies[i] + '_area_μm2']))

def mwP_Ind(biov):
    """
    This function uses the allometric relationship on P content for each size class (Hillebrand et al. 2022) Fig. 5C
    :param biov: input ESD (µm)
    :return: µg P count-1
    """
    slope, intercept = 0.88, -2.95  # slope and intercept regressed from P content data of Hillebrand et al. (2022)
    # 1. picogram phosphate per cell at a certain cell size
    pgPcount = (10 ** intercept) * (biov ** slope)
    # 2. microgram phosphorus per cell at a certain cell size
    µgP_count = pgPcount * 1e-6
    return µgP_count


def Phy_abun2biomass(biov, abun):
    """
    Converting phytoplankton abundance of specific size classes to biomass (count mL-1 to µmol P L-1)
    :param biov: input biovolume (µm3)
    :param abun:  abundance (count mL-1)
    :return: µmol P L-1
    """
    mwP = 30.973762  # µg/L         1 µg P/l = 1/MW P = 0.032285 µmol/l (https://www.ices.dk/data/tools/Pages/Unit-conversions.aspx)
    mL2L = 1e3
    µgP_ind = mwP_Ind(biov)
    µmolP_ind = µgP_ind / mwP  # from g to mol
    µmolP_L = µmolP_ind * (abun * mL2L)
    return µmolP_L

### Deriving zooplankton biomass

# calculating the biovolume of ciliates
zoodata_used.insert(1, 'ciliates_biov2', Length2Vol(zoodata_used['ciliates_MiL_μm'], zoodata_used['ciliates_MiL_μm']*(2/3), zoodata_used['ciliates_MaL_μm']))

def CiliatePcontent_Putt(biov):
    """
    Scaling function for ciliate body size and carbon content (Putt and Stoecker 1989)
    #(10**0.12) * (v**0.19)
    :param biov: input biovolume (µm3)
    :return: µmol P ind-1
    """
    Cfactor = 0.19  # pg C um-3
    pg2µg = 1e-6
    mwC = 12.011
    µgC_ind = ((10**0.12) * biov * Cfactor) * pg2µg
    µmolC_ind = µgC_ind / mwC
    C2P_ratio = 100     # a mean from 80-120 of Golz et al. (2015) - assuming redfield ratio for carbon to phosphate transformation - but the range can vary between 80-300 for daphnia
    µmolP_ind = µmolC_ind / C2P_ratio
    return µmolP_ind
  
def Daph_L_W_Schalau(MaL_mm):
    """
    Length-weight ratio for daphnia used in the model of Schalau et al. (2008) and sourced from Urabe and Watanabe (1991) & Lynch et al. (1986)
    :param MaL_mm: Maximum Axis Length (mm)
    :return: µmol P ind-1
    """
    mwC = 12.011
    L = MaL_mm * 0.75                            # ref: Ranta et al. (1993); Karpowicz et al. (2020)
    µgC_ind = 1.6 * (L**3)
    µmolC_ind = µgC_ind / mwC           # convert to molar
    C2P_ratio = 350  # the mean threshold elemental ratio (to maintain Daphnia growth - good reference for C:P)
                               # a mean from Hessen (2006) - assuming redfield ratio for carbon to phosphate transformation -
                               # but the range can vary between 80-385 for daphnia
    µmolP_ind = µmolC_ind / C2P_ratio
    return µmolP_ind



## phytoplankton total biomasses
for i in range(len(physpecies)):
    phydata.insert(1 + i, physpecies[i] + '_biomass', Phy_abun2biomass(phydata[physpecies[i] + '_biov'], phydata[physpecies[i] + '_count/mL']))
phydata.insert(1, 'Phy_TB', phydata.loc[:, ['dinobryon_biomass', 'uroglena_biomass', 'centric_diatom_biomass', 'cryptophyceae_biomass',
                                            'rhodomonas_biomass', 'chlorophytes_biomass']].sum(axis=1))

## zooplankton total biomasses
zoodata_used.insert(1, 'daphnia_biomass', Daph_L_W_Schalau(zoodata_used['daphnia_MaL_mm']) * zoodata_used['daphnia_count/mL'] * 1e3)
zoodata_used.insert(2, 'ciliates_biomass', CiliatePcontent_Putt(zoodata_used['ciliates_biov2']) * zoodata_used['ciliates_count/mL'] * 1e3)

zoodata_used.insert(1, 'Zoo_TB', zoodata_used.loc[:, ['daphnia_biomass', 'ciliates_biomass']].sum(axis=1))



### biomass weighted-mean biovolume
def WMeanSize(biom, biov):
    """
    ab = abundance of a specific size class; s = that size class (i.e. size array)
    axis=1 because the result data array is in the size of array[days, size groups, nut, mix]
    """
    return np.nansum(biom * biov, axis=1) / np.nansum(biom, axis=1)
    # return np.nansum(biom * np.log10(biov), axis=1) / np.nansum(biom, axis=1)

npBiom = phydata.loc[:, ['dinobryon_biomass', 'uroglena_biomass', 'centric_diatom_biomass', 'cryptophyceae_biomass',
                         'rhodomonas_biomass', 'chlorophytes_biomass']].to_numpy()
npBiov = phydata.loc[:, ['dinobryon_biov', 'uroglena_biov', 'centric_diatom_biov', 'cryptophyceae_biov', 'rhodomonas_biov',
                         'chlorophytes_biov']].to_numpy()

Sw_df = pd.DataFrame(WMeanSize(npBiom, npBiov), columns=['Sw'])


### Add julian date stamps
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
for i in range(len(phydata)):
    jday = np.append(jday, datestdtojd(phydata['date'][i]))

phydata.insert(1, 'Julian day', pd.DataFrame(jday))
zoodata_used.insert(1, 'Julian day', pd.DataFrame(jday))
Sw_df.insert(1, 'Julian day', pd.DataFrame(jday))


phydata['year'] = pd.DatetimeIndex(phydata['date']).year
phy_median = phydata.groupby(['Julian day'], as_index=False)['Phy_TB'].median().to_numpy()
phy_mean = phydata.groupby(['Julian day'], as_index=False)['Phy_TB'].mean().to_numpy()


Sw_df['year'] = pd.DatetimeIndex(phydata['date']).year
Sw_median = Sw_df.groupby(['Julian day'], as_index=False)['Sw'].median().to_numpy()
Sw_mean = Sw_df.groupby(['Julian day'], as_index=False)['Sw'].mean().to_numpy()


## export to csv
PhyTB_arr = phydata.loc[:, ['dinobryon_biomass', 'uroglena_biomass', 'centric_diatom_biomass', 'cryptophyceae_biomass',
                            'rhodomonas_biomass', 'chlorophytes_biomass']].to_numpy()
PhyBiov_arr = phydata.loc[:, ['dinobryon_biov', 'uroglena_biov', 'centric_diatom_biov', 'cryptophyceae_biov', 'rhodomonas_biov', 
                              'chlorophytes_biov']].to_numpy()


plankdata = np.column_stack((Sw_df['Julian day'].to_numpy(), phydata['Phy_TB'].to_numpy(), Sw_df['Sw'].to_numpy(),
                             zoodata_used['Zoo_TB'].to_numpy()))
plankdata = pd.DataFrame(plankdata)
plankdata.columns = ['Julian day', 'PhyBiom', 'Sw', 'ZooBiom']


plankdata.to_csv(wd + "/PlankData4Calibr.csv")

