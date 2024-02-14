# TempSizeMod - Temperature-size Model
## Background
Over half of the global freshwater bodies are reporting threats of anthropogenic eutrophication (Ho et al. 2019). Anthropogenic eutrophication has become a major environmental problem since the mid-20th century. It is characterized by excessive input of nutrient in lakes that facilitates an overgrowth of algae in the aquatic ecosystem (Carpenter 2005). Such overabundance of phytoplantkon population can cause multiple harmful effects to the ecosystem like degradation in water quality, harmful algae blooms, and trophic disorganization such as mass fish kills due to the deprivation of oxygen by large-scale degradations of dead algae (Huisman et al. 2018).

Climate warming is another factor increasingly threatening freshwater ecosystem biodiversity (Paerl et al. 2016; Dudgeon 2019; Reid et al. 2019). Phytoplankton is one of the groups at the forefront of rising water temperautures. Temperature change has led to alterations in the temporal dynamics of phytoplankton (i.e. phenological shifts), the community compositions and even the trophic structures. It is crucial to understand how temperature drives changes to the assembly and the dynamics of the phytoplankton community (Petchey et al. 1999; Yvon-Durocher et al. 2011; Shurin et al. 2012; Striebel et al. 2016).

In the current realm of global environmental change, understanding the effects of temperature and eutrophication on phytoplankton community is highly important for ecosystem management (Paerl et al. 2016). Nevertheless, in a multi-stressor system, disentangling the effects of temperature on phytoplankotn is not easy (Dudgeon 2019). Temperature often interacts with other environmental factors like nutrient and zooplankton grazer (Pomati et al. 2020), thus contributing to various nonlinear feedbacks to the phytoplankton community and making predictions on community dynamics difficult. For example, the occurrence of phytoplankton blooms is becoming more unpredictable (e.g. Sterner et al. 2020; Reinl et al. 2021, 2023).

Trait-based models have been applied to investigate the effects of environmental conditions on phytoplankton population dynamics (Litchman 2023). Phytoplantkon cell size is a master trait and has been used widely in modelling works (Litchman and Klausmeier 2008). Size-based models allow explorations on aggregated community properties such as total biomass, community mean cell size, and size variances (e.g. Ward et al. 2012; Acevedo-Trejos et al. 2018). They are useful for understanding changes in the macroecological patterns of the phytoplankton community size compositions (Merico et al. 2009).


## Model description
The model is adapted from the well-established Nutrient-Phytoplankton-Zooplankton-Detritus (NPZD) model (_sensu_ Fasham et al., 1990) incorporated to a size-based framework (e.g. Moloney and Field 1991; Armstrong 1994; Stock et al. 2008). The model is differential equation-based and includes one nutrient source, phosphorus $PO_4^{3-}$, available for uptake by different phytoplankton size classes ($P_i$). The phytoplankton are subject to grazing by two zooplankton of different size groups ($Z_1$, $Z_2$). The phytoplankton growth is limited by light and nutrient, and is scaled by a temperature dependence. The detritus pool, $D$, collects the dead and ungrazed matters, follows by recharging the nutrient pool through remineralization processes.

<p align="center">
  <img width="560" alt="Figure1_v3" src="https://github.com/Debbcwing/TempSizeMod/assets/51200142/49e96eaa-3a22-4bfc-bfd0-036739bc0ac4">


The model focuses on capturing size-dependent bottom-up and top-down interactions through data-driven allometric relationships of phytoplankton growth and zooaplankton grazing (Hansen et al. 1994, 1997; Edwards et al. 2012). The model aims at studying changes in the size compositions of lake phytoplankton communities. 


## Temperature dependence in the model
The temperature dependence for phytoplankton growth follows a bell-shaped thermal tolerance curve, given by,

$$E(T) = e^{0.063T}  \left[1- \left(\frac{T-T_{opt}}{\sigma_T}\right)^2 \right] $$

