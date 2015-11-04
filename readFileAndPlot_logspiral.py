import numpy as np
import pylab as pl
# Use numpy to load the data contained in the file
# 'SKA_logspiral_Mwieringa1.txt' into a 2-D array called data
# data = np.loadtxt('SKA_logspiral_Mwieringa1.txt',usecols = (1,2))
# data = np.loadtxt('SKA-antenna.txt',usecols = (1,2))
data = np.loadtxt('ants_Na40_logspiral1a.txt',usecols = (2,3))
print data[:,0]
print data[:,1]
# plot the first column as x, and second column as y
fig = pl.figure()
ax = fig.add_subplot(111)
for label in ax.get_xticklabels() + ax.get_yticklabels():
    label.set_fontsize(8.5)
pl.plot(data[:,0], data[:,1], 'ro')
pl.xlabel('x (meters)')
pl.ylabel('y (meters)')
pl.title('Sample SKA log-spiral configuration, clipped to Australian Continent, Mark Wieringa', fontsize = 9.0)
pl.grid(True)
pl.show()

