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

##[ Name        ]## electruth.various
##[ Maintainer  ]## Niels Serup <ns@metanohi.org>
##[ Description ]## Various minor (but still important) parts
##[ Start date  ]## 2010 September 13

import sys
import subprocess
import textwrap
import electruth.generalinformation as ginfo
try:
    from termcolor import colored
except ImportError:
    from electruth.external.termcolor import colored

def error(msg, done=None, pre=None, **kwds):
    errstr = str(msg) + '\n'
    if pre is not None:
        errstr = pre + ': ' + errstr
    if kwds.get('color'):
        errstr = colored(errstr, 'red')
    sys.stderr.write(errstr)
    if done is not None:
        if done in (True, False):
            sys.exit(1)
        else:
            sys.exit(done)

def _usable_error(msg, done=None, **kwds):
    error(msg, done, ginfo.program_name + ': ', **kwds)

def print_text_table(*rows, **kwds):
    header = kwds.get('header')
    line_width = kwds.get('width') or 70
    rows = list(rows)
    if header is not None:
        rows.insert(0, header)
    try:
        colnum = len(rows[0])
    except IndexError:
        raise IndexError('no rows given')

    colwidth_gen = line_width / colnum - 3
    line_width = (colwidth_gen + 3) * 3 - 3

    width = []
    total = 0
    for i in range(colnum):
        top = 0
        for x in rows:
            l = len(x[i])
            if l > top:
                top = l
        total += top
        width.append(top)
    if total > line_width:
        ratio = float(colnum * colwidth_gen) / sum(width)
        nwidth = []
        for x in width:
            nwidth.append(int(ratio * x))
        width = nwidth

    for x in rows:
        _print_table_row(x, width)
        if header:
            print('=' * line_width)
            header = None
        else:
            print('-' * line_width)

def exec_program(*args):
    return subprocess.call(tuple(map(str, args)),
                           stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE)

def _print_table_row(data, width=20):
    if not isinstance(width, list) or isinstance(width, tuple):
        nwidth = []
        for x in data[0]:
            nwidth.append(width)
        width = nwidth

    with_whitespace = lambda t, i: t + (width[i] - len(t)) * ' ' + \
        (i != len(data) - 1 and ' |' or '')
    extra_data = []
    i = 0
    for x in data:
        if len(x) <= width[i]:
            print(with_whitespace(x, i), end='')
            extra_data.append(None)
        else:
            wrap = textwrap.wrap(x, width[i])
            print(with_whitespace(wrap[0], i), end='')
            extra_data.append(wrap[1:])
        i += 1
    print()

    ok = False
    for x in extra_data:
        if x:
            ok = True
    if not ok:
        return
    while ok:
        ok = False
        i = 0
        for x in extra_data:
            if x:
                print(with_whitespace(x[0], i), end='')
                x.pop(0)
                if x:
                    ok = True
            else:
                print(with_whitespace('', i), end='')
            i += 1
        if not ok:
            print()
