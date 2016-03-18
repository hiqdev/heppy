hiqdev/heppy commits history
----------------------------

## Under development

- Fixed `secDNS` extension
    - d91a4bd 2016-03-18 + secDNS domain info parsing (sol@hiqdev.com)
    - fc0f10a 2016-03-18 + `Response.find_text` (sol@hiqdev.com)
    - 6c90cde 2016-03-18 + `domain.render_auth_info` and hosts option in domain:info (sol@hiqdev.com)
    - 05284bb 2016-03-18 + `Doc.has` (sol@hiqdev.com)
- Fixed `login` command, added `extURIs` and `objURIs`
    - 699989b 2016-03-17 fixed stupid error (sol@hiqdev.com)
    - d00f4d6 2016-03-14 improved login: added extURI, objURI (sol@hiqdev.com)
    - f7eb934 2016-03-14 * Client: added lazy connect and auto reconnect (sol@hiqdev.com)
    - dc69850 2016-03-11 fixed `download_url` in setup.py (sol@hiqdev.com)

## 0.0.2 2016-03-11

- Changed: renamed to `heppy`
    - 12871b8 2016-03-11 renamed to heppy (sol@hiqdev.com)
    - fb64481 2016-03-11 renamed to heppy (sol@hiqdev.com)

## 0.0.1 2016-03-11

- Added PyPI packaging
    - bb25600 2016-03-11 rehideved (sol@hiqdev.com)
    - 89ff36e 2016-03-11 + setup.py, setup.cfg (sol@hiqdev.com)
- Added secDNS extension
    - 65582fe 2016-03-10 + secDNS:update (sol@hiqdev.com)
    - 872f46a 2016-03-10 improved secDNS (sol@hiqdev.com)
    - 5acfcab 2016-03-10 + Doc.mget (sol@hiqdev.com)
    - ffd65fa 2016-03-10 fixed epp:poll (sol@hiqdev.com)
    - 68a0279 2016-03-10 + secDNS:keyData (sol@hiqdev.com)
    - 09550d8 2016-03-10 improved Request.subfields to get value from other name (sol@hiqdev.com)
    - bc96776 2016-03-09 improved secDNS:create rendering (sol@hiqdev.com)
    - 83183a2 2016-03-09 improved hello parsing (sol@hiqdev.com)
    - 134eb23 2016-03-09 + secDNS extension module (sol@hiqdev.com)
- Added basics
    - 110c8ef 2016-03-09 reorganized modules into own dir (sol@hiqdev.com)
    - cc6b7e8 2016-03-08 cleaned away old junk, now everything in modules (sol@hiqdev.com)
    - 38a2641 2016-03-07 fixed typos (sol@hiqdev.com)
    - 7fd9709 2016-03-07 still improving (sol@hiqdev.com)
    - 63c4511 2016-03-07 another MAJOR upgrade rendering (sol@hiqdev.com)
    - cf0dc6c 2016-03-06 another MAJOR: reorganized parsing into modules (sol@hiqdev.com)
    - f6d83a3 2016-03-05 + rgp status in response (sol@hiqdev.com)
    - 7ce30dd 2016-03-05 + Namestore extension (sol@hiqdev.com)
    - 421ddb1 2016-03-05 used Request.prettifyxml (sol@hiqdev.com)
    - 22b56ee 2016-03-05 + initial DomainInfo and DomainDelete (sol@hiqdev.com)
    - 7e09225 2016-03-05 fixed import Request (sol@hiqdev.com)
    - d649ea4 2016-03-03 MAJOR step forward: Args, Config, Daemon, Request, Response (sol@hiqdev.com)
    - 7d8b36b 2016-02-29 changed reppyc to work with config file <- socket address (sol@hiqdev.com)
    - 2e7627e 2016-02-12 + Hello and DomainCreate (sol@hiqdev.com)
    - c0f7a0a 2016-02-12 + Error module (sol@hiqdev.com)
    - ff6134b 2016-02-12 better error output - Error: type\nmessage (sol@hiqdev.com)
    - 3d0e953 2016-02-12 + `Client.try_connect` (sol@hiqdev.com)
    - 35da144 2016-02-12 + proper Login error processing (sol@hiqdev.com)
    - 4890a7e 2016-02-12 + `start_time` to eppyd info (sol@hiqdev.com)
    - 4eaab99 2016-02-12 + `check_connection()` to check if socket is already busy (sol@hiqdev.com)
    - 593ad47 2016-02-09 rehideved (sol@hiqdev.com)
    - a9a78dd 2016-02-08 fixed hidev config (sol@hiqdev.com)
    - e7b55e6 2015-11-17 organized immports (sol@hiqdev.com)
    - 3d02756 2015-11-17 + gitignore (sol@hiqdev.com)
    - 68e6d31 2015-11-17 hideved (sol@hiqdev.com)
    - 5d83f10 2015-11-17 moved to bin (sol@hiqdev.com)
    - 713489f 2015-11-17 + readme for async (sol@hiqdev.com)
    - 27ac10c 2015-11-17 moved to src (sol@hiqdev.com)
    - cedbc65 2015-11-17 + reppyc (sol@hiqdev.com)
    - d29f6b1 2015-11-17 added basics (sol@hiqdev.com)
    - 741ee8d 2015-11-17 used Client module (sol@hiqdev.com)
    - e943570 2015-11-16 + Client, Request, Response modules (sol@hiqdev.com)
    - 63883bb 2015-10-29 + unlink socket descriptor file (sol@hiqdev.com)
    - cc1fc19 2015-10-28 redone local connections to UNIX sockets (sol@hiqdev.com)
    - 508c7fd 2015-10-28 + text xml (sol@hiqdev.com)
    - 4d221bb 2015-10-27 + async version (sol@hiqdev.com)
    - 6c8a39f 2015-10-27 redone back to non-async epp (sol@hiqdev.com)
    - b74c7f3 2015-10-27 fixed REPP `handle_read` (sol@hiqdev.com)
    - 7644c6b 2015-10-27 + read config from json file (sol@hiqdev.com)
    - f8bae00 2015-10-19 basically working (sol@hiqdev.com)
    - 486e78d 2015-10-19 NOT FINISHED but looks working (sol@hiqdev.com)
    - ee07c0a 2015-10-18 doing asyncronous epp (sol@hiqdev.com)
    - b7f2f9f 2015-10-17 lowered connect timeout and info command (sol@hiqdev.com)
    - ae39190 2015-10-17 working version with non-async epp (sol@hiqdev.com)
    - 0b62aee 2015-10-16 + asynchronous wait (sol@hiqdev.com)
    - d2ca75e 2015-10-16 + greeting to REPP (sol@hiqdev.com)
    - 70499d6 2015-10-16 first looking working (sol@hiqdev.com)
    - 6dfa31c 2015-10-12 renamed to eppy (sol@hiqdev.com)
    - ecb3788 2015-10-12 inited (sol@hiqdev.com)

## Development started 2015-10-12

