#!/usr/bin/env python
# -*- coding: utf-8 -*-

# electruth: a collection of boolean logic tools
# Copyright (C) 2010  Niels Serup

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

##[ Name        ]## electruth.netlist
##[ Maintainer  ]## Niels Serup <ns@metanohi.org>
##[ Description ]## Controls netlists

import tempfile
import os.path
import electruth.booleanexpression as boolexpr
from electruth.booleanexpression import AND, OR, NOT, XOR, NAND, NOR, XNOR
import electruth.various as various

#####################################################################

# Type of logic gate with number of inputs; may contain erroneous
# information. It is probably best to use the basic devices (7408 for
# AND, 7432 for OR, 7404 for NOT, 7486 for XOR, 7400 for NAND, 7402
# for NOR, and 74266 for XNOR).
_gates_information = {
    '7408': (AND, 2),
    '7409': (AND, 2),
    '74130': (AND, 2),
    '74131': (AND, 2),
    '7411': (AND, 3),
    '7415': (AND, 3),
    '7421': (AND, 4),

    '7432': (OR, 2),
    '744075': (OR, 3),

    '7404': (NOT, 1),
    '7405': (NOT, 1),
    '7406': (NOT, 1),
    '7414': (NOT, 1),
    '7416': (NOT, 1),
    '7419': (NOT, 1),

    '7486': (XOR, 2),
    '74136': (XOR, 2),
    '74386': (XOR, 2),

    '7400': (NAND, 2),
    '7401': (NAND, 2),
    '7403': (NAND, 2),
    '7424': (NAND, 2),
    '7426': (NAND, 2),
    '7410': (NAND, 3),
    '7412': (NAND, 3),
    '7413': (NAND, 4),
    '7418': (NAND, 4),
    '7420': (NAND, 4),
    '7422': (NAND, 4),
    '7430': (NAND, 8),
    '74134': (NAND, 12),
    '74133': (NAND, 13),

    '7402': (NOR, 2),
    '7428': (NOR, 2),
    '7433': (NOR, 2),
    '7436': (NOR, 2),
    '74128': (NOR, 2),
    '7427': (NOR, 3),
    '7423': (NOR, 4),
    '7425': (NOR, 4),
    '74232': (NOR, 4),
    '744002': (NOR, 4),
    '74260': (NOR, 5),

    '74266': (XNOR, 2),
    '747266': (XNOR, 2)
}

#####################################################################

# Notes on structuring the data: A netlist consists of one single
# collection of nets. Nets --- or "wires" --- link the gates
# together. A net can be linked to several inputs, but it will never
# be linked to more than one output. Nets that are not linked to any
# output will be considered starting points of the net.

# This may be easier to understand with a little graphical example:

#        ,_____           ,------------ Net with 1 output (7408)
# [...]__|     \          v             and 2 inputs (7432 and 7404)
# [...]__| 7408 |-------------,    ___
#        |_____/              |   |   \__
# ,___________________________|   |      \
# |     ,______               '---| 7404  >----[...]
# |_____\      \                  |    __/
# ,_____ | 7432 |----[...]        |___/
# |     /______/
# |___________________________,
#        ,_____               |
# [...]__|     \              | <------ Net with 1 output (7408)
# [...]__| 7408 |-------------'         and 1 input (7432)
#        |_____/

#####################################################################

class Gate(object):
    def __init__(self, name, device):
        try:
            func, inputs_num = _gates_information[device]
        except KeyError:
            raise Exception('logic gate %s is not recognized (is it \
even a logic gate?)' % device)
        self.name = name
        self.func = func
        self.input_numbers = range(1, inputs_num + 1)
        self.pins = [] # GatePin objects will append themselves to
                       # this list

    def get_input_nets(self):
        nets = []
        for x in self.pins:
            if x.is_input:
                nets.append(x.parent)
        return nets

    def get_output_net(self):
        for x in self.pins:
            if x.is_output:
                return x

