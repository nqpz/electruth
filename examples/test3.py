#!/usr/bin/env python3
"""
This example shows how to load and use schematics and netlists (works
only with gEDA).
"""
import os.path

# Import electruth submodule needed for this example
import electruth.netlist as nl

_filedir = os.path.dirname(os.path.realpath(__file__))

# Load sample schematic
netlist = nl.parse_geda_netlist_from_schematic(os.path.join(
        _filedir, 'simple_schematic.sch'))

print('Netlist loaded: {}'.format(netlist))
ends = netlist.get_end_nets()
print('Ends found: {}'.format(end.name for end in ends))
for end in ends:
    print('Found {}: {}'.format(end.name, netlist.get_logic_path(end)))

# Load the same schematic, but this time convert all paths to boolean
# expressions immediately and also transform the expressions into
# simpler ones using truth tables (this will sometimes result in OR
# operators with only one member; ignore that)
netlist_exprs = nl.parse_geda_netlist_from_schematic(os.path.join(
        _filedir, 'simple_schematic.sch'), True)

for name, expr in sorted(netlist_exprs.items()):
    print('Refound {}: {}'.format(name, expr))
