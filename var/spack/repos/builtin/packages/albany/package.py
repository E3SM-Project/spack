# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Albany(CMakePackage):
    """Albany is an implicit, unstructured grid, finite element code for the
       solution and analysis of multiphysics problems.  The Albany repository
       on the GitHub site contains hundreds of regression tests and examples
       that demonstrate the code's capabilities on a wide variety of problems
       including fluid mechanics, solid mechanics (elasticity and plasticity),
       ice-sheet flow, quantum device modeling, and many other applications."""

    homepage = "http://sandialabs.github.io/Albany"
    git      = "https://github.com/sandialabs/Albany.git"

    maintainers = ['ikalash']

    version('develop', branch='master')

    variant('debug',          default=False,
            description='Enable DEBUGGING')
    variant('fpe',          default=False,
            description='Enable CHECK_FPE')
    variant('landice',          default=True,
            description='Enable LANDICE')
    variant('unit_tests',          default=True,
            description='Enable_UNIT_TESTS')
    variant('confgui',          default=True,
            description='Enable Albany configuration (CI) GUI')
    variant('perf',          default=False,
            description='Enable PERFORMANCE_TESTS')
    variant('64bit',          default=True,
            description='Enable 64BIT')
    variant('sfad',          default=False,
            description='Enable SFad build')
    variant('mpas',          default=False,
            description='Enable MPAS interface in build')
    variant('sfadsize', default='4', values=('4', '6', '8', '12', '24'), multi=False,
            description='SFad size')

    # Add dependencies
    depends_on('mpi')
    #depends_on('trilinos@develop~superlu-dist+exodus+chaco+isorropia+tempus+rythmos+teko+intrepid+intrepid2+minitensor+phalanx+pnetcdf+nox+piro+rol+shards+stk+amesos2~hypre+ifpack2~mumps~suite-sparse gotype=long_long', when='~sandybridge')
    #depends_on('trilinos@develop~superlu-dist+exodus+chaco+isorropia+tempus+rythmos+teko+intrepid+intrepid2+minitensor+phalanx+pnetcdf+nox+piro+rol+shards+stk+amesos2~hypre+ifpack2~mumps~suite-sparse+sandybridge gotype=long_long', when='+sandybridge')
    depends_on('trilinos@develop~superlu-dist+exodus+chaco+isorropia+tempus+rythmos+teko+intrepid+intrepid2+minitensor+phalanx+nox+piro+rol+shards+stk+amesos2~hypre+ifpack2~mumps~suite-sparse gotype=long_long')

    def cmake_args(self):
        spec = self.spec
        trilinos_dir = spec['trilinos'].prefix
        options = []

        options.extend([
            '-DALBANY_TRILINOS_DIR:FILEPATH={0}'.format(trilinos_dir),
            '-DINSTALL_ALBANY:BOOL=ON'
        ])

        options.extend([
                       '-DENABLE_LANDICE:BOOL=%s' % (
                           'ON' if '+landice' in spec else 'OFF'),
                       '-DENABLE_UNIT_TESTS:BOOL=%s' % (
                           'ON' if '+unit_tests' in spec else 'OFF'),
                       '-DENABLE_DEBUGGING:BOOL=%s' % (
                           'ON' if '+debug' in spec else 'OFF'),
                       '-DENABLE_CHECK_FPE:BOOL=%s' % (
                           'ON' if '+fpe' in spec else 'OFF'),
                       '-DENABLE_ALBANY_CI:BOOL=%s' % (
                           'ON' if '+ci' in spec else 'OFF'),
                       '-DENABLE_PERFORMANCE_TESTS:BOOL=%s' % (
                           'ON' if '+perf' in spec else 'OFF'),
                       '-DENABLE_64BIT_INT:BOOL=%s' % (
                           'ON' if '+64bit' in spec else 'OFF'),
                       '-DENABLE_FAD_TYPE:STRING=%s' % (
                           'SFad' if '+sfad' in spec else 'DFad'),
                       '-DENABLE_MPAS_INTERFACE:=%s' % (
                           'ON' if 'mpas' in spec else 'OFF')
                       ])

        if '+sfad' in spec: 
          options.extend([
            '-DALBANY_SFAD_SIZE=%d' % int(spec.variants['sfadsize'].value)
                       ])
        return options
