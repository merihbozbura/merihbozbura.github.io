
import numpy as N

import Scientific.IO.NetCDF as S
'''
fileobj = S.NetCDFFile('air.mon.mean.nc', mode='r')
print fileobj.title
print fileobj.dimensions
print fileobj.variables
data = fileobj.variables['air'].getValue()
print N.shape(data)
print data[0:10,30,40]
print fileobj.variables['air'].long_name
'''
'''
fileobj = S.NetCDFFile('air.mon.mean.nc', mode='r')
time_data = fileobj.variables['time'].getValue()
time_units = fileobj.variables['time'].units
fileobj.close()

'''
'''
fileobj = S.NetCDFFile('new.nc', mode='w')

lat = N.arange(10, dtype='f')
lon = N.arange(20, dtype='f')

data1 = N.reshape(N.sin(N.arange(200, dtype='f')*0.1),(10,20))
data2 = 42.0

fileobj.createDimension('lat', len(lat))
fileobj.createDimension('lon', len(lon))

lat_var = fileobj.createVariable('lat', 'f', ('lat',))
lon_var = fileobj.createVariable('lon', 'f', ('lon',))

data1_var = fileobj.createVariable('data1', 'f',('lat','lon'))
data2_var = fileobj.createVariable('data2', 'f', ())

lat_var[:] = lat[:]
lon_var[:] = lon[:]

data1_var[:,:] = data1[:,:]
data1_var.units = 'kg'
data2_var.assignValue(data2)

fileobj.title = "New netCDF file"
fileobj.close()
'''