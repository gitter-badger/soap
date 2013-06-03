import itertools
import gmpy2

import ce.logger as logger
from ce.common import ignored
from ce.precision.common import PRECISIONS


def precision_context(prec):
    try:
        prec += 1
    except TypeError:
        raise TypeError('Precision must be an integer, found %s.' % prec)
    return gmpy2.local_context(gmpy2.ieee(128), precision=prec)


def set_precision_recursive(expr, prec):
    from ce.expr import BARRIER_OP
    if expr.op != BARRIER_OP:
        expr.prec = prec
    for a in expr.args:
        with ignored(ValueError, AttributeError):
            set_precision_recursive(a, prec)


def precision_permutations(expr, prec_list=PRECISIONS):
    from ce.expr import Expr, BARRIER_OP
    try:
        with logger.local_context(l=logger.levels.off):
            p1, p2 = [precision_permutations(a, prec_list) for a in expr.args]
        if expr.op == BARRIER_OP:
            prec_list = [None]
        elif not expr.prec is None:
            prec_list = [expr.prec]
        s = set()
        n = len(p1) * len(p2) * len(prec_list)
        i = 0
        for a1, a2 in itertools.product(p1, p2):
            for p in prec_list:
                i += 1
                if i % 100 == 0:
                    logger.persistent('Permutation', '%d/%d' % (i, n),
                                      l=logger.levels.debug)
                s.add(Expr(expr.op, a1, a2, prec=p))
        logger.unpersistent('Permutation')
        return s
    except AttributeError:
        return {expr}


def precision_variations(expr, prec_list=PRECISIONS):
    from ce.expr import Expr
    s = set()
    for p in prec_list:
        s |= precision_permutations(expr, prec_list=[p])
    return s
