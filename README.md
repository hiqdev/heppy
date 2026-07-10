# hEPPy

**EPP client and library in Python**

[![GitHub version](https://badge.fury.io/gh/hiqdev%2Fheppy.svg)](https://badge.fury.io/gh/hiqdev%2Fheppy)
[![Scrutinizer Code Coverage](https://img.shields.io/scrutinizer/coverage/g/hiqdev/heppy.svg)](https://scrutinizer-ci.com/g/hiqdev/heppy/)
[![Scrutinizer Code Quality](https://img.shields.io/scrutinizer/g/hiqdev/heppy.svg)](https://scrutinizer-ci.com/g/hiqdev/heppy/)

[EPP](https://en.wikipedia.org/wiki/Extensible_Provisioning_Protocol) is Extensible Provisioning Protocol used for registrar-registry communication to register and manage domains.

This package provides:

- library for building and parsing EPP requests and responses
- EPP client implemented as a UNIX daemon, RabbitMQ-based (`bin/heppyd` + `bin/heppyc`), with alternate Unix-socket variants (`bin/eppyd`/`bin/eppyc`, `bin/reppyd`/`bin/reppyc`) for setups without a message queue
- whole infrastructure for implementing domain name registrar

In production use since 2016.

## Requirements

- **Python**: developed on 3.6, actively maintained through 3.14 (see `#57 python-3.14-migration`). Two spots in the code branch on the interpreter version to bridge that whole range:
  - `bin/heppyd`/`bin/heppyc` reconfigure `stdout` to be line-buffered via `TextIOWrapper.reconfigure()` (3.7+) with a manual `io.TextIOWrapper` fallback for 3.6.
  - `heppy/EPP.py` uses `ssl.wrap_socket()` where available and falls back to `ssl.create_default_context().wrap_socket()` on 3.12+, where `wrap_socket()` was removed.
- **Unix-like OS only** — relies on `fcntl` (`heppy/Config.py`), Unix signals `SIGHUP`/`SIGUSR1`/`SIGUSR2` (`heppy/SignalHandler.py`), and, for the socket-based daemons, Unix domain sockets (`local.address`). Not expected to run on Windows.
- **Third-party packages** — not declared in `setup.py` (no `install_requires`), so install them yourself:
  - [`pika`](https://pypi.org/project/pika/) — required by the RabbitMQ-based `bin/heppyd`/`bin/heppyc`.
  - [`sentry-sdk`](https://pypi.org/project/sentry-sdk/) — imported unconditionally at the top of `bin/heppyd`/`bin/heppyc` even if you don't set `sentry_dsn` in the config (it's only *initialized* then, but the import itself is not optional).

  ```sh
  pip install pika sentry-sdk
  ```

## Configuration

### etc/verisign/epp.json

```json
{
    "name":         "verisign.epp",
    "keepaliveInterval": {
        "minutes":  5
    },
    "forcequitInterval": {
        "hours":    23
    },
    "epp": {
        "host":         "epp.verisign-grs.com",
        "port":         700,
        "login":        "LOGIN",
        "password":     "PASSWORD",
        "certfile":     "ssl/my.cert",
        "keyfile":      "ssl/my.key",
        "ca_certs":     "ssl/my.intermediate"
    },
    "RabbitMQ": {
        "host":         "localhost"
    },
    "zones" : [
        ".com",
        ".net"
    ]
}
```

`name` is required — it's used to derive the RabbitMQ queue name (`heppy-<name>`, override with an explicit `RabbitMQ.queue`) and the systemd service name. `certfile`/`keyfile`/`ca_certs` are resolved relative to the directory of the config file itself.

`keepaliveInterval` (default shown above — 5 minutes) controls how often an `epp:hello` keepalive is sent to the registry when idle. `forcequitInterval` (default shown above — 23 hours) controls how often the daemon gracefully logs out, disconnects, and exits — under `systemd` (`Restart=always`) it immediately reconnects with a fresh session. Both accept any [`timedelta`](https://docs.python.org/3/library/datetime.html#datetime.timedelta) keyword arguments, e.g. `{"minutes": 30}` or `{"seconds": 45}`.

For the Unix-socket daemons (`eppyd`/`reppyd`) instead of `RabbitMQ`, provide a `local` block:

```json
"local": {
    "address": "/tmp/epp/epp.verisign-grs.com:01"
}
```

## Usage

Start EPP client daemon:

```sh
./bin/heppyd etc/verisign/epp.json start
```

Configure and start EPP client daemon with systemd:

```sh
./bin/heppyd etc/verisign/epp.json systemd up
```

Stop / check the systemd unit:

```sh
./bin/heppyd etc/verisign/epp.json systemd down
./bin/heppyd etc/verisign/epp.json systemd status
```

See [docs/systemd.md](docs/systemd.md) for the generated unit files.

Check domain availability:

```sh
./bin/heppyc etc/verisign/epp.json domain:check -names.0=example.com
```

Register domain:

```sh
./bin/heppyc etc/verisign/epp.json domain:create '-name=xn----0tbbnc0a.com' -pw=23_sA:d34 -period=1 -extensions.1=idnLang:tag -idnLang.tag=RUS -extensions.0=namestoreExt:subProduct -namestoreExt.subProduct=COM
```

More extension examples (fee, namestoreExt, secDNS) in [docs/examples.md](docs/examples.md).

## Tests

```sh
python -m pytest tests/
```

## PHP client

[hiqdev/hiapi-heppy](https://github.com/hiqdev/hiapi-heppy) is a companion Yii2/hiAPI plugin that talks to a running `heppyd` over the same RabbitMQ RPC protocol `heppy/RabbitMQ.py` implements: it publishes a JSON-encoded request to the daemon's queue with `reply_to`/`correlation_id` set, and blocks on its own exclusive callback queue for the matching reply (`src/RabbitMQClient.php`). It requires PHP ≥8.1 and `php-amqplib/php-amqplib`, and needs the target queue name (`heppy-<name>`, or the config's explicit `RabbitMQ.queue`) configured as `hiapi.heppy.rabbitmq.queue`.

## License

This project is released under the terms of the BSD-3-Clause [license](LICENSE).
Read more [here](http://choosealicense.com/licenses/bsd-3-clause).

Copyright © 2015-2017, HiQDev (http://hiqdev.com/)
