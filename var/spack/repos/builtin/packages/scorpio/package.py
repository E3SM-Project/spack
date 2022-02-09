# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Scorpio(CMakePackage):
    """Software for Caching Output and Reads for Parallel I/O (SCORPIO),
    derived from the Parallel IO libraries (PIO), is a high-level Parallel I/O
    Library for structured grid applications."""

    homepage = "https://github.com/E3SM-Project/scorpio"
    url      = "https://github.com/E3SM-Project/scorpio/archive/refs/tags/scorpio-v1.2.2.tar.gz"

    maintainers = ['xylar']

    version('1.2.2', sha256='f944a8b8527b188cf474d9cd26c0aaae5d8a263c245eb67cad92d8dd02ca7bfb')
    version('1.2.1', sha256='b106843008dd33fed8e2aca0cb5f13733342e398d94a489a0d474dfac8c902cc')
    version('1.2.0', sha256='db2b8db71fe65c5152c10df255ab45a7f5a8870219fc2034ca29feba02c8167b')

    variant('pnetcdf', default=False, description='enable pnetcdf')
    variant('timing', default=False, description='enable GPTL timing')
    variant('internal-timing', default=False,
            description='gather and print GPL timing stats')
    variant('tools', default=False, description='enable SCORPIO tools')
    variant('malloc', default=True,
            description='use native malloc (instead of bget package)')

    depends_on('mpi')
    depends_on('netcdf-c +mpi', type='link')
    depends_on('netcdf-fortran', type='link')
    depends_on('parallel-netcdf', type='link', when='+pnetcdf')

    def cmake_args(self):
        define = self.define
        define_from_variant = self.define_from_variant
        spec = self.spec
        env['CC'] = spec['mpi'].mpicc
        env['CXX'] = spec['mpi'].mpicxx
        env['FC'] = spec['mpi'].mpifc
        src = self.stage.source_path
        args = [
            define('NetCDF_C_PATH', spec['netcdf-c'].prefix),
            define('NetCDF_Fortran_PATH', spec['netcdf-fortran'].prefix),
        ]
        if spec.satisfies('+pnetcdf'):
            args.extend([
                define('PnetCDF_C_PATH', spec['parallel-netcdf'].prefix),
                define('PnetCDF_Fortran_PATH', spec['parallel-netcdf'].prefix),
            ])
        args.extend([
            define_from_variant('WITH_PNETCDF', 'pnetcdf'),
            define_from_variant('PIO_ENABLE_TIMING', 'timing'),
            define_from_variant('PIO_ENABLE_INTERNAL_TIMING',
                                'internal-timing'),
            define_from_variant('PIO_ENABLE_TOOLS ', 'tools'),
            define_from_variant('PIO_USE_MALLOC', 'malloc'),
        ])
        return args
