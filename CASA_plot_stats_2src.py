# CASA script for generating a histogram/plot and pixel statistics of FITS file
# image simulations
# Execute this script from within the CASA environment by issuing the CASA
# command: execfile('CASA_histogram_stats.py')

import sys
import pickle
import os
import numpy
import pylab
from pylab import *
import matplotlib.pyplot as plt

nbins = 50 # number of bins in histogram

# Open up the FITS file for reading and processing

# imagename = '/3data/MS_sims1/casa_sims_fits/SKA_LOGSPIRAL50_CASA_90min_2src_75arcmin_2048_64ch_1400mhz_CORRDATA_uni_w128_casaimag.fits'
# imagename2 ='SKA_LOGSPIRAL50_CASA_90min_2src_75arcmin_2048_64ch_1400mhz_CORRDATA_uni_w128_casaimag.fits'

# imagename = '/3data/MS_sims1/casa_sims_fits/SKA_LOGSPIRAL50_CASA_90min_2src_75arcmin_2048_64ch_1400mhz_cortes_CORRDATA_uni_w128_casaimag.fits'
# imagename2 ='SKA_LOGSPIRAL50_CASA_90min_2src_75arcmin_2048_64ch_1400mhz_cortes_CORRDATA_uni_w128_casaimag.fits'

# imagename = '/3data/MS_sims1/casa_sims_fits/SKA_LOGSPIRAL50_CASA_90min_2src_75arcmin_2048_64ch_1400mhz_cortes_point_CORRDATA_uni_w128_casaimag.fits'
# imagename2 = 'SKA_LOGSPIRAL50_CASA_90min_2src_75arcmin_2048_64ch_1400mhz_cortes_point_CORRDATA_uni_w128_casaimag.fits'

# imagename = '/3data/MS_sims1/casa_sims_fits/SKA_LOGSPIRAL50_CASA_90min_2src_75arcmin_2048_64ch_1400mhz_cortes_point_CORRDATA_uni_w128_casaimag_imagediff.fits'
# imagename2 = 'SKA_LOGSPIRAL50_CASA_90min_2src_75arcmin_2048_64ch_1400mhz_cortes_point_CORRDATA_uni_w128_casaimag_imagediff.fits'

# imagename = '/3data/MS_sims1/casa_sims_fits/SKA_LOGSPIRAL50_CASA_90min_2src_75arcmin_2048_64ch_1400mhz_cortes_CORRDATA_uni_w128_casaimag_imagediff.fits'
# imagename2 = 'SKA_LOGSPIRAL50_CASA_90min_2src_75arcmin_2048_64ch_1400mhz_cortes_CORRDATA_uni_w128_casaimag_imagediff.fits'

# imagename = '/3data/MS_sims1/casa_sims_fits/SKA_LOGSPIRAL50_CASA_90min_2src_75arcmin_2048_64ch_1400mhz_cortes_point_CORRDATA_uni_w128_casaimag_imagediff.fits'
# imagename2 = 'SKA_LOGSPIRAL50_CASA_90min_2src_75arcmin_2048_64ch_1400mhz_cortes_point_CORRDATA_uni_w128_casaimag_imagediff.fits'

# imagename = '/3data/MS_sims1/casa_sims_fits/SKA_LOGSPIRAL50_MEQ_90min_2src_75arcmin_2048_64ch_1400mhz_cortes_CORRDATA_uni_w128_casaimag.fits'
# imagename2 = 'SKA_LOGSPIRAL50_MEQ_90min_2src_75arcmin_2048_64ch_1400mhz_cortes_CORRDATA_uni_w128_casaimag.fits'

# imagename = '/3data/MS_sims1/casa_sims_fits/SKA_LOGSPIRAL75_CASA_90min_2src_75arcmin_2048_64ch_1400mhz_CORRDATA_uni_w128_casaimag.fits'
# imagename2 = 'SKA_LOGSPIRAL75_CASA_90min_2src_75arcmin_2048_64ch_1400mhz_CORRDATA_uni_w128_casaimag.fits'