, where $T$ is the ambient lake water surface temperature (LWST), $T_{opt}$ is the thermal optima that determines the median of the curve, and $\sigma_T$ is the thermal tolerance that determines the width of the curve. In this study, we assume a community mean thermal tolerance curve to all phytoplankton size classes.

The maximum ingestion rates of zooplankton follows a Q10 model such that, the maximum grazing increases with temperature. The equation for the dependence is,

$$I_{max}(S_j^Z) \cdot Q_{10}^{\frac{T-T_{ref}}{10}} $$

The Q10 temperature coefficient here specifies the amount of maximum ingestion rate increases with a 10$^{\circ}$C temperature increase. It describes the sensitivity of zooplankton response to a higher temperature. $T$ refers to the lake temperature, while $T_{ref}$ refers to the reference temperature when the rate is equal to the baseline rate (i.e. no effects from temperature).

## Allometric relationships in the model
The model comprises of three allometric equations. These allometries allow an ecological trade-off to arise in the model based on water temperature throughout the year. The small phytoplantkon can grow faster than the large phytoplankton, but are subject to stronger grazing from the smaller zooplankton, who will selectively graze on the small cells. 

The allometric relationships considered in the model are:

$$\mu_{max}(S_i^P) = \beta_{\mu_{max}}\cdot (S_i^P)^{\alpha_{\mu_{max}}}$$

$$I_{max}(S_j^Z) = \beta_{I_{max}}\cdot (S_j^Z)^{\alpha_{I_{max}}}$$

$$P_{opt}(S_i^P, S_j^Z) = \beta_{P_{opt}}\cdot (S_j^Z)^{\alpha_{P_{opt}}}$$

representing, respectively, maximum growth rate, $\mu_{max}(S_i^P)$, for phytoplankton size class $i$, and maximum ingestion rate, $I_{max}(S_j^Z)$, and optimal prey size, $P_{opt}(S_i^P, S_j^Z)$, for zooplankton size class $j$.




