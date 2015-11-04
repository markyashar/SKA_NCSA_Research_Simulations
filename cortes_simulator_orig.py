# standard preamble
#
#% $Id$ 
#
#
# Copyright (C) 2002-2007
# The MeqTree Foundation & 
# ASTRON (Netherlands Foundation for Research in Astronomy)
# P.O.Box 2, 7990 AA Dwingeloo, The Netherlands
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, see <http://www.gnu.org/licenses/>,
# or write to the Free Software Foundation, Inc., 
# 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#

# This script uses parallactic angle rotation to simulate the behaviour
# of an Az-El mounted dish as it tracks a specific area of sky.

from Timba.TDL import *
from Timba.Meq import meq
import math
import random
import numpy

import Meow
from Meow import Bookmarks
from Meow import Context
import Meow.StdTrees

import sky_models

Settings.forest_state.cache_policy = 100

normalization_factor = math.sqrt(9384.0)    # obtained from results of read_cortes_data_linear.py for poln 1
#normalization_factor = math.sqrt(7814.004) # obtained from results of read_cortes_data_linear.py for poln 0

# some GUI options
Meow.Utils.include_ms_options(has_input=False,tile_sizes=[16,32,48,96]);
TDLRuntimeMenu("Imaging options",
    *Meow.Utils.imaging_options(npix=256,arcmin=sky_models.imagesize(),channels=[[32,1,1]]));

# useful constant: 1 deg in radians
DEG = math.pi/180.;
ARCMIN = DEG/60;
ARCSEC = ARCMIN/60;

# define desired half-intensity width of power pattern (HPBW)
# as we are fitting total intensity I pattern (here .021 rad = 74.8 arcmin)
fwhm  = 0.021747 # beam FWHM, note: this value is only used in this script to lay out
                 # grid of point sources, and is not necessarily directly relavant to
                 # Cortes HPBW

def tdp_voltage_response(ns,s,p,E,lm):
  """computes response of tdp beam for the given direction
  'E' is output node
  'lm' is direction (2-vector node)
  """
  name = s.name
  infile_name_re_xx = '/usr/lib/meqtrees/Cattery/Siamese/fits_test/beam_real_co_1.fits'
  infile_name_im_xx = '/usr/lib/meqtrees/Cattery/Siamese/fits_test/beam_imag_co_1.fits'
  ns.image_re_xx ** Meq.FITSImage(filename=infile_name_re_xx,cutoff=1.0,mode=2)
  ns.image_im_xx ** Meq.FITSImage(filename=infile_name_im_xx,cutoff=1.0,mode=2)

  infile_name_re_xy = '/usr/lib/meqtrees/Cattery/Siamese/fits_test/beam_real_cx_1.fits'
  infile_name_im_xy = '/usr/lib/meqtrees/Cattery/Siamese/fits_test/beam_imag_cx_1.fits'
  ns.image_re_xy ** Meq.FITSImage(filename=infile_name_re_xy,cutoff=1.0,mode=2)
  ns.image_im_xy ** Meq.FITSImage(filename=infile_name_im_xy,cutoff=1.0,mode=2)

  ns.resampler_re_xx ** Meq.Resampler(ns.image_re_xx,dep_mask = 0xff)
  ns.resampler_im_xx ** Meq.Resampler(ns.image_im_xx,dep_mask = 0xff)
  ns.sample_re_xx(name,p) << Meq.Compounder(children=[lm,ns.resampler_re_xx],common_axes=[hiid('l'),hiid('m')])
  ns.sample_im_xx(name,p) << Meq.Compounder(children=[lm,ns.resampler_im_xx],common_axes=[hiid('l'),hiid('m')])

  ns.resampler_re_xy ** Meq.Resampler(ns.image_re_xy,dep_mask = 0xff)
  ns.resampler_im_xy ** Meq.Resampler(ns.image_im_xy,dep_mask = 0xff)
  ns.sample_re_xy(name,p) << Meq.Compounder(children=[lm,ns.resampler_re_xy],common_axes=[hiid('l'),hiid('m')])
  ns.sample_im_xy(name,p) << Meq.Compounder(children=[lm,ns.resampler_im_xy],common_axes=[hiid('l'),hiid('m')])

  ns.e_xx(name,p) << Meq.ToComplex(ns.sample_re_xx(name,p),ns.sample_im_xx(name,p))
  ns.e_xy(name,p) << Meq.ToComplex(ns.sample_re_xy(name,p),ns.sample_im_xy(name,p))

  E << Meq.Matrix22(ns.e_xx(name,p), ns.e_xy(name,p), 0.0, 0.0) / normalization_factor
  return E;

def _define_forest (ns):

 # create Array object
  num_antennas = 36   # for ASKAP simulation
  xntd_list = [ str(i) for i in range(1,num_antennas+1) ];
  array = Meow.IfrArray(ns,xntd_list,ms_uvw=True);
  # create an Observation object
  observation = Meow.Observation(ns);
  # set global context
  Meow.Context.set(array=array,observation=observation);

  # create a source model and make list of corrupted sources
  allsky = Meow.Patch(ns,'all',observation.phase_centre);
  sources = sky_models.make_model(ns,"S");
  for src in sources:
    lm = src.direction.lm();
    E = ns.E(src.name);
    for p in array.stations():
      pa= ns.ParAngle(p) << Meq.ParAngle(observation.phase_centre.radec(), array.xyz(p))
      ns.CosPa(p) << Meq.Cos(pa)
      ns.SinPa(p) << Meq.Sin(pa)
      ns.rot_matrix(p) << Meq.Matrix22(ns.CosPa(p),-1.0 * ns.SinPa(p),ns.SinPa(p),ns.CosPa(p))
      # compute "apparent" position of source per each antenna
      lm_rot=ns.lm_rot(src.name,p) << Meq.MatrixMultiply(ns.rot_matrix(p),lm) 
      # compute E for apparent position
      tdp_voltage_response(ns,src,p,E(p),lm_rot);
    allsky.add(src.corrupt(E));

  observed = allsky.visibilities();

  # make some useful inspectors. Collect them into a list, since we need
  # to give a list of 'post' nodes to make_sinks() below
  pg = Bookmarks.Page("Inspectors",1,2);
  inspectors = [];
  inspectors.append(
    Meow.StdTrees.vis_inspector(ns.inspect_observed,observed) );
  pg.add(ns.inspect_observed,viewer="Collections Plotter");

  Meow.StdTrees.make_sinks(ns,observed,spigots=False,post=inspectors);

def _test_forest(mqs,parent):
  # we pass the request to the VisDataMux, a mysterious root node 
  # created deep in the bowels of Meow.
  req = Meow.Utils.create_io_request();
  # execute    
  mqs.execute('VisDataMux',req,wait=False);
  
# this is a useful thing to have at the bottom of the script,  
# it allows us to check the tree for consistency simply by 
# running 'python script.tdl'

if __name__ == '__main__':
  ns = NodeScope();
  _define_forest(ns);
  # resolves nodes
  ns.Resolve();  
  
  print len(ns.AllNodes()),'nodes defined';

