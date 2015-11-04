#!/usr/bin/env python

# reads in a Cortes antenna pattern, converts it to L,M coordinate equivalent,
# writes out the corresponding fits files for co and cross pol, and plots the
# amplitude

import sys
import numpy
import math 
from string import split, strip
from matplotlib.mlab import griddata
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter
from matplotlib.ticker import MultipleLocator, FormatStrFormatter
from matplotlib.ticker import *
import matplotlib.cm as cm
from matplotlib.colors import LogNorm
from matplotlib import ticker
import os


# filename = 'F_1_4GHz_67.pat'
filename = 'F_1_4GHz_42deg.pat'
def create_fits_file(data,scale,name):
        """ create a FITS file from the beam/array data that is passed into this function """
        # at present MeqTrees / FITS  uses scales given in degrees, not radians

        scale = scale  * 180.0 / math.pi

        x_max = 0.0
        y_max = 0.0
        
        # turn 2D array into a 4D array so that pyfits will
        Z1 = data
        temp_array = numpy.zeros((1,1,Z1.shape[0],Z1.shape[1]),dtype=Z1.dtype)
        temp_array[0,0,:Z1.shape[0],:Z1.shape[1]] = Z1

# check for NaNs and Infs etc as the matplotlib griddata function returns the outer bounds of the array as undefined
# they are turned into NaNs inthe above statement
        nan_test = numpy.isnan(temp_array)
        inf_test = numpy.isinf(temp_array)
        if nan_test.max() > 0 or inf_test.max() > 0:
          delete = nan_test | inf_test
          keep = ~nan_test & ~inf_test
#         temp_array[delete] = 0.0001
          temp_array[delete] = 0.0

# def getdata(filename):
print 'processing ', filename
radians = 180.0 / math.pi
num_grid_elements = 101
f = open(filename, 'r')
first_row = f.next()   # first row is just a comment
second_row = f.next()
info = split(strip(second_row))
num_theta = int(info[0])      # 901 data points here
poln = int(info[8])
print 'polarization', poln
print num_theta
third_row = f.next()
info = split(strip(third_row))
start_phi = float(info[3])    # 0.0 here
end_phi = float(info[4])      # 359.0 here
delta_phi = float(info[5])    # 1 deg here
print start_phi, end_phi, delta_phi
num_phi = int((end_phi - start_phi  + 1) / delta_phi)
print num_phi
# create storage arrays
l_list = []
m_list = []
cx_ampl_theta = []
cx_real_theta = []
cx_imag_theta = []
cx_ampl_phi = []
cx_real_phi = []
cx_imag_phi = []
cx_ampl = []
max_ampl = 0.0
boresight_done = False
start_phi = start_phi - delta_phi
print 'working ...'
for i in range(num_phi):
    start_phi = start_phi + delta_phi
    phi = start_phi / radians
    for j in range(num_theta):
      string_data = f.next()
      theta = float(string_data[0:9]) 
      ampl_theta_db = float(string_data[10:19])
      ampl_theta = pow(10, ampl_theta_db/20)
      phase_theta = float(string_data[20:29]) / radians
      ampl_phi_db = float(string_data[30:39])
      ampl_phi = pow(10, ampl_phi_db/20)
      phase_phi = float(string_data[40:49]) / radians
      data_real = ampl_theta * math.cos(phase_theta) 
      data_imag = ampl_theta * math.sin(phase_theta)
      theta_complex = complex(data_real, data_imag)
      data_real = ampl_phi * math.cos(phase_phi)
      data_imag = ampl_phi * math.sin(phase_phi)
      phi_complex = complex(data_real, data_imag)

      # rotate to common origin
      theta_complex_rot = theta_complex * math.cos(phi) - phi_complex * math.sin(phi)  # the correct way?`
      phi_complex_rot = theta_complex * math.sin(phi) + phi_complex * math.cos(phi) # the correct way?
      theta_real = theta_complex_rot.real
      theta_imag = theta_complex_rot.imag
      theta_ampl = math.sqrt(theta_real * theta_real + theta_imag * theta_imag)
      phi_real = phi_complex_rot.real
      phi_imag = phi_complex_rot.imag
      phi_ampl = math.sqrt(phi_real * phi_real + phi_imag * phi_imag)
      if theta < 0.002:
        if not boresight_done:
          cx_ampl_theta.append(theta_ampl)
          cx_real_theta.append(theta_real)
          cx_imag_theta.append(theta_imag)
          cx_ampl_phi.append(phi_ampl)
          cx_real_phi.append(phi_real)
          cx_imag_phi.append(phi_imag)
          l_list.append(0.0)
          m_list.append(0.0)
          if theta_ampl > max_ampl:
            max_ampl = theta_ampl
          boresight_done = True
      theta = theta / radians
      if theta > 0.002 and theta < math.pi / 2.0:
#       ll = math.sin(theta) * math.cos(phi) / math.cos(theta)
#       mm = math.sin(theta) * math.sin(phi) / math.cos(theta)
        ll = math.sin(theta) * math.cos(phi) 
        mm = math.sin(theta) * math.sin(phi)
        if abs(ll) <=0.15 and abs(mm) <= 0.15:
          l_list.append(ll)
          m_list.append(mm)
          cx_ampl_theta.append(theta_ampl)
          cx_real_theta.append(theta_real)
          cx_imag_theta.append(theta_imag)
          cx_ampl_phi.append(phi_ampl)
          cx_real_phi.append(phi_real)
          cx_imag_phi.append(phi_imag)
          if theta_ampl > max_ampl:
            max_ampl = theta_ampl

l = numpy.array(l_list,'f')
m = numpy.array(m_list,'f')
if poln:
  real_data_co = numpy.array(cx_real_phi,'f')
  imag_data_co = numpy.array(cx_imag_phi,'f')
  real_data_cx = numpy.array(cx_real_theta,'f')
  imag_data_cx = numpy.array(cx_imag_theta,'f')
else:
  real_data_co = numpy.array(cx_real_theta,'f')
  imag_data_co = numpy.array(cx_imag_theta,'f')
  real_data_cx = numpy.array(cx_real_phi,'f')
  imag_data_cx = numpy.array(cx_imag_phi,'f')
ampl_theta = numpy.array(cx_ampl_theta,'f')
ampl_phi = numpy.array(cx_ampl_phi,'f')
l_min = -0.15
l_max = 0.15
m_min = -0.15
m_max = 0.15

numxout = num_grid_elements
numyout = numxout

xc      = (l_max-l_min)/(numxout-1)
yc      = (m_max-m_min)/(numyout-1)
print 'pixel seps ', xc, yc

xo = -0.15 + xc*numpy.arange(0,numxout)
yo = -0.15 + yc*numpy.arange(0,numxout)
  
print 'gridding ...'
result_real_co = griddata(l, m, real_data_co, xo, yo)
result_imag_co = griddata(l, m, imag_data_co, xo, yo)
result_real_cx = griddata(l, m, real_data_cx, xo, yo)
result_imag_cx = griddata(l, m, imag_data_cx, xo, yo)
result_theta =  griddata(l, m, ampl_theta, xo, yo)
result_phi =  griddata(l, m, ampl_phi, xo, yo)
# result_theta,result_phi,result_real_co,result_imag_co,result_real_cx,result_imag_cx,xc,l,m,xo,yo,poln

#def make(filename):
#    result_theta,result_phi,result_real_co,result_imag_co,result_real_cx,result_imag_cx,xc,l,m,xo,yo,poln = getdata(filename)
#    print 'making fits files'
#    fits_file_imag = 'beam_imag_co_' +str(poln)
#    create_fits_file(result_imag_co,xc,fits_file_imag)
#    fits_file_real = 'beam_real_co_' +str(poln)
#    create_fits_file(result_real_co,xc,fits_file_real)
#    fits_file_imag = 'beam_imag_cx_' +str(poln)
#    create_fits_file(result_imag_cx,xc,fits_file_imag)
#    fits_file_real = 'beam_real_cx_' +str(poln)
#    create_fits_file(result_real_cx,xc,fits_file_real)
print 'plotting ...'
    
# plt.subplot(121)
plt.rcParams['font.size']=7.1
ax = plt.subplot(121)
# contour the gridded data, plotting dots at the nonuniform data points.
if poln:
  CS = plt.contourf(xo,yo,result_theta,15,locator=ticker.LogLocator(),cmap=plt.cm.jet)	
  #CS = plt.contourf(xo,yo,result_theta**2,15,locator=ticker.LogLocator(),cmap=plt.cm.jet)
  #CS = plt.contourf(xo,yo,result_real_cx,15,locator=ticker.LogLocator(),cmap=plt.cm.jet)
  #CS = plt.contourf(xo,yo,result_imag_cx,15,locator=ticker.LogLocator(),cmap=plt.cm.jet)
  # CS = plt.contourf(xo,yo,result_real_cx**2,15,locator=ticker.LogLocator(),cmap=plt.cm.jet)
