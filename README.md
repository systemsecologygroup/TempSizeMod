# TempSizeMod - Temperature-size Model
## Background
Over half of the global lakes are recording increases in lake temperature and reporting rising bloom events (O'Reilley et al. 2015; Ho et al. 2019; Dokulil et al. 2021). Climate warming is increasingly threatening freshwater ecosystem biodiversity (Paerl et al. 2016; Dudgeon 2019; Reid et al. 2019). Temperature change leads to alterations in the temporal dynamics (also known as phenological shifts) and community compositions of phytoplankton (Winder and Sommer 2012; Zohary et al. 2021). It is crucial to understand how temperature drives changes to the assembly and the dynamics of the phytoplankton community (Petchey et al. 1999; Yvon-Durocher et al. 2011; Shurin et al. 2012; Striebel et al. 2016).

In the current realm of global environmental change, understanding the effects of temperature on the phytoplankton community is highly important for ecosystem management (Paerl et al. 2016). Nevertheless, in a multi-stressor system, disentangling the effects of temperature on phytoplankton is not easy (Dudgeon 2019). Temperature often interacts with other environmental factors like lake mixing and stratification, lights, and zooplankton grazer (Pomati et al. 2020), thus affecting phytoplankton communities both directly and indirectly (Zohary et al. 2021). This makes predicting plankton dynamics difficult. For instance, the occurrence of phytoplankton blooms is becoming more unpredictable as blooms are found in both cold and warm waters (e.g. Sterner et al. 2020; Reinl et al. 2021, 2023).

Trait-based models are valuable tools to disentangle possible effects and test the possible mechanisms that water temperature has on phytoplankton (Litchman 2023). Phytoplankton cell size is a master trait and has been widely used in modelling work (Litchman and Klausmeier 2008). Size-based models allow explorations of aggregated community properties such as total biomass and community mean cell size of phytoplankton (e.g. Ward et al. 2012; Acevedo-Trejos et al. 2018; To et al. 2024). They are useful for understanding changes in the macroecological patterns of the phytoplankton community size compositions in response to changes in environmental conditions.
<br/><br/>
## Model description
The model is adapted from the well-established Nutrient-Phytoplankton-Zooplankton-Detritus (NPZD) model (_sensu_ Fasham et al., 1990; Post et al. 2024) incorporated into a size-based framework (e.g., Armstrong 1994; To et al. 2024). The model is differential equation-based and includes one nutrient source, phosphorus $PO_4^{3-}$, available for uptake by different phytoplankton size classes ($P_i$). The phytoplankton are subject to grazing by two zooplankton of different size groups ($Z_1$, $Z_2$). The growth of phytoplankton is limited by light and nutrients, and is scaled by temperature dependence. The detritus pool, $D$, collects the dead and ungrazed matters, followed by recharging the nutrient pool through remineralization processes.

<p align="center">
  <img width="720" alt="Figure1_v3" src="https://github.com/user-attachments/assets/4a14a86d-2ded-4cb8-a04b-1d7c4959f2fc">


The model focuses on capturing size-dependent bottom-up and top-down interactions through data-driven allometric relationships between phytoplankton growth and zooplankton grazing. In this study, the allometric parameters are calibrated against lake-specific data within the reported ranges (Hansen et al. 1994, 1997; Edwards et al. 2012). For this study, the model aims at capturing nutrient and plankton dynamics in a Swiss lake, Greifensee, followed by projecting changes to these dynamics based on IPCC reported climate change scenarios (RCPs). Alternatively, the model can be used to study changes in the size compositions of lake phytoplankton communities under varying temperature and nutrient conditions. 

<br/>
## Temperature dependence in the model
The temperature dependence for phytoplankton growth follows a bell-shaped thermal tolerance curve, given by,


$$E(T) = e^{0.063T}  \left[1- \left(\frac{T-T_{opt}}{\sigma_T}\right)^2 \right] $$,

<br/>
where $T$ is the ambient lake water surface temperature (LWST), $T_{opt}$ is the thermal optima that determines the median of the curve, and $\sigma_T$ is the thermal tolerance that determines the width of the curve. In this study, we assume a community mean thermal tolerance curve to all phytoplankton size classes.

The maximum ingestion rates of zooplankton follows a Q10 model such that, the maximum grazing increases with temperature. The equation for the dependence is,

$$I_{max}(S_j^Z) \cdot Q_{10}^{\frac{T-T_{ref}}{10}} $$.

<br/>
The Q10 temperature coefficient here specifies the amount of maximum ingestion rate increases with a 10 $^{\circ}$ C temperature increase. It describes the sensitivity of zooplankton response to a higher temperature. $T$ refers to the lake temperature, while $T_{ref}$ refers to the reference temperature when the rate is equal to the baseline rate (i.e. no effects from temperature).

<br/><br/>
## Allometric relationships in the model
The model comprises of three allometric equations. These allometries allow an ecological trade-off to arise in the model based on water temperature throughout the year. The small phytoplantkon can grow faster than the large phytoplankton, but are subject to stronger grazing from the smaller zooplankton, who will selectively graze on the small cells. 

The allometric relationships considered in the model are:

$$\mu_{max}(S_i^P) = \beta_{\mu_{max}}\cdot (S_i^P)^{\alpha_{\mu_{max}}}$$

$$I_{max}(S_j^Z) = \beta_{I_{max}}\cdot (S_j^Z)^{\alpha_{I_{max}}}$$

$$P_{opt}(S_i^P, S_j^Z) = \beta_{P_{opt}}\cdot (S_j^Z)^{\alpha_{P_{opt}}}$$
<br/>
representing, respectively, maximum growth rate, $\mu_{max}(S_i^P)$, for phytoplankton size class $i$, and maximum ingestion rate, $I_{max}(S_j^Z)$, and optimal prey size, $P_{opt}(S_i^P, S_j^Z)$, for zooplankton size class $j$.

<br/><br/>
## Model calibration
We fine-tuned selected parameters against the time-averaged plankton data collected from lake Greifensee, consisting plankton size (bio-area) and abundance (ROI/sec). For details, please refer to the related publication of this model (under review). After calibrating the parameter values, we obtained a best-fit model that reflect the current average state of the lake.


<br/><br/>
## Experiments
Using the standard model, we conduct two numerical experiments:<br/>
1. a projection based on Representative Climate Pathways (RCPs) issued by IPCC
2. a sensitivity test for the two thermal traits, $T_{opt}$ and $\sigma_T$ in different RCP scenarios

For details, please refer to the related publication of this model (under review).


<br/><br/><br/><br/><br/><br/>
Reference:
+ Acevedo-Trejos, E., E. Marañón, and A. Merico. 2018. Phytoplankton size diversity and ecosystem   function relationships across oceanic regions. Proc. R. Soc. B. 285: 20180621. doi:10.1098/rspb.2018.0621
+ Armstrong, R. A. 1994. Grazing limitation and nutrient limitation in marine ecosystems: Steady state solutions of an ecosystem model with multiple food chains. Limnol. Oceanogr. 39: 597–608. doi:10.4319/lo.1994.39.3.0597
+ Bestion, E., Schaum, C., & Yvon‐Durocher, G. (2018). Nutrient limitation constrains thermal tolerance in freshwater phytoplankton. Limnology and Oceanography Letters, 3(6), 436–443. https://doi.org/10.1002/lol2.10096
+ Cagle, S. E., & Roelke, D. L. (2021). Relative roles of fundamental processes underpinning PEG dynamics in dimictic lakes as revealed by a self-organizing, multi-population plankton model. Ecological Modelling, 462, 109793. https://doi.org/10.1016/j.ecolmodel.2021.109793
+ Carpenter, S. R. 2005. Eutrophication of aquatic ecosystems: Bistability and soil phosphorus. Proc. Natl. Acad. Sci. U.S.A. 102: 10002–10005. doi:10.1073/pnas.0503959102
+ Chen, B. (2022). Thermal diversity affects community responses to warming. Ecological Modelling, 464, 109846. https://doi.org/10.1016/j.ecolmodel.2021.109846
+ Dokulil, M. T., De Eyto, E., Maberly, S. C., May, L., Weyhenmeyer, G. A., & Woolway, R. I. (2021). Increasing maximum lake surface temperature under climate change. Climatic Change, 165(3–4), 56. https://doi.org/10.1007/s10584-021-03085-1
+ Dudgeon, D. 2019. Multiple threats imperil freshwater biodiversity in the Anthropocene. Current Biology 29: R960–R967. doi:10.1016/j.cub.2019.08.002
+ Edwards, K. F., M. K. Thomas, C. A. Klausmeier, and E. Litchman. 2012. Allometric scaling and taxonomic variation in nutrient utilization traits and maximum growth rate of phytoplankton. Limnol. Oceanogr. 57: 554–566. doi:10.4319/lo.2012.57.2.0554
+ Edwards, K. F., Thomas, M. K., Klausmeier, C. A., & Litchman, E. (2016). Phytoplankton growth and the interaction of light and temperature: A synthesis at the species and community level: Light-Temperature Interactions. Limnology and Oceanography, 61(4), 1232–1244. https://doi.org/10.1002/lno.10282
+ Fasham, M. J. R., H. W. Ducklow, and S. M. McKelvie. 1990. A nitrogen-based model of plankton dynamics in the oceanic mixed layer. j mar res 48: 591–639. doi:10.1357/002224090784984678
+ Hansen, B., P. K. Bjørnsen, and P. J. Hansen. 1994. The size ratio between planktonic predators and their prey. Limnology and Oceanography 39: 395–403. doi:10.4319/lo.1994.39.2.0395
+ Hansen, P. J., P. K. Bjørnsen, and B. Hansen. 1997. Zooplankton grazing and growth: Scaling within the 2-2,000um body size range. Limnology and Oceanography 42: 687–704.
Ho, P.-C., Chang, C.-W., Hsieh, C. H., Shiah, F.-K., & Miki, T. (2013). Effects of increasing nutrient supply and omnivorous feeding on the size spectrum slope: A size-based nutrient-phytoplankton-zooplankton model. Population Ecology, 55(2), 247–259. https://doi.org/10.1007/s10144-013-0368-3
+ Ho, J. C., A. M. Michalak, and N. Pahlevan. 2019. Widespread global increase in intense lake phytoplankton blooms since the 1980s. Nature 574: 667–670. doi:10.1038/s41586-019-1648-7
+ Litchman, E. 2023. Understanding and predicting harmful algal blooms in a changing climate: A trait‐based framework. Limnol Oceanogr Letters 8: 229–246. doi:10.1002/lol2.10294
+ Litchman, E., and C. A. Klausmeier. 2008. Trait-Based Community Ecology of Phytoplankton. Annu. Rev. Ecol. Evol. Syst. 39: 615–639. doi:10.1146/annurev.ecolsys.39.110707.173549
+ O’Reilly, C. M., Sharma, S., Gray, D. K., Hampton, S. E., Read, J. S., Rowley, R. J., Schneider, P., Lenters, J. D., McIntyre, P. B., Kraemer, B. M., Weyhenmeyer, G. A., Straile, D., Dong, B., Adrian, R., Allan, M. G., Anneville, O., Arvola, L., Austin, J., Bailey, J. L., … Zhang, G. (2015). Rapid and highly variable warming of lake surface waters around the globe. Geophysical Research Letters, 42(24). https://doi.org/10.1002/2015GL066235
+ Petchey, O. L., P. T. McPhearson, T. M. Casey, and P. J. Morin. 1999. Environmental warming alters food-web structure and ecosystem function. Nature 402: 69–72. doi:10.1038/47023
+ Pomati, F., J. B. Shurin, K. H. Andersen, C. Tellenbach, and A. D. Barton. 2020. Interacting Temperature, Nutrients and Zooplankton Grazing Control Phytoplankton Size-Abundance Relationships in Eight Swiss Lakes. Front. Microbiol. 10: 3155. doi:10.3389/fmicb.2019.03155
+ Post, B., Acevedo-Trejos, E., Barton, A. D., & Merico, A. (2024). The XSO framework (v0.1) and Phydra library (v0.1) for a flexible, reproducible, and integrated plankton community modeling environment in Python. Geoscientific Model Development, 17(3), 1175–1195. https://doi.org/10.5194/gmd-17-1175-2024
+ Reid, A. J., A. K. Carlson, I. F. Creed, and others. 2019. Emerging threats and persistent conservation challenges for freshwater biodiversity. Biological Reviews 94: 849–873. doi:10.1111/brv.12480
+ Reinl, K. L., J. D. Brookes, C. C. Carey, and others. 2021. Cyanobacterial blooms in oligotrophic lakes: Shifting the high‐nutrient paradigm. Freshwater Biology 66: 1846–1859. doi:10.1111/fwb.13791
+ Reinl, K. L., T. D. Harris, R. L. North, and others. 2023. Blooms also like it cold. Limnol Oceanogr Letters 8: 546–564. doi:10.1002/lol2.10316
+ Striebel, M., S. Schabhüttl, D. Hodapp, P. Hingsamer, and H. Hillebrand. 2016. Phytoplankton responses to temperature increases are constrained by abiotic conditions and community composition. Oecologia 182: 815–827. doi:10.1007/s00442-016-3693-3
+ To, S., Acevedo‐Trejos, E., Chakraborty, S., Pomati, F., & Merico, A. (2024). Grazing strategies determine the size composition of phytoplankton in eutrophic lakes. Limnology and Oceanography, lno.12538. https://doi.org/10.1002/lno.12538
+ Ward, B. A., S. Dutkiewicz, O. Jahn, and M. J. Follows. 2012. A size-structured food-web model for the global ocean. Limnol. Oceanogr. 57: 1877–1891. doi:10.4319/lo.2012.57.6.1877
+ Winder, M., & Sommer, U. (2012). Phytoplankton response to a changing climate. Hydrobiologia, 698(1), 5–16. https://doi.org/10.1007/s10750-012-1149-2
+ Woolway, R. I., Sharma, S., Weyhenmeyer, G. A., Debolskiy, A., Golub, M., Mercado-Bettín, D., Perroud, M., Stepanenko, V., Tan, Z., Grant, L., Ladwig, R., Mesman, J., Moore, T. N., Shatwell, T., Vanderkelen, I., Austin, J. A., DeGasperi, C. L., Dokulil, M., La Fuente, S., … Jennings, E. (2021). Phenological shifts in lake stratification under climate change. Nature Communications, 12(1), 2318. https://doi.org/10.1038/s41467-021-22657-4
+ Yvon-Durocher, G., J. M. Montoya, M. Trimmer, and G. Woodward. 2011. Warming alters the size spectrum and shifts the distribution of biomass in freshwater ecosystems. Global Change Biology 17: 1681–1694. doi:10.1111/j.1365-2486.2010.02321.x
+ Zohary, T., Flaim, G., & Sommer, U. (2021). Temperature and the size of freshwater phytoplankton. Hydrobiologia, 848(1), 143–155. https://doi.org/10.1007/s10750-020-04246-6
