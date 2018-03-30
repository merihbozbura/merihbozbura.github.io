---
layout: post
title: A Great First Post
---

Hi!
This is it!
What a wonderful post!


![Image of Avatar The Last Airbender](https://github.com/merihbozbura/merihbozbura.github.io/blob/master/images/avatar-last-airbender.jpg?raw=true)

*Image: Nickelodeon*



```R
data=readLines("/Users/merihbozbura/Documents/THESIS RELATED/WinSCP
/edt-—5-DJF-ERA-N40-c2-c01—2")

data=data[-(1:4)]
```

```python


######################################################################################
######################################################################################
                                                                              ########
                                                                              ########
import numpy as np                                                            ########
                                                                              ########
import Scientific.IO.NetCDF as si                                             ########
                                                                              ########
import netCDF4                                                                ########
                                                                              ########
from netCDF4 import Dataset                                                   ########
                                                                              ########
import datetime                                                               ########
                                                                              ########
                                                                              ########
                                                                              ########
# import multiprocessing as mp                                                ########
#import matplotlib.pyplot as plt                                              ########
#from mpl_toolkits.basemap import Basemap, addcyclic, shiftgrid               ########
                                                                              ########
                                                                              ########
                                                                              ########
######################################################################################
######################################################################################


path='/home/maryjane/1000_850_500_geopotantial_height.nc'


#### Time conversion

'''
f = Dataset(path)

p1000 = f.variables['z'][0,2,35,55]
time_var = f.variables['time']
dtime = netCDF4.num2date(time_var[:],time_var.units)

'''
#########################################################################




def minimum (time1, time2, lat1,lat2,lon1,lon2):


    fileobj = si.NetCDFFile(path , mode='r')

    lon = fileobj.variables['longitude'].getValue()
    lat = fileobj.variables['latitude'].getValue()
    time = fileobj.variables['time'].getValue()
    geo = fileobj.variables['z'].getValue()  # z = geopotantial m**2/s**2

    scale_factor = 0.983600461790243
    add_offset = 26901.5785122691
    Treshold = 1020.0



    #### Search for  Mininmum Pressure over 3*3 Gridpoint Area ####

    rank_of_loop = np.ndarray(0)

    pressure = np.zeros(16)

    time_steps ={}

    for t in range(time1,time2):

        candidate_pressures = np.ndarray(0)


        for i in range(lat1,lat2):
            for j in range(lon1,lon2):


                index = {"lattitude": i , "longitude": j}

                rank_of_loop = np.append(rank_of_loop,index)

                ####### Unpacking the data
                packed_value = geo[t , 2 , i , j]
                unpacked_value = ((packed_value * scale_factor) + add_offset)

                ####### Geopotantial to geopotantial meter (m**2/s**2  to  m)
                geopotantial_meter = (unpacked_value // 9.80665)

                #######  Geopotatial meter to hectopascal
                P_at_z1000 = (geopotantial_meter * 0.121) + 1000

                pressure = P_at_z1000
                pressure_array = np.asfarray(pressure, np.float64)
                candidate_pressures = np.append(candidate_pressures , pressure_array)

        candidate_center = np.amin(candidate_pressures)

        if candidate_center < Treshold:
            index = np.where(candidate_center == candidate_pressures)
        else:
            print "There is no pressure point below 1020 hPa."

        print rank_of_loop[index]

        time_steps['candidate_pressures%s'  %t] = candidate_pressures

        #print time_steps['candidate_pressures%s'  %t] #candidate_pressures over a*b gridpoint area

        print "Time step is " + str(t)+"." ; print "------------------------------"




minimum(54964,54966,37,39,53,55)























