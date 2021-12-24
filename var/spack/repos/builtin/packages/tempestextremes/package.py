# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import shutil
import glob
from spack import *


class Tempestextremes(MakefilePackage):
    """ TempestExtremes is a growing collection of detection and
    characterization algorithms for large climate datasets, leveraging C++ for
    rapid throughput and a command line interface that maximizes flexibility
    of each kernel. The tracking kernels in this package have been already
    used for tracking and characterizing tropical cyclones (TCs), extratropical
    cyclones (ETCs), monsoonal depressions, atmospheric blocks, atmospheric
    rivers, and mesoscale convective systems (MCSs). By considering multiple
    extremes within the same framework, we can study the joint characteristics
    of extremes while minimizing the total data burden.
    """

    homepage = "https://github.com/ClimateGlobalChange/tempestextremes"
    url = "https://github.com/ClimateGlobalChange/tempestextremes/archive/2.2.tar.gz"

    maintainers = ['xylar', 'paullric']

    version('2.2', sha256='d8fdc4a2c1b8794cb1699739e5d0119f0ed5a4eb5ab6212cfbc0215ec6110bc5')
    version('2.1', sha256='fc31940d855297964fa091ed5da0f96c28e8a25fd237dfa660357a054600ab70')
    version('2.0', sha256='121ed3184f51b2830a00ca37da5848553763df38afb9b970125a712440f1ead6')

    variant('mpi', default=True, description='Build with MPI support')

    # Required dependencies
    depends_on('makedepend', type='build')
    depends_on('netcdf-c')

    # Optional dependencies
    depends_on('mpi', when='+mpi')

    # Make sure not to use special make configurations for specific systems
    patch('system.patch')

    parallel = False

    def edit(self, spec, prefix):
        if '+mpi' not in spec:
            # Configure for no MPI
            makefile = FileFilter('mk/config.make')
            makefile.filter('PARALLEL= MPIOMP', 'PARALLEL= NONE')

        makefile = FileFilter('mk/system/default.make')
        makefile.filter('CXX=               g\+\+',
                        'CXX = {}'.format(os.environ['CXX']))
        if '+mpi' in spec:
            makefile.filter('MPICXX=            mpiCC',
                            'MPICXX = {}'.format(spec['mpi'].mpicxx))

        makefile.filter('NETCDF_ROOT =       $(NETCDF_HOME)',
                        'NETCDF_ROOT = {}'.format(spec['netcdf-c'].prefix))

    def install(self, spec, prefix):
        bin_files = sorted(
            glob.glob(join_path(self.build_directory, 'bin', '*')))

        mkdirp(prefix.bin)
        for bin_filename in bin_files:
            install(bin_filename, prefix.bin)
