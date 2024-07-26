# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Albany(CMakePackage):
    """Albany is an implicit, unstructured grid, finite element code for the
    solution and analysis of multiphysics problems.  The Albany repository
    on the GitHub site contains hundreds of regression tests and examples
    that demonstrate the code's capabilities on a wide variety of problems
    including fluid mechanics, solid mechanics (elasticity and plasticity),
    ice-sheet flow, quantum device modeling, and many other applications."""

    homepage = "http://sandialabs.github.io/Albany"
    git      = "https://github.com/sandialabs/Albany.git"

    maintainers("ikalash")

    version('compass-2024-03-13', tag='compass-2024-03-13')
    version('compass-2023-08-03', tag='compass-2023-08-03')
    version("develop", branch="master")

    variant("debug",          default=False,
            description="Enable DEBUGGING")
    variant("fpe",          default=False,
            description="Enable CHECK_FPE")
    variant("landice",          default=True,
            description="Enable LANDICE")
    variant("unit_tests",          default=True,
            description="Enable_UNIT_TESTS")
    variant("confgui",          default=True,
            description="Enable Albany configuration (CI) GUI")
    variant("perf",          default=False,
            description="Enable PERFORMANCE_TESTS")
    variant("64bit",          default=True,
            description="Enable 64BIT")
    variant("sfad",          default=False,
            description="Enable SFad build")
    variant("sandybridge", default=False,
            description="Compile Trilinos used by Albany for Sandybridge architecture")
    variant("zen3", default=False,
            description="Compile Trilinos used by Albany for Zen3 architecture")
    variant("ampere80", default=False,
            description="Compile Trilinos used by Albany for Ampere80 architecture")
    variant("mpas",          default=False,
            description="Enable MPAS interface in build")
    variant("sfadsize", default="4", values=("4", "6", "8", "12", "24"), multi=False,
            description="SFad size")
    variant("py",          default=False,
            description="Enable PyAlbany interface in build")
    variant("mesh_depends_on_params",          default=False,
            description="Enable MESH_DEPENDS_ON_PARAMETERS option in build")
    variant("optimization",          default=False,
            description="Enable packages needed for Albany optimization capabilities (SuperLU, FROSCh, ROL)"),
    variant("omegah",          default=False,
            description="Enable Omega_h in build")
    variant("cuda", default=False,
            description="Enable CUDA in build")
    variant("uvm", default=False, when="+cuda",
            description="Enable UVM for CUDA builds")

    # Add dependencies
    depends_on("mpi")
    # Starting Feb. 2023, Trilinos and hence Albany requires cmake 3.23 or higher.
    depends_on("cmake@3.23:")

    depends_on("trilinos-for-albany~superlu-dist+exodus+chaco~isorropia+tempus+teko~intrepid+intrepid2+minitensor+phalanx+pnetcdf+nox+piro+shards+stk+amesos2~amesos~hypre+ifpack2~mumps~suite-sparse~epetra~ifpack~ml+muelu~aztec gotype=long_long", when="~sandybridge~optimization")
    depends_on("trilinos-for-albany~superlu-dist+exodus+chaco~isorropia+tempus+teko~intrepid+intrepid2+minitensor+phalanx+pnetcdf+nox+piro+shards+stk+amesos2~amesos~hypre+ifpack2~mumps~suite-sparse+sandybridge~epetra~ifpack~ml+muelu~aztec gotype=long_long", when="+sandybridge~optimization")

    depends_on("trilinos-for-albany~superlu-dist+exodus+chaco~isorropia+tempus+teko~intrepid+intrepid2+minitensor+phalanx+pnetcdf+nox+piro+shards+stk+amesos2~amesos~hypre+ifpack2~mumps~suite-sparse~epetra~ifpack~ml+muelu~aztec+rol gotype=long_long", when="~sandybridge~optimization+py")
    depends_on("trilinos-for-albany~superlu-dist+exodus+chaco~isorropia+tempus+teko~intrepid+intrepid2+minitensor+phalanx+pnetcdf+nox+piro+shards+stk+amesos2~amesos~hypre+ifpack2~mumps~suite-sparse+sandybridge~epetra~ifpack~ml+muelu~aztec+rol gotype=long_long", when="+sandybridge~optimization+py")

    depends_on("trilinos-for-albany~superlu-dist+exodus+chaco~isorropia+tempus+teko~intrepid+intrepid2+minitensor+phalanx+pnetcdf+nox+piro+shards+stk+amesos2~amesos~hypre+ifpack2~mumps~suite-sparse~epetra~ifpack~ml+muelu~aztec+superlu+rol+frosch gotype=long_long", when="~sandybridge+optimization")
    depends_on("trilinos-for-albany~superlu-dist+exodus+chaco~isorropia+tempus+teko~intrepid+intrepid2+minitensor+phalanx+pnetcdf+nox+piro+shards+stk+amesos2~amesos~hypre+ifpack2~mumps~suite-sparse+sandybridge~epetra~ifpack~ml+muelu~aztec+superlu+rol+frosch gotype=long_long", when="+sandybridge+optimization")

    depends_on("trilinos-for-albany+cuda+uvm", when="+uvm")
    depends_on("trilinos-for-albany+cuda", when="+cuda~uvm")
    depends_on("trilinos-for-albany+zen3", when="+zen3")
    depends_on("trilinos-for-albany+ampere80", when="+ampere80")

    depends_on("trilinos-for-albany@develop", when="@develop")
    depends_on("trilinos-for-albany@compass-2023-08-03", when="@compass-2023-08-03")
    depends_on("trilinos-for-albany@compass-2024-03-13", when="@compass-2024-03-13")

    extends("python@:3.9",        when="+py")

    depends_on("py-pybind11",     when="+py")
    depends_on("py-numpy",        when="+py")
    depends_on("py-mpi4py",       when="+py")
    depends_on("py-scipy",        when="+py")

    #IKT, 2/27/2022: comment the above lines and uncomment the followint to use trilinos, instead of
    #trilinos-for-albany.  The code should build but will not run (there are seg faults at the end of
    #each test that is run, after time monitor output).
    #depends_on("trilinos~superlu-dist+exodus+chaco+isorropia+tempus+rythmos+teko+intrepid+intrepid2+minitensor+phalanx+nox+piro+shards+stk+amesos2~hypre+ifpack2~mumps~suite-sparse+panzer gotype=long_long")
    def cmake_args(self):
        spec = self.spec
        #trilinos_dir = spec["trilinos"].prefix
        trilinos_dir = spec["trilinos-for-albany"].prefix
        options = []

        options.extend(
            ["-DALBANY_TRILINOS_DIR:FILEPATH={0}".format(trilinos_dir), "-DINSTALL_ALBANY:BOOL=ON"]
        )

        options.extend([
            '-DCMAKE_C_COMPILER=%s'       % spec['mpi'].mpicc,
            '-DCMAKE_CXX_COMPILER=%s'     % spec['mpi'].mpicxx
                       ])

        options.extend([
                       "-DENABLE_LANDICE:BOOL=%s" % (
                           "ON" if "+landice" in spec else "OFF"),
                       "-DENABLE_UNIT_TESTS:BOOL=%s" % (
                           "ON" if "+unit_tests" in spec else "OFF"),
                       "-DENABLE_CHECK_FPE:BOOL=%s" % (
                           "ON" if "+fpe" in spec else "OFF"),
                       "-DENABLE_ALBANY_CI:BOOL=%s" % (
                           "ON" if "+ci" in spec else "OFF"),
                       "-DENABLE_PERFORMANCE_TESTS:BOOL=%s" % (
                           "ON" if "+perf" in spec else "OFF"),
                       "-DENABLE_64BIT_INT:BOOL=%s" % (
                           "ON" if "+64bit" in spec else "OFF"),
                       "-DENABLE_FAD_TYPE:STRING=%s" % (
                           "SFad" if "+sfad" in spec else "DFad"),
                       "-DENABLE_MPAS_INTERFACE:BOOL=%s" % (
                           "ON" if "+mpas" in spec else "OFF"),
                       "-DENABLE_ALBANY_PYTHON:BOOL=%s" % (
                           "ON" if "+py" in spec else "OFF"),
                       "-DENABLE_MESH_DEPENDS_ON_PARAMETERS:BOOL=%s" % (
                           "ON" if "+mesh_depends_on_params" in spec else "OFF"),
                       "-DENABLE_OMEGAH:BOOL=%s" % (
                           "ON" if "+omegah" in spec else "OFF")
                       ])
        if "+py" in spec:
            options.append(
                "-DPYTHON_EXECUTABLE=%s" % (spec["python"].command.path)
                )

        if "+sfad" in spec:
          options.extend([
            "-DALBANY_SFAD_SIZE=%d" % int(spec.variants["sfadsize"].value)
                       ])
        if "+debug" in spec:
          options.extend([
            "-DCMAKE_BUILD_TYPE:STRING=DEBUG"
                       ])
        else:
          options.extend([
            "-DCMAKE_BUILD_TYPE:STRING=RELEASE"
                       ])

        return options
