import sys
from numpy import *
import numpy as np

data = np.loadtxt('F_1_4GHz_42deg.pat',usecols = (0,1))
theta= data[:,0]
E_theta_mag= data[:,1]

fig = plt.figure()
ax = fig.add_subplot(111)
for label in ax.get_xticklabels() + ax.get_yticklabels():
    label.set_fontsize(8.5)
ax.set_xlabel(r'station x coordinate in meters')
ax.set_ylabel(r'station y coordinate in meters')
ax.set_title(r'$SKA\ Log-spiral\ Configuration:\ 5\ arm\ asymmetric\ configuration\ beyond\ central\ area; N_{ant}=%s $' %(Na),fontsize=9.0)
ax.plot(xx,yy,'ro') 
# ax.semilogx(xx,yy,'ro')
# ax.plot(xx,yy)
plt.grid(True)
plt.show()  # display plot
