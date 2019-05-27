SIRIUS-CSI:FingerID for Galaxy
==============================
|Build Status (Travis)| |Git| 

Galaxy tool wrapper for SIRIUS-CSI:FingerID.

Website (and CLI download): https://bio.informatik.uni-jena.de/software/sirius/

Source code: https://github.com/boecker-lab/sirius


Version
------

0.2.0 Galaxy tool (using `SIRIUS-CSI:FingerID v4.0.1 <https://bio.informatik.uni-jena.de/repository/dist-release-local/de/unijena/bioinf/ms/sirius/4.0.1/sirius-4.0.1-linux64-headless.zip>`_)  

Galaxy
------
`Galaxy <https://galaxyproject.org>`_ is an open, web-based platform for data intensive biomedical research. Whether on the free public server or your own instance, you can perform, reproduce, and share complete analyses. 

Installation note
------

The SIRIUS-CSI:FingerID CLI used for the Galaxy wrapper  is not available currently in Bioconda but is accessible used the channel `tomnl <https://anaconda.org/tomnl/sirius-csifingeridx>`_, the Galaxy tool is currently using `SIRIUS-CSI:FingerID v4.0.1 <https://bio.informatik.uni-jena.de/repository/dist-release-local/de/unijena/bioinf/ms/sirius/4.0.1/sirius-4.0.1-linux64-headless.zip>`_).

The conda channel "tomnl" needs to be available as a channel for Galaxy or Planemo, e.g. for planemo the following command is requried "--conda_ensure_channels tomnl,iuc,bioconda,conda-forge,defaults".


Developers & Contributors
-------------------------
 - Jordi Capellades (j.capellades.to@gmail.com) - Universitat Rovira i Virgili (Tarragona, Spain)
 - Tom Lawson (t.n.lawson@bham.ac.uk) - `University of Birmingham (UK) <http://www.birmingham.ac.uk/index.aspx>`_
 - Ralf J. M. Weber (r.j.weber@bham.ac.uk) - `University of Birmingham (UK) <http://www.birmingham.ac.uk/index.aspx>`_


Changes
-------
Version 0.2.0:
 - Update to handle multiple types of MSP files
 - Autohandling of adducts (if in MSP file)
 - Update code structure to match the metfrag-galaxy tool
 - Update to version 4.0.1 of SIRIUS-CSI:FingerID

License
-------
Released under the GNU General Public License v3.0 (see LICENSE file)


.. |Build Status (Travis)| image:: https://img.shields.io/travis/computational-metabolomics/sirius-csifingerid-galaxy.svg?style=flat&maxAge=3600&label=Travis-CI
   :target: https://travis-ci.org/computational-metabolomics/sirius-csifingerid-galaxy

.. |Git| image:: https://img.shields.io/badge/repository-GitHub-blue.svg?style=flat&maxAge=3600
   :target: https://github.com/boecker-lab/sirius


