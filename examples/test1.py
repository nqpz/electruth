#!/usr/bin/env python3
"""
This example shows how to create expressions and how to convert back
and forth between truth tables and expressions.
"""

# Import electruth submodules needed for this example
import electruth.booleanexpression as b
import electruth.truthtable as tt

# Create boolean expressions in different ways
expr1 = b.BooleanOperator('and', b.BooleanVariable('A'),
                          b.BooleanVariable('B'))
expr2 = b.parse_raw_expression('C xor A')
expr3 = b.BooleanOperator('or', expr1, expr2)
print(expr1, 'or', expr2, '=', expr3, '\n')

# Express the expressions
expr_types = ('basic', 'internal', 'math', 'bool', 'latex-bool')

print('Expressing {}:'.format(expr3))
for typ in expr_types:
    print('{:>10}:  {}'.format(typ, expr3.express(typ)))

tt_expr = tt.create_from_expression(expr3).shorten()
print('\nExpressing {}:'.format(tt_expr))
for typ in expr_types:
    print('{:>10}:  {}'.format(typ, tt_expr.express(typ)))
