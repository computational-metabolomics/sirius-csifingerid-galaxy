SIRIUS-CSI:FingerID for Galaxy
==============================
|Build Status (Travis)| |Git| 

Galaxy tool wrapper for SIRIUS-CSI:FingerID.

Website (and CLI download): https://bio.informatik.uni-jena.de/software/sirius/

Source code: https://github.com/boecker-lab/sirius


Version
------

v4.9.8+Galaxy0

Galaxy
------
`Galaxy <https://galaxyproject.org>`_ is an open, web-based platform for data intensive biomedical research. Whether on the free public server or your own instance, you can perform, reproduce, and share complete analyses. 

Installation note
------

The SIRIUS-CSI:FingerID CLI used for the Galaxy wrapper is available in Conda via the Bioconda channel. 


Developers & Contributors
-------------------------
 - Jordi Capellades (j.capellades.to@gmail.com) - Universitat Rovira i Virgili (Tarragona, Spain)
 - Tom Lawson (t.n.lawson@bham.ac.uk) - `University of Birmingham (UK) <http://www.birmingham.ac.uk/index.aspx>`_
 - Simon Bray (sbray@informatik.uni-freiburg.de) - `University of Freiburg (Germany) <https://www.uni-freiburg.de/>`_
 - Ralf J. M. Weber (r.j.weber@bham.ac.uk) - `University of Birmingham (UK) <http://www.birmingham.ac.uk/index.aspx>`_


Changes
-------
v4.9.8+Galaxy1:
 - Fix galaxy wrapper rank and confidence filter
 - Put Galaxy "profile" as 19.01 rather than 21.01

v4.9.8+Galaxy0:
 - Update to work with v4.9.8 of SIRIUS-CSI:FingerID
 - Output now includes summary of CANOPUS analysis

v4.0.1+Galaxy4:
 - Add adduct choice from tool or via MSP

v4.0.1+Galaxy3:
 - Add profile to XML to enforce correct conda build

v4.0.1+Galaxy2:
 - Change owner of repository to computational-metabolomics

v4.0.1+Galaxy1:
 - IUC updates

v4.0.1+Galaxy0.2.6:
 - More updates for check empty results

v4.0.1+Galaxy0.2.5:
 - Updated check for empty results

v4.0.1+Galaxy0.2.4:
 - Check for empty input file added
 - Added Glucose unit-test

v0.2.3:
 - Removed quotes "" for values in output table

v0.2.2:
 - Bug Fix for skipping final MSP spectra if two empty lines not present

v0.2.1:
 - Fixed bug where ID was not being updated

v0.2.0:
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