class GatePin(object):
    def __init__(self, gate, pinnum):
        self.gate = gate
        self.pin = pinnum
        self.is_input = self.pin in self.gate.input_numbers
        self.is_output = not self.is_input
        self.gate.pins.append(self)
        self.parent = None # Will be set when put on a net

class Net(object):
    def __init__(self, name, *links):
        self.is_end_net = name.startswith('>')
        if self.is_end_net:
            name = name[1:]
        self.name = name
        for x in links:
            x.parent = self
        self.links = links
        self.parent = None # Will be set when put in a collection

    def get_output(self):
        for x in self.links:
            if x.is_output:
                return x.gate
        # Else
        return None

    def get_logic_path(self):
        return self.parent.get_logic_path(self)

class NetCollection(object):
    def __init__(self, *nets):
        for x in nets:
            x.parent = self
        self.nets = nets

    def get_end_nets(self, prefix='>'):
        nets = []
        for x in self.nets:
            if x.is_end_net:
                nets.append(x)
        return nets

    def get_logic_path(self, net, used_gates=[]):
        used_gates = used_gates[:]
        output_gate = net.get_output()
        if output_gate in used_gates:
            net_names_lst = [repr(x.parent.name) for x in
                             output_gate.pins]
            if len(net_names_lst) == 1:
                net_names = net_names_lst[0]
            else:
                net_names = ', '.join(net_names_lst[:-1]) + ' and ' + net_names_lst[-1]
            raise Exception('gate %s on nets %s cannot be used more than once' %
                            (output_gate.name, net_names))
        used_gates.append(output_gate)
        if output_gate is None:
            return boolexpr.BooleanVariable(net.name)

        # Else (if the net is not a starting net)
        input_nets = output_gate.get_input_nets()
        objs = []
        for x in input_nets:
            objs.append(self.get_logic_path(x, used_gates))
        op = boolexpr.BooleanOperator(output_gate.func, *objs)
        return op

#####################################################################

def parse_geda_netlist(path, return_end_nets_exprs=False):
    gates = {}
    nets = []
    pins = []
    
    in_group = None
    for line in open(path, 'r'):
        line = line.strip()
        if not line: continue
        data = line.split(' ')
        if data[0] == 'START':
            in_group = data[1]
        elif data[0] == 'END':
            in_group = None
        elif in_group == 'components':
            gates[data[0]] = Gate(data[0], data[1].split('=')[1])
        elif in_group == 'nets':
            data = [x.strip() for x in line.split(':')]
            if data[0] not in ('Vcc', 'GND'):
                net_links = [x.strip().split(' ')
                             for x in data[1].split(',')]
                for i in range(len(net_links)):
                    x = net_links[i]
                    pin_inf = gates[x[0]], int(x[1])
                    ok = False
                    for y in pins:
                        if y[0] == pin_inf[0] and y[1] == pin_inf[1]:
                            pin = y[2]
                            ok = True
                            break
                    if not ok:
                        pin = GatePin(*pin_inf)
                        pins.append((pin_inf[0], pin_inf[1], pin))
                    net_links[i] = pin
                nets.append(Net(data[0], *net_links))

    coll = NetCollection(*nets)
    if return_end_nets_exprs:
        exprs = {}
        for x in coll.get_end_nets():
            exprs[x.name] = x.get_logic_path().simplify()
        return exprs
    else:
        return coll

def parse_geda_netlist_from_schematic(path, return_end_nets_exprs=False):
    filename = os.path.join(tempfile.gettempdir(), 'output.net')
    if not various.exec_program('gnetlist', '-g', 'geda', '-o',
                               filename, path) == 0:
        raise Exception('gnetlist does not work')
    return parse_geda_netlist(filename, return_end_nets_exprs)

# On direct execution:
if __name__ == '__main__':
    # Show a test
    import sys
    if len(sys.argv) == 1:
        print 'No path was given.'
    else:
        collection = parse_geda_netlist(sys.argv[1])
        end_nets = collection.get_end_nets()
        for x in end_nets:
            print x.name, '=', x.get_logic_path().express()
            
