#In  this python script, I'm trying to place a set number of
# antennas randomly within a logarithmic spiral configuration.
# The output antenna locations (x,y.z ECEF coordinates) are
# written to a text file.
# A plot is also generated of the random
# antenna positions for visual inspection.

# from visual import *
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

#defining some parameters for the locations catalog, i.e., the 'ants.txt' file
dbcode = 'SKA_'
dbname = 'SKA'
axistype = 'ALT-AZ'
diam = 12


# The (geodetic) latitude and longitude of the center of the VLA in
# dd:mm:ss is: lat. (north) = 34:04:43.75, long. (west) = 107:37:05.91
lat_vla = 34.012152777777779 # degrees
lon_vla = 107.00164166666667 # degrees
h_vla = 2115 # station elevation (height or altitude) of the VLA center above
             # sea level (meters), or height in meters above the reference
             # ellipsoid

# Need to convert from Geodetic to Earth-Centered, Earth Fixed (ECEF) cartesian
# coordinate system. ECEF coordinate system rotates with Earth and has origin at
# Earth's center. Implementation of ECEF coordinate system assumes X-axis intersects
# Greenwich meridian @ equator, Z-axis is mean spin axis of Earth, positive to north
# and passing through North Pole, and Y-axis completes right-hand system, passing through
# equator at 90 degrees longitude (?)

# WGS84 Defining Parameters (note that the locationsSB2.dat file seems to have been using GRS 80
# system; see http://www.ferris.edu/faculty/burtchr/geodesy/datm_faq.html#1.3 to see the
# differences between how the constants are defined for these two cases.
a = 6378137.0 # Earth's equatorial radius or semi-major axis in meters
f = 0.0033528106647474805  # flattening parameter = (a-b)/a, where b is Earth's semi-minor
                           # axis. It's ratio of difference between equatorial and polar
                           # radii to a; this is a measure of how "elliptical a polar cross
                           # section is. Note: e = eccentricity of figure of earth=sqrt(2f-f^2).
denom = sqrt(np.cos(lat_vla*np.pi/180)**2+(1-f)*(1-f)*np.sin(lat_vla*np.pi/180)**2)
C = 1/denom
S=(1-f)*(1-f)*C
# Reference: http://mathforum.org/library/drmath/view/51832.html

# Then a point with (geodetic) latitude and longitude and altitude h above
# the reference ellipsoid has ECEF coordinates (these are the central coordinates
# of our simulated SKA array, which is the same as the center of the VLA array:

x_c = (a*C+h_vla)*np.cos(lat_vla*np.pi/180)*np.cos(lon_vla*np.pi/180)
y_c = -(a*C+h_vla)*np.cos(lat_vla*np.pi/180)*np.sin(lon_vla*np.pi/180) # I think the minus sign
# is needed here to give the right answer (y_c < 0 for VLA); not exactly sure why yet.
z_c = (a*S+h_vla)*np.sin(lat_vla*np.pi/180)
# Reference: http://mathforum.org/library/drmath/view/51832.html

# 'Radius' (r) we're considering for log-spiral curve -- or radius of circle that log-spiral
# configuration is contained within (?). Log-spiral configuration of Na antennas centered
# around (x_c,y_c,z_c).
# Maximum baseline length = 35 km (?), for example
radius = 29500
# Parameters for the log-spiral curve
aprime = 11.0     # don't know what aprime and b should be ... random draws?
b = 0.01  # values of b close to 0 give small pitch angles for the log-spiral
pitch = 90-np.arctan((1/b)*np.pi/180)

Na = 150  # number of antennas
# To cut down on the math, we'll pre-compute R^2

radiusSquared = radius * radius

# Number of points inside the circle. Not really sure if this is needed here ...
numInside = 0

# Total number of random points we've considered
total = 0
# Not sure if this part is needed ...
    # Collection of points that are inside the circle (on the log-sprial?)
insidePoints = []
insidePoints1 = []
xx = []
yy = []
xy = []
yx = []
zz = []
thetaa = []

