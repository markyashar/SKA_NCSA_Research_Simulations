# Copyright (C) 2009
# The MeqTree Foundation & 
# JIVE (Joint Institute for VLBI in Europe)
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

EVN = ['EB','JB','MC','NT','ON','SG','TR','UR','WB']
EEVN = ['EB','CM','JB2','MC','ON','TR','WB']
MERLIN6 = ['CM', 'JB2', 'DA', 'DE', 'KN', 'TA']
MERLIN7 = ['CM', 'JB2', 'JB', 'DA', 'DE', 'KN','TA']
VLBA = ['BR', 'FD','HN','KP','LA','MK','NL','OV','PT','SC']
VLA_A = ['YN8','YN16','YN24','YN32','YN40','YN48','YN56','YN64','YN72',
         'YE8','YE16','YE24','YE32','YE40','YE48','YE56','YE64','YE72',
         'YW8','YW16','YW24','YW32','YW40','YW48','YW56','YW64','YW72']
VLA_ANB = ['YN8','YN16','YN24','YN32','YN40','YN48','YN56','YN64','YN72',
           'YE4','YE8','YE12','YE16','YE20','YE24','YE28','YE32','YE36',
           'YW4','YW8','YW12','YW16','YW20','YW24','YW28','YW32','YW36']
VLA_B = ['YN4','YN8','YN12','YN16','YN20','YN24','YN28','YN32','YN36',
         'YE4','YE8','YE12','YE16','YE20','YE24','YE28','YE32','YE36',
         'YW4','YW8','YW12','YW16','YW20','YW24','YW28','YW32','YW36']
VLA_BNC = ['YN4','YN8','YN12','YN16','YN20','YN24','YN28','YN32','YN36',
           'YE2','YE4','YE6','YE8','YE10','YE12','YE14','YE16','YE18',
           'YW2','YW4','YW6','YW8','YW10','YW12','YW14','YW16','YW18']
VLA_C = ['YN2','YN4','YN6','YN8','YN10','YN12','YN14','YN16','YN18',
         'YE2','YE4','YE6','YE8','YE10','YE12','YE14','YE16','YE18',
         'YW2','YW4','YW6','YW8','YW10','YW12','YW14','YW16','YW18']
VLA_CND = ['YN2','YN4','YN6','YN8','YN10','YN12','YN14','YN16','YN18',
           'YE1','YE2','YE3','YE4','YE5','YE6','YE7','YE8','YE9',
           'YW1','YW2','YW3','YW4','YW5','YW6','YW7','YW8','YW9']
VLA_D = ['YN1','YN2','YN3','YN4','YN5','YN6','YN7','YN8','YN9',
         'YE1','YE2','YE3','YE4','YE5','YE6','YE7','YE8','YE9',
         'YW1','YW2','YW3','YW4','YW5','YW6','YW7','YW8','YW9']
HSA = ['AR','EB','GB', 'Y'] + VLBA
GLOBAL = EVN + VLBA
GMVA = ['EB','ON','MH','PV','NL','FD','LA','KP','PT','OV','BR','MK'] # PB?
WSRT = ['WRT0','WRT1','WRT2','WRT3','WRT4',
        'WRT5','WRT6','WRT7','WRT8','WRT9',
        'WRTA','WRTB','WRTC','WRTD']
WSRT10 = ['WRT0','WRT1','WRT2','WRT3','WRT4',
          'WRT5','WRT6','WRT7','WRT8','WRT9']
GMRT = ['GMRT:C00:01', 'GMRT:C01:02', 'GMRT:C02:03', 'GMRT:C03:04',
        'GMRT:C04:05', 'GMRT:C05:06', 'GMRT:C06:07', 'GMRT:C08:08',
        'GMRT:C09:09', 'GMRT:C10:10', 'GMRT:C11:11', 'GMRT:C12:12',
        'GMRT:C13:13', 'GMRT:C14:14', 'GMRT:E02:15', 'GMRT:E03:16',
        'GMRT:E04:17', 'GMRT:E05:18', 'GMRT:E06:19', 'GMRT:S01:20',
        'GMRT:S02:21', 'GMRT:S03:22', 'GMRT:S04:23', 'GMRT:S06:24',
        'GMRT:W01:25', 'GMRT:W02:26', 'GMRT:W03:27', 'GMRT:W04:28',
        'GMRT:W05:29', 'GMRT:W06:30', 'GMRT:C07:31', 'GMRT:S05:32']

LOFAR_CORE_LBA = ['CS002LBA', 'CS003LBA', 'CS004LBA', 'CS005LBA',
                 'CS006LBA', 'CS007LBA', 'CS021LBA', 'CS024LBA',
                 'CS030LBA', 'CS032LBA', 'CS103LBA', 'CS201LBA',
                 'CS301LBA', 'CS302LBA', 'CS401LBA', 'CS501LBA']
LOFAR_CORE_HBA = ['CS002HBA0', 'CS002HBA1', 'CS003HBA0', 'CS003HBA1',
                 'CS004HBA0', 'CS004HBA1', 'CS005HBA0', 'CS005HBA1',
                 'CS006HBA0', 'CS006HBA1', 'CS007HBA0', 'CS007HBA1',
                 'CS021HBA0', 'CS021HBA1', 'CS024HBA0', 'CS024HBA1',
                 'CS030HBA0', 'CS030HBA1', 'CS032HBA0',
LOFAR_REMOTE_LBA = ['RS106LBA', 'RS208LBA', 'RS306LBA', 'RS307LBA',
                   'RS503LBA', 'RS509LBA']
LOFAR_REMOTE_HBA = ['RS106HBA', 'RS208HBA', 'RS306HBA', 'RS307HBA',
                   'RS503HBA', 'RS509HBA']
LOFAR_INTERNATIONAL_LBA = ['DE601LBA', 'DE602LBA', 'DE603LBA']
LOFAR_INTERNATIONAL_HBA = ['DE602HBA']
LOFAR_CORE = LOFAR_CORE_LBA + LOFAR_CORE_HBA
LOFAR_REMOTE = LOFAR_REMOTE_LBA + LOFAR_REMOTE_HBA
LOFAR_INTERNATIONAL = LOFAR_INTERNATIONAL_LBA + LOFAR_INTERNATIONAL_HBA
LOFAR_NL_LBA = LOFAR_CORE_LBA + LOFAR_REMOTE_LBA
LOFAR_NL_HBA = LOFAR_CORE_HBA + LOFAR_REMOTE_HBA
LOFAR_NL = LOFAR_CORE + LOFAR_REMOTE
ELOFAR_LBA = LOFAR_CORE_LBA + LOFAR_REMOTE_LBA + LOFAR_INTERNATIONAL_LBA
ELOFAR_HBA = LOFAR_CORE_HBA + LOFAR_REMOTE_HBA + LOFAR_INTERNATIONAL_HBA
ELOFAR = LOFAR_CORE + LOFAR_REMOTE + LOFAR_INTERNATIONAL

MWA512 = ['MWA512_%03d' % i for i in range(1, 513)]
MWA32T = ['MWA32T_%03d' % i for i in range(1, 33)]
# SKA = ['SKA%d' % i for i in range(0, 49)] 
SKA = ['SKA%d' % i for i in range(0, 175)]
# SKA = ['SKA%04d' % i for i in range(1, 60)]
del i  # Don't want i to end up in the namespace

VLAA = VLA_A; VLAB = VLA_B; VLAC = VLA_C; VLAD = VLA_D # backwards compatibility

