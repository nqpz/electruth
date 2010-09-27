#!/usr/bin/env python
# -*- coding: utf-8 -*-

import booleanexpression

def parse_truthtable(path):
    outputs = []
    input_numbers = []
    output_numbers = []
    input_names = []
    output_names = []

    f = open(path, 'r')

    i = 0
    for name in f.readline().strip().split('\t'):
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
        data = [int(x) for x in line.strip().split('\t')]

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
        t = ''
        for x in outputs[i]:
            t += '('
            for y in x:
                if not y[1]:
                    t += '!'
                t += input_names[y[0]] + '&'
            t = t[:-1]
            t += ')|'
        t = t[:-1]
        final[output_names[i]] = t
    return final

# On direct execution:
if __name__ == '__main__':
    import sys
    if len(sys.argv) == 1:
        sys.exit()

    exprs = parse_truthtable(sys.argv[1])
    for name, expr in exprs.iteritems():
        print name
        booleanexpression.process_expression(expr)
        print
        print

