This model forcing adopts in-situ data from  Greifensee, Switzerland. 
There are three environmental forcing functions to the model, respectively, Water Temperature from photic zone (LWST), Photosynthetically-active Radiance (PAR), and Mixed Layer Depth (MLD). 
These forcing are derived from various time-series data sources, and the data cover different time periods. The LWST is obtained from the CTD profiles as daily epilimnetic temperature from 13/3/2019 to 31/12/2022 (n=1390), measured by the Swiss Federal Institute of Aquatic Science and Technology, Eawag. The PAR data is converted from the solar radiance data collected from a weather station next to Greifensee, measured daily by MeteoSwiss for the same period as the LWST. The PAR conversion is detailed in the related publication of this model. Finally, we retrieve MLD data from Pomati et al. (2020), which documented monthly MLD of Greifensee from 1972 to 2015 (n=270).

To generate an annual forcing profile, LWST was taken from a three-year mean, PAR was taken from a 75 percentile due to high daily variations, and MLD was derived by month to preserve the key mixing of the epilimnion in the water column. The steps deriving these forcing profile is shown in the python script 'TSM_TempForcing.py', 'TSM_PARForcing.py', and 'TSM_MLDForcing.py' respectively.

<p align="center">
  <img width="403" alt="Figure1_v2 1" src="https://github.com/Debbcwing/TempSizeMod/assets/51200142/7aa79bf9-705e-4312-b2d0-2849bc4d074c">

<br/><br/>                                     
Reference
+ Pomati, F., J. B. Shurin, K. H. Andersen, C. Tellenbach, and A. D. Barton. 2020. Interacting temperature, nutrients and zooplankton grazing control phytoplankton size-abundance relationships in eight Swiss lakes [Data set]. In Frontiers in Microbiology, Aquatic Microbiology. Zenodo. https://doi.org/10.5281/zenodo.3582838
