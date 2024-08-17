from radmc3dPy import *
import matplotlib.pylab as plb
import matplotlib.pyplot as plt
import numpy as np
import math
import sys
from astropy.io import fits 
AU  =  1.4960e13 	# cm
AMU = 1.660538921e-24 	# atomic mass unit [g]

data = analyze.readData(ddens=True)
def sph2cart(az, el, r):
    rsin_theta = np.outer(r,np.sin(el))  
    x = rsin_theta * np.cos(az)
    y = rsin_theta * np.sin(az)
    z = np.outer(r,np.cos(el))   
#(x[:,None]*y)
    return x, y, z
x,y,z=sph2cart(np.pi,data.grid.y, data.grid.x)
print(data.grid.y)
#x=abs(x)
#print(x)
#print(x.shape)
#print(len(y))
#print(z)
#print(z.shape)
#print(data.rhodust.shape)
#print(data.rhodust[:,:,0,0])
dusty=np.zeros((150,100))
#print(dusty)
#c= plb.contourf(data.grid.x/natconst.au,np.pi/2.-data.grid.y, np.log10(rhodust.T, 30)
region=0
for i in range(2):
	if i%2==0:
		p='small' 
	else:
		p='large' 

	c = plb.contourf(x/natconst.au,z/natconst.au,np.log10(data.rhodust[:,:,0,i]),cmap='BuPu',levels=np.linspace(-22,-14,100),extend='both')
#	E =[*range(-22,-14,1)]
	cf = plt.contour(x/natconst.au,z/natconst.au,np.log10(data.rhodust[:,:,0,i]))
	plt.clabel(cf,fontsize='smaller')
#	lines,labels = cf.legend_elements()
	plb.xlabel('x [AU]')
	plb.ylabel('z [AU]')
#	plb.xticks(np.arange(0,-100,-5))
	plb.xlim(-250,0)
#	plb.yticks(np.arange(0,100,5))
	plb.ylim(-100,100)
	cb = plb.colorbar(c)
	cb.set_ticks(np.arange(-23,-13))
	cb.set_label(r'$\log_{10}{\rho}$', rotation=270.,verticalalignment='baseline')
	plb.title('dust density %d,%s'%(region,p))
	plb.savefig('dust density contour %d,%s.png'%(region,p))
	plb.clf()
	dusty=np.add(dusty,data.rhodust[:,:,0,i])
	if not i%2==0:
		region=region+1

#au = 1.496e13     # Astronomical unit [cm]
#plb.xlabel('r [AU]')
#plb.ylabel(r'$\pi/2-\theta$')
#plb.xscale('log')
#plt.xlim(0,250)
#plt.ylim(-100,100)
#plt.show()
"""
c = plb.contourf(x/natconst.au,z/natconst.au,np.log10(dusty), 100)
plb.xlabel('x [AU]')
plb.ylabel('z [AU]')
cb = plb.colorbar(c)
cb.set_label(r'$\log_{10}{\rho}$', rotation=270.,verticalalignment='baseline')
plb.title('dust density (all species combined)')
plb.savefig('dust density contour(all species combined).png')
plb.clf()
"""
'''
#opac = analyze.readOpac(idust=[0])
#plb.loglog(opac.wav[0], opac.kabs[0])
#plb.xlabel(r'$\lambda$ [$\mu$m]')
#plb.ylabel(r'$\kappa_{\rm abs}$ [cm$^2$/g]')
#plb.savefig('dustopacity.png')
'''
regionopac=0
for i in [0,1]: 
	opac = analyze.readOpac(scatmat=True,idust=i)
	if i%2==0:
		l='small'
	else:
		l='large'
	plb.loglog(opac.wav[0], opac.kabs[0],label='dust species %d,%s'%(regionopac,l))
	plb.xlabel(r'$\lambda$ [$\mu$m]')
	plb.ylabel(r'$\kappa_{\rm abs}$ [cm$^2$/g]')
	plb.legend()
	plb.title('Dust Opacities')
	plb.savefig('dust opacity(%d,%s).png'%(regionopac,l))
	plb.clf()
	if not i%2==0:
		regionopac=regionopac+1
