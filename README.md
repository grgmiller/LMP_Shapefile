# LMP_Shapefile
Version 1

Last Updated January 16, 2019

This python script creates a shapefile and csv file of Locational Marginal Pricing Nodes in CAISO and most of WECC from the json data that is used in the map found at:  http://wwwmobile.caiso.com/Web.Service.Chart/pricecontourmap.html

This repository contains:
  - **CAISO_LMP.py**: used to create a new csv file and shapefile 
  - **LMP**: folder that contains the shapefile (current as of January 16, 2019)
  - **LMP_coordinates.csv**: contains latitude, longitude, balancing area, node ID, and node type
  
This code adapts a function that was deleted from WattTime/pyiso/caiso.py commit [c99beaf44436753d30e48cc7f8f692d3a524d2c5](https://github.com/WattTime/pyiso/commit/c99beaf44436753d30e48cc7f8f692d3a524d2c5) committed by r24mille on Dec 14, 2017
  
This data is pulled from the json file located at http://wwwmobile.caiso.com/Web.Service.Chart/api/v3/ChartService/PriceContourMap1

The following is the document tree for the json file with a description of each of the data points included
```
  <PriceContourMapDto>
    <l>
        <PriceContourLayer> <l>3</l>
            <m>
                <PriceCountourMarker> #each LMP node
                    <c xmlns:d6p1="http://schemas.microsoft.com/2003/10/Serialization/Arrays">
                        <d6p1:decimal>40.53944</d6p1:decimal>           #latitude
                        <d6p1:decimal>-111.89667</d6p1:decimal>         #longitude
                    </c>
                    <dc>52.81386</dc>           #Day-ahead energy $
                    <dg>-3.52064</dg>           #Day-ahead congestion $
                    <dk>0</dk>                  #price color code
                    <dl>-2.26571</dl>           #Day-ahead losses $
                    <do>1</do>                  #unique ordering key for each node
                    <dp>47.02751</dp>           #Day-ahead price $
                    <fc>56.60284</fc>           #Fifteen Minute Market energy $
                    <fg>0</fg>                  #FMM congestion $
                    <fk>1</fk>
                    <fl>-3.01127</fl>           #FMM losses $
                    <fo>1</fo>
                    <fp>53.59157</fp>           #FMM price $
                    <n>118THSO_LNODER1</n>      #Node Name
                    <p>LOAD</p>                 #Load Type
                    <qc>73.41486</qc>           #Real-Time Dispatch energy $
                    <qg>-0.0024</qg>            #RTD congestion $
                    <qk>4</qk>                  
                    <ql>-3.94959</ql>           #RTD losses $
                    <qo>1</qo>                  
                    <qp>69.46287</qp>           #RTD price $
                    <t>Node</t>
                </PriceContourMarker>
```
