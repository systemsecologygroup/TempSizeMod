Here contains two sets of model results, one for the projection of future RCP scenarios ('Proj.nc') and one for sensitivity test ('Sensit.nc') over thermal traits (i.e. thermal optima and thermal tolerance) in the standard and RCP scenarios.


----------------------- Proj.nc -----------------------\
This file stores the output data from the projection, and is saved as a multi-dimensional dataset in a netCDF file.
The dataset contains nutrient fluxes ('Nut'), phytoplankton biomass ('Phy'; $P_i$, $i$=1,2,..,10) and zooplankton biomass ('Zoo'; $Z_j$, $j$=1,2) data of each size class from day 3285 to day 3650, on the 10th year of the simulation. This is a time range after the spin-up stage of the model.

To extract the data, one could use the netCDF4 library in python (https://unidata.github.io/netcdf4-python/)

````
wd = '/YourWorkingDirectory'

import netCDF4    
out = netCDF4.Dataset(wd+'/Proj.nc')  # output file
Phy = out.variables['Phy'][:]
Zoo = out.variables['Zoo'][:]
Nut = out.variables['Nut'][:]
````

The coordinates (dimensions) of the 'Phy' dataset are as below:\
'time': '365 days',\
'PhySize': '10 phytoplankton size classes ranged from 1 to 200µm ESD',\
'RCP': '4 different climate change scenarios considered by IPCC: RCP 2.6; RCP 6.0; and RCP 8.5'\
\
The coordinates (dimensions) of the 'Zoo' dataset are as below:\
'time': '365 days',\
'ZooSize': '2 zooplankton size classes at 20 and 600µm ESD',\
'RCP': '4 different climate change scenarios considered by IPCC: RCP 2.6; RCP 6.0; and RCP 8.5'\
\
The coordinates (dimensions) of the 'Nut' dataset are as below:\
'time': '365 days',\
'RCP': '4 different climate change scenarios considered by IPCC: RCP 2.6; RCP 6.0; and RCP 8.5'\

\
\
----------------------- Sensit.nc -----------------------\
This file stores the output data from the sensitivity test, and is saved as a multi-dimensional dataset in a netCDF file.
The dataset contains nutrient fluxes ('Nut'), phytoplankton biomass ('Phy'; $P_i$, $i$=1,2,..,10) and zooplankton biomass ('Zoo'; $Z_j$, $j$=1,2) data of each size class from day 0 to day 3650. For analyses, we used data from the last year, after the model is spinned-up, hence, day 3285 to 3650.
````
wd = '/YourWorkingDirectory'

import netCDF4    
out = netCDF4.Dataset(wd+'/Sensit.nc')  # output file
Phy = out.variables['Phy'][:]
Zoo = out.variables['Zoo'][:]
Nut = out.variables['Nut'][:]
````
The coordinates (dimensions) of the 'Phy' dataset are as below:\
'time': '365 days',\
'PhySize': '10 phytoplankton size classes ranged from 1 to 200µm ESD',\
'RCP': '4 different climate change scenarios considered by IPCC: RCP 2.6; RCP 6.0; and RCP 8.5',\
'Sensit': '4 different configurations on thermal traits to test their sensitivities in climate change scenarios considered by IPCC: RCP 2.6; RCP 6.0; and RCP 8.5'\
\
The coordinates (dimensions) of the 'Zoo' dataset are as below:\
'time': '365 days',\
'ZooSize': '2 zooplankton size classes at 20 and 600µm ESD',\
'RCP': '4 different climate change scenarios considered by IPCC: RCP 2.6; RCP 6.0; and RCP 8.5',\
'Sensit': '4 different configurations on thermal traits to test their sensitivities in climate change scenarios considered by IPCC: RCP 2.6; RCP 6.0; and RCP 8.5'\
\
The coordinates (dimensions) of the 'Nut' dataset are as below:\
'time': '365 days',\
'RCP': '4 different climate change scenarios considered by IPCC: RCP 2.6; RCP 6.0; and RCP 8.5',\
'Sensit': '4 different configurations on thermal traits to test their sensitivities in climate change scenarios considered by IPCC: RCP 2.6; RCP 6.0; and RCP 8.5'\
