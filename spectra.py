from radmc3dPy import *
import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits  
cube=fits.open('image1.fits')
cube.info()
data1=cube[0].data
#print(np.shape(data1))
header=cube[0].header
NAXIS1=header['NAXIS1']
NAXIS2=header['NAXIS2']
NAXIS3=header['NAXIS3']
#print(header,NAXIS1,NAXIS2,NAXIS3)

wavelength=[]
f=open('camera_wavelength_micron.inp','r')
count=int(f.readline())
print(count)
for line in f:
   line=float(line)
   wavelength.append(line)
f.close()
print(wavelength)
flux=[]
for i in range(count):
   #print(data1[i,:,:])            #function that creates fits files made the shape of the data this way. number of arrays=number of wavelengths, number of rows for each array=number of nx pixel, number of columns for each array=number of ny pixel
   image=data1[i,:,:].ravel()
   #print(image)
   flux.append(sum(image))    #summing up Jansky/pixel flux values

def wavtofreq(x):
	return 1e4*natconst.cc/x
nu=list(map(wavtofreq,wavelength))
arr1=np.array(nu)
arr2=np.array(flux)
nuflux=np.multiply(arr1,arr2)
plt.plot(wavelength,flux,label='Total SED')
#plt.step(wavelength,flux,where='mid',label='Total SED')
plt.legend()
plt.xlabel('$\lambda\; [\mu \mathrm{m}$]')
plt.ylabel('Jansky $[\mathrm{erg}\,\mathrm{cm}^{-2}\,\mathrm{s}^{-1}]$')
plt.xlim(2,16)
plt.ylim(0,0.007)
plt.show()
#plt.savefig('spectra.png')




