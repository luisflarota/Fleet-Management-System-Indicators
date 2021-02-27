# Luisin Soluciones - Web Dashboard - Fleet Management Systems Analyzer

**1. Short Summary**: This is a web data analyzer that handles a local database that comes from FMS at big-large mining companies.
  - How does it look like?:

    ![first](https://user-images.githubusercontent.com/64980133/109397992-f067d280-7907-11eb-8919-598258ed1268.png)


#### Features:


1. ##### Cycle time handler:
    - It consults the local database and gets:
       * Routes: Its distance and weights routes based on queue time. *¿Why do I do it?*
            > To watch routes with bad performance. It is just to analyze better

        ![cicl](https://user-images.githubusercontent.com/64980133/109398000-feb5ee80-7907-11eb-811a-10e6afe7e942.jpg)


        **Why do we need this?** So you can decide whether to change truck assignment or keep them going.

2. ##### Match factor tab:

    - Is it that we need to add/substract truck from a specific loader?. *The app handles it based on the well-know formula*

    <img src="https://latex.codecogs.com/gif.latex?Trucks-needed&space;=&space;\frac{Dumptravel_t&space;&plus;&space;Dumping_t&space;&plus;&space;Loadtrave_t&space;&plus;&space;Spot_t&space;&plus;&space;Load_t}{Spot_t&space;&plus;&space;Load_t}" title="Camiones-esperado = \frac{Dumptravel_t + Dumping_t + Loadtrave_t + Spot_t + Load_t}{Spot_t + Load_t}" />

    <img src="https://latex.codecogs.com/gif.latex?Match-factor&space;=&space;\frac{Trucks&space;(actual)}{Trucks-needed}" title="Match-factor = \frac{Trucks (actual)}{Trucks-needed}" />

    
    ![Inkedtruck_needed_LI](https://user-images.githubusercontent.com/64980133/109398013-17260900-7908-11eb-9efa-28c9b820eebc.jpg)


3. ##### Availability and UoD:

    - Based on a specific model time for each mine - This tab helps you with your reports (if we talk about automation)

    ![Inkedavailability_uod_LI](https://user-images.githubusercontent.com/64980133/109398024-21e09e00-7908-11eb-8b3f-18147dfe1d25.jpg)


4. ##### Issue:
   - The project is still in development