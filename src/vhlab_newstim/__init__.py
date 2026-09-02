"""Read NewStim data files and data structures written by MATLAB.

This package reads what `vhlab-NewStim-matlab
<https://github.com/VH-Lab/vhlab-NewStim-matlab>`_ wrote -- principally the
``stimscript`` stored as ``saveScript`` in a ``stims.mat``. It does not present
stimuli and does not talk to hardware: NewStim's presentation half is built on
Psychtoolbox, which exists only for MATLAB.

Which MATLAB function has a Python home here, which one is deliberately out of
scope, and why, is recorded per function in the
``vhlab_newstim_matlab_python_bridge.yaml`` files that this package and each of
its subpackages carry. See ``PORTING_INSTRUCTIONS`` at the repository root.
"""

__all__ = []