# Process Na random points, i.e., Na antenna stations
# We are considering constant antenna heights/altitudes (set to be the same
# as the height of the center of the VLA array), so I've commented out this
# part of the code.
## First, cosider a range of antenna altitudes h; take h_min = h_vla-1000 meters
## and h_max = h_vla+1000 meters
# h_min = h_vla-1000
# h_max = h_vla+1000
lat_vla_min = lat_vla-0.157
lat_vla_max = lat_vla+0.157
lon_vla_min = lon_vla-0.189
lon_vla_max = lon_vla+0.189

#Creating an opening an output text file for antenna locations, etc.
sys.stdout=open("ants_Na%s_logspiral1a.txt" %(Na),'w')
for p in xrange(Na):
# We are considering antennas with the same fixed height here, so this part
# has been commented out:
## Create random antenna altitudes within the range h_min and h_max or try other options
#    h = random.uniform(h_min,h_max)
    lat = random.uniform(lat_vla_min,lat_vla_max)
    lon = random.uniform(lon_vla_min,lon_vla_max)
    denom_rand = (np.cos(lat*np.pi/180)*np.cos(lat*np.pi/180)+(1-f)*(1-f)*np.sin(lat*np.pi/180)*np.sin(lat*np.pi/180))**(1/2)
    C_rand = 1/denom_rand
    S_rand=(1-f)*(1-f)*C_rand


    # Generating random r, theta, X, Y, and Z.
    r = sqrt(np.random.uniform(size=None))*radius  # but this is never actually used in the script (?)
    
    # theta = np.random.uniform(size=None)*2*np.pi
    # theta = p*2*np.pi/Na
    # theta=np.random.vonmises(mu=0.0,kappa=0.0,size=None)*180/np.pi
    theta = (1/b)*np.log(r/aprime)

    # x = x_c + np.random.uniform(size=None)*aprime*np.exp(b*np.random.uniform(size=None)*theta)*np.cos(theta*np.pi/180)
    # y = y_c + np.random.uniform(size=None)*aprime*np.exp(b*np.random.uniform(size=None)*theta)*np.sin(theta*np.pi/180)
    x = x_c + aprime*np.exp(b*theta)*np.cos(theta*np.pi/180)
    y = y_c + aprime*np.exp(b*theta)*np.sin(theta*np.pi/180)
    z = (a*S_rand + h_vla)*np.sin(lat*np.pi/180)
    
    # Check if X,Y coordinates are within the circle -- not sure if this is needed
    #  (Note that we don't bother with a square root...in this case,
    #   it makes no difference because we're just comparing)
    if ( x - x_c)**2 + ( y - y_c)**2 <= radiusSquared:
    # if ( x - x_c)**2 + ( y - y_c)**2 <= r**2:
    # if x*x+y*y <= radiusSquared:
    # if x*x+y*y <= r**2:    
    # if ( x * x ) + ( y * y ) <= aprime*aprime*np.exp(2*b*theta*np.pi/180):    
            # Point is inside circle -- add it to point collection and
            #  increment number of points inside circle
          insidePoints.append( (x, y) )
          insidePoints1.append( (y, x) )
          xx.append(x)
          yy.append(y)
          xy.append([x,y])
          yx.append([y,x])
          zz.append(z)
          thetaa.append(theta)
          numInside += 1
          dbcode = "SKA%s" % (numInside-1)
          print dbcode," ",dbname," ", x," ",y," ",z," ",axistype," ",diam
# I don't believe that this part of the code is necessary, so commented it
# out for now.
## We just processed, e.g., 500 more points, so increase the total
total += Na
         
# Here, we are just testing some things out, e.g., seeing if the circular
# area encompassing the log-spiral configuration has a radius that is at
# or near what we specified and checking that the number of antennas listed
# in the output locations text file is at or near what we specified.

