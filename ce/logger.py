#!/usr/bin/env python
# vim: set fileencoding=UTF-8 :


import sys


class levels():
    pass
levels = levels()


labels = ['debug', 'info', 'warning', 'error', 'off']
for i, l in enumerate(labels):
    levels.__dict__[l] = i


context = {
    'level': levels.off,
    'file': None,
    'persistent': {},
}


def set_context(**kwargs):
    context.update(kwargs)


def get_context():
    return context


def log(*args, l=levels.info):
    if l >= get_context()['level']:
        f = context['file'] or sys.stdout
        print(*args, end='', file=f)


def line(*args, l=levels.info):
    args += ('\n', )
    log(*args, l=l)


def rewrite(*args, l=levels.info):
    log('\r', *args, l=l)


def persistent(name, *args, l=levels.info):
    get_context()['persistent'][name] = args + (l, )
    _persistent()


def unpersistent(*args):
    p = get_context()['persistent']
    for n in args:
        if not n in p:
            continue
        del p[n]


def _persistent():
    log('\r')
    for k, v in get_context()['persistent'].items():
        *v, l = v
        v += ('.', )
        log(' ', k, *v, l=l)


def log_level(l):
    def wrapper(f):
        def wrapped(*args, l=l):
            f(*args, l=l)
        return wrapped
    return wrapper


def log_enable(l):
    def wrapper(f):
        def wrapped(*args, **kwargs):
            if l < get_context()['level']:
                return
            return f(*args, **kwargs)
        return wrapped
    return wrapper


labels = ['debug', 'info', 'warning', 'error', 'off']
for i, l in enumerate(labels):
    globals()[l] = log_level(i)(line)
    globals()[l + '_enable'] = log_enable(i)


if __name__ == '__main__':
    info('Hello')
    debug('Hello')
    import time
    debug_enable(time.sleep)(100)