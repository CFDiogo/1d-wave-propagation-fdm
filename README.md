1D Elastic Wave Simulation (Fortran)

A numerical project implementing the Finite Difference Method (FDM) to simulate the propagation of elastic waves and vibration dynamics in a one-dimensional bar.

This Fortran program models an elastic bar with fixed and free end conditions, applying an initial impulse ($v_0$) to the free end. The code focuses on calculating stable time steps using the CFL condition and includes numerical integration for the principal time steps.

Key Features:

Implemented in modern Fortran (using dp for double precision).

Handles fixed-free boundary conditions.

Outputs simulation results (deslocamento vs. posição) to a .dat file for plotting.