data.getTau(wav=0.5)
taux=data.taux
print(np.shape(taux))
print(taux)
'''
#c = plb.contour(data.grid.x/natconst.au, np.pi/2.-data.grid.y, data.taux[:,:,0].T, [1.0],  colors='w', linestyles='solid')
c = plb.contour(x/natconst.au,z/natconst.au, data.taux[:,:,0], [1.0],  colors='w', linestyles='solid')
plb.clabel(c, inline=1, fontsize=10)
plb.savefig('optical depth.png')
'''
"""
plb.clf()
data2 = analyze.readData(dtemp=True)  #reading dust temperature (The readData() function is only an interface to the methods of the radmc3dData class.)
#print(data.dusttemp[:,:,0,0])
#c = plb.contourf(data.grid.x/natconst.au, np.pi/2.-data.grid.y, data.dusttemp[:,:,0,0].T, 30)
tempy=np.zeros((150,100))
print(np.shape(data2.dusttemp))
for i in range(2):
	if i%2==0:
		t='small'
	else:
		t='large'
	c = plb.contourf(x/natconst.au,z/natconst.au,np.log10(data2.dusttemp[:,:,0,i]), 100)
	plb.xlabel('x [AU]')
	plb.ylabel('z [AU]')
	cb = plb.colorbar(c)
	cb.set_label(r'$\log_{10}T(K)$', rotation=270.,verticalalignment='baseline')
	plb.title('dust temperature %s'% t)
	plb.savefig('dust temperature contour(enveloped) %s.png'% t)
	plb.clf()
	tempy=np.add(tempy,data2.dusttemp[:,:,0,i])

c = plb.contourf(x/natconst.au,z/natconst.au,np.log10(tempy), 100)
#plb.xlabel('r [AU]')
plb.xlabel('x [AU]')
#plb.ylabel(r'$\pi/2-\theta$')
plb.ylabel('z [AU]')
#plb.xscale('log')
cb = plb.colorbar(c)
cb.set_label(r'$\log_{10}T(K)$', rotation=270.,verticalalignment='baseline')

#print(x/natconst.au,z/natconst.au,data.dusttemp[:,:,0,0])
#c = plb.contour(data.grid.x/natconst.au, np.pi/2.-data.grid.y, data.dusttemp[:,:,0,0].T, 10,  colors='k', linestyles='solid')
#c = plb.contour(x/natconst.au,z/natconst.au,data.dusttemp[:,:,0,0], 200,  colors='k', linestyles='solid')
#plb.clabel(c, inline=1, fontsize=10)
plb.title('dust temperature (all species combined)')
plb.savefig('dust temperature contour enveloped(all species combined).png')
"""
###Combined figure of dust density + temperature distribution 
data2 = analyze.readData(dtemp=True)  #reading dust temperature (The readData() function is only an interface to the methods of the radmc3dData class.)
#print(data.dusttemp[:,:,0,0])
for i in range(2):
	if i%2==0:
		t='small'
	else:
		t='large'
	V = [20,80,155]      #for temperature contour lines
	c = plb.contourf(x/natconst.au,z/natconst.au,np.log10(data.rhodust[:,:,0,i]),100,cmap='BuPu',levels=np.linspace(-22,-14,100),extend='both')
	cb = plb.colorbar(c)
	cb.set_ticks(np.arange(-23,-13))
	cb.set_label(r'$\log_{10}{\rho}$', rotation=270.,verticalalignment='baseline')
	plb.ylim(-100,100)
	plb.xlim(-250,0)
	con=plt.contour(x/natconst.au,z/natconst.au,data2.dusttemp[:,:,0,i],V)	
	plt.clabel(con,fontsize='smaller')
	lines,labels = con.legend_elements()
	plt.legend(lines,['CO','CO2','H2O'])
	plt.xlabel('x [AU]')
	plt.ylabel('z [AU]')
#	plt.title('%s dust population'% t)
	plt.savefig('new dust density with temperature %s.png'% t)
	plt.clf()



