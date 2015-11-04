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

# This script uses a standard pointing model for AzEl mounted telescopes
# to generate an observation which has been corrupted by pointing errors.
# Adapted from Oleg's workshop script example10-tracking.py
# The script includes the possibility of a parallactic angle track tilt - 
# i.e we simulate a 'sky rotator' error.

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

# normalization_factor = math.sqrt(9384.0)    # obtained from results of read_cortes_data_linear.py for poln 1
#normalization_factor = math.sqrt(9231.94)    # obtained from results of read_cortes_data_linear.py for poln 1 (when using only parallel hands)
normalization_factor = math.sqrt(7814.004) # obtained from results of read_cortes_data_linear.py for poln 0  -- consistent with 'cortes_simulator.py'

# some GUI options
# Meow.Utils.include_ms_options(has_input=False,tile_sizes=[16,32,48,96]);
# TDLRuntimeMenu("Imaging options",
#    *Meow.Utils.imaging_options(npix=256,arcmin=sky_models.imagesize(),channels=[[32,1,1]]));

# useful constant: 1 deg in radians
DEG = math.pi/180.;
ARCMIN = DEG/60;
ARCSEC = ARCMIN/60;

# Measured Cortes beam parameters
fwhm  = 0.021747
l_offset = 0.00172179
m_offset = 0.00041211

def ASKAP_voltage_response(E, lm):
  """This makes the nodes to compute the beam gain, E, given an lm position.
  'lm' is an input node, giving position of source
  'E' is an output node to which the gain will be assigned""";
  ln_16  = -2.7725887
  # gaussian to which we want to optimize beams
  lmsq = E('lmsq') << Meq.Sqr(lm);
  lsq = E('lsq') << Meq.Selector(lmsq,index=0);
  msq = E('msq') << Meq.Selector(lmsq,index=1);
  lm_sq  = lsq + msq
  E << Meq.Sqrt(Meq.Exp((lm_sq * ln_16)/(fwhm * fwhm)))
  return E


def tdp_voltage_response(ns,s,p,E,lm):
  """computes response of tdp beam for the given direction
  'label' is node label distinguisher
  'E' is output node
  'lm' is direction (2-vector node)
  """
  ns = E.Subscope()
  name = s.name
  infile_name_re_xx = '/usr/lib/meqtrees/Cattery/Siamese/fits_test/beam_real_co_0.fits'
  infile_name_im_xx = '/usr/lib/meqtrees/Cattery/Siamese/fits_test/beam_imag_co_0.fits'
  ns.image_re_xx ** Meq.FITSImage(filename=infile_name_re_xx,cutoff=1.0,mode=2)
  ns.image_im_xx ** Meq.FITSImage(filename=infile_name_im_xx,cutoff=1.0,mode=2)

  infile_name_re_xy = '/usr/lib/meqtrees/Cattery/Siamese/fits_test/beam_real_cx_0.fits'
  infile_name_im_xy = '/usr/lib/meqtrees/Cattery/Siamese/fits_test/beam_imag_cx_0.fits'
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
# E << Meq.Matrix22(ns.e_xx(name,p), 0.0, 0.0, 0.0) / normalization_factor
  return E;

TDLCompileOption("beam_model","Beam Model",[tdp_voltage_response]);

def compute_jones (Jones,sources,stations=None,pointing_offsets=None,**kw):
  """Computes beam gain for a list of sources.
  The output node, will be qualified with either a source only, or a source/station pair """;  

  ns = Jones.Subscope();
  ns.l_offset << Meq.Constant(l_offset)
  ns.m_offset << Meq.Constant(m_offset)
  lm_offset = ns.lm_offset << Meq.Composer(ns.l_offset,ns.m_offset)

  # create an Array object
  # num_antennas = 36   # for ASKAP simulation
  # xntd_list = [ str(i) for i in range(1,num_antennas+1) ];
  # array = Meow.IfrArray(ns,xntd_list,ms_uvw=True);
  # create an Observation object
  # observation = Meow.Observation(ns);
  # set global context
  # Meow.Context.set(array=array,observation=observation);

  # create a source model and make list of corrupted sources
  # allsky = Meow.Patch(ns,'all',observation.phase_centre);
  # sources = sky_models.make_model(ns,"S");
  for src in sources:
    lm = src.direction.lm();
    E = ns.E(src.name);
    for p in Context.array.stations():
      pa= ns.ParAngle(p) << Meq.ParAngle(Context.observation.radec0(), Context.array.xyz(p))
      ns.CosPa(p) << Meq.Cos(pa)
      ns.SinPa(p) << Meq.Sin(pa)
      ns.rot_matrix(p) << Meq.Matrix22(ns.CosPa(p),-1.0 * ns.SinPa(p),ns.SinPa(p),ns.CosPa(p))
      # compute "apparent" position of source per each antenna
      lm_rot=ns.lm_rot(src.name,p) << Meq.MatrixMultiply(ns.rot_matrix(p),lm) 
      lm_relative = ns.lm_relative(src.name,p) << Meq.Add(lm_rot,lm_offset)
      # compute E for apparent position
      # tdp_voltage_response(ns,src,p,E(p),lm_relative);
      beam_model(ns,src,p,Jones(src.name,p),lm_relative);
#     ASKAP_voltage_response(E(p), lm_rot)
    #allsky.add(src.corrupt(E));

  # observed = allsky.visibilities();
  return Jones;

_model_option = TDLCompileOption('beam_model',"Beam model", [tdp_voltage_response]);
  
def _show_option_menus (model):
  _model_option.show(model==tdp_voltage_response);

_model_option.when_changed(_show_option_menus);

  # make some useful inspectors. Collect them into a list, since we need
  # to give a list of 'post' nodes to make_sinks() below
  # pg = Bookmarks.Page("Inspectors",1,2);
  # inspectors = [];
  # inspectors.append(
  #  Meow.StdTrees.vis_inspector(ns.inspect_observed,observed) );
  #pg.add(ns.inspect_observed,viewer="Collections Plotter");

  #Meow.StdTrees.make_sinks(ns,observed,spigots=False,post=inspectors);

# def _test_forest(mqs,parent):
# first, make sure that any previous version of the mep table is
# obliterated so nothing strange happens in succeeding steps
#  req = Meow.Utils.create_io_request();
  # execute    
#  mqs.execute('VisDataMux',req,wait=False);
  
# this is a useful thing to have at the bottom of the script,  
# it allows us to check the tree for consistency simply by 
# running 'python script.tdl'

# if __name__ == '__main__':
#   ns = NodeScope();
#  _define_forest(ns);
  # resolves nodes
#  ns.Resolve();  
  
#  print len(ns.AllNodes()),'nodes defined';

