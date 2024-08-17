from radmc3dPy import *
import matplotlib.pylab as plb
import matplotlib.pyplot as plt
import numpy as np
import math
import sys
from astropy.io import fits 

im = image.readImage()
image.plotImage(im, au=True, log=True, maxlog=5, saturate=1e-1,ifreq=250, cmap=plb.cm.gist_heat)
im.writeFits('image1.fits', dpc=185., coord='11h04m22.8s -77d18m08.0s')


