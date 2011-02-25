#!/usr/bin/env python
# -*- coding: utf-8 -*-

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

##[ Name        ]## electruth.utility
##[ Maintainer  ]## Niels Serup <ns@metanohi.org>
##[ Description ]## Controls the actions of the command-line utility

import os
from electruth.settingsparser import SettingsParser
import electruth.various as various
import electruth.generalinformation as ginfo
import electruth.booleanexpression as boolexpr
import electruth.truthtable as truthtable
import electruth.netlist as netlist

_available_types = (
    ('Boolean expression', 'expr', 'none (given directly)'),
    ('Truthtable (tab-separated)', 'tsv', '.tsv'),
    ('Truthtable (comma-separated)', 'csv', '.csv'),
    ('Schematic (from gschem, using \'gnetlist -g geda\')',
     'sch', '.sch'),
    ('Netlist (only output from \'gnetlist -g geda\' is \
supported)', 'net', '.net')
)

_config_file_translations = {
    'verbose': 'term_verbose',
    'color errors': 'term_color_errors',
    'auto compare': 'auto_compare',
    'express': 'express_type'
}

class Utility(SettingsParser):
    def __init__(self, **options):
        SettingsParser.__init__(self, _config_file_translations,
                                **options)
        # Get values, or set them to default ones
        self.set_if_nil('error_function', various._usable_error)
        self.set_if_nil('term_verbose', True)
        self.set_if_nil('term_color_errors', True)
        self.set_if_nil('auto_compare', True)
        self.set_if_nil('express_type', 'basic')

        self.do_compare = len(self.inputs) > 1 and self.auto_compare

        self.exprs = []

    def error(self, msg, done=None):
        if self.term_verbose:
            self.error_function(msg, done, color=self.term_color_errors)

    def status(self, msg):
        print ginfo.program_name + ': ' + msg

    def add_expression(self, o_name, expr):
        if self.do_compare:
            name = o_name + '_0'
            names = [x[0] for x in self.exprs]
            i = 0
            while name in names:
                i += 1
                name = o_name + '_%d' % i
        else:
            name = o_name
        self.exprs.append((name, o_name, expr))

    def add_expressions(self, **exprs):
        for key, val in exprs.iteritems():
            self.add_expression(key, val)

    def start(self):
        self.load_inputs()
        self.exprs.sort()
        self.print_exprs()

    def load_inputs(self):
        # inputs are in the form [type, path/expression]
        for x in self.inputs:
            typ = x[0]
            data = x[1]

            if typ == 'tsv':
                self.add_expressions(**truthtable.parse_raw_truthtable(data, '\t'))
            elif typ == 'csv':
                self.add_expressions(**truthtable.parse_raw_truthtable(data, ','))
            elif typ == 'net':
                self.add_expressions(
                    **netlist.parse_geda_netlist(data, True))
            elif typ == 'sch':
                self.add_expressions(
                    **netlist.parse_geda_netlist_from_schematic(data, True))
            else:
                if '=' in data:
                    spl = data.split('=')
                    data = spl[1]
                    name = spl[0]
                else:
                    name = 'unnamed-expression'
                self.add_expression(
                    name, boolexpr.parse_raw_expression(data, False, True))

    def print_exprs(self):
        if not self.exprs:
            print 'No expressions given'
            return

        prevs = []
        def maybe_compare():
            if len(prevs) > 1:
                i = 1
                for x in prevs[:-1]:
                    for y in prevs[i:]:
                        print ' \'-', x[0], 'matches', y[0] + '?', x[2].match(y[2])
                    i += 1
                print

        prev = self.exprs[0]
        for x in self.exprs:
            if x[1] == prev[1]:
                prevs.append(x)
            else:
                maybe_compare()
                prevs = [x]

            print x[0] + ' =', x[2].express(self.express_type)
            prev = x
        maybe_compare()

    def end(self):
        pass

