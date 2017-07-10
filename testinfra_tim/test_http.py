'''
Copyright (C) 2017 Scaleway. All rights reserved.
Use of this source code is governed by a MIT-style
license that can be found in the LICENSE file.
'''

import re
from http.client import HTTPConnection
from .tooling import get_host_addr, yaml_params


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
    'method', 'url', 'status', 'encoding', 'check_encoding'
    and 'response_regex'.

    Example:
    >> http:
    >>   port: 8080
    >>   requests:
    >>     - {}
    >>     - method: GET
    >>       url: /test_not_found
    >>       status: 404

    """

    addr, port = get_host_addr(host), params.get('port', 80)
    conn = HTTPConnection(addr, port)
    for test in params.get('requests', ({},)):
        method, url = test.get('method', 'GET'), test.get('url',  '/')
        status = test.get('status', 200)

        conn.request(method, url)
        response = conn.getresponse()
        content = response.read()

        assert response.status == status

        check_encoding = test.get('check_encoding', True)
        response_regex = test.get('response_regex')

        if not check_encoding and response_regex:
            raise RuntimeError('Cannot check if the answer matches '
                               'a regex without decoding the content. '
                               'Please enable the encoding check in test:'
                               f'{test}')

        if check_encoding:
            decoded_content = content.decode(encoding=test.get('encoding', 'utf-8'))

        if response_regex:
            assert re.match(response_regex, decoded_content)