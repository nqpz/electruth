#!/usr/bin/env python3

# electruth: a collection of boolean logic tools
# Copyright (C) 2010, 2011  Niels Serup

# This file is part of electruth.
#
# electruth is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# electruth is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with electruth.  If not, see <http://www.gnu.org/licenses/>.

# This file is based on "settingsparser.py" from the shadowloss
# project, <http://metanohi.org/projects/shadowloss/>, released under
# the GNU General Public License, version 3 or any later version.

##[ Name        ]## electruth.settingsparser
##[ Maintainer  ]## Niels Serup <ns@metanohi.org>
##[ Description ]## Eases parsing settings from both the
                  # command-line and from config files

import os
import electruth.various as various
try:
    from qvikconfig import parse as config_parse
except ImportError:
    from electruth.external.qvikconfig import parse as config_parse

basic_config_translations = {}

class SettingsParser(object):
    def is_nil(self, prop):
        return not prop in dir(self) or self.__dict__[prop] is None

    def set_if_nil(self, prop, val):
        if self.is_nil(prop):
            self.__dict__[prop] = val

    def __init__(self, ok_config_translations={}, **etc):
        for key, val in basic_config_translations.items():
            ok_config_translations[key] = val
        ok_config_values = set(ok_config_translations.keys())

        for x in etc.items():
            self.__setattr__(*x)

        if not self.is_nil('config_file_path'):
            # Attempt to parse a config file
            try:
                conf = config_parse(self.config_file_path)
                ok_keys = set(conf) & ok_config_values

                for key in ok_keys:
                    o_key = key
                    if key in ok_config_values:
                        n_key = ok_config_translations[key]
                        if n_key is not None:
                            key = n_key
                        self.set_if_nil(key, conf[o_key])
            except IOError:
                pass