# imagename = '/3data/MS_sims1/casa_sims_fits/SKA_LOGSPIRAL75_CASA_90min_2src_75arcmin_2048_64ch_1400mhz_cortes_CORRDATA_uni_w128_casaimag.fits'
# imagename2 = 'SKA_LOGSPIRAL75_CASA_90min_2src_75arcmin_2048_64ch_1400mhz_cortes_CORRDATA_uni_w128_casaimag.fits'

# imagename = '/3data/MS_sims1/casa_sims_fits/SKA_LOGSPIRAL75_CASA_90min_2src_75arcmin_2048_64ch_1400mhz_cortes_point_CORRDATA_uni_w128_casaimag.fits'
# imagename2 = 'SKA_LOGSPIRAL75_CASA_90min_2src_75arcmin_2048_64ch_1400mhz_cortes_point_CORRDATA_uni_w128_casaimag.fits'

# imagename = '/3data/MS_sims1/casa_sims_fits/SKA_LOGSPIRAL75_CASA_90min_2src_75arcmin_2048_64ch_1400mhz_cortes_CORRDATA_uni_w128_casaimag_imagediff.fits'
# imagename2 = 'SKA_LOGSPIRAL75_CASA_90min_2src_75arcmin_2048_64ch_1400mhz_cortes_CORRDATA_uni_w128_casaimag_imagediff.fits'

imagename = '/3data/MS_sims1/casa_sims_fits/SKA_LOGSPIRAL75_CASA_90min_2src_75arcmin_2048_64ch_1400mhz_cortes_point_CORRDATA_uni_w128_casaimag_imagediff.fits'
imagename2 = 'SKA_LOGSPIRAL75_CASA_90min_2src_75arcmin_2048_64ch_1400mhz_cortes_point_CORRDATA_uni_w128_casaimag_imagediff.fits'

# imagename = '/3data/MS_sims1/casa_sims_fits/SKA_LOGSPIRAL100_CASA_90min_2src_75arcmin_2048_64ch_1400mhz_CORRDATA_uni_w128_casaimag.fits'
# imagename2 = 'SKA_LOGSPIRAL100_CASA_90min_2src_75arcmin_2048_64ch_1400mhz_CORRDATA_uni_w128_casaimag.fits'

# imagename = '/3data/MS_sims1/casa_sims_fits/SKA_LOGSPIRAL100_CASA_90min_2src_75arcmin_2048_64ch_1400mhz_cortes_CORRDATA_uni_w128_casaimag.fits'
# imagename2 = 'SKA_LOGSPIRAL100_CASA_90min_2src_75arcmin_2048_64ch_1400mhz_cortes_CORRDATA_uni_w128_casaimag.fits'

# imagename = '/3data/MS_sims1/casa_sims_fits/SKA_LOGSPIRAL100_CASA_90min_2src_75arcmin_2048_64ch_1400mhz_cortes_point_CORRDATA_uni_w128_casaimag.fits'
# imagename2 = 'SKA_LOGSPIRAL100_CASA_90min_2src_75arcmin_2048_64ch_1400mhz_cortes_point_CORRDATA_uni_w128_casaimag.fits'

# imagename = '/3data/MS_sims1/casa_sims_fits/SKA_LOGSPIRAL100_CASA_90min_2src_75arcmin_2048_64ch_1400mhz_cortes_CORRDATA_uni_w128_casaimag_imagediff.fits'
# imagename2 = 'SKA_LOGSPIRAL100_CASA_90min_2src_75arcmin_2048_64ch_1400mhz_cortes_CORRDATA_uni_w128_casaimag_imagediff.fits'

# imagename = '/3data/MS_sims1/casa_sims_fits/SKA_LOGSPIRAL100_CASA_90min_2src_75arcmin_2048_64ch_1400mhz_cortes_point_CORRDATA_uni_w128_casaimag_imagediff.fits'
# imagename2 = 'SKA_LOGSPIRAL100_CASA_90min_2src_75arcmin_2048_64ch_1400mhz_cortes_point_CORRDATA_uni_w128_casaimag_imagediff.fits'

##

# imagename = '/3data/MS_sims1/casa_sims_fits/SKA_LOGSPIRAL150_CASA_90min_2src_75arcmin_2048_64ch_1400mhz_CORRDATA_uni_w128_casaimag.fits'
# imagename2 = 'SKA_LOGSPIRAL150_CASA_90min_2src_75arcmin_2048_64ch_1400mhz_CORRDATA_uni_w128_casaimag.fits'