# print "x=",xx
# print "y=",yy
# print "theta=",thetaa
# print insidePoints
# sys.stdout=open("info_logsprial1.txt",'w')
Xmax=max(np.absolute(xx))
Xmin=min(np.absolute(xx))
Ymax=max(np.absolute(yy))
Ymin=min(np.absolute(yy))
XYmax = max(xy)
XYmin = min(xy)
YXmax = max(yx)
YXmin = min(yx)
xxyymax = max(insidePoints)
xxyymin = min(insidePoints)
yyxxmax = max(insidePoints1)
yyxxmin = min(insidePoints1)
thetamin=min(thetaa)
thetamax=max(thetaa)
dist1 = Xmax-Xmin
dist2 = Ymax-Ymin
dist3 = sqrt((Xmax-x_c)**2+(Ymax-y_c)**2)
dist4 = sqrt((Xmax-Xmin)**2+(Ymax-Ymin)**2)
dist5 = sqrt((np.absolute(XYmax[0])-np.absolute(XYmin[0]))**2+(np.absolute(XYmax[1])-np.absolute(XYmin[1]))**2)
dist6 = np.absolute(XYmax[0])-np.absolute(XYmin[0])
dist7 = np.absolute(XYmax[1])-np.absolute(XYmin[1])
dist8 = sqrt((np.absolute(xxyymax[0])-np.absolute(xxyymin[0]))**2+(np.absolute(xxyymax[1])-np.absolute(xxyymin[1]))**2)
dist9 = np.absolute(xxyymax[0])-np.absolute(xxyymin[0])
dist10 = np.absolute(xxyymax[1])-np.absolute(xxyymin[1])
dist11 = sqrt((np.absolute(YXmax[0])-np.absolute(YXmin[0]))**2+(np.absolute(YXmax[1])-np.absolute(YXmin[1]))**2)
dist12 = np.absolute(YXmax[0])-np.absolute(YXmin[0])
dist13 = np.absolute(YXmax[1])-np.absolute(YXmin[1])
dist14 = sqrt((Xmax-np.absolute(x_c))**2+(Ymax-np.absolute(y_c))**2)
dist15 = sqrt((np.absolute(yyxxmax[0])-np.absolute(yyxxmin[0]))**2+(np.absolute(yyxxmax[1])-np.absolute(yyxxmin[1]))**2)
dist16 = np.absolute(yyxxmax[0])-np.absolute(yyxxmin[0])
dist17 = np.absolute(yyxxmax[1])-np.absolute(yyxxmin[1])
# dist4 = sqrt((Xmax-Xmin)**2+(Ymax-Ymin)**2)
print "pitch=",pitch
lengthx = len(xx)
lengthy = len(yy)
lengthz = len(zz)
print dist1, dist2, dist3, dist4,dist5,dist6,dist7,dist8,dist9,dist10,dist11,dist12,dist13,dist14,dist15,dist16,dist17
length = len(insidePoints) 
print lengthx,lengthy,lengthz,length,numInside,total

# Finally, we want to generate an (X,Y) plot of the antenna configuration
# to see if it actually appears to be a log-spiral configuration
# within a circular area of the specified diameter.

fig = plt.figure()
ax = fig.add_subplot(111)
for label in ax.get_xticklabels() + ax.get_yticklabels():
    label.set_fontsize(8.5)
ax.set_xlabel(r'station x coordinate in meters')
ax.set_ylabel(r'station y coordinate in meters')
# ax.set_title(r'$Random\ configuration\ of\ antenna\ in\ on log-spiral;\ N_{ant}=%s,B_{max}=%s\ km $' %(lengthx,2*radius/1000),fontsize=8.7)
ax.set_xlim(xmin=-radius)
ax.set_xlim(xmax=radius)
ax.set_ylim(ymin=-radius)
ax.set_ylim(ymax=radius)

# ax.set_xlim(xmin=xmin1)
# ax.set_xlim(xmax=xmax1)
# ax.set_ylim(ymin=ymin1)
# ax.set_ylim(ymax=ymax1)
# ax.plot(xx,yy,'ro')
ax.plot(xx,yy,'k.')
plt.grid(True)
# plt.show()  # display plot
matplotlib.pyplot.savefig('logspiral1a_rand_Na%s.pdf' % Na, dpi=None)
