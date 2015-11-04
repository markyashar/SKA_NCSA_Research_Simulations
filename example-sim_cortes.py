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

 # standard preamble
from Timba.TDL import *
from Timba.Meq import meq
import math

import Meow
import Meow.StdTrees


# MS options first
mssel = Meow.MSUtils.MSSelector(has_input=False,tile_sizes=[8,16,32],flags=False);
# MS compile-time options
TDLCompileOptions(*mssel.compile_options());
TDLCompileOption("run_purr","Start Purr on this MS",True);
# MS run-time options
TDLRuntimeOptions(*mssel.runtime_options());
## also possible:
# TDLRuntimeMenu("MS selection options",open=True,*mssel.runtime_options());

# UVW
TDLCompileOptions(*Meow.IfrArray.compile_options());

# simulation mode menu
SIM_ONLY = "sim only";
ADD_MS   = "add to MS";
SUB_MS   = "subtract from MS";
simmode_opt = TDLCompileOption("sim_mode","Simulation mode",[SIM_ONLY,ADD_MS,SUB_MS]);
simmode_opt.when_changed(lambda mode:mssel.enable_input_column(mode!=SIM_ONLY));

# now load optional modules for the ME maker
from Meow import MeqMaker
meqmaker = MeqMaker.MeqMaker();

# specify available sky models
# these will show up in the menu automatically
from Siamese.OMS import gridded_sky
from Siamese.OMS import transient_sky
from Siamese.OMS import fitsimage_sky
import sky_models
import Meow.LSM
lsm = Meow.LSM.MeowLSM(include_options=False);

meqmaker.add_sky_models([gridded_sky,transient_sky,fitsimage_sky,sky_models,lsm]);

# now add optional Jones terms
# these will show up in the menu automatically

# Ncorr - correct for N
from Siamese.OMS import oms_n_inverse
meqmaker.add_sky_jones('Ncorr','n-term correction',oms_n_inverse);

# P - Parallactic angle
from Siamese.OMS import par_angle
meqmaker.add_sky_jones('P','parallactic angle',par_angle);

# Z - ionosphere
from Siamese.OMS import oms_ionosphere
meqmaker.add_sky_jones('Z','ionosphere',oms_ionosphere);

# L - dipole projection
from Siamese.OMS import oms_dipole_projection
meqmaker.add_sky_jones('L','dipole projection',oms_dipole_projection);

# E - beam
from Siamese.OMS import analytic_beams
from Siamese.SBY import sarod_cs1_beams
from Siamese.OMS import wsrt_beams
from Siamese.SBY import lofar_beams
# from Siamese import embrace_beams
from Siamese import vla_beams
from Siamese import mwa_beams
from Siamese import cortes_beams
from Siamese.OMS import oms_pointing_errors
meqmaker.add_sky_jones('E','beam',[analytic_beams,sarod_cs1_beams,wsrt_beams,lofar_beams,vla_beams,mwa_beams,cortes_beams],pointing=oms_pointing_errors);

# P - Parallactic angle
# from Siamese.OMS import par_angle
from Siamese.OMS import feed_angle
# meqmaker.add_sky_jones('P','parallactic angle',par_angle);
meqmaker.add_uv_jones('P','feed angle',feed_angle);

# G - gains
from Siamese.OMS import oms_gain_models
meqmaker.add_uv_jones('G','gains/phases',oms_gain_models);

# very important -- insert meqmaker's options properly
TDLCompileOptions(*meqmaker.compile_options());
# TDLRuntimeOptions(*meqmaker.runtime_options());

# noise option
TDLCompileOption("noise_stddev","Add noise, Jy",[None,1e-6,1e-3],more=float);

# visualisation option
# from Siamese.OMS import Visualisation
# from Timba.Contrib.SJG import Visualisation
# TDLCompileOptions(*Visualisation.compile_options())


# MPI options
from Meow import Parallelization
TDLCompileOptions(*Parallelization.compile_options());