# imagename = '/3data/MS_sims1/casa_sims_fits/SKA_LOGSPIRAL150_CASA_90min_2src_75arcmin_2048_64ch_1400mhz_cortes_CORRDATA_uni_w128_casaimag.fits'
# imagename2 = 'SKA_LOGSPIRAL150_CASA_90min_2src_75arcmin_2048_64ch_1400mhz_cortes_CORRDATA_uni_w128_casaimag.fits'

# imagename = '/3data/MS_sims1/casa_sims_fits/SKA_LOGSPIRAL150_CASA_90min_2src_75arcmin_2048_64ch_1400mhz_cortes_point_CORRDATA_uni_w128_casaimag.fits'
# imagename2 = 'SKA_LOGSPIRAL150_CASA_90min_2src_75arcmin_2048_64ch_1400mhz_cortes_point_CORRDATA_uni_w128_casaimag.fits'

# imagename = '/3data/MS_sims1/casa_sims_fits/SKA_LOGSPIRAL150_CASA_90min_2src_75arcmin_2048_64ch_1400mhz_cortes_CORRDATA_uni_w128_casaimag_imagediff.fits'
# imagename2 = 'SKA_LOGSPIRAL150_CASA_90min_2src_75arcmin_2048_64ch_1400mhz_cortes_CORRDATA_uni_w128_casaimag_imagediff.fits'

# imagename = '/3data/MS_sims1/casa_sims_fits/SKA_LOGSPIRAL150_CASA_90min_2src_75arcmin_2048_64ch_1400mhz_cortes_point_CORRDATA_uni_w128_casaimag_imagediff.fits'
# imagename2 = 'SKA_LOGSPIRAL150_CASA_90min_2src_75arcmin_2048_64ch_1400mhz_cortes_point_CORRDATA_uni_w128_casaimag_imagediff.fits'

##

# imagename = '/3data/MS_sims1/casa_sims_fits/SKA_LOGSPIRAL175_CASA_90min_2src_75arcmin_2048_64ch_1400mhz_CORRDATA_uni_w128_casaimag.fits'
# imagename2 = 'SKA_LOGSPIRAL175_CASA_90min_2src_75arcmin_2048_64ch_1400mhz_CORRDATA_uni_w128_casaimag.fits'

# imagename = '/3data/MS_sims1/casa_sims_fits/SKA_LOGSPIRAL175_CASA_90min_2src_75arcmin_2048_64ch_1400mhz_cortes_CORRDATA_uni_w128_casaimag.fits'
# imagename2 = 'SKA_LOGSPIRAL175_CASA_90min_2src_75arcmin_2048_64ch_1400mhz_cortes_CORRDATA_uni_w128_casaimag.fits'

# imagename = '/3data/MS_sims1/casa_sims_fits/SKA_LOGSPIRAL175_CASA_90min_2src_75arcmin_2048_64ch_1400mhz_cortes_point_CORRDATA_uni_w128_casaimag.fits'
# imagename2 = 'SKA_LOGSPIRAL175_CASA_90min_2src_75arcmin_2048_64ch_1400mhz_cortes_point_CORRDATA_uni_w128_casaimag.fits'

# imagename = '/3data/MS_sims1/casa_sims_fits/SKA_LOGSPIRAL175_CASA_90min_2src_75arcmin_2048_64ch_1400mhz_cortes_CORRDATA_uni_w128_casaimag_imagediff.fits'
# imagename2 = 'SKA_LOGSPIRAL175_CASA_90min_2src_75arcmin_2048_64ch_1400mhz_cortes_CORRDATA_uni_w128_casaimag_imagediff.fits'

# imagename = '/3data/MS_sims1/casa_sims_fits/SKA_LOGSPIRAL175_CASA_90min_2src_75arcmin_2048_64ch_1400mhz_cortes_point_CORRDATA_uni_w128_casaimag_imagediff.fits'
# imagename2 = 'SKA_LOGSPIRAL175_CASA_90min_2src_75arcmin_2048_64ch_1400mhz_cortes_point_CORRDATA_uni_w128_casaimag_imagediff.fits'

ia.open(imagename)

