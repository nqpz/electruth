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

##[ Name        ]## electruth.booleanexpression
##[ Maintainer  ]## Niels Serup <ns@metanohi.org>
##[ Description ]## This is the core of electruth: the implementation
                  # of boolean logic

# Operator names
_operator_names = ('not', 'and', 'or', 'xor', 'nand', 'nor', 'xnor')

_inverted_operator_names = {
    'and': 'nand',
    'or': 'nor',
    'xor': 'xnor'
}

# Operator types
def NOT(obj):
    return not obj

def AND(*objs):
    r = objs[0]
    for x in objs[1:]:
        r &= x
    return r

def OR(*objs):
    r = objs[0]
    for x in objs[1:]:
        r |= x
    return r

def XOR(obj1, obj2):
    return obj1 ^ obj2

def NAND(*objs):
    return not AND(*objs)

def NOR(*objs):
    return not OR(*objs)

def XNOR(*objs):
    return not XOR(*objs)


def _both_as_keys(*lsts):
    dicts = []
    lsts_len = len(lsts)
    lsts_range = range(lsts_len)
    for x in lsts:
        dicts.append({})
    min_len = min([len(x) for x in lsts])
    for i in range(min_len):
        for x in lsts_range:
            dicts[x][lsts[x][i]] = lsts[(x + 1) % lsts_len][i]

    return dicts

_infty = float('inf')
_operator_arg_limits = {
    'not': 1,
    NOT: 1,
    'and': _infty,
    AND: _infty,
    'or': _infty,
    OR: _infty,
    'xor': 2,
    XOR: 2,
    'nand': _infty,
    NAND: _infty,
    'nor': _infty,
    NOR: _infty,
    'xnor': 2,
    XNOR: 2
}

_operator_types = (NOT, AND, OR, XOR, NAND,
                   NOR, XNOR)

_translated_operator_types, _translated_operator_names = \
    _both_as_keys(_operator_names, _operator_types)

_raw_aliases = {
    '(': ' ( ',
    ')': ' ) ',
    '!': ' not ',
    '*': ' and ',
    '.': ' and ',
    '·': ' and ',
    '+': ' or ',
    '&': ' and ',
    '|': ' or ',
    '&&': ' and ',
    '||': ' or ',
    '^': ' xor ',
    'nand': 'not and',
    'nor': 'not or',
    'xnor': 'not xor'
}

class BooleanExpressionError(Exception):
    pass

def is_operator(obj):
    return 'func' in obj.__dict__ and 'objs' in obj.__dict__

def is_multi_operator(obj):
    return is_operator(obj) and \
        _operator_arg_limits[obj.get_name()] == _infty

def is_variable(obj):
    return 'name' in obj.__dict__

def _recursive_show_loop(op):
    text = '%s(' % op.get_name()
    t_objs = []
    for x in op.objs:
        if is_operator(x):
            t_objs.append(_recursive_show_loop(x))
        else:
            t = x.name
            t_objs.append(t)
    text += ', '.join(t_objs)
    text += ')'
    return text

def _recursive_express_loop(op):
    if not is_operator(op):
        return op.name
    
    if op.func == NOT:
        return '!' + _recursive_express_loop(op.objs[0])
    text = '('
    t_objs = []
    for x in op.objs:
        t_objs.append(_recursive_express_loop(x))
    text += (' %s ' % op.get_name().upper()).join(t_objs)
    text += ')'
    return text

def _recursive_test_loop(op, **keyvals):
    objs = []
    for x in op.objs:
        if is_operator(x):
            objs.append(_recursive_test_loop(x, **keyvals))
        else:
            objs.append(keyvals[x.get_name()])
    return op.func(*objs)

class BooleanBaseObject(object):
    def is_operator(self):
        return False

class BooleanVariable(BooleanBaseObject):
    def __init__(self, name):
        self.name = name

    def get_name(self):
        return self.name

    def simplify(self):
        return self

    def __str__(self):
        return self.name

