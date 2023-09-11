# TempSizeMod - Temperature-size Model
## Background
Over half of the global freshwater bodies are under the threat of anthropogenic eutrophication. Anthropogenic eutrophication has become a major environmental problem since the mid-20th century. It is characterized by excessive input of nutrient in lakes that facilitates an overgrowth of algae in the aquatic ecosystem. Such overabundance of phytoplantkon population can cause multiple harmful effects to the ecosystem like degradation in water quality, harmful algae blooms, and trophic disorganization such as mass fish kills due to the deprivation of oxygen by large-scale degradations of dead algae.

Climate warming is another factor increasingly threatening ecosystem and the organisms living in it. Phytoplankton is one of the groups at the forefront of rising water temperautures. Temperature change has led to alterations in the temporal dynamics of phytoplankton (i.e. phenological shifts), the community compositions and even the trophic structures. It is crucial to understand how temperature drives changes to the assembly and the dynamics of the phytoplankton community.

In the current realm of global environmental change and climate warming, understanding the effects of temperature and eutrophication on phytoplankton community is highly important. Nevertheless, in a multi-stressor system, disentangling the effects of temperature on phytoplankotn is not easy. Temperature often interacts with other environmental factors like nutrient, thus contributing to various nonlinear feedbacks to the phytoplankton community and making predictions on community dynamics difficult.

Trait-based models have been applied to investigate the effects of environmental conditions on phytoplankton population dynamics. Phytoplantkon cell size is a master trait and has been used widely in modelling works. Size-based models allow explorations on aggregated community properties such as total biomass, community mean cell size, and size variances. They are useful for understanding changes in the macroecological patterns of the phytoplankton community size compositions.


## Model description
The size-based model is adapted from the well-established Nutrient-Phytoplankton-Zooplankton-Detritus (NPZD) framework (_sensu_ Fasham et al., 1990 and Armstrong, 1994) and is a differential equation-based model. The model includes one nutrient source, phosphorus $PO_4^{3-}$, available for uptake by different phytoplankton size classes ($P_i$). The phytoplankton are subject to grazing by two zooplankton of different sizes ($Z_1$, $Z_2$). The phytoplankton growth is limited by light and nutrient, and is scaled by temperature dependence. The detritus pool, $D$, collects the dead and ungrazed matters, follows by recharging the nutrient pool through remineralization processes.

<img width="1009" alt="Figure1_v2" src="https://github.com/Debbcwing/TempSizeMod/assets/51200142/ddae39b7-f956-460d-8738-2a3c6e6a5b39">


The model focuses on capturing size-dependent bottom-up and top-down interactions through data-driven allometric relationships of phytoplankton growth and zooaplankton grazing. The model aims at studying changes in the size compositions of lake phytoplankton communities. 


## Allometric relationships in the model
Based on multiple allometric equations, the model produce an ecological trade-off that favour a certain phytoplantkon size classes at different environmental conditions.

The allometric relationships considered in the model are:

$$\mu_{max}(S_i^P) = \beta_{\mu_{max}}\cdot (S_i^P)^{\alpha_{\mu_{max}}}$$

$$K_n(S_i^P) = \beta_{K_n}\cdot (S_i^P)^{\alpha_{K_n}}$$

$$T_{opt}(S_i^P) = \beta_{T_{opt}}\cdot (S_i^P)^{\alpha_{T_{opt}}}$$

$$I_{max}(S_j^Z) = \beta_{I_{max}}\cdot (S_j^Z)^{\alpha_{I_{max}}}$$

$$P_{opt}(S_i^P, S_j^Z) = \beta_{P_{opt}}\cdot (S_j^Z)^{\alpha_{P_{opt}}}$$

representing, respectively, maximum growth rate, $\mu_{max}(S_i^P)$, half-saturation for nutrient uptake, $K_n(S_i^P)$, and thermal optima, $T_{opt}(S_i^P)$, for phytoplankton size class $i$, and maximum ingestion rate, $I_{max}(S_j^Z)$, and optimal prey size, $P_{opt}(S_i^P, S_j^Z)$, for zooplankton size class $j$.



