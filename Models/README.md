Theoretical model is set up with constant nutrient input, similar to a chemostat type model with other environmental forcing like the irradiance and the temperature. Nutrient is required to input with a forcing array in the model. 

The model output is a multi-dimensional array, containing the solutions for every time step. The model solution includes the below variables:
1. One nutrient;
2. Two zooplankton of different sizes;
3. One detritus;
4. _N_ classes of phytoplankton in different sizes;
5. Total growth from phytoplankton;
6. Grazing from small zooplankton;
7. Grazing from large zooplankton;
8. Temperature dependence for phytoplankton growth; and
9. Nutrient limitation for phytoplankton growth.

The model solution contains all variable fluxes for environmental conditions as below:
- Nutrient levels (oligotrophic, eutrophic, and hypertrophic)
- Grazing regimes (nanoflagellate+daphnia, ciliates+daphnia, and copepods+daphnia)
- Grazing strategies (non-daphnia zooplankton as a specialist or as a generalist)
