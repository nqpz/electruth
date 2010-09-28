#!/usr/bin/env python
# -*- coding: utf-8 -*-

import booleanexpression as boolexpr
from booleanexpression import AND, OR, NOT, XOR, NAND, NOR, XNOR

#####################################################################

# Type of logic gate with number of inputs; may contain erroneous
# information. It is probably best to use the basic devices (7408 for
# AND, 7432 for OR, 7404 for NOT, 7486 for XOR, 7400 for NAND, 7402
# for NOR, and 74266 for XNOR).
_gates_information = {
    '7408': (AND, 2)
    '7409': (AND, 2)
    '74130': (AND, 2)
    '74131': (AND, 2)
    '7411': (AND, 3)
    '7415': (AND, 3)
    '7421': (AND, 4)

    '7432': (OR, 2)
    '744075': (OR, 3)

    '7404': (NOT, 1)
    '7405': (NOT, 1)
    '7406': (NOT, 1)
    '7414': (NOT, 1)
    '7416': (NOT, 1)
    '7419': (NOT, 1)

    '7486': (XOR, 2)
    '74136': (XOR, 2)
    '74386': (XOR, 2)

    '7400': (NAND, 2)
    '7401': (NAND, 2)
    '7403': (NAND, 2)
    '7424': (NAND, 2)
    '7426': (NAND, 2)
    '7410': (NAND, 3)
    '7412': (NAND, 3)
    '7413': (NAND, 4)
    '7418': (NAND, 4)
    '7420': (NAND, 4)
    '7422': (NAND, 4)
    '7430': (NAND, 8)
    '74134': (NAND, 12)
    '74133': (NAND, 13)

    '7402': (NOR, 2)
    '7428': (NOR, 2)
    '7433': (NOR, 2)
    '7436': (NOR, 2)
    '74128': (NOR, 2)
    '7427': (NOR, 3)
    '7423': (NOR, 4)
    '7425': (NOR, 4)
    '74232': (NOR, 4)
    '744002': (NOR, 4)
    '74260': (NOR, 5)

    '74266': (XNOR, 2)
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

class Gate(object)

class Net(object)

class NetCollection(object)

#####################################################################

def parse_netlist(path):
    objs = []

             
# On direct execution:
if __name__ == '__main__':
    # Show a test
    import sys
    if len(sys.argv) == 1:
        print 'No path was given.'
    else:
        print parse_netlist(sys.argv[1])
