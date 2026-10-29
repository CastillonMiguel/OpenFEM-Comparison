.. _FEM_software_calculix:

CalculiX
========
`CalculiX <https://github.com/Dhondtguido/CalculiX>`_ :footcite:t:`book_calculix` is an open-source finite element analysis (FEA) software suite for structural mechanics simulations.

Compilation on macOS (Apple Silicon)
------------------------------------
The code used in this example is based on the official CalculiX source code repository maintained by Guido Dhondt:

* `CalculiX source code <https://github.com/Dhondtguido/CalculiX>`_

The software was successfully compiled and executed on macOS running on Apple Silicon (ARM64).

The build configuration uses the following external libraries and dependencies:

* LAPACK and ARPACK are installed and managed using Homebrew.
* SPOOLES was compiled locally on the target machine. Minor modifications to the original source code and Makefile were required to ensure compatibility with the platform.

Compilation configuration

The following Makefile contains the compiler options, library paths, and linking flags used to build CalculiX on macOS ARM64.

.. literalinclude:: Makefile_macos_arm64
   :language: make
   :caption: Makefile configuration for CalculiX on macOS ARM64
   :linenos:


.. footbibliography::