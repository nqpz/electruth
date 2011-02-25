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

##[ Name        ]## electruth.truthtable
##[ Maintainer  ]## Niels Serup <ns@metanohi.org>
##[ Description ]## Controls truth tables

import math
import electruth.booleanexpression as boolexpr

def decimal_to_binary(dec, min_size=None):
    if dec == 0:
        string = '0'
    else:
        string = ''.join(str((dec >> bin) & 1) for
                         bin in range(dec.bit_length() - 1, -1, -1))
    if min_size is not None:
        string = '0' * (min_size - len(string)) + string
    return string

class Truthtable(object):
    """A truthtable with only one output"""
    def __init__(self, names, rows):
        self.names = names
        self.rows = rows

    def shorten(self):
        return _shorten_truthtable(self).ungroup()

def parse_raw_truthtable(path, delimiter='\t', shorten=True):
    outputs = []
    input_numbers = []
    output_numbers = []
    input_names = []
    output_names = []

    f = open(path, 'r')

    i = 0
    for name in f.readline().strip().split(delimiter):
        tmp = ''
        if name.startswith('<'):
            input_names.append(name[1:])
            input_numbers.append(i)
        elif name.startswith('>'):
            output_names.append(name[1:])
            output_numbers.append(i)
            outputs.append([])
        i += 1
    for line in f:
        data = [int(x) for x in line.strip().split(delimiter)]

        c = 0
        for i in output_numbers:
            if data[i]:
                t = []
                for j in input_numbers:
                    t.append((j, data[j]))
                outputs[c].append(t)
            c += 1
    f.close()
    
    final = {}
    for i in range(len(outputs)):
        t = []
        for x in outputs[i]:
            tt = []
            t.append(tt)
            for y in x:
                tt.append(None)
            for y in x:
                tt[y[0]] = bool(y[1])
        if shorten:
            final[output_names[i]] = Truthtable(input_names, t).shorten()
        else:
            final[output_names[i]] = Truthtable(input_names, t)
    return final

def create_from_expression(expr):
    input_names = expr.get_variables()
    inlen = len(input_names)
    rows = []
    for i in range(2 ** inlen):
        test_list = [bool(int(x)) for x in
                     list(decimal_to_binary(i, inlen))]
        test_dict = {}
        for i in range(inlen):
            test_dict[input_names[i]] = test_list[i]

        if expr.test(**test_dict):
            rows.append(test_list)
    return Truthtable(input_names, rows)


def _shorten_truthtable(table):
    reqs = table.rows
    while True:
        nreqs = _shorten(reqs)
        ok = False
        if len(nreqs) == len(reqs):
            ok = True
            for i in range(len(reqs)):
                for j in range(len(reqs[i])):
                    if nreqs[i][j] != reqs[i][j]:
                        ok = False
                        break
                if not ok:
                    break
        reqs = nreqs
        if ok:
            # It cannot be shortened any further
            break

    inputs = []
    for x in table.names:
        inputs.append(boolexpr.BooleanVariable(x))

    or_objs = []
    for x in reqs:
        and_objs = []
        for i in range(len(x)):
            if x[i] is True:
                and_objs.append(inputs[i])
            elif x[i] is False:
                and_objs.append(boolexpr.BooleanOperator(
                        boolexpr.NOT, inputs[i]))
        or_objs.append(boolexpr.BooleanOperator(boolexpr.AND, *and_objs))
    expr = boolexpr.BooleanOperator(boolexpr.OR, *or_objs)
    return expr

def _shorten(reqs):
    nreqs = []
    i = 0
    for x in reqs:
        i += 1
        close_matches = 0
        for y in reqs[i:]:
            found = None
            nones = []
            for j in range(len(x)):
                if y[j] is not x[j]:
                    if found is None:
                        found = True
                        place = j
                    else:
                        found = False
                        break
            if found is True:
                temp = y[:]
                temp[place] = None
                nreqs.append(temp)
                close_matches += 1
        if close_matches == 0:
            nreqs.append(x)

    nnreqs = []
    for x in nreqs:
        if x not in nnreqs and (True in x or False in x):
            nnreqs.append(x)
    nreqs = nnreqs
    nnreqs = []
    ignore = []
    for x in nreqs:
        if x in ignore:
            continue
        ignore.append(x)
        for y in nreqs:
            if y in ignore:
                continue
            is_duplicate = True
            for j in range(len(x)):
                if x[j] is not None and x[j] != y[j]:
                    is_duplicate = False
                    break
            if is_duplicate:
                ignore.append(y)
        nnreqs.append(x)
    
    return nnreqs

