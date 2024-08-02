# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Scorpio(CMakePackage):
    """Software for Caching Output and Reads for Parallel I/O (SCORPIO),
    derived from the Parallel IO libraries (PIO), is a high-level Parallel I/O
    Library for structured grid applications."""

    homepage = "https://github.com/E3SM-Project/scorpio"
    url      = "https://github.com/E3SM-Project/scorpio/archive/refs/tags/scorpio-v1.2.2.tar.gz"

    maintainers("xylar", "altheaden")
    version("1.6.5", sha256="b81af12f3cadec25898c9b102775f77457f3dd95b878ee6c7edaf6eb0b16d4fc")
    version("1.6.4", sha256="4739718c82f39fa8f9922280175dcdab56786193df8f6fb07f145df1274ed828")
    version("1.6.3", sha256="66350046fa22c8a06fffb8bf2a0fc48c66f05bf00da3a6ab83a0fad9c3c91da4")
    version("1.6.2", sha256="fa97e3255c6c558960356ef7726db7ce21072cd42fb4cc18a5e2d54ca8eb8d56")
    version("1.6.1", sha256="5e2a406cfa9e8e54622e1671bbebc6f364992fa3671d71d154666a274aa8c5a3")
    version("1.6.0", sha256="fcc18b7eaf0dae4fc83e17a7ca2fc695f476fa96539881e37406efbcb821947d")
    version("1.4.2", sha256="e41b2725b2389df48b91932224a0dfb8c8fe6e98c7a49e1dfd65f7d49f7ffa81")
    version("1.4.1", sha256="7cb4589410080d7e547ef17ddabe68f749e6af019c1d0e6ee9f11554f3ff6b1a")
    version("1.3.2", sha256="663805fa24e85c88509ecd7893264e3d7d2ff27efb304e0f75dd1f0c450b08a6")
    version("1.3.1", sha256="4ee6db92fff562e49c58ca1e147f242dd6c7168b7d10c3ec47b399f0d683ce5b")
    version("1.2.2", sha256="f944a8b8527b188cf474d9cd26c0aaae5d8a263c245eb67cad92d8dd02ca7bfb")
    version("1.2.1", sha256="b106843008dd33fed8e2aca0cb5f13733342e398d94a489a0d474dfac8c902cc")
    version("1.2.0", sha256="db2b8db71fe65c5152c10df255ab45a7f5a8870219fc2034ca29feba02c8167b")

    variant("pnetcdf", default=False, description="enable pnetcdf")
    variant("timing", default=False, description="enable GPTL timing")
    variant("internal-timing", default=False,
            description="gather and print GPL timing stats")
    variant("tools", default=False, description="enable SCORPIO tools")
    variant("malloc", default=True,
            description="use native malloc (instead of bget package)")

    depends_on("gptl", when="+timing")
    depends_on("mpi")
    depends_on("netcdf-c +mpi", type="link")
    depends_on("netcdf-fortran", type="link")
    depends_on("parallel-netcdf", type="link", when="+pnetcdf")

    patch("6f1ecba7774293d3db34226b09339b32a28f24a3.patch", when="@1.3.2")
    patch("a248097a015b14c7015a3ce23a032f15b5fe7612.patch", when="@1.3.2")

    def cmake_args(self):
        define = self.define
        define_from_variant = self.define_from_variant
        spec = self.spec
        env["CC"] = spec["mpi"].mpicc
        env["CXX"] = spec["mpi"].mpicxx
        env["FC"] = spec["mpi"].mpifc
        args = [
            define("NetCDF_C_PATH", spec["netcdf-c"].prefix),
            define("NetCDF_Fortran_PATH", spec["netcdf-fortran"].prefix),
        ]
        if spec.satisfies("+pnetcdf"):
            args.extend([
                define("PnetCDF_C_PATH", spec["parallel-netcdf"].prefix),
                define("PnetCDF_Fortran_PATH", spec["parallel-netcdf"].prefix),
            ])
        args.extend([
            define_from_variant("WITH_PNETCDF", "pnetcdf"),
            define_from_variant("PIO_ENABLE_TIMING", "timing"),
            define_from_variant("PIO_ENABLE_INTERNAL_TIMING",
                                "internal-timing"),
            define_from_variant("PIO_ENABLE_TOOLS ", "tools"),
            define_from_variant("PIO_USE_MALLOC", "malloc"),
        ])
        if spec.satisfies("%cce"):
            # force lowercase fortran modules
            args.extend([
                define("CMAKE_Fortran_FLAGS", "-em -ef")
                ])
        return args
