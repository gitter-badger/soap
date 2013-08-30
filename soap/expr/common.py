"""
.. module:: soap.expr.common
    :synopsis: Common definitions for expressions.
"""
ADD_OP = '+'
SUBTRACT_OP = '-'
UNARY_SUBTRACT_OP = '-'
MULTIPLY_OP = '*'
DIVIDE_OP = '/'

EQUAL_OP = '=='
GREATER_OP = '>'
LESS_OP = '<'
UNARY_NEGATION_OP = '~'
AND_OP = '&'
OR_OP = '|'

BARRIER_OP = '#'

OPERATORS = [ADD_OP, MULTIPLY_OP]
BOOLEAN_OPERATORS = [
    EQUAL_OP, GREATER_OP, LESS_OP, UNARY_NEGATION_OP, AND_OP, OR_OP
]
ARITHMETIC_OPERATORS = [
    ADD_OP, SUBTRACT_OP, UNARY_SUBTRACT_OP, MULTIPLY_OP, DIVIDE_OP
]
UNARY_OPERATORS = [UNARY_SUBTRACT_OP, UNARY_NEGATION_OP]

ASSOCIATIVITY_OPERATORS = [ADD_OP, MULTIPLY_OP]

COMMUTATIVITY_OPERATORS = ASSOCIATIVITY_OPERATORS

COMMUTATIVE_DISTRIBUTIVITY_OPERATOR_PAIRS = [(MULTIPLY_OP, ADD_OP)]
# left-distributive: a * (b + c) == a * b + a * c
LEFT_DISTRIBUTIVITY_OPERATOR_PAIRS = \
    COMMUTATIVE_DISTRIBUTIVITY_OPERATOR_PAIRS
# Note that division '/' is only right-distributive over +
RIGHT_DISTRIBUTIVITY_OPERATOR_PAIRS = \
    COMMUTATIVE_DISTRIBUTIVITY_OPERATOR_PAIRS

LEFT_DISTRIBUTIVITY_OPERATORS, LEFT_DISTRIBUTION_OVER_OPERATORS = \
    list(zip(*LEFT_DISTRIBUTIVITY_OPERATOR_PAIRS))
RIGHT_DISTRIBUTIVITY_OPERATORS, RIGHT_DISTRIBUTION_OVER_OPERATORS = \
    list(zip(*RIGHT_DISTRIBUTIVITY_OPERATOR_PAIRS))


def is_expr(e):
    return is_arith_expr(e) or is_bool_expr(e)


def is_arith_expr(e):
    """Check if `e` is an expression."""
    if is_bool_expr(e):
        return False
    from soap.expr.arith import Expr
    return isinstance(e, Expr)


def is_bool_expr(e):
    """Check if `e` is a boolean expression."""
    from soap.expr.bool import BoolExpr
    return isinstance(e, BoolExpr)


def concat_multi_expr(*expr_args):
    """Concatenates multiple expressions into a single expression by using the
    barrier operator.
    """
    from soap.expr.arith import Expr
    me = None
    for e in expr_args:
        e = Expr(e)
        me = me | e if me else e
    return me


def split_multi_expr(e):
    """Splits the single expression into multiple expressions."""
    if e.op != BARRIER_OP:
        return [e]
    return split_multi_expr(e.a1) + split_multi_expr(e.a2)