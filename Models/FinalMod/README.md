To run the model, one needs the model script 'FinalMod_Sbm.py' and the model run script 'FinalMod_run.py'.
<br/><br/>

#### FinalMod_Sbm.py
This is the file containing the size-based NPZD model. The default parameter values are coded in the model.


<br/><br/>
#### FinalMod_run.py
In the run script, one could adjust the number of year and of phytoplankton size classes according to their own preferences.
````
Pnum = 10      # specify the nos of phytoplankton size groups
Ynum = 10       # no. of modelling year
````

To change model parameter values from the default values, one enters their preferred values in below lines.
````
sol = SizeModLogspace(mld=mld_run, par=PAR_run, sst=LWST_run, dmdt=dmdt_run, N0=N0, numP=Pnum, numYears=Ynum).solution
````
For example, if one wants to change remineralization rate to 0.5, please input it as
````
sol = SizeModLogspace(mld=mld_run, par=PAR_run, sst=LWST_run, dmdt=dmdt_run, N0=N0, numP=Pnum, numYears=Ynum, Rem=0.5).solution
````
or if one wants to change the parameters that determine the allometric relationships for $\mu_{max}$ i.e. $\alpha_{\mu_{max}}$ to 0.25, 
````
sol = SizeModLogspace(mld=mld_run, par=PAR_run, sst=LWST_run, dmdt=dmdt_run, N0=N0, numP=Pnum, numYears=Ynum, mu_alpha=0.25).solution
````

The code for the parameters can be found in FinalMod_Sbm.py.



<br/><br/>
#### FinalMod_proj.py
In this script one can run a number of projection sceanrios, i.e. linear increase in temperature, automatically.
If one wants to configure the increase in temperature by their own preferred values, or adjust the number of scenarios, please change at the below line:
````
temp_incr = [0, 1.4, 2.5, 4.2]
````

<br/><br/><br/><br/><br/>
* Shall there be any queries or difficulties in conducting the runs, please feel free to reach out at: sto@constructor.university





