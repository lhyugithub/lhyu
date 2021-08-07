# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>
#This file has to be downloaded to local computer to be able use scatter3D plot, togehter with the data used in the file.

from __future__ import print_function
import matplotlib.pylab as plt
import numpy as np
import os
import sys
#import commands
from numpy import array
from numpy import linalg
import time
import matplotlib
import matplotlib.cm as cm
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
t0=time.clock()

import pickle
import scipy
from scipy import optimize


global scalex,  tol


tol=1e-12

print(time.clock()-t0 ,"seconds for import sqdf and jfdf")
t0=time.clock()


def sv(filename,x):
	ff=open(filename,'wb')
	pickle.dump(x,ff)
	ff.close()

def rl(filename):
	ff=open(filename,'rb')
	xx=pickle.load(ff,encoding='latin1')
	ff.close()
	return xx

st,st1,std,std1,label=rl('junk')
xlabel1=label['xlabel1']
ylabel1=label['ylabel1']
xlabel2=label['xlabel2']
ylabel2=label['ylabel2']
xlabel4=label['xlabel4']
ylabel4=label['ylabel4']
xlabel5=label['xlabel5']
ylabel5=label['ylabel5']
zlabel1=label['zlabel1']
zlabel2=label['zlabel2']
zlabel4=label['zlabel4']
zlabel5=label['zlabel5']
fign=label['fign']

#st,st1,st2=rl('junk')
#plt.figure(1)
#plt.plot(st[3],st[1],'.') #phiy vz Jy
#plt.axes().set_aspect('equal')
#plt.figure(2)
#plt.plot(st[2],st[1],'.')#phix vz. Jx

from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter
matplotlib.rc('xtick', labelsize=20) 
matplotlib.rc('ytick', labelsize=20) 

fig = plt.figure(1)
ax = fig.add_subplot(111, projection='3d')
zmax=max(st[1].real)
zmin=min(st[1].real)
zmean=np.mean(st[1])
print(" xp, zmax,zmin=",zmax,zmin)
#matplotlib.rc('xtick', labelsize=10) 
#matplotlib.rc('ytick', labelsize=10)
#ax.set_zlim3d(zmin*0.,zmax*1.1)
'''
xlabel=r'$\theta_1$'
ylabel=r'$\theta_2$'
zlabel1=r'$Re(\phi_2)$'
zlabel2=r'$Im(\phi_2)$'
zlabel4=r'$Re(\phi_1)$'
zlabel5=r'$Im(\phi_1)$'
'''
ax.scatter(st[2], st[3], st[1], c='r', marker='.')
ax.scatter(std[2], std[3], std[1], c='b', marker='.')
ztick=ax.get_zticks(minor=False)
lbl=[ ('%0.03e'%a).split("e") for a in ztick]
lbl2=list(zip(*[ [i[0],str(int(i[1]))] for i in lbl]))
lbl3=["$ \\times 10^{"+str(tmp)+"}$" for tmp in lbl2[1] ]
lbl4=list(zip(*[lbl2[0],lbl3]))
lbl5=[ i[0]+i[1] for i in lbl4]
ax.set_zticklabels(lbl5,rotation=0,ha='center',size='xx-large')
ax.set_xlabel('\n\n'+xlabel1,fontsize=20)
ax.set_ylabel('\n\n'+ylabel1,fontsize=20)
ax.set_zlabel('                    '+zlabel1+'\n\n',fontsize=20)
#ax.set_xlim3d(-4,4)
#ax.set_ylim3d(-4,4)

plt.title('Fig.'+str(fign[0]))
plt.savefig('junk1.png')



fig = plt.figure(2)
ax = fig.add_subplot(111, projection='3d')

zmax=max(st1[1].real)
zmin=min(st1[1].real)
zmean=np.mean(st1[1])

print(" for yp,  zmax,zmin=",zmax,zmin)

ax.scatter(st1[2], st1[3], st1[1], c='r', marker='.')
ax.scatter(std1[2], std1[3], std1[1], c='b', marker='.')

ax.set_xlabel('\n\n'+xlabel2,fontsize=20)
ax.set_ylabel('\n\n'+ylabel2,fontsize=20)
ax.set_zlabel('                    '+zlabel2+'\n\n',fontsize=20)
#ax.set_xlim3d(-4,4)
#ax.set_ylim3d(-4,4)
#ax.set_zlim3d(zmin*0.,zmax*1.1)
plt.title('Fig.'+str(fign[1]))
plt.savefig('junk2.png')


fig = plt.figure(4)
ax = fig.add_subplot(111, projection='3d')

zmax=max(st[0].real)
zmin=min(st[0].real)
zmean=np.mean(st[0])
print(" for x,  zmax,zmin=",zmax,zmin)
#ax.set_zlim3d(zmin*0.,zmax*1.1)
ax.scatter(st[2], st[3], st[0], c='r', marker='.')
ax.scatter(std[2], std[3], std[0], c='b', marker='.')
ztick=ax.get_zticks(minor=False)
lbl=[ ('%0.3e'%a).split("e") for a in ztick]
lbl2=list(zip(*[ [i[0],str(int(i[1]))] for i in lbl]))
lbl3=["$ \\times 10^{"+str(tmp)+"}$" for tmp in lbl2[1] ]
lbl4=list(zip(*[lbl2[0],lbl3]))
lbl5=[ i[0]+i[1] for i in lbl4]
ax.set_zticklabels(lbl5,rotation=0,ha='center',size='xx-large')
#plt.gca().zaxis.set_major_formatter(FormatStrFormatter('%.1e'))
ax.set_xlabel('\n\n'+xlabel4,fontsize=20)
ax.set_ylabel('\n\n'+ylabel4,fontsize=20)
ax.set_zlabel('                    '+zlabel4+'\n\n',fontsize=20)
#ax.set_xlim3d(-4,4)
#ax.set_ylim3d(-4,4)

plt.title('Fig.'+str(fign[2]))
plt.savefig('junk4.png')

fig = plt.figure(5)
ax = fig.add_subplot(111, projection='3d')

zmax=max(st1[0].real)
zmin=min(st1[0].real)
zmean=np.mean(st1[0])

print(" for y,  zmax,zmin=",zmax,zmin)

ax.scatter(st1[2], st1[3], st1[0], c='r', marker='.')
ax.scatter(std1[2], std1[3], std1[0], c='b', marker='.')
ax.set_xlabel('\n\n'+xlabel5,fontsize=20)
ax.set_ylabel('\n\n'+ylabel5,fontsize=20)
ax.set_zlabel('                    '+zlabel5+'\n\n',fontsize=20)
#ax.set_xlim3d(-4,4)
#ax.set_ylim3d(-4,4)
#ax.set_zlim3d(zmin*0.,zmax*1.1)
plt.title('Fig.'+str(fign[3]))
plt.savefig('junk5.png')
plt.show()
#sys.exit(0)
