'''
Copyright (C) 2017 Scaleway. All rights reserved.
Use of this source code is governed by a MIT-style
license that can be found in the LICENSE file.
'''

import os
from os.path import join
from subprocess import Popen
from .tooling import get_host_attr

DEFAULT_HOST_PARAMS = ('NAME', 'host', 'user', 'port')
DEFAULT_PARAMS_MAP = {
    'user': 'remote_user',
    'host': 'remote_host',
    'NAME': 'remote_method',
    'port': 'remote_port'
}

def get_params(host, attrs=DEFAULT_HOST_PARAMS, tr_map=DEFAULT_PARAMS_MAP):
    '''
    This function returns a dictionnary containing some infos about the target host.
    It fails if the host backend does not provide requested informations.
    '''
    def translate(entry):
        return tr_map.get(entry) or entry

    return dict(filter(lambda pair: bool(pair[1]),
                       map(lambda a: (translate(a).upper(),
                                      get_host_attr(host, a)),
                           attrs)))

def test_simple(host, simple_tests):
    """
    Ensures all tests in the simple test folder run without an error.
    """
    for root, _, fnames in os.walk(simple_tests):
        simple_env = os.environ.copy()
        simple_env.update(get_params(host))
        for test in filter(lambda f: os.access(f, os.X_OK),
                           (join(root, fname) for fname in fnames)):
            with Popen([test], env=simple_env) as test_proc:
                # reference test in the assert in order to
                # get the file name in case of faillure
                assert test and not test_proc.wait()
