..
  Copyright The dnf Project Authors
  SPDX-License-Identifier: GPL-2.0-or-later

#############################################
 Changes in the DNF hook API compared to YUM
#############################################


.. only :: html
   

This table provides what alternative hooks are available in DNF compared to
YUM.

===========  =================  ==============================
Hook Number  YUM hook           DNF hook
-----------  -----------------  ------------------------------
``1``        ``config``         ``init``
``2``        ``postconfig``     ``init``
``3``        ``init``           ``init``
``4``        ``predownload``          
``5``        ``postdownload``         
``6``        ``prereposetup``          
``7``        ``postreposetup``  ``sack``
``8``        ``exclude``        ``resolved``
``9``        ``preresolve``              
``10``       ``postresolve``    ``resolved but no re-resolve``
``11``       ``pretrans``       ``pre_transaction``
``12``       ``postrans``       ``transaction``
``13``       ``close``          ``transaction``
``14``       ``clean``                   
===========  =================  ==============================

Feel free to file an RFE_ for missing functionality if you need it.

.. _RFE: https://github.com/rpm-software-management/dnf/wiki/Bug-Reporting#new-feature-request