# Restrict statistics and histogram to within this region
blc=[963,634,0,0]  #bb1: absolute pixel coordinate of the bottom left corner of
blc_src1 = [935,940,0,0]
blc_src2 = [935,370,0,0]
# bounding box surrounding selected region.
trc=[1112,787,0,0]  #bb1: absolute pixel coordinate of the top right corner of the
trc_src1 = [1139,1093,0,0]
trc_src2 = [1116,528,0,0]
# bounding box surrounding the selected region.
bbox=rg.box(blc=blc,trc=trc) # creating the bounding box region
bbox_src1=rg.box(blc=blc_src1,trc=trc_src1)
bbox_src2=rg.box(blc=blc_src2,trc=trc_src2)
ia.statistics(region=bbox) # generate and output statistics within bounding
# box region
print ia.statistics(region=bbox,robust=T)
summary = ia.summary()
print summary

# Generate and plot labeled histogram
pl.clf()
mean=ia.statistics(region=bbox,axes=[0,1,2,3],robust=T)['mean'][0]
mean_src1=ia.statistics(region=bbox_src1,axes=[0,1,2,3],robust=T)['mean'][0]
mean_src2=ia.statistics(region=bbox_src2,axes=[0,1,2,3],robust=T)['mean'][0]
median_src1=ia.statistics(region=bbox_src1,axes=[0,1,2,3],robust=T)['median'][0]
median_src2=ia.statistics(region=bbox_src2,axes=[0,1,2,3],robust=T)['median'][0]
sigma_src1=ia.statistics(region=bbox_src1,robust=T)['sigma'][0]
sigma_src2=ia.statistics(region=bbox_src2,robust=T)['sigma'][0]
rms_src1=ia.statistics(region=bbox_src1,robust=T)['rms'][0]
rms_src2=ia.statistics(region=bbox_src2,robust=T)['rms'][0]
rms=ia.statistics(region=bbox,robust=T)['rms'][0]
sigma=ia.statistics(region=bbox,robust=T)['sigma'][0]
max=ia.statistics(region=bbox,robust=T)['max'][0]
min=ia.statistics(region=bbox,robust=T)['min'][0]
median=ia.statistics(region=bbox,robust=T)['median'][0]
medabsdevmed=ia.statistics(region=bbox,robust=T)['medabsdevmed'][0]
quartile=ia.statistics(region=bbox,robust=T)['quartile'][0]
maxall=ia.statistics()['max'][0]
minall=ia.statistics()['min'][0]
sum=ia.statistics(region=bbox,robust=T)['sum'][0]
sumsq=ia.statistics(region=bbox,robust=T)['sumsq'][0]
dr=maxall/rms
# ia.fromshape(shape=[125,459])
r = ia.histograms(region=bbox,list = T, axes=[0,1,2,3],force=T,nbins=50)
print r
print len(r)
print r.keys()
# n,bins,patches = plt.hist(r['histout']['values'],bins=30,facecolor='green',alpha=0.3)
plt.plot(r['histout']['values'],r['histout']['counts'])
ax = subplot(111)
ax.set_xlim(xmin=-0.008)
ax.set_xlim(xmax=0.008)
# ax.set_xlim(xmin=-0.0001)# for difference images (cortes,pointing)
# ax.set_xlim(xmax=0.0001)
xlabel('Pixel Brightness Value')
ylabel('Counts')
title('Plot of Number of Counts vs. Pixel Brightness Values in Region Between 2 Sources in Simulated CASA FITS Image',fontsize=8.1)
figtext(0.25, 0.86,'FITS file: %s' % imagename2, fontsize = 6.9)
figtext(0.25,0.83,'Mean of pixel brightness values = %s' % mean, fontsize = 8.3)
figtext(0.25,0.80,'Root Mean Square of pixel brightness values = %s' % rms, fontsize = 8.3)
figtext(0.25,0.77,'Standard Deviation about the mean of pixel brightness values = %s' % sigma, fontsize = 8.3)
figtext(0.25,0.74,'Number of bins in histogram = %s' % nbins, fontsize = 8.3)
figtext(0.25,0.71,'Maximum pixel brightness value: %s' % max, fontsize = 8.3)
figtext(0.25,0.68,'Median of pixel brightness values: %s' % median, fontsize = 8.3)
figtext(0.25,0.65,'Minimum of pixel brightness values: %s' % min, fontsize = 8.3)
figtext(0.25,0.62,'Median of the absolute deviations from median of pixel brightness values: %s' % medabsdevmed, fontsize = 8.3)
figtext(0.25,0.59,'Inter-quanitle range of pixel brightness values: %s' % quartile, fontsize = 8.3)
figtext(0.25,0.56,'Sum of all pixel values: %s' % sum, fontsize = 8.3)
figtext(0.25,0.53,'Bounding Box Region: %s, %s' % (blc,trc), fontsize = 8.3)
figtext(0.25,0.50,'Dynamic Range Estimate for entire image: %s' % dr, fontsize = 8.3)
savefig('/3data/MS_sims1/casa_sims_fits/Plot_%s.pdf' % imagename2)  #bb1

