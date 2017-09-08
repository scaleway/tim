# TestInfra yaMl

TIM is a plugin for [testinfra](https://github.com/philpep/testinfra) parametrizing tests as described by a yaml file.

# Setup

TIM depends on python 3.3, testinfra and pytest.
```sh
pip3 install git+git://github.com/scaleway/tim.git
```

# Usage

```sh
yamltest --timdir tests/ root@banana root@duck
```

```
$ yamltest -h
usage: yamltest [-h] [--tim_verbose] [--timdir TIMDIR] [--pytestdir PYTESTDIR]
                [--pytestarg PYTESTARG]
                hosts [hosts ...]

Run TIM on test directories

positional arguments:
  hosts                 hosts to run tests on

optional arguments:
  -h, --help            show this help message and exit
  --tim_verbose         print pytest's args
  --timdir TIMDIR       adds a new TIM test dir
  --pytestdir PYTESTDIR
                        add dir to pytest search path
  --pytestarg PYTESTARG
                        args to be passed to pytest
```

`--timdir tests` registers all yaml tests matching `tests/*.test.yml`, all pytest tests in `tests/pytest/`, and all executable programs in `tests/simple/`:
```
├── scaleway-wordpress.test.yml
├── pytest
│   └── test_example.py
└── simple
    └── test.sh
```


When `--raw` is passed as the first argument, if forwards the next arguments directly to pytest. It also adds the path to the tim tests at the end of the argument list.

```sh
yamltest --raw --yamltest tests/example.test.yml \
	 --simpletests tests/simple/ \
	 --hosts root@banana,root@duck \
	 tests/pytest/
```

# Yaml test files

## Structure

Yaml test files must have a dictionnary or a list of dictionnaries as a root. Each key is the name of a test function in the test library, and each value its corresponding parameters.

Here is an example:


```yaml
http: [80, 8080]
ssh: 22
file:
 - path: /etc/configfile
   perm: O644
   owner: root:root
```

This test file would call these test functions:

```
test_http([80, 8080])
test_ssh(22)
test_file([{'path': '/etc/configfile',
            'perm': O644,
            'owner': 'root:root'}])
```

## Yaml test modules

There are several modules you can call using the yaml interface. They are documented inside the `testinfra_tim/` folder.

# Simple tests

Simple tests run on the controller rather than on the tested host, but should still be able to connect to it using the environment variable-provided connection parameters.
These settings currenty only are available when connecting over ssh.

```ini
REMOTE_METHOD=paramiko # can also be ssh
REMOTE_HOST=testedhost
REMOTE_USER=root
```

`REMOTE_METHOD` holds the name of the testinfra module being used to connect to the host.

# Writting pytest tests

These just are regular testinfra tests. Please refer to the documentation of [testinfra](https://testinfra.readthedocs.io/) and [pytest](https://docs.pytest.org/) for further information.

# Licensing

© 2017 Scaleway - [MIT License](https://github.com/scaleway/tim/blob/master/LICENSE).
A project by [![Scaleway](https://avatars1.githubusercontent.com/u/5185491?v=3&s=42)](https://www.scaleway.com/)
