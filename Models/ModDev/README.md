## Model development from a size-based NPZD model

The models recorded here are additional modifications done from the base model recorded in https://github.com/Debbcwing/Sizeb_NPZD

Each modified version is an addition of the previous one, using the base model as v0. In each model variation we examine the change in aggergate biomass concentration of different variables.
All model variations are subject to a medium nutrient level (1 µmol PO4 L-1) and a sinusoidal mixing frequency (4 times year-1). 
Model runs for 5 years, model contains 3 phytoplankton size classes.

v1.0
The modifications are:
  - wider range of zooplankton (5-400µm)
  - wider range of phytoplankton  (1-200µm)
  - re-adapting phosphorus as the limiting nutrient of the model (instead of nitrate)
  - allowing dynamic nutrient forcing to the model (a fixed nutrient input is still possible by forcing a repeated array as the nutrient forcing)


v1.1
The modifications are:
  - using a different temperature forcing

v1.2
The modifications are:
  - an updated PAR conversion


v2.0
The modifications are:
  - adding allometric scaling for thermal optima

v3.0
The modifications are:
  - adding Q10 for zooplankton grazing

v3.0.1
The modifications are:
  - reducing Q10 values for zooplankton grazing

v3.1
The modifications are:
  - applying realistic lake forcing (Greifensee) to the model: Temperature, PAR, MLD, PO4
  - standard run

v3.2.0
The modifications are:
  - different combinations of zooplankton size

v3.2.1
The modifications are:
  - different combinations of zooplankton grazing strategies
    
v4.0 (Pending)
The modifications are:
  - An advanced assumption associating nutrient levels with thermal optima of the phytoplankton
