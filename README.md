hEPPy
=====

**EPP client and library in Python**

[![GitHub version](https://badge.fury.io/gh/hiqdev%2Fheppy.svg)](https://badge.fury.io/gh/hiqdev%2Fheppy)
[![Scrutinizer Code Coverage](https://img.shields.io/scrutinizer/coverage/g/hiqdev/heppy.svg)](https://scrutinizer-ci.com/g/hiqdev/heppy/)
[![Scrutinizer Code Quality](https://img.shields.io/scrutinizer/g/hiqdev/heppy.svg)](https://scrutinizer-ci.com/g/hiqdev/heppy/)

[EPP](https://en.wikipedia.org/wiki/Extensible_Provisioning_Protocol) is Extensible Provisioning Protocol used for registrar-registry communication to register and manage domains.

This package provides:

- library for building and parsing EPP requests and responses
- EPP client implemented as a UNIX daemon
- whole infrastructure for implementing domain name registrar

For the moment it is in early stage of development.

## Configuration

## `etc/epp.verisign-grs.com.json`

```json
{
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
        "queue":        "epp.verisign-grs.com",
        "host":         "localhost"
    },
    "local": {
        "address":      "/tmp/epp/epp.verisign-grs.com:NN"
    },
    "zones" : [
        ".com",
        ".net"
    ]
}
```

## Usage

Start EPP client:

```sh
./bin/heppyd epp.verisign-grs.com start
```

Register domain:

```sh
./bin/heppyc epp.verisign-grs.com domain:create '-name=xn----0tbbnc0a.com' -pw=23_sA:d34 -period=1 -extensions.1=idnLang:tag -idnLang.tag=RUS -extensions.0=namestoreExt:subProduct -namestoreExt.subProduct=COM
```

## License

This project is released under the terms of the BSD-3-Clause [license](LICENSE).
Read more [here](http://choosealicense.com/licenses/bsd-3-clause).

Copyright © 2015-2016, HiQDev (http://hiqdev.com/)
