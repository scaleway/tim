'''
Copyright (C) 2017 Scaleway. All rights reserved.
Use of this source code is governed by a MIT-style
license that can be found in the LICENSE file.
'''

from functools import reduce
from .tooling import yaml_params, listize, map_sum


def _get_services(params, running=True, enabled=True):
    """
    This generator yields services names and
    expected states from an input tree.
    """
    if isinstance(params, str):
        yield (params, running, enabled)
    elif isinstance(params, (list, tuple)):
        for subparam in params:
            yield from _get_services(subparam)
    elif isinstance(params, dict):
        running = params.get('running', running)
        enabled = params.get('enabled', enabled)
        get_name_attr = lambda name: listize(params.get(name, []))
        for subparam in map_sum(get_name_attr, ('name', 'names',)):
            yield from _get_services(subparam, running, enabled)
    else:
        raise RuntimeError('service test takes a dict, list'
                           ' or string as parameter')


@yaml_params
def test_service(host, params):
    """
    Test the status of one or more services.
    By default, services are required to be
    enabled and running.

    It is meant to be very flexible and should
    accept any reasonable input.

    It even features inheritance :)

    You can use nested lists and dictionnaries
    to list service names. The tested state of
    the service is running and enabled by default.
    This behavior can be changed using the
    'running' and 'enabled' attributes of
    dictionnarires. Child services are read
    from the name and names keys.

    Example:
    >> - service:
    >>     names:
    >>       - running_enabled
    >>       - running_enabled
    >>     running: true
    >>     enabled: true
    >>
    >> - service:
    >>     - running_enabled
    >>     - running_enabled
    >>
    >> - service: running_enabled
    >>
    >> - service:
    >>     - names:
    >>         - stopped_disabled
    >>         - name: running_disabled
    >>           running: true
    >>       running: false
    >>       enabled: false
    >>     - running_enabled

    """

    for name, running, enabled in _get_services(params):
        service = host.service(name)
        assert name and service.is_running == running
        assert name and service.is_enabled == enabled
