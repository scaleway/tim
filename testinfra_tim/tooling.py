'''
Copyright (C) 2017 Scaleway. All rights reserved.
Use of this source code is governed by a MIT-style
license that can be found in the LICENSE file.
'''

import yaml


_XGET_ANCHOR = object()
def custom_xget(subject):
    def xget(dic, attr):
        ret = dic.get(attr, _XGET_ANCHOR)
        if ret is _XGET_ANCHOR:
            raise RuntimeError(f'{subject} has no attribute `{attr}`')
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
        raise RuntimeError(f'The backend for {host} does not have'
                           f' the requested attribute: {ex}')


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
        raise RuntimeError(f'Expected a dict or a nested list'
                           f' of dicts, got {type(ldish)}')


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