Reference:
+ Acevedo-Trejos, E., E. Marañón, and A. Merico. 2018. Phytoplankton size diversity and ecosystem   function relationships across oceanic regions. Proc. R. Soc. B. 285: 20180621. doi:10.1098/rspb.2018.0621
+ Armstrong, R. A. 1994. Grazing limitation and nutrient limitation in marine ecosystems: Steady state solutions of an ecosystem model with multiple food chains. Limnol. Oceanogr. 39: 597–608. doi:10.4319/lo.1994.39.3.0597
+ Carpenter, S. R. 2005. Eutrophication of aquatic ecosystems: Bistability and soil phosphorus. Proc. Natl. Acad. Sci. U.S.A. 102: 10002–10005. doi:10.1073/pnas.0503959102
Dudgeon, D. 2019. Multiple threats imperil freshwater biodiversity in the Anthropocene. Current Biology 29: R960–R967. doi:10.1016/j.cub.2019.08.002
+ Edwards, K. F., M. K. Thomas, C. A. Klausmeier, and E. Litchman. 2012. Allometric scaling and taxonomic variation in nutrient utilization traits and maximum growth rate of phytoplankton. Limnol. Oceanogr. 57: 554–566. doi:10.4319/lo.2012.57.2.0554
+ Fasham, M. J. R., H. W. Ducklow, and S. M. McKelvie. 1990. A nitrogen-based model of plankton dynamics in the oceanic mixed layer. j mar res 48: 591–639. doi:10.1357/002224090784984678
+ Hansen, B., P. K. Bjørnsen, and P. J. Hansen. 1994. The size ratio between planktonic predators and their prey. Limnology and Oceanography 39: 395–403. doi:10.4319/lo.1994.39.2.0395
+ Hansen, P. J., P. K. Bjørnsen, and B. Hansen. 1997. Zooplankton grazing and growth: Scaling within the 2-2,000um body size range. Limnology and Oceanography 42: 687–704.
+ Ho, J. C., A. M. Michalak, and N. Pahlevan. 2019. Widespread global increase in intense lake phytoplankton blooms since the 1980s. Nature 574: 667–670. doi:10.1038/s41586-019-1648-7
+ Huisman, J., G. A. Codd, H. W. Paerl, B. W. Ibelings, J. M. H. Verspagen, and P. M. Visser. 2018. Cyanobacterial blooms. Nature Reviews Microbiology 16: 471–483. doi:10.1038/s41579-018-0040-1
+ Litchman, E. 2023. Understanding and predicting harmful algal blooms in a changing climate: A trait‐based framework. Limnol Oceanogr Letters 8: 229–246. doi:10.1002/lol2.10294
+ Litchman, E., and C. A. Klausmeier. 2008. Trait-Based Community Ecology of Phytoplankton. Annu. Rev. Ecol. Evol. Syst. 39: 615–639. doi:10.1146/annurev.ecolsys.39.110707.173549
+ Merico, A., J. Bruggeman, and K. Wirtz. 2009. A trait-based approach for downscaling complexity in plankton ecosystem models. Ecological Modelling 220: 3001–3010. doi:10.1016/j.ecolmodel.2009.05.005
+ Moloney, C. L., and J. G. Field. 1991. The size-based dynamics of plankton food webs. I. A simulation model of carbon and nitrogen flows. J Plankton Res 13: 1003–1038. doi:10.1093/plankt/13.5.1003
+ Paerl, H. W., W. S. Gardner, K. E. Havens, A. R. Joyner, M. J. McCarthy, S. E. Newell, B. Qin, and J. T. Scott. 2016. Mitigating cyanobacterial harmful algal blooms in aquatic ecosystems impacted by climate change and anthropogenic nutrients. Harmful Algae 54: 213–222. doi:10.1016/j.hal.2015.09.009
+ Petchey, O. L., P. T. McPhearson, T. M. Casey, and P. J. Morin. 1999. Environmental warming alters food-web structure and ecosystem function. Nature 402: 69–72. doi:10.1038/47023
+ Pomati, F., J. B. Shurin, K. H. Andersen, C. Tellenbach, and A. D. Barton. 2020. Interacting Temperature, Nutrients and Zooplankton Grazing Control Phytoplankton Size-Abundance Relationships in Eight Swiss Lakes. Front. Microbiol. 10: 3155. doi:10.3389/fmicb.2019.03155
+ Reid, A. J., A. K. Carlson, I. F. Creed, and others. 2019. Emerging threats and persistent conservation challenges for freshwater biodiversity. Biological Reviews 94: 849–873. doi:10.1111/brv.12480
+ Reinl, K. L., J. D. Brookes, C. C. Carey, and others. 2021. Cyanobacterial blooms in oligotrophic lakes: Shifting the high‐nutrient paradigm. Freshwater Biology 66: 1846–1859. doi:10.1111/fwb.13791
+ Reinl, K. L., T. D. Harris, R. L. North, and others. 2023. Blooms also like it cold. Limnol Oceanogr Letters 8: 546–564. doi:10.1002/lol2.10316
+ Stock, C. A., T. M. Powell, and S. A. Levin. 2008. Bottom–up and top–down forcing in a simple size-structured plankton dynamics model. Journal of Marine Systems 74: 134–152. doi:10.1016/j.jmarsys.2007.12.004
+ Striebel, M., S. Schabhüttl, D. Hodapp, P. Hingsamer, and H. Hillebrand. 2016. Phytoplankton responses to temperature increases are constrained by abiotic conditions and community composition. Oecologia 182: 815–827. doi:10.1007/s00442-016-3693-3
+ Ward, B. A., S. Dutkiewicz, O. Jahn, and M. J. Follows. 2012. A size-structured food-web model for the global ocean. Limnol. Oceanogr. 57: 1877–1891. doi:10.4319/lo.2012.57.6.1877
+ Yvon-Durocher, G., J. M. Montoya, M. Trimmer, and G. Woodward. 2011. Warming alters the size spectrum and shifts the distribution of biomass in freshwater ecosystems: WARMING ALTERS COMMUNITY SIZE STRUCTURE. Global Change Biology 17: 1681–1694. doi:10.1111/j.1365-2486.2010.02321.x
