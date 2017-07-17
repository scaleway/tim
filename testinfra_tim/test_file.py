'''
Copyright (C) 2017 Scaleway. All rights reserved.
Use of this source code is governed by a MIT-style
license that can be found in the LICENSE file.
'''

from .tooling import yaml_params, listize, re_match


def file_run(host, params):
    def check_type(f, type_name):
        return getattr(f, f'is_{type_name}')
    exists = params.get('exists', True)
    path = params.get('path', None)
    mode = params.get('mode', None)
    regex = params.get('regex', None)
    ftype = params.get('type', 'file').lower()
    regex_policy = params.get('regex_policy', 'any')
    empty = params.get('empty', False)
    user = params.get('user', None)
    group = params.get('group', None)

    if not isinstance(path, str):
        raise RuntimeError("incorrect file path")

    file = host.file(path)
    assert file.exists == exists

    if not exists:
        return

    assert user is None or file.user == user
    assert group is None or file.group == group
    assert check_type(file, ftype)
    assert ftype != 'file' or (file.size == 0) == empty
    assert mode is None or file.mode == mode
    if isinstance(regex, str):
        assert re_match(regex, file.content_string, regex_policy)


@yaml_params
def test_file(host, params):
    """
    Performs some tests on files.

    Example:
    >> - file:
    >>     - path: /etc/shadow
    >>       user: root
    >>       group: root
    >>       type: file
    >>       mode: 0640
    >>     - path: /etc/passwd
    >>       mode: 0644
    >>       regex: '^root:x:0:0:root:'
    >>       regex_policy: any
    >>     - path: /var/log/nginx/error.log
    >>       exists: False
    """
    for fileparams in listize(params):
        file_run(host, fileparams)
