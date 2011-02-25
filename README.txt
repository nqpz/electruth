
=========
electruth
=========

electruth is a collection of boolean logic tools. It can be used as
both a command-line tool and a Python library. It understands boolean
algebra (to some extent) and can be used to simplify boolean
expressions using the Quine-McClusky method. This can be useful if you
have a truth table in need of basic shortening. electruth can also be
used to compare boolean expressions, which can be very useful if you
need to compare a truth table with a schematic you created based on
that truth table. electruth can also be used to transform complex
boolean expressions into simpler ones consisting only of ANDS, ORS and
NOTS.


License
=======

electruth is free software under the terms of the GNU General Public
License version 3 (or any later version). The author of electruth is
Niels Serup, contactable at ns@metanohi.org. This is version 0.2.0 of
the program, the first version to support Python 3.1+ (if you need
support for Python 2.6+, you should download v0.1.1).

The libraries used by electruth are GPL-compatible.


Installation
============

Way #1
------
Just run this (requires that you have python-setuptools installed)::

  $ sudo easy_install3 electruth

Way #2
------
Get the newest version of electruth at
http://metanohi.org/projects/electruth/ or at
http://pypi.python.org/pypi/electruth

Extract the downloaded file and run this in a terminal::

  # python3 setup.py install

Dependencies
============

Python 3.1+ is a requirement.

``qvikconfig``
 + Web address: http://pypi.python.org/pypi/qvikconfig/
 + License: GPLv3+
 + Installing: ``$ sudo easy_install qvikconfig``
 + Author: Niels Serup

Note that ``qvikconfig`` is included with electruth, so you don't really
have to install it.

Optional extras
---------------
If present, electruth will also use these Python modules:

``termcolor``
 + Web address: http://pypi.python.org/pypi/termcolor/
 + License: GPLv3+
 + Installing: ``$ sudo easy_install termcolor``
 + Author: Konstantin Lepa <konstantin lepa at gmail com>

Note that ``termcolor`` is included with electruth, so you don't
really have to install it.
 
``setproctitle``
 + Web address: http://pypi.python.org/pypi/setproctitle/
 + License: New BSD License
 + Installing: ``$ sudo easy_install setproctitle``
 + Author: Daniele Varrazzo <daniele varrazzo at gmail com>


Use
===

Installing electruth installs a command-line utility named
``electruth``. This program has many settings, and it's recommended to
run ``electruth --help`` to get an overview of them.

The program creates boolean expressions from whatever input you give
it. If you give it more than one input, it will compare the two inputs
(unless if you tell it not to do that). Many inputs are supported:

* Basic boolean expressions (e.g. ``A and (B or C)`` or ``A * (B +
  C)`` (the same))
* Truthtables, using tab-separated (.tsv) or comma-separated (.csv)
  values in a file, the first row specifying the names of the inputs
  and outputs with a ``<`` prefix for inputs and a ``>`` prefix for
  outputs.
* Netlists (.net), e.g. those generated from ``gnetlist`` from the gEDA
  project (gEDA schematics from ``gschem`` can also be loaded, but
  they will be converted to netlists (saved in temporary files) at
  first).

Some settings can also be set in a config file. Config files use a
``property = value`` syntax (e.g. ``auto compare = false``) separated
by newlines.


To see the help for electruth, run::

  pydoc3 electruth

And especially::

  pydoc3 electruth.booleanexpression
  pydoc3 electruth.netlist
  pydoc3 electruth.truthtable


Development
===========

electruth is written in Python and uses Git for code management. To
get the latest branch, download it from gitorious.org like this::

  $ git clone git://gitorious.org/electruth/electruth.git


Logo
====

electruth's current logo has been put into the public domain.


This document
=============
Copyright (C) 2010, 2011  Niels Serup

Copying and distribution of this file, with or without modification,
are permitted in any medium without royalty provided the copyright
notice and this notice are preserved.  This file is offered as-is,
without any warranty.