f=open('/3data/MS_sims1/casa_sims_fits/Plot_%s.txt' % imagename2,'w')  #bb1
f.write('FITS file: %s\n' %imagename2)
f.write('Bottom left corner of bounding box region: %s\n' %blc)
f.write('Top right corner of bounding box region: %s\n' %trc)
f.write('Mean of pixel brightness values: %s\n' %mean)
f.write('Root Mean Square of pixel brightness values: %s\n' %rms)
f.write('Standard Deviation about the mean of pixel brightness values: %s\n' %sigma)
f.write('Number of bins in histogram: %s\n' %nbins)
f.write('Maximum pixel brightness value: %s\n' %max)
f.write('Median of pixel brightness values: %s\n' %median)
f.write('Minimum of pixel brightness values: %s\n' %min)
f.write('Median of the absolute deviations from median of pixel brightness values: %s\n' %medabsdevmed)
f.write('Inter-quanitle range of pixel brightness values: %s\n' %quartile)
f.write('Sum of pixel values: %s\n' %sum)
f.write('Sum of squares of pixel values: %s\n' %sumsq)
f.write('Dynamic Range Estimate for all of image: %s\n' %dr)
f.write('Minimum of pixel brightness values for all of image: %s\n' %minall)
f.write('Maximum pixel brightness value for all of image: %s\n' %maxall)
f.write('Mean pixel brightness value for src1 : %s\n' %mean_src1)
f.write('Mean pixel brightness value for src2 : %s\n' %mean_src2)
f.write('Median pixel brightness value for src1 : %s\n' %median_src1)
f.write('Median pixel brightness value for src2 : %s\n' %median_src2)
f.write('Sigma pixel brightness value for src1 : %s\n' %sigma_src1)
f.write('Sigma pixel brightness value for src2 : %s\n' %sigma_src2)
f.write('R.M.S. pixel brightness value for src1 : %s\n' %rms_src1)
f.write('R.M.S. pixel brightness value for src2 : %s\n' %rms_src2)
f.close()
print "FITS file", imagename2
print "Bounding box region in FITS file: ", blc, trc
print "Mean of pixel brightness values = ", mean
print "Root Mean Square of pixel brightness values = ", rms
print "Standard Deviation about the mean of pixel brightness values = ", sigma
print "Number of bins in histogram = ", nbins
print "Maximum pixel brightness value = ", max
print "Median of pixel brightness values = ", median
print "Minimum of pixel brightness values = ", min
print "Median of the absolute deviations from median of pixel brightness values = ", medabsdevmed
print "Inter-quanitle range of pixel brightness values = ", quartile
print "Sum of pixel values = ", sum
print "Sum of squares of pixel values = ", sumsq
print "Dynamic Range Estimate for all of image: ", dr
print "Minimum of pixel brightness values for all of image:", minall
print "Maximum of pixel brightness values for all of image:", maxall
print "Mean pixel brightness value for src1 :", mean_src1
print "Mean pixel brightness value for src2 :", mean_src2
print "Median pixel brightness value for src1 :", median_src1
print "Median pixel brightness value for src2 :", median_src2
print "Sigma pixel brightness value for src1 :", sigma_src1
print "Sigma pixel brightness value for src2 :", sigma_src2
print "R.M.S. pixel brightness value for src1 :", rms_src1
print "R.M.S. pixel brightness value for src2 :", rms_src2






