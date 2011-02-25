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

##[ Name        ]## electruth.booleanexpression
##[ Maintainer  ]## Niels Serup <ns@metanohi.org>
##[ Description ]## This is the core of electruth: the implementation
                  # of boolean logic

# Operator names
_operator_names = ('not', 'and', 'or', 'xor', 'nand', 'nor', 'xnor')

_inverted_operator_names = {
    'and': 'nand',
    'or':  'nor',
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
    'xnor': 'not xor',
    '⊕': 'xor',
    '∨': ' or ',
    '∧': ' and ',
    '¬': ' not '
}

class BooleanExpressionError(Exception):
    pass


def _recursive_show_loop(op):
    text = '{}('.format(op.get_name())
    t_objs = []
    for x in op.objs:
        if x.is_operator:
            t_objs.append(_recursive_show_loop(x))
        else:
            t = x.name
            t_objs.append(t)
    text += ', '.join(t_objs)
    text += ')'
    return text

def _match_two(a, b):
    if a == b or (a.is_variable and b.is_variable and a.name == b.name):
        return True
    elif a.is_operator and b.is_operator and a.func == b.func and \
            len(a.objs) == len(b.objs):
        used = []
        for i in range(len(a.objs)):
            ok = False
            for j in range(len(a.objs)):
                if j not in used and _match_two(a.objs[i], b.objs[j]):
                    used.append(j)
                    ok = True
                    break
            if not ok:
                return False
        return True
    else:
        return False

def _recursive_express_loop(op, and_symbol, or_symbol, not_symbol, xor_symbol):
    if not op.is_operator:
        return op.name
    
    if op.func == NOT:
        rec = _recursive_express_loop(
            op.objs[0], and_symbol, or_symbol, not_symbol, xor_symbol)
        return (not_symbol or '!{}').format(rec)
    text = '('
    t_objs = []
    for x in op.objs:
        t_objs.append(_recursive_express_loop(
            x, and_symbol, or_symbol,
            not_symbol, xor_symbol))
    opname = op.func == AND and and_symbol or op.func == OR and \
        or_symbol or op.func == XOR and xor_symbol or \
        op.get_name().upper()
    text += (' {} '.format(opname)).join(t_objs)
    text += ')'
    return text

def _recursive_test_loop(op, **keyvals):
    objs = []
    for x in op.objs:
        if x.is_operator:
            objs.append(_recursive_test_loop(x, **keyvals))
        else:
            objs.append(keyvals[x.get_name()])
    return op.func(*objs)

class BooleanBaseObject:
    is_operator=False
    is_variable=False

    def get_name(self):
        return self.name

    def express(self, typ=None):
        return str(self)

    def simplify(self):
        return self

class BooleanVariable(BooleanBaseObject):
    is_variable=True

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name

class BooleanOperator(BooleanBaseObject):
    is_operator=True

    def __init__(self, kind, *objs):
        self.set_kind(kind)
        self.objs = objs

    def set_kind(self, kind):
        if isinstance(kind, str):
            try:
                self.func = _translated_operator_types[kind]
            except KeyError:
                raise BooleanExpressionError(
                    'operator {} does not exist'.format(kind))
        else:
            self.func = kind

    def get_variables(self):
        return _get_all_variables(self)

    def is_multi_operator(self):
        return _operator_arg_limits[obj.get_name()] == _infty

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

    def match(self, other):
        return _match_two(self, other)
    
    def express(self, typ='basic'):
        """Return a string formatted in a human-friendly way"""
        if typ == 'internal':
            return str(self)
        else:
            if typ == 'math':
                _and = '∧'
                _or = '∨'
                _not = '¬{}'
                _xor = '⊕'
            elif typ == 'bool':
                _and = '·'
                _or = '+'
                _not = '{}´'
                _xor = '⊕'
            elif typ == 'latex-bool':
                _and = '\cdot'
                _or = '+'
                _not = '\overline{{{}}}'
                _xor = '\oplus'
            else:
                _and = None
                _or = None
                _not = None
                _xor = None
            return _recursive_express_loop(
                self, _and, _or, _not, _xor)

    def __str__(self):
        return _recursive_show_loop(self)

def parse_raw_expression(expr, always_return_op=False, simplify=False):
    """Convert a raw expression into an internal format."""
    for orig, new in _raw_aliases.items():
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
        if x.is_variable:
            vs.append(x.get_name())
        else:
            vs.extend(_get_all_variables(x))
    return list(set(vs))
    
def _ungroup_expression(expr):
    # Ungroup objects in operators with only one object (not counting
    # NOT operators)
    objs = []
    if expr.is_operator:
        for x in expr.objs:
            if x.is_operator:
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

