"""Display objects carried by every stimulus: ``displayprefs``, ``displaystruct``.

Ports ``Stimuli/Display objs/`` from vhlab-NewStim-matlab. ``displayprefs`` is
persistent data and is present in every stimulus read from a ``stims.mat``;
``displaystruct`` is the Psychtoolbox display state, which
``@stimulus/strip.m`` clears before the file is written, so a reader always
finds it empty.

Nothing is ported yet. ``vhlab_newstim_matlab_python_bridge.yaml`` in this
directory lists every MATLAB function in ``Stimuli/Display objs/`` with its
status; update the entry in the same commit that ports the function.
"""

__all__ = []
