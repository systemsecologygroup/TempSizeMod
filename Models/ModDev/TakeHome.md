```
Take home from v1.0
- almost same biomass level when changing the number of phytoplankton size classes from 3 to 15.
- Zooplankton couple well with phytoplankton
- Regular cycles
```
<img width="569" alt="image" src="https://github.com/Debbcwing/TempSizeMod/assets/51200142/37fcb989-6a5e-4d4d-92dc-ca65864a964d">

```
Take home from v1.1
- we updated the temperature forcing 
- the dynamics of the state variables are almost the same as v1.0
```

```
Take home from v1.2
- we additionally updated the PAR conversion
- the dynamics of the state variables are almost the same as v1.0 and v1.1
```

```
## Key take home from v1
- This base model is not highly sensitive to temperature and PAR forcing
- Zooplankton couple well with phytoplankton -> grazing is active
```


```
Take home from v2.0
- We added temperature performance curve to replace the Eppley function from v1
- There are more fluctuations in the dynamics of the state variables
- Occasional peaks are observed for nutrient
- Zooplankton-Phytoplankton gets decoupled
- The patterns are less cyclic compared to v1
```
<img width="570" alt="image" src="https://github.com/Debbcwing/TempSizeMod/assets/51200142/b79de3e8-614d-44e5-8d9a-f8c2aae8352e">


```
Take home from v3.0
- We added Q10 to zooplankton max. ingestion rate (grazing)
- The Q10 grazing has removed some fluctuations from phytoplankton biomass
- Zooplankton almost always catch up instantaneously with phytoplankton and control their development -> Those are highly edible cells
- Fluctuations in nutrient and detritus persist
```
<img width="574" alt="image" src="https://github.com/Debbcwing/TempSizeMod/assets/51200142/92375cbe-67ee-4244-8bbb-ae4cef80b4b3">

```
Take home from v3.0.1
- We reduce the Q10 value for zooplankton max. ingestion rate (grazing)
- Phytoplankton get more persistence
- But there are higher nutrient peaks -> uptake is not efficient
```
<img width="575" alt="image" src="https://github.com/Debbcwing/TempSizeMod/assets/51200142/c1d480e1-6e9b-40ec-9c4e-c10a4673ec87">

```
Take home from v3.1
- We introduce realistic MLD forcing (from Greifensee)
- Phytoplankton persist for a prolonged period in the year cycle
- Zooplankton decouple with phytoplankton as MLD gets shallow (stratification) -> grazing is not efficient during a certain period
- There are no more nutrient peaks
```
<img width="577" alt="image" src="https://github.com/Debbcwing/TempSizeMod/assets/51200142/dcaf2373-80e2-46d1-8759-cdf46392eb67">

```
Take home from v3.2
- We change the combination of zooplankton size to 150 and 400 (previously 5 and 400)
- We find that grazing parameters are rather sensitive e.g. when changing the size combination of the zooplankton, model often collapse due to different other grazing parameters such as Q10, grazing strategies etc.
- We parametrize the Q10 values that are robust to all selected zooplankton size
```

```
## Key take home from v3
- When added parametrization to grazing, the system begins to produce extreme values and become unstable e.g. phytoplankton can go extinct in some cases
- Immigration might be needed to compensate the extinction, before we can further experiment on the grazing configurations
```

```
Take home from v4.0
- We add immigration for the phytoplankton community
```
