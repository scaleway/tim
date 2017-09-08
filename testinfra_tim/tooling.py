'''
Copyright (C) 2017 Scaleway. All rights reserved.
Use of this source code is governed by a MIT-style
license that can be found in the LICENSE file.
'''

import re
import warnings
from enum import Enum
from functools import reduce
import yaml


_XGET_ANCHOR = object()
def custom_xget(subject):
    def xget(dic, attr):
        ret = dic.get(attr, _XGET_ANCHOR)
        if ret is _XGET_ANCHOR:
            raise RuntimeError(
                '{} has no attribute `{}`'.format(subject, attr))
        return ret
    return xget

xget = custom_xget('dictionnary')

def get_host_attr(host, prop):
    """
    Tries to fetch an attribute for a testinfra host.
    It might fail and raise a RuntimeError depending on
    the backend and requested attribute.
    """
    try:
        return getattr(host.backend, prop)
    except AttributeError as ex:
        raise RuntimeError(
            ('The backend for {} does not have the requested '
             'attribute: {}').format(host, ex))


def get_host_addr(host):
    """ Returns the hostname of a testinfra host """
    return get_host_attr(host, 'host')


def yaml_get_dict(path):
    """ Reads a python dictionnary from a yaml file. """
    with open(path, 'r') as yml_file:
        return yaml.load(yml_file)


def listdict(ldish):
    """
    Yields a sequence of tuples from a dictionnary
    or a nested list of dictionnaries.
    """
    if isinstance(ldish, (list, tuple)):
        for elem in ldish:
            yield from listdict(elem)
    elif isinstance(ldish, dict):
        yield from ldish.items()
    else:
        raise RuntimeError(
            'Expected a dict or a nested list of dicts, got {}'.format(
                type(ldish)))


def listize(elem):
    if isinstance(elem, (list, tuple)):
        return elem
    return [elem]


def yaml_params(func):
    """
    Marks a test to be parametrized using
    the yaml configuration file.
    """
    func.yaml_params = True
    return func


def map_sum(f, vals):
    """ Takes a function and a list and computes f(l[0]) + f(l[1]) + ... """
    return reduce(lambda a, b: a + b, map(f, vals))


class CommandBuilder():
    """
    Helper to build testinfra commands.

    """
    def __init__(self, *args, sudo=None):
        self.args = list(args)
        if sudo:
            self.args = ['sudo', '-u', sudo, '--'] + self.args

    def append(self, arg):
        self.args += listize(arg)
        return self

    def build(self):
        return [' '.join('%s' for _ in range(len(self.args)))] + self.args


class _NonDescWrapper():
    """
    The python enum module ignores descriptors.
    This wrapper isn't a descriptor, and enable a
    callable descriptor object to be used as an enum value.
    """
    def __init__(self, function):
        self.function = function

    def __call__(self, *args, **kwargs):
        return self.function(*args, **kwargs)


class MatchPolicy(Enum):
    @classmethod
    def from_string(cls, s):
        return cls[s.upper()]

    @classmethod
    def cast(cls, e):
        if isinstance(e, cls):
            return e
        elif isinstance(e, str):
            return cls.from_string(e)
        elif isinstance(e, type(None)):
            return cls.from_string('NONE')
        raise RuntimeError(
            'Cannot cast type `{}` to {}'.format(
                type(e), cls.__name__))


    ANY = any
    ALL = all
    NONE = _NonDescWrapper(lambda it: not any(it))


def re_match(regex, lines, regex_policy=MatchPolicy.ANY):
    if not callable(regex_policy):
        regex_policy = MatchPolicy.cast(regex_policy)
    if isinstance(lines, str):
        lines = lines.splitlines()
    comp_regex = re.compile(regex)
    return regex_policy.value(re.match(comp_regex, line) for line in lines)


def params_warn(pars):
    if pars:
        warnings.warn('unused yaml attributes: {}'.format(
            ', '.join(pars)))
