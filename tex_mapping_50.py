from matplotlib.cm import get_cmap
import numpy as np
import nrrd
import pyvista as pv
from pyvista import examples
from PIL import Image
import mcubes
import nrrd
import time

###########################################################################read data

data = np.load("new_50_2.npy")
data = data.transpose(2,1,0)
nrrd_filename = '5A.nrrd'
nrrd_data, nrrd_options = nrrd.read(nrrd_filename)


###########################create an image using numpy
time_start = time.time()
vertices, triangles = mcubes.marching_cubes(data, 11.02)
texmash = np.asarray(vertices)
V = np.zeros((970,936))
for i in range(len(texmash)):
    V[int(texmash[i][1]),int(texmash[i][2])] = (nrrd_data[int(texmash[i][0]),int(texmash[i][1]),int(texmash[i][2])])
V = np.asarray(V)
image=Image.fromarray(V)
if image.mode != 'RGB':
    image = image.convert('RGB')
image.save("1.jpg")
time_end = time.time()
print(time_end - time_start,"s")
tex2 = pv.read_texture("1.jpg")
x = texmash[...,0]
y = texmash[...,1]
z = texmash[...,2]
curvsurf = pv.StructuredGrid(x,y,z)
curvsurf.texture_map_to_plane(inplace=True)
curvsurf.plot(texture=tex2)