class BooleanOperator(BooleanBaseObject):
    def __init__(self, kind, *objs):
        self.set_kind(kind)
        self.objs = objs

    def set_kind(self, kind):
        if isinstance(kind, basestring):
            try:
                self.func = _translated_operator_types[kind]
            except KeyError:
                raise BooleanExpressionError(
                    'operator %s does not exist' % kind)
        else:
            self.func = kind

    def get_variables(self):
        return _get_all_variables(self)

    def get_name(self):
        return _translated_operator_names[self.func]

    def create_truthtable(self):
        import electruth.truthtable as truthtable
        return truthtable.create_from_expression(self)

    def test(self, **keyvals):
        return _recursive_test_loop(self, **keyvals)

    def ungroup(self):
        return _ungroup_expression(self)

    def simplify(self):
        """Simplifies the expression. Will sometimes shorten it as well"""
        return self.create_truthtable().shorten()

    def express(self):
        """Return a string formatted in a human-friendly way"""
        return _recursive_express_loop(self)

    def __str__(self):
        return _recursive_show_loop(self)

def parse_raw_expression(expr, always_return_op=False, simplify=False):
    """Convert a raw expression into an internal format."""
    for orig, new in _raw_aliases.iteritems():
        expr = expr.replace(orig, new)
    expr = expr.split()
    complete = _parse_raw_part(expr)
    if always_return_op and not complete.is_operator:
        complete = BooleanOperator(OR, complete)
    if simplify:
        complete = complete.simplify()
    return complete

def _get_all_variables(op):
    vs = []
    for x in op.objs:
        if is_variable(x):
            vs.append(x.get_name())
        else:
            vs.extend(_get_all_variables(x))
    return list(set(vs))
    
def _ungroup_expression(expr):
    # Ungroup objects in operators with only one object (not counting
    # NOT operators)
    objs = []
    if is_operator(expr):
        for x in expr.objs:
            if is_operator(x):
                if len(x.objs) == 1 and \
                        _operator_arg_limits[x.get_name()] == _infty:
                    objs.append(x.objs[0])
                else:
                    objs.append(_ungroup_expression(x))
            else:
                objs.append(x)
    expr.objs = objs
    return expr
    
def _parse_raw_part(expr, obj_history={}):
    levels = 0
    objs = []
    op = None
    invert_next = False
    invert_operator = False

    for i in range(len(expr)):
        x = expr[i]
        x_lowered = x.lower()
        if x == '(':
            if levels == 0:
                group_start = i + 1
            levels += 1
        elif x == ')':
            levels -= 1
            if levels == 0:
                o = _parse_raw_part(expr[group_start:i], obj_history)
                if invert_next:
                    o = BooleanOperator(NOT, o)
                    invert_next = False
                objs.append(o)
        elif levels == 0:
            if x_lowered == 'not':
                invert_next = not invert_next
            elif x_lowered in _operator_names:
                if x != op or len(objs) == _operator_arg_limits[op]:
                    if op is not None:
                        if len(objs) == 1:
                            if invert_operator:
                                objs[0] = BooleanOperator(NOT, objs[0])
                        else:
                            if invert_operator:
                                op = _inverted_operator_names[op]
                                invert_operator = False
                            objs = [BooleanOperator(op, *objs)]
                    op = x
                    if invert_next:
                        invert_operator = True
                        invert_next = False
            else:
                if x in obj_history.keys():
                    obj = obj_history[x]
                    if op is not None and obj in objs and \
                            _operator_arg_limits[op] == _infty:
                        # Expressions like 'A and A' might as well be
                        # shortened to 'A' at once, but expressions
                        # requiring a specific number of arguments,
                        # such as 'A xor A', should not be altered at
                        # this point, as these different expressions
                        # require separate actions.
                        continue
                else:
                    obj = BooleanVariable(x)
                    obj_history[x] = obj
                if invert_next:
                    obj = BooleanOperator(NOT, obj)
                objs.append(obj)
                if invert_next:
                    invert_next = False

    if op is None:
        if len(objs) > 1:
            raise BooleanExpressionError('expression lacks an operator')
        return objs[0]
    else:
        if len(objs) == 1:
            if invert_operator:
                objs[0] = BooleanOperator(NOT, objs[0])
            return objs[0]
        else:
            if invert_operator:
                op = _inverted_operator_names[op]
            return BooleanOperator(op, *objs)

