The sensitivity test is conducted to estimate the uncertainty of different model parameters on the model results. I selected 14 model parameters, which are neither examined by the sensitivty analysis (i.e., the thermal traits) nor the sensitivty run (i.e., the lake mixing parameters). 
For these 14 parameters, I tested ±25% the default parameter values and examined the changes in the model results, i.e., total nutrient concentration (μM P), community biomass of phytoplankton and zooplankton (μM P), and community-weighted mean phytoplankton biovolume (μm3).

To run this test, we first define a dictionary of the parameters with their default values.
```
Param = {                       # these are all default parameter values
    'alpha': 0.02,  # Initial slope of P-I curve
    'Pmax': 1.1,  # Max photosynthesis rate
    'Kpar': 0.1,  # Attenuation-phytoplankton self-shading
    'Mz': 0.1,  # Mortality - zooplankton
    'Mp': 0.1,  # Mortality - phytoplankton
    'Mz2': 0.34,  # Mortality - zooplankton from higher predators
    'Ieff': 0.75,  # Ingestion efficiency (sloppy feeding)
    'beta': 0.69,  # Assimilation effiency
    'Kp': 0.19,  # Phytoplankton half-saturation constant (mmol*m^-3)
    'Rem': 0.15,  # Remineralization rate [time lagged for nutrient recharge]
    'k': 0.1,  # Cross thermocline mixing factor
    'mu_alpha': -0.36,
    'mu_beta': 10 ** 0.69,
    'Kn': 0.06,
    'graz_Q10': 2.8,
    'graz_alpha': -0.28,
    'graz_beta': 23,
    'ops_alpha': 0.7,
    'ops_beta': 0.45}
```

We followed by creating the output arrays

```
numParam = len(Param.keys())
outM25 = np.zeros((365*Ynum, Pnum*4 + 2 + 4, numParam))    #-25%
outP25 = np.zeros((365*Ynum, Pnum*4 + 2 + 4, numParam))    #+25%
```

To run the solution, we loop over the parameter values via the dictionary.

```
for k, v in enumerate(Param.keys()):
    Param[v] = Param[v]*0.75                                       # change value (+/- 25%)
    print('test value', k, v, Param[v])                              # check value before run
    solM25 = SizeModLogspace(mld=mld_run, par=PAR_run, sst=LWST_run, dmdt=dmdt_run, N0=N0, numP=Pnum,
                             numYears=Ynum, **Param)
    outM25[:, :, k] = solM25.solution[:, :]                         # store results
    Param[v] = Param[v]/0.75                                        # recover the value in the dictionary
    print('default value', k, v, Param[v])                          # check value after restoring the value
print(Param.items())                                                     # check the whole dictionary after run
```

The results are attached in this folder. More details can be found in the related publication of this work (See front page).
