# CASA script to create, clean, and display an image.
# Execute this script from within the CASA environment by issuing the
# CASA command: execfile('CASA_imager_SKA_2src.py') 

# get rid of old versions of files to be created in this script
import os
os.system('rm -rf /3data/casapy-stable-31.0.13516-001-64b/bin/image.res* /3data/casapy-stable-31.0.13516-001-64b/bin/image.clean /3data/casapy-stable-31.0.13516-001-64b/bin/image.psf /3data/casapy-stable-31.0.13516-001-64b/bin/test_image.fits')

# start using the imager (im) tool

# msname = '/3data/MS_sims1/SKA_LOGSPIRAL40_CASA_2.MS'
# msname = '/3data/MS_sims1/SKA_LOGSPIRAL40_CASA_3.MS'
# msname = '/3data/MS_sims1/SKA_LOGSPIRAL40_CASA_1src.MS'
# msname = '/3data/MS_sims1/SKA_LOGSPIRAL40_CASA_0src.MS'
# msname = '/3data/MS_sims1/SKA_LOGSPIRAL40_CASA_2src.MS'
# msname = '/3data/MS_sims1/SKA_LOGSPIRAL50_CASA_2src.MS'
# msname = '/3data/MS_sims1/SKA_LOGSPIRAL75_CASA_2src.MS'
# msname = '/3data/MS_sims1/SKA_LOGSPIRAL100_CASA_2src.MS'
msname = '/3data/MS_sims1/SKA_LOGSPIRAL150_CASA_2src.MS'
# msname = '/3data/MS_sims1/SKA_LOGSPIRAL175_CASA_2src.MS'
# msname = '/3data/MS_sims1/SKA_LOGSPIRAL40_CASA_1src_off.MS'
# msname = '/3data/MS_sims1/SKA_LOGSPIRAL40_CASA_1src_offset.MS'
# msname = '/3data/MS_sims1/SKA_LOGSPIRAL40_CASA.MSs'
# msname = '/3data/MS_sims1/SKA_LOGSPIRAL40_MEQ.MS'
# msname = '/3data/MS_sims1/SKA_LOGSPIRAL50_MEQ.MS'
# msname = '/3data/MS_sims1/ASKAP_sim_orig.MS'
cellsize = '8arcsec'
imsize = 2048
restored_image = 'image.restored'
model_image = 'image.clean'
residual_image = 'image.residual'
psf_image = 'image.psf'
flux_image = 'image.flux'

# im.selectvis(vis=msname, field=0)
im.selectvis(vis=msname)
im.defineimage(stokes='I',mode='mfs',cellx=cellsize, celly=cellsize, nx=imsize, ny=imsize)
# we use w-projection correction      

im.setoptions(ftmachine='wproject', wprojplanes=128)

im.weight(type='uniform')

#function call for CLEAN

# default('clean')
# clean(gridmode='aprojection', cfcache= 'cfcache.dir',painc=10.0)
# gridmode='aprojection'
# cfcache= 'cfcache.dir'
# painc=10.0

im.clean(algorithm='wfclark', niter=0, gain=0.1, threshold='0.0mJy',
                  displayprogress=True, interactive=False,
                  image=restored_image, model=model_image, psfimage=psf_image,
                  residual=residual_image)

# clean(im.clean)
# use the image (ia) tool to get a fits file output
#ia.open(restored_image)
#ia.tofits('/3data/MS_sims1/casa_sims_fits/SKA_LOGSPIRAL40_CASA_2_90min_2src_75arcmin_2048_64ch_1400mhz_cortes_uni_w128.fits')
#os.system('ds9 /3data/MS_sims1/casa_sims_fits/SKA_LOGSPIRAL40_CASA_2_90min_2src_75arcmin_2048_64ch_1400mhz_cortes_uni_w128_modchane1.fits &')
#os.system('/home/yashar/Downloads/casapy-30.2.11761-001-64b/bin/casaviewer /3data/MS_sims1/casa_sims_fits/SKA_LOGSPIRAL40_CASA_2_90min_2src_75arcmin_2048_64ch_1400mhz_cortes_uni_w128_modchane1.fits &')

ia.open(restored_image)
ia.tofits('/3data/MS_sims1/casa_sims_fits/SKA_LOGSPIRAL150_CASA_90min_2src_75arcmin_2048_64ch_1400mhz_cortes_CORRDATA_uni_w128_aproj_casaimag.fits')
os.system('ds9 /3data/MS_sims1/casa_sims_fits/SKA_LOGSPIRAL150_CASA_90min_2src_75arcmin_2048_64ch_1400mhz_cortes_CORRDATA_uni_w128_aproj_casaimag.fits &')
os.system('/home/yashar/Downloads/casapy-30.2.11761-001-64b/bin/casaviewer /3data/MS_sims1/casa_sims_fits/SKA_LOGSPIRAL150_CASA_90min_2src_75arcmin_2048_64ch_1400mhz_cortes_CORRDATA_uni_w128_aproj_casaimag.fits &')

# ia.open(flux_image)
# ia.tofits('/3data/MS_sims1/casa_sims_fits/flux_image_test.fits')
# os.system('/home/yashar/Downloads/casapy-30.2.11761-001-64b/bin/casaviewer /3data/MS_sims1/casa_sims_fits/flux_image_test.fits &')

# ia.open(model_image)
# ia.tofits('/3data/MS_sims1/casa_sims_fits/SKA_LOGSPIRAL40_CASA_2_90min_2src_75arcmin_2048_64ch_1400mhz_cortes_uni_w128_model_image.fits')
# os.system('ds9 /3data/MS_sims1/casa_sims_fits/SKA_LOGSPIRAL40_CASA_2_90min_2src_75arcmin_2048_64ch_1400mhz_cortes_uni_w128_model_image.fits &')
# os.system('/home/yashar/Downloads/casapy-30.2.11761-001-64b/bin/casaviewer /3data/MS_sims1/casa_sims_fits/SKA_LOGSPIRAL40_CAS

# ia.open(residual_image)
# ia.tofits('/3data/MS_sims1/casa_sims_fits/SKA_LOGSPIRAL40_CASA_2_90min_2src_75arcmin_2048_64ch_1400mhz_cortes_uni_w128_resid_image.fits')
# os.system('ds9 /3data/MS_sims1/casa_sims_fits/SKA_LOGSPIRAL40_CASA_2_90min_2src_75arcmin_2048_64ch_1400mhz_cortes_uni_w128_resid_image.fits &')
# os.system('/home/yashar/Downloads/casapy-30.2.11761-001-64b/bin/casaviewer /3data/MS_sims1/casa_sims_fits/SKA_LOGSPIRAL40_CASA_2_90min_2src_75arcmin_2048_64ch_1400mhz_cortes_uni_w128_resid_image.fits &')

# ia.open(psf_image)
# ia.tofits('/3data/MS_sims1/casa_sims_fits/SKA_LOGSPIRAL40_CASA_2_90min_2src_75arcmin_2048_64ch_1400mhz_cortes_uni_w128_psf_image.fits')
# os.system('ds9 /3data/MS_sims1/casa_sims_fits/SKA_LOGSPIRAL40_CASA_2_90min_2src_75arcmin_2048_64ch_1400mhz_cortes_uni_w128_psf_image.fits &')
# os.system('/home/yashar/Downloads/casapy-30.2.11761-001-64b/bin/casaviewer /3data/MS_sims1/casa_sims_fits/SKA_LOGSPIRAL40_CASA_2_90min_2src_75arcmin_2048_64ch_1400mhz_cortes_uni_w128_psf_image.fits &')

