#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Operator names
_operator_names = ('not', 'and', 'or', 'xor', 'nand', 'nor', 'xnor')

_inverted_operator_names = {
    'and': 'nand',
    'or': 'nor',
    'xor': 'xnor'
}

_infty = float('inf')
_operator_arg_limits = {
    'not': 1,
    'and': _infty,
    'or': _infty,
    'xor': 2,
    'nand': _infty,
    'nor': _infty,
    'xnor': 2
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

def is_object(obj):
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

class BooleanObject(object):
    def __init__(self, name):
        self.name = name

    def get_name(self):
        return self.name

    def __str__(self):
        return self.name

class BooleanOperator(object):
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

    def get_name(self):
        return _translated_operator_names[self.func]

    def express(self):
        """Return a string formatted in a human-friendly way"""
        return _recursive_express_loop(self)

    def __str__(self):
        return _recursive_show_loop(self)

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
                    obj = BooleanObject(x)
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

def parse_raw_expression(expr):
    """Convert a raw expression into an internal format."""
    for orig, new in _raw_aliases.iteritems():
        expr = expr.replace(orig, new)
    expr = expr.split()
    complete = _parse_raw_part(expr)
    return complete

def _simplify_xor(op):
    op.set_kind(OR)
    objs = []
    for i in range(2):
        objs.append(BooleanOperator(
                AND, op.objs[i], BooleanOperator(
                    NOT, op.objs[(i + 1) % 2])))
    op.objs = objs
    return op

def _simplify_and(op):
    op.objs = [_simplify_invert(x) for x in op.objs]
    op = _simplify_invert(op, OR)
    return op

def _simplify_invert(obj, new_kind=None):
    if new_kind is not None:
        obj.set_kind(new_kind)
    return BooleanOperator(NOT, obj)

def _simplify_part(op):
    objs = []
    for x in op.objs:
        if is_operator(x):
            objs.append(_simplify_part(x))
        else:
            objs.append(x)
    op.objs = objs

    if op.func == AND:
        op = _simplify_and(op)
    elif op.func == XOR:
        op = _simplify_xor(op)
    elif op.func == NAND:
        op.func = OR
        op.objs = [_simplify_invert(x) for x in op.objs]
    elif op.func == NOR:
        op = _simplify_invert(op, OR)
    elif op.func == XNOR:
        op = _simplify_invert(_simplify_xor(op))

    return op

def _unnot_part(op):
    objs = []
    for x in op.objs:
        if is_operator(x):
            objs.append(_unnot_part(x))
        else:
            objs.append(x)
    op.objs = objs

    if op.func == NOT:
        sub = op.objs[0]
        if is_operator(sub) and sub.func == NOT:
            op = sub.objs[0]

    return op

def simplify_expression(expr):
    """
    Convert all XORS, NANDS, NORS and XNORS into their simpler (and
    longer) equivalents, and convert all ANDS to combinations of NOTS
    and ORS.
    """
    if not is_operator(expr):
        return expr

    return _unnot_part(_simplify_part(expr))

def _ungroup_part(op):
    if not is_operator(op):
        return op

    objs = []
    if op.func == OR:
        for x in op.objs:
            if is_operator(x):
                ungrouped = _ungroup_part(x)
                if x.func == OR:
                    objs.extend(ungrouped.objs)
                else:
                    objs.append(ungrouped)
            else:
                objs.append(x)
    else:
        for x in op.objs:
            objs.append(_ungroup_part(x))
    op.objs = objs
    return op

def ungroup_expression(expr):
    """
    Open groups of expressions wherever possible.
    """
    if not is_operator(expr):
        return expr

    return _ungroup_part(expr)

def _match_two(a, b):
    if a == b or (is_object(a) and is_object(b) and a.name == b.name):
        return True
    elif is_operator(a) and is_operator(b) and a.func == b.func and \
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

def _shorten_part(op):
    objs = []
    for x in op.objs:
        if is_operator(x):
            objs.append(_shorten_part(x))
        else:
            objs.append(x)

            # Eh... Didn't go too well. Tried to apply this:
            # (A AND B AND C) OR (A AND D AND E) =
            # !(!A OR !(!B OR !C) OR !(!D OR !E))
    # def or_in_not(o):
    #     return is_operator(o) and o.func == NOT and \
    #         is_operator(o.objs[0]) \
    #         and o.objs[0].func == OR

#     if is_operator(op) and op.func == OR:
#         for x in objs:
#             if or_in_not(x):
# #                print x.objs[0]
#                 for xx in x.objs[0].objs:
#                     matches = 0
#                     for y in objs:
#                         if y != x and or_in_not(y):
# #                            print ' ', y.objs[0]
#                             for yy in y.objs[0].objs:
#                                 if _match_two(xx, yy):
#                                     print 2, xx, '|||', yy
#                                     matches += 1
#                                     #y.objs[0].objs.remove(yy)
#                     if matches > 0:
#                         x.objs[0].objs.remove(xx)
#                         objs.append(xx)


        # for a in objs:
        # if is_operator(a) and a.func == OR:
        #     for x in a.objs:
        #         if is_operator(x) and x.func == OR:
        #             print x
        #             for y in x.objs[0].objs:
        #                 for z in objs:
        #                     if or_in_not(z):
        #                         for u in z.objs[0].objs:
        #                             print y, u
        #                             if _match_two(y, u):
        #                                 print y, u
                        

    for x in reversed(objs):
        new_objs = [x]
        for y in objs:
            if not _match_two(x, y):
                new_objs.append(y)
        objs = new_objs

    op.objs = objs
    return _unnot_part(_unor_part(op))

def _unor_part(op):
    objs = []
    for x in op.objs:
        if is_operator(x):
            objs.append(_unor_part(x))
        else:
            objs.append(x)
    op.objs = objs

    if op.func == OR and len(op.objs) == 1:
        op = op.objs[0]
    return op

def shorten_expression(expr):
    """
    Shorten expression, i.e. remove parts that have the same function.
    """
    if not is_operator(expr):
        return expr

    return _shorten_part(expr)

def process_expression(expr, show=True):
    if show:
        def put(text):
            print text
    else:
        put = lambda text: None

    put('Original expression:\n%s\n' % expr)
    expr = parse_raw_expression(expr)
    put('Parsed expression:\n%s\n' % expr.express())
    expr = simplify_expression(expr)
    put('Simplified expression:\n%s\n' % expr.express())
    expr = ungroup_expression(expr)
    put('Expression with fewer subgroups:\n%s\n' % expr.express())
    expr = shorten_expression(expr)
    put('Expression with fewer redundancies:\n%s' % expr.express())
    return expr

# On direct execution:
if __name__ == '__main__':
    # Show a test
    import sys
    expr = ' '.join(sys.argv[1:])
    if not expr:
        expr = '(A and B) or (A and (C or !D))'

    process_expression(expr)
