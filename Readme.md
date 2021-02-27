# Luisin Soluciones - Web Dashboard - Fleet Management Systems Analyzer

**Short Summary**: This is a web data analyzer that handles a local database that comes from FMS at big-large mining companies.
  - How does it look like?:



#### Features:


1. ##### Cycle time handler:
    - It consults the local database and gets:
       * Routes: Its distance and weights routes based on queue time. *¿Why do I do it?*
            > To watch routes with bad performance. It is just to analyze better



        **Why do we need this?** So you can decide whether to change truck assignment or keep them going.

2. ##### Match Pala-Camión tab:

    - Is it that we need to add/substract truck from a specific loader?. *The app handles it based on the well-know formula*


<img src="https://render.githubusercontent.com/render/math?math=e^{i +\pi} =x+1">

<img src="https://latex.codecogs.com/gif.latex?Camiones-esperado&space;=&space;\frac{Dumptravel_t&space;&plus;&space;Dumping_t&space;&plus;&space;Loadtrave_t&space;&plus;&space;Spot_t&space;&plus;&space;Load_t}{Spot_t&space;&plus;&space;Load_t}" title="Camiones-esperado = \frac{Dumptravel_t + Dumping_t + Loadtrave_t + Spot_t + Load_t}{Spot_t + Load_t}" />

3. ##### Issues:

    - **"Rock parameters" tab is still on development**. However, as far as this is developed, you can calculate it by your own and input that!