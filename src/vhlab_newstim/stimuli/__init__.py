"""Stimulus classes: ``stimulus`` and the concrete stimuli that inherit it.

Ports ``Stimuli/`` from vhlab-NewStim-matlab, excluding ``Stimuli/Display
objs`` which is :mod:`vhlab_newstim.display`. Every one of the nineteen classes
defines ``getparameters``, and that is the read surface; ``loadstim``,
``unloadstim``, ``customdraw`` and ``animate`` are Psychtoolbox and are not
ported.

Nothing is ported yet. ``vhlab_newstim_matlab_python_bridge.yaml`` in this
directory lists every MATLAB function in ``Stimuli/`` with its status; update
the entry in the same commit that ports the function.
"""

__all__ = []
