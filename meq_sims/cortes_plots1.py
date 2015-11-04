from pylab import *
import sys
from numpy import *
import numpy as np
import matplotlib
from matplotlib import *
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter
from matplotlib.ticker import MultipleLocator, FormatStrFormatter
from matplotlib.ticker import *


data = np.loadtxt('F_1_4GHz_42deg_2.pat',usecols = (0,1,2,3,4))
theta= data[:,0]
E_theta_mag= data[:,1]
E_theta_phase= data[:,2]
E_phi_mag= data[:,3]
E_phi_phase=data[:,4]

fig = plt.figure()
ax = fig.add_subplot(111)
for label in ax.get_xticklabels() + ax.get_yticklabels():
    label.set_fontsize(8.5)
ax.set_xlabel(r'$\theta$')
ax.set_ylabel(r'$E_{\theta}$ (dB)')
ax.set_title(r'$Cortes\ Beam\ Pattern:\ E_{\theta}\ (dB)\ vs.\ \theta\ (deg.)$',fontsize=9.0)

# ax.plot(theta,E_theta_mag,'ro')
ax.plot(theta,E_theta_mag,'ro') 
# ax.semilogx(xx,yy,'ro')
# ax.plot(xx,yy)
plt.grid(True)
plt.show()  # display plot