else:
  CS = plt.contourf(xo,yo,result_phi,15,locator=ticker.LogLocator(),cmap=plt.cm.jet)	
  #CS = plt.contourf(xo,yo,result_phi**2,15,locator=ticker.LogLocator(),cmap=plt.cm.jet)
  #CS = plt.contourf(xo,yo,result_real_co,15,locator=ticker.LogLocator(),cmap=plt.cm.jet)
  # CS = plt.contourf(xo,yo,result_imag_co,15,locator=ticker.LogLocator(),cmap=plt.cm.jet)
  # CS = plt.contourf(xo,yo,result_real_co**2,15,locator=ticker.LogLocator(),cmap=plt.cm.jet)
plt.colorbar() # draw colorbar
    # plot data points.
for label in ax.get_xticklabels() + ax.get_yticklabels():
    label.set_fontsize(7.9)
# plt.scatter(l,m,marker='o',c='w',s=1)
plt.xlim(-0.15,0.15)
plt.ylim(-0.15,0.15)
plt.xlabel('M, (log color scale)',fontsize=8.5)
plt.ylabel('L',fontsize=8.2)
title = filename + ' cross-pol'
#title = filename + ' cross-pol, log color scale'
#title = filename + ' cross-pol, total beam power, log color scale'
# title = filename + ' cross-pol, real part of p.b. response'
# title = filename + ' cross-pol, imag. part of p.b. response'
#title = filename + ' cross-pol, power of real part of p.b. response'
plt.title(title,fontsize=7.5)
ax=plt.subplot(122)
if poln:
  CS = plt.contourf(xo,yo,result_phi,15,locator=ticker.LogLocator(),cmap=plt.cm.jet)	
  #CS = plt.contourf(xo,yo,result_phi**2,15,locator=ticker.LogLocator(),cmap=plt.cm.jet)
  #CS = plt.contourf(xo,yo,result_real_co,15,locator=ticker.LogLocator(),cmap=plt.cm.jet)
  #CS = plt.contourf(xo,yo,result_imag_co,15,locator=ticker.LogLocator(),cmap=plt.cm.jet)
  # CS = plt.contourf(xo,yo,result_real_co**2,15,locator=ticker.LogLocator(),cmap=plt.cm.jet)
else:
  CS = plt.contourf(xo,yo,result_theta,15,locator=ticker.LogLocator(),cmap=plt.cm.jet)	
  #CS = plt.contourf(xo,yo,result_theta**2,15,locator=ticker.LogLocator(),cmap=plt.cm.jet)
  #CS = plt.contourf(xo,yo,result_real_cx,15,locator=ticker.LogLocator(),cmap=plt.cm.jet)
  #CS = plt.contourf(xo,yo,result_imag_cx,15,locator=ticker.LogLocator(),cmap=plt.cm.jet)
  # CS = plt.contourf(xo,yo,result_real_cx,15,locator=ticker.LogLocator(),cmap=plt.cm.jet)
plt.colorbar() # draw colorbar
    # plot data points.
for label in ax.get_xticklabels() + ax.get_yticklabels():
    label.set_fontsize(7.9)
# plt.scatter(l,m,marker='o',c='w',s=1)
plt.xlim(-0.15,0.15)
plt.ylim(-0.15,0.15)
plt.xlabel('M, (log color scale)',fontsize=8.5)
plt.ylabel('L',fontsize=8.2)
# title = filename + ' co-pol'
# title = filename + ' co-pol, log color scale'
# title = filename + ' co-pol, total beam power, log color scale'
# title = filename + ' co-pol, real part of p.b. response'
# title = filename + ' co-pol, imag. part of p.b. response'
title = filename + ' co-pol, power of real part of p.b. response'
plt.title(title,fontsize=7.5)
save_file = str(filename) + '_ant_pats_log_color.pdf'
#save_file = str(filename) + '_ant_pats_real_log_color.pdf'
#save_file = str(filename) + '_ant_pats_imag_log_color.pdf'
# save_file = str(filename) + '_ant_pats_power_real_log_color.pdf'
plt.savefig(save_file)
# savefig(savev_file)
plt.show()

# make()


#def main(argv):
#    make(argv[1])

# main()


# Admire
#if __name__ == '__main__':
#    main(sys.argv)

# Local Variables: ***
# mode: python ***
# End: ***
