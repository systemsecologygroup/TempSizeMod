This model adapts data from a specific Swiss lake close to Zurich, Greifensee. 
There are three environmental forcing to the model, respectively, Water Temperature from photic zone (WT), Photosynthetically-active Radiance (PAR), and Mixed Layer Depth (MLD). 
These data are collected from different sources. LWST is obtained from the in-situ CTD probe (documented in Pomati et al. 2011) averaged from depths range from 0 to 8m. PAR is obtained from the nearby weather station by MeteoSwiss. Mixed layer depth is adopted from the published data for Greifensee in Pomati et al. (2020), https://zenodo.org/record/3582838#.YzQzuexBwc8. 

The original dataset contains an approximately three-year time-series from 13/3/2019 to 31/12/2022, containing 1390 data points. To generate an annual forcing profile, LWST was taken from a three-year mean, PAR was taken from a 75 percentile due to high daily variations, and MLD was derived by month to preserve the key mixing of the epilimnion in the water column. 

The steps deriving these forcing profile is shown in the python script 'TSM_TempForcing.py', 'TSM_PARForcing.py', and 'TSM_MLDForcing.py' respectively.




                                     
Reference
Pomati, F., J. Jokela, M. Simona, M. Veronesi, and B. W. Ibelings. 2011. An Automated Platform for Phytoplankton Ecology and Aquatic Ecosystem Monitoring. Environ. Sci. Technol. 45: 9658–9665. doi:10.1021/es201934n
Pomati, F., J. B. Shurin, K. H. Andersen, C. Tellenbach, and A. D. Barton. 2020. Interacting Temperature, Nutrients and Zooplankton Grazing Control Phytoplankton Size-Abundance Relationships in Eight Swiss Lakes. Front. Microbiol. 10: 3155. doi:10.3389/fmicb.2019.03155
