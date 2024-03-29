.. image:: https://zenodo.org/badge/32748849.svg
   :target: https://zenodo.org/badge/latestdoi/32748849

=========================================================================
pyMPM - python implementation of the milimeter wave propagation model MPM
=========================================================================

A Python implementation of the millimeter wave propagation model MPM as described in H.J. Liebe, G.A. Hufford, M.G. Cotton, " *Propagation modeling of moist air and suspended water/ice particles at frequencies below 1000 GHz*" Proc. NATO/AGARD Wave Propagation Panel, 52nd meeting, No. 3/1-10, Mallorca, Spain, 17 - 20 May, 1993.

**Currently only dry air and water vapor are considered**. The other MPM modules will be added later (hopefully...).

This implementation is based on the MATLAB version of MPM93 developed at the `university of Bern <http://www.iapmw.unibe.ch/teaching/vorlesungen/mikrowellenphysik/software>`_.

Installation
------------

pyMPM uses Python 3 (tested with 3.8, 3.9, 3.10 and 3.11) and depends on `numpy`. It can be installed via `pip`::

    $ pip install pyMPM

Usage
-----

Here is an example provided as `IPython notebook <http://nbviewer.ipython.org/github/cchwala/pyMPM/blob/master/notebooks/Example.ipynb>`_.

A further example notebook `dealing with the relation of attenuation and absolute humidity at the frequencies commonly used in commercial microwave links <http://nbviewer.ipython.org/github/cchwala/pyMPM/blob/master/notebooks/Water%20vapor%20attenuation%20at%20MW%20link%20frequencies.ipynb>`_.
