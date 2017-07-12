'''
Copyright (C) 2017 Scaleway. All rights reserved.
Use of this source code is governed by a MIT-style
license that can be found in the LICENSE file.
'''

import re
from .tooling import yaml_params, listize, CommandBuilder


def mysql_run(host, params):
    user = params.get('user', None)
    db_user = params.get('db_user', 'root')
    db = params.get('db', None)
    query = params.get('query', '')
    mysql_bin = params.get('mysql_bin', 'mysql')
    expect_regex = params.get('expect_regex', None)
    skip_column_names = params.get('skip_column_names', True)

    cmd = CommandBuilder(mysql_bin, sudo=user)
    cmd.append(['-u', db_user])
    cmd.append(['-e', query])

    if skip_column_names:
        cmd.append('-N')

    if db is not None:
        cmd.append(db)

    res = host.check_output(*cmd.build())

    if isinstance(expect_regex, str):
        assert re.match(expect_regex, res)


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
    >>       expect_regex: '^42\\t3$'
    """
    for par in listize(params):
        mysql_run(host, par)
