'''
Copyright (C) 2017 Scaleway. All rights reserved.
Use of this source code is governed by a MIT-style
license that can be found in the LICENSE file.
'''

from .tooling import yaml_params


@yaml_params
def test_system_state(host, params):
    """
    Tests the system state exported by systemd.

    Example:
    >> - system_state: running

    """

    possible_states = (
        'initializing',
        'starting',
        'running',
        'degraded',
        'maintenance',
        'stopping',
        'offline',
        'unknown'
    )

    if not params in possible_states:
        raise RuntimeError(f'expected system state should be a string among'
                           f' {possible_states.join(", ")}. got ({params})')

    res = host.run('systemctl is-system-running')
    assert not res.stderr
    assert res.stdout.strip() == params # params is the expected state
