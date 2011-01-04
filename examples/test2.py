#!/usr/bin/env python
"""
This example shows how to load and use truth tables.
"""
import os.path

# Import electruth submodule needed for this example
import electruth.truthtable as tt

_filedir = os.path.dirname(os.path.realpath(__file__))

# Load sample truth table
truth_tables = tt.parse_raw_truthtable(os.path.join(
        _filedir, 'simple_truth_table.csv'), ',', False)
print truth_tables

# Get only truth table in sample file
truth_table = truth_tables['out']
print truth_table

# Convert to boolean expression
expr = truth_table.shorten()
print expr
