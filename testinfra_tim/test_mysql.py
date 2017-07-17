'''
Copyright (C) 2017 Scaleway. All rights reserved.
Use of this source code is governed by a MIT-style
license that can be found in the LICENSE file.
'''

from .tooling import yaml_params, listize, CommandBuilder, re_match, params_warn


def mysql_run(host, params):
    user = params.pop('user', None)
    db_user = params.pop('db_user', 'root')
    db = params.pop('db', None)
    query = params.pop('query', '')
    mysql_bin = params.pop('mysql_bin', 'mysql')
    regex = params.pop('regex', None)
    skip_column_names = params.pop('skip_column_names', True)
    regex_policy = params.pop('regex_policy', 'all')

    cmd = CommandBuilder(mysql_bin, sudo=user)
    cmd.append(['-u', db_user])
    cmd.append(['-e', query])

    if skip_column_names:
        cmd.append('-N')

    if db is not None:
        cmd.append(db)

    res = host.check_output(*cmd.build())

    if isinstance(regex, str):
        assert re_match(regex, res, regex_policy)

    params_warn(params)


@yaml_params
def test_mysql(host, params):
    """
    Performs some requests on a mysql database using the
    mysql command line utility.

    Example:
    >> - mysql:
    >>     - db: test
    >>       db_user: test_db_user
    >>       user: www-data
    >>       query: SELECT 42, 3
    >>       regex: '^42\\t3$'
    >>       regex_policy: 'all'
    """
    for par in listize(params):
        mysql_run(host, par)