def _define_forest (ns):
  #ANTENNAS = mssel.get_antenna_set(range(1,28));
  #array = Meow.IfrArray(ns,ANTENNAS);
  #observation = Meow.Observation(ns);
  #Meow.Context.set(array,observation);
  #stas = array.stations();
  if not mssel.msname:
    raise RuntimeError,"MS not set up in compile-time options";
  if run_purr:
    print mssel.msname;
    import os.path
    purrlog = os.path.normpath(mssel.msname)+".purrlog";
    Timba.TDL.GUI.purr(purrlog,[mssel.msname,'.']);
  # setup contexts properly
  array,observation = mssel.setup_observation_context(ns);

  # setup imaging options (now that we have an imaging size set up)
  imsel = mssel.imaging_selector(npix=512,arcmin=meqmaker.estimate_image_size());
  TDLRuntimeMenu("Imaging options",*imsel.option_list());
  
  # get a predict tree from the MeqMaker
  output = meqmaker.make_predict_tree(ns);
  
  # throw in a bit of noise
  if noise_stddev:
    # make two complex noise terms per station (x/y)
    noisedef = Meq.GaussNoise(stddev=noise_stddev)
    noise_x = ns.sta_noise('x');
    noise_y = ns.sta_noise('y');
    for p in array.stations():
      noise_x(p) << Meq.ToComplex(noisedef,noisedef);
      noise_y(p) << Meq.ToComplex(noisedef,noisedef);
    # now combine them into per-baseline noise matrices
    for p,q in array.ifrs():
      noise = ns.noise(p,q) << Meq.Matrix22(
        noise_x(p)+noise_x(q),noise_x(p)+noise_y(q),
        noise_y(p)+noise_x(q),noise_y(p)+noise_y(q)
      );
      ns.noisy_predict(p,q) << output(p,q) + noise;
    output = ns.noisy_predict;
    
  # in add or subtract sim mode, make some spigots and add/subtract visibilities
  if sim_mode == ADD_MS:
    spigots = array.spigots();
    for p,q in array.ifrs():
      ns.sum(p,q) << output(p,q) + spigots(p,q);
    output = ns.sum;
  elif sim_mode == SUB_MS:
    spigots = array.spigots();
    for p,q in array.ifrs():
      ns.diff(p,q) << spigots(p,q) - output(p,q);
    output = ns.diff;
  else:
    spigots = False;

  meqmaker.make_per_ifr_bookmarks(output,"Output visibilities");
  
  # make sinks and vdm.
  # The list of inspectors comes in handy here
  # inspectors = list(meqmaker.get_inspectors() or [])
  # Add any visualisations that are selected
  # inspectors.extend(Visualisation.get_inspectors(ns))
  Meow.StdTrees.make_sinks(ns,output,spigots=spigots,post=meqmaker.get_inspectors());
  # Meow.StdTrees.make_sinks(ns,output,spigots=spigots,post=inspectors); 
  # gets all the current inspectors (convert to list as tuple originally)
  # inspectors = list(meqmaker.get_inspectors() or [])

  # very important -- insert meqmaker's options properly
  TDLRuntimeOptions(*meqmaker.runtime_options());

  # Add any visualisations that are selected
  # inspectors.extend(Visualisation.get_inspectors(ns))

  # Meow.StdTrees.make_sinks(ns,output,spigots=spigots,post=meqmaker.get_inspectors());

   # moved here from outside function when visualisation used
  #TDLRuntimeOptions(*meqmaker.runtime_options());

    
  # close the meqmaker. This produces annotations, etc.
  meqmaker.close();


def _tdl_job_1_simulate_MS (mqs,parent,wait=False):
  mqs.execute('VisDataMux',mssel.create_io_request(),wait=wait);
  
  
# this is a useful thing to have at the bottom of the script, it allows us to check the tree for consistency
# simply by running 'python script.tdl'

if __name__ == '__main__':
  ns = NodeScope();
  _define_forest(ns);
  # resolves nodes
  ns.Resolve();  
  
  print len(ns.AllNodes()),'nodes defined';

