#!/usr/bin/env python
# Cusize for an icosahedral grid, see README for more information


import numpy as np
from netCDF4 import Dataset
import os
path = '/home/thirza/Cusize_python/PyRipser/python'
os.chdir(path)
#print os.listdir('.')
from unionfind import UnionFind



# Load files and variables

# Grid file
# ql file

grid = Dataset('/home/thirza/Cusize_python/subsubgrid.nc','r',format='NETCDF4')

clon = grid.variables['clon'][:]
clat = grid.variables['clat'][:]
clon_vertices = grid.variables['clon_vertices'][:]
clat_vertices = grid.variables['clat_vertices'][:]
cell_area = grid.variables['cell_area'][:]
neighbor_cell_index = grid.variables['neighbor_cell_index'][:]

darea = max(cell_area)

ql_file = Dataset('/home/thirza/Cusize_python/subsubdomain_lasttimestep.nc','r',format='NETCDF4')
ncells = ql_file.variables['ncells'][:]

def nextfield(ql_file):
    ql = ql_file.variables['qc'][time,:]
    ql_proj = np.sum(ql,axis=0)
    ql_binary = np.where(ql_proj>1E-8,1,0)
    return ql_binary


# Do time loop (will follow later)
time = 0

ql_binary = nextfield(ql_file)
sum_ql = float(np.sum(ql_binary))
cloudcover = sum_ql/ncells

print cloudcover

##############################################

# Clustering part


idx_clouds = np.array(np.where(ql_binary))[0]

nr_cloud_cells = len(idx_clouds)

test = UnionFind(nr_cloud_cells)

counter = 0


#for j in range(0,nr_cloud_cells):
for j in range(0,10):
    cell_1 = idx_clouds[j]
    for i in range(0,3):
        cell_2 = neighbor_cell_index[i,cell_1]
        if cell_2 != -1:
            if ql_binary[cell_2]:
                print cell_2
                idx_2 = np.where(idx_clouds==cell_2)
                test.link(j,idx_2)
                counter += 1
       
print 'counter:',counter

for j in range(0, nr_cloud_cells):
    test.find(j)

#print test.parent
       
###################################################################

# Labelling, plus calculating size and center

cloud_label = 0
cloud_size_long = np.zeros(ncells)

parents = set(test.parent)
for p in parents:
    #print '%d --- %s' % (p, np.where(test.parent == p))
    idx_parent = np.where(test.parent == p)
    #print idx_parent
    cloud_cells = idx_clouds[idx_parent]
    #print cloud_cells
    cloud_size_long[cloud_label] = len(idx_parent[0])
    cloud_label += 1
    
    
cloud_size = np.trim_zeros(cloud_size_long)

print cloud_size
nr_clouds = len(cloud_size)
print nr_clouds 
