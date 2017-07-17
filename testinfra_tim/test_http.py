'''
Copyright (C) 2017 Scaleway. All rights reserved.
Use of this source code is governed by a MIT-style
license that can be found in the LICENSE file.
'''

from http.client import HTTPConnection
from .tooling import get_host_addr, yaml_params, re_match, params_warn


@yaml_params
def test_http(host, params):
    """
    Performs some test on an http server
    using a single HTTP connection.

    You can specify an optionnal 'port' parameter as well
    as an optionnal list of http 'requests' to perform.
    The default port is 80 and the requests list defaults
    to a single request using default parameters.

    By defaults, requests use the GET method on /,
    and expect answer code 200 as well as a response
    encoded using utf-8 and matching regex '.*'.
    You can override this behavior using parameters
    'method', 'url', 'status', 'encoding', 'check_encoding',
    'regex' and 'regex_policy'.

    Example:
    >> http:
    >>   port: 8080
    >>   requests:
    >>     - {}
    >>     - method: GET
    >>       url: /test_not_found
    >>       status: 404

    """

    addr, port = get_host_addr(host), params.pop('port', 80)
    conn = HTTPConnection(addr, port)
    for test in params.pop('requests', ({},)):
        method, url = test.pop('method', 'GET'), test.pop('url', '/')
        status = test.pop('status', 200)

        conn.request(method, url)
        response = conn.getresponse()
        content = response.read()

        assert response.status == status

        check_encoding = test.pop('check_encoding', True)
        regex = test.pop('regex', None)

        if not check_encoding and regex:
            raise RuntimeError('Cannot check if the answer matches '
                               'a regex without decoding the content. '
                               'Please enable the encoding check in test:'
                               f'{test}')

        if check_encoding:
            decoded_content = content.decode(encoding=test.pop('encoding', 'utf-8'))

        if regex:
            assert re_match(regex, decoded_content, test.pop('regex_policy', 'any'))

        params_warn(params)
