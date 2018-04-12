import numpy as np
from mpl_toolkits.basemap import Basemap
from netCDF4 import Dataset
import sys
import matplotlib.pyplot as plt
from netcdf_functions import nc_read
import datetime
import netCDF4
import iris.palette
import matplotlib.image as mgimg
from matplotlib import animation





# read the variables
u = nc_read('1000_850_geo_u_v_katrina_area.nc','u')
v = nc_read('1000_850_geo_u_v_katrina_area.nc','v')
lon = nc_read('1000_850_geo_u_v_katrina_area.nc','longitude')
lat = nc_read('1000_850_geo_u_v_katrina_area.nc','latitude')
path='/Users/merihbozbura/Documents/Pycharm/GFD/1000_850_geo_u_v_katrina_area.nc'
f = Dataset(path)
time_var = f.variables['time']

dtime = netCDF4.num2date(time_var[:],time_var.units)



for i in range(89,124,1):

        # just extract one level at one time
        # in this example I select 110 but you should make a for loop and save all
        # plots and make a movie



    uvel = np.copy(u[i,0,:,:])
    vvel = np.copy(v[i,0,:,:])

    dx = dy = 80000 # meter

        # compute dudy
        # Be careful first dimension is lat which has 41 elements and second dimension
        # is lon which has 55 elements, thus the computations below are for that

    dudy = (uvel[1:,:]-uvel[:-1,:])/dy
        # compute dvdx
    dvdx = (vvel[:,1:]-vvel[:,:-1])/dx

        # the dimensions of dudy and dvdx are off p
        # so I add the last row/column to the end+1 so that dimensions will match
        # ignore boundaries
    aa = np.copy(dudy[-1,:])*np.ones((1, 55))
    dudy = np.r_[dudy,aa]

    #print aa.shape
    #print dudy
    aa = np.transpose(np.copy(dvdx[:,-1])*np.ones((1, 41)))
    dvdx = np.c_[dvdx,aa]


        # vorticity is equal to dvdx-dudy
    vort = dvdx-dudy
        # next line I will find the maximum vorticity location but you can find maximum
        # absolute vorticity etc.
    indcs = np.where(vort==vort.max())





        #### Okubo Weiss Parameter (1/s^2)   w = dvdx-dudy = vort,        Sn = du/dx - dv/dy,      Ss = dv/dx + du/dy,       W = Sn^2 + Ss^2 - w^2,

    Ss = dvdx + dudy


        # For Sn =dudx-dvdy

    dvdy = (vvel[1:,:]-vvel[:-1,:])/dy

    dudx = (uvel[:,1:]-uvel[:,:-1])/dx

    aaaa = np.copy(dvdy[-1,:])*np.ones((1, 55))
    dvdy = np.r_[dvdy,aaaa]

    aaaa = np.transpose(np.copy(dudx[:,-1])*np.ones((1, 41)))
    dudx = np.c_[dudx,aaaa]

    Sn = dudx - dvdy

    W = Sn**2 + Ss**2 - vort**2

#print W.max()







    fig = plt.figure()

        # plot the Okuba Weiss
    x,y = np.meshgrid(lon,lat)

    indcs_W = np.where(W==W.max())



    nice_cmap = plt.get_cmap('brewer_RdYlBu_11')


    m=Basemap(llcrnrlon=-130,llcrnrlat=10,urcrnrlon=-55,urcrnrlat=55,projection='cyl')
    m.drawcoastlines()
        #m.fillcontinents()
    parallels = np.arange(20,55,10.) # make latitude lines ever 5 degrees from 30N-50N
    meridians = np.arange(-130,-60,10.) # make longitude lines every 5 degrees from 95W to 70W
    m.drawparallels(parallels,labels=[1,0,0,0],fontsize=10)
    m.drawmeridians(meridians,labels=[0,0,0,1],fontsize=10)
    im1 = m.pcolormesh(x-360,y,np.ma.masked_invalid(W),shading='flat',latlon=True , cmap=nice_cmap, vmin=0.00000001, vmax= 0.00000007)
    plt.title('Okubo W  ' + str(dtime[i]))
    plt.xlabel('Longitude' , labelpad= 30 )
    plt.ylabel('Latitude' ,labelpad = 40)
    lonWmax,latWmax = m(x[indcs_W], y[indcs_W])
    m.plot(lonWmax-360, latWmax, 'ko', markersize=7)
        #m.plot(x[indcs],y[indcs],linewidth=1.5,color='k')
    cb = m.colorbar(im1,"right", size="5%", pad="10%") # pad is the distance between colorbar and

    fig.tight_layout()
    plt.show()
    fig.savefig('Okuba_' + str(dtime[i]) + '.png')


   
    
    fig1 = plt.figure()



        # plot the vorticity
    x,y = np.meshgrid(lon,lat)


    nice_cmap = plt.get_cmap('brewer_RdYlBu_11')


    map=Basemap(llcrnrlon=-130,llcrnrlat=10,urcrnrlon=-55,urcrnrlat=55,projection='cyl')
    map.drawcoastlines()
        #map.fillcontinents()
    parallels = np.arange(20,55,10.) # make latitude lines ever 5 degrees from 30N-50N
    meridians = np.arange(-130,-60,10.) # make longitude lines every 5 degrees from 95W to 70W
    map.drawparallels(parallels,labels=[1,0,0,0],fontsize=10)
    map.drawmeridians(meridians,labels=[0,0,0,1],fontsize=10)
    im2 = map.pcolormesh(x-360,y,np.ma.masked_invalid(vort),shading='flat',latlon=True, cmap = nice_cmap, vmin=0 , vmax = 0.0002)
    plt.title('Vorticity  ' + str(dtime[i]))
    plt.xlabel('Longitude' , labelpad= 30 )
    plt.ylabel('Latitude' ,labelpad = 40)
    lonvortmax,latvortmax = map(x[indcs], y[indcs])
    map.plot(lonvortmax-360, latvortmax, 'ko', markersize=7)
        #map.plot(x[indcs],y[indcs],linewidth=1.5,color='k')
    cb = map.colorbar(im2,"right", size="5%", pad="10%") # pad is the distance between colorbar and figure
    fig1.tight_layout()

    print lon




    plt.show()


    fig1.savefig('Vort_' + str(dtime[i]) + '.png')



