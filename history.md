hiqdev/heppy
------------

## [Under development]

- Added more documentation and examples
    - [4560e80] 2016-10-15 + usage examples [sol@hiqdev.com]
    - [9a8d427] 2016-09-05 fixed Usage manual [sol@hiqdev.com]
    - [a5f58a6] 2016-09-06 added sample config [sol@hiqdev.com]
    - [26f9b2c] 2016-09-05 + Usage readme section [sol@hiqdev.com]
- Added autoreconnect if EPP session died
    - [bf2fba6] 2016-09-09 added `Daemon.smart_request` with auto restart if logged out [sol@hiqdev.com]
- Added path finding to `Config`
    - [ce47da1] 2016-10-15 csfixed [sol@hiqdev.com]
    - [e64b3e8] 2016-10-15 added path property to Config [sol@hiqdev.com]
    - [1328fcb] 2016-10-15 used Config class [sol@hiqdev.com]
    - [c63ac63] 2016-09-09 + find ssl files [sol@hiqdev.com]
    - [f22fd94] 2016-09-07 improved Config: + find path to config files [sol@hiqdev.com]
    - [3c6c3f4] 2016-09-26 fixed Args to split `=` properly [sol@hiqdev.com]
    - [2cfde17] 2016-09-09 improved Config.find added extension finding [sol@hiqdev.com]
    - [24b8f95] 2016-09-08 ignore heppy.egg-info [sol@hiqdev.com]
    - [17a065f] 2016-09-08 trying php instead of python in travis [sol@hiqdev.com]
- Added signal handling
    - [f97e797] 2016-09-08 + signal handling to Daemon [sol@hiqdev.com]
    - [60ccaaf] 2016-09-08 used python -u for unbuffered output [sol@hiqdev.com]
    - [ce81052] 2016-09-07 used SignalHandler [sol@hiqdev.com]
    - [d4067df] 2016-09-07 used deepcopy to keep sys.argv unchanged [sol@hiqdev.com]
    - [d7717e4] 2016-09-07 improved SignalHandler to handle multiple signals to different callbacks [sol@hiqdev.com]
    - [66ee295] 2016-09-06 + SignalHandler [sol@hiqdev.com]
- Added `systemd` config example
    - [8d9777c] 2016-09-08 + User and Group [sol@hiqdev.com]
    - [879323f] 2016-09-07 + systemd config example [sol@hiqdev.com]
- Added `RabbitMQ` based version
    - [1c0f485] 2016-09-06 adding RabbitMQ [sol@hiqdev.com]
    - [c2bdbac] 2016-09-06 + testServer [sol@hiqdev.com]
    - [d49e9f0] 2016-09-06 + `get_greeting()` [sol@hiqdev.com]
    - [e16d03d] 2016-09-06 * Daemon: implemented two types of clients [sol@hiqdev.com]
    - [1f364a7] 2016-09-06 splitted out Login class [sol@hiqdev.com]
    - [b34b71d] 2016-09-05 splitted out EPP class [sol@hiqdev.com]
    - [9bd74f7] 2016-09-05 redone extension params passed as arrays [sol@hiqdev.com]
    - [0aed840] 2016-09-05 renamed heppyc/d <- reppyc/d [sol@hiqdev.com]
- Added `idnLang` extension
    - [5fa56c3] 2016-09-05 renamed param idnLang:tag <- `idnLang_tag` [sol@hiqdev.com]
    - [d926653] 2016-09-05 added idnLang extension [sol@hiqdev.com]
    - [3bad9e9] 2016-08-23 + render contact:create [sol@hiqdev.com]
    - [7268e1f] 2016-08-23 + render fee:create [sol@hiqdev.com]
    - [18d750e] 2016-03-21 + host/contact check & info commands [sol@hiqdev.com]
- Fixed `secDNS` extension
    - [d91a4bd] 2016-03-18 + secDNS domain info parsing [sol@hiqdev.com]
    - [fc0f10a] 2016-03-18 + `Response.find_text` [sol@hiqdev.com]
    - [6c90cde] 2016-03-18 + `domain.render_auth_info` and hosts option in domain:info [sol@hiqdev.com]
    - [05284bb] 2016-03-18 + `Doc.has` [sol@hiqdev.com]
- Fixed `login` command, added `extURIs` and `objURIs`
    - [699989b] 2016-03-17 fixed stupid error [sol@hiqdev.com]
    - [d00f4d6] 2016-03-14 improved login: added extURI, objURI [sol@hiqdev.com]
    - [f7eb934] 2016-03-14 * Client: added lazy connect and auto reconnect [sol@hiqdev.com]
    - [dc69850] 2016-03-11 fixed `download_url` in setup.py [sol@hiqdev.com]

## [0.0.2] - 2016-03-11

- Changed: renamed to `heppy`
    - [12871b8] 2016-03-11 renamed to heppy [sol@hiqdev.com]
    - [fb64481] 2016-03-11 renamed to heppy [sol@hiqdev.com]

## [0.0.1] - 2016-03-11

- Added PyPI packaging
    - [bb25600] 2016-03-11 rehideved [sol@hiqdev.com]
    - [89ff36e] 2016-03-11 + setup.py, setup.cfg [sol@hiqdev.com]
- Added secDNS extension
    - [65582fe] 2016-03-10 + secDNS:update [sol@hiqdev.com]
    - [872f46a] 2016-03-10 improved secDNS [sol@hiqdev.com]
    - [5acfcab] 2016-03-10 + Doc.mget [sol@hiqdev.com]
    - [ffd65fa] 2016-03-10 fixed epp:poll [sol@hiqdev.com]
    - [68a0279] 2016-03-10 + secDNS:keyData [sol@hiqdev.com]
    - [09550d8] 2016-03-10 improved Request.subfields to get value from other name [sol@hiqdev.com]
    - [bc96776] 2016-03-09 improved secDNS:create rendering [sol@hiqdev.com]
    - [83183a2] 2016-03-09 improved hello parsing [sol@hiqdev.com]
    - [134eb23] 2016-03-09 + secDNS extension module [sol@hiqdev.com]
- Added basics
    - [110c8ef] 2016-03-09 reorganized modules into own dir [sol@hiqdev.com]
    - [cc6b7e8] 2016-03-08 cleaned away old junk, now everything in modules [sol@hiqdev.com]
    - [38a2641] 2016-03-07 fixed typos [sol@hiqdev.com]
    - [7fd9709] 2016-03-07 still improving [sol@hiqdev.com]
    - [63c4511] 2016-03-07 another MAJOR upgrade rendering [sol@hiqdev.com]
    - [cf0dc6c] 2016-03-06 another MAJOR: reorganized parsing into modules [sol@hiqdev.com]
    - [f6d83a3] 2016-03-05 + rgp status in response [sol@hiqdev.com]
    - [7ce30dd] 2016-03-05 + Namestore extension [sol@hiqdev.com]
    - [421ddb1] 2016-03-05 used Request.prettifyxml [sol@hiqdev.com]
    - [22b56ee] 2016-03-05 + initial DomainInfo and DomainDelete [sol@hiqdev.com]
    - [7e09225] 2016-03-05 fixed import Request [sol@hiqdev.com]
    - [d649ea4] 2016-03-03 MAJOR step forward: Args, Config, Daemon, Request, Response [sol@hiqdev.com]
    - [7d8b36b] 2016-02-29 changed reppyc to work with config file <- socket address [sol@hiqdev.com]
    - [2e7627e] 2016-02-12 + Hello and DomainCreate [sol@hiqdev.com]
    - [c0f7a0a] 2016-02-12 + Error module [sol@hiqdev.com]
    - [ff6134b] 2016-02-12 better error output - Error: type\nmessage [sol@hiqdev.com]
    - [3d0e953] 2016-02-12 + `Client.try_connect` [sol@hiqdev.com]
    - [35da144] 2016-02-12 + proper Login error processing [sol@hiqdev.com]
    - [4890a7e] 2016-02-12 + `start_time` to eppyd info [sol@hiqdev.com]
    - [4eaab99] 2016-02-12 + `check_connection()` to check if socket is already busy [sol@hiqdev.com]
    - [593ad47] 2016-02-09 rehideved [sol@hiqdev.com]
    - [a9a78dd] 2016-02-08 fixed hidev config [sol@hiqdev.com]
    - [e7b55e6] 2015-11-17 organized immports [sol@hiqdev.com]
    - [3d02756] 2015-11-17 + gitignore [sol@hiqdev.com]
    - [68e6d31] 2015-11-17 hideved [sol@hiqdev.com]
    - [5d83f10] 2015-11-17 moved to bin [sol@hiqdev.com]
    - [713489f] 2015-11-17 + readme for async [sol@hiqdev.com]
    - [27ac10c] 2015-11-17 moved to src [sol@hiqdev.com]
    - [cedbc65] 2015-11-17 + reppyc [sol@hiqdev.com]
    - [d29f6b1] 2015-11-17 added basics [sol@hiqdev.com]
    - [741ee8d] 2015-11-17 used Client module [sol@hiqdev.com]
    - [e943570] 2015-11-16 + Client, Request, Response modules [sol@hiqdev.com]
    - [63883bb] 2015-10-29 + unlink socket descriptor file [sol@hiqdev.com]
    - [cc1fc19] 2015-10-28 redone local connections to UNIX sockets [sol@hiqdev.com]
    - [508c7fd] 2015-10-28 + text xml [sol@hiqdev.com]
    - [4d221bb] 2015-10-27 + async version [sol@hiqdev.com]
    - [6c8a39f] 2015-10-27 redone back to non-async epp [sol@hiqdev.com]
    - [b74c7f3] 2015-10-27 fixed REPP `handle_read` [sol@hiqdev.com]
    - [7644c6b] 2015-10-27 + read config from json file [sol@hiqdev.com]
    - [f8bae00] 2015-10-19 basically working [sol@hiqdev.com]
    - [486e78d] 2015-10-19 NOT FINISHED but looks working [sol@hiqdev.com]
    - [ee07c0a] 2015-10-18 doing asyncronous epp [sol@hiqdev.com]
    - [b7f2f9f] 2015-10-17 lowered connect timeout and info command [sol@hiqdev.com]
    - [ae39190] 2015-10-17 working version with non-async epp [sol@hiqdev.com]
    - [0b62aee] 2015-10-16 + asynchronous wait [sol@hiqdev.com]
    - [d2ca75e] 2015-10-16 + greeting to REPP [sol@hiqdev.com]
    - [70499d6] 2015-10-16 first looking working [sol@hiqdev.com]
    - [6dfa31c] 2015-10-12 renamed to eppy [sol@hiqdev.com]
    - [ecb3788] 2015-10-12 inited [sol@hiqdev.com]

## [Development started] - 2015-10-12

[d91a4bd]: https://github.com/hiqdev/heppy/commit/d91a4bd
[fc0f10a]: https://github.com/hiqdev/heppy/commit/fc0f10a
[6c90cde]: https://github.com/hiqdev/heppy/commit/6c90cde
[05284bb]: https://github.com/hiqdev/heppy/commit/05284bb
[699989b]: https://github.com/hiqdev/heppy/commit/699989b
[d00f4d6]: https://github.com/hiqdev/heppy/commit/d00f4d6
[f7eb934]: https://github.com/hiqdev/heppy/commit/f7eb934
[dc69850]: https://github.com/hiqdev/heppy/commit/dc69850
[12871b8]: https://github.com/hiqdev/heppy/commit/12871b8
[fb64481]: https://github.com/hiqdev/heppy/commit/fb64481
[bb25600]: https://github.com/hiqdev/heppy/commit/bb25600
[89ff36e]: https://github.com/hiqdev/heppy/commit/89ff36e
[65582fe]: https://github.com/hiqdev/heppy/commit/65582fe
[872f46a]: https://github.com/hiqdev/heppy/commit/872f46a
[5acfcab]: https://github.com/hiqdev/heppy/commit/5acfcab
[ffd65fa]: https://github.com/hiqdev/heppy/commit/ffd65fa
[68a0279]: https://github.com/hiqdev/heppy/commit/68a0279
[09550d8]: https://github.com/hiqdev/heppy/commit/09550d8
[bc96776]: https://github.com/hiqdev/heppy/commit/bc96776
[83183a2]: https://github.com/hiqdev/heppy/commit/83183a2
[134eb23]: https://github.com/hiqdev/heppy/commit/134eb23
[110c8ef]: https://github.com/hiqdev/heppy/commit/110c8ef
[cc6b7e8]: https://github.com/hiqdev/heppy/commit/cc6b7e8
[38a2641]: https://github.com/hiqdev/heppy/commit/38a2641
[7fd9709]: https://github.com/hiqdev/heppy/commit/7fd9709
[63c4511]: https://github.com/hiqdev/heppy/commit/63c4511
[cf0dc6c]: https://github.com/hiqdev/heppy/commit/cf0dc6c
[f6d83a3]: https://github.com/hiqdev/heppy/commit/f6d83a3
[7ce30dd]: https://github.com/hiqdev/heppy/commit/7ce30dd
[421ddb1]: https://github.com/hiqdev/heppy/commit/421ddb1
[22b56ee]: https://github.com/hiqdev/heppy/commit/22b56ee
[7e09225]: https://github.com/hiqdev/heppy/commit/7e09225
[d649ea4]: https://github.com/hiqdev/heppy/commit/d649ea4
[7d8b36b]: https://github.com/hiqdev/heppy/commit/7d8b36b
[2e7627e]: https://github.com/hiqdev/heppy/commit/2e7627e
[c0f7a0a]: https://github.com/hiqdev/heppy/commit/c0f7a0a
[ff6134b]: https://github.com/hiqdev/heppy/commit/ff6134b
[3d0e953]: https://github.com/hiqdev/heppy/commit/3d0e953
[35da144]: https://github.com/hiqdev/heppy/commit/35da144
[4890a7e]: https://github.com/hiqdev/heppy/commit/4890a7e
[4eaab99]: https://github.com/hiqdev/heppy/commit/4eaab99
[593ad47]: https://github.com/hiqdev/heppy/commit/593ad47
[a9a78dd]: https://github.com/hiqdev/heppy/commit/a9a78dd
[e7b55e6]: https://github.com/hiqdev/heppy/commit/e7b55e6
[3d02756]: https://github.com/hiqdev/heppy/commit/3d02756
[68e6d31]: https://github.com/hiqdev/heppy/commit/68e6d31
[5d83f10]: https://github.com/hiqdev/heppy/commit/5d83f10
[713489f]: https://github.com/hiqdev/heppy/commit/713489f
[27ac10c]: https://github.com/hiqdev/heppy/commit/27ac10c
[cedbc65]: https://github.com/hiqdev/heppy/commit/cedbc65
[d29f6b1]: https://github.com/hiqdev/heppy/commit/d29f6b1
[741ee8d]: https://github.com/hiqdev/heppy/commit/741ee8d
[e943570]: https://github.com/hiqdev/heppy/commit/e943570
[63883bb]: https://github.com/hiqdev/heppy/commit/63883bb
[cc1fc19]: https://github.com/hiqdev/heppy/commit/cc1fc19
[508c7fd]: https://github.com/hiqdev/heppy/commit/508c7fd
[4d221bb]: https://github.com/hiqdev/heppy/commit/4d221bb
[6c8a39f]: https://github.com/hiqdev/heppy/commit/6c8a39f
[b74c7f3]: https://github.com/hiqdev/heppy/commit/b74c7f3
[7644c6b]: https://github.com/hiqdev/heppy/commit/7644c6b
[f8bae00]: https://github.com/hiqdev/heppy/commit/f8bae00
[486e78d]: https://github.com/hiqdev/heppy/commit/486e78d
[ee07c0a]: https://github.com/hiqdev/heppy/commit/ee07c0a
[b7f2f9f]: https://github.com/hiqdev/heppy/commit/b7f2f9f
[ae39190]: https://github.com/hiqdev/heppy/commit/ae39190
[0b62aee]: https://github.com/hiqdev/heppy/commit/0b62aee
[d2ca75e]: https://github.com/hiqdev/heppy/commit/d2ca75e
[70499d6]: https://github.com/hiqdev/heppy/commit/70499d6
[6dfa31c]: https://github.com/hiqdev/heppy/commit/6dfa31c
[ecb3788]: https://github.com/hiqdev/heppy/commit/ecb3788
[ce47da1]: https://github.com/hiqdev/heppy/commit/ce47da1
[4560e80]: https://github.com/hiqdev/heppy/commit/4560e80
[e64b3e8]: https://github.com/hiqdev/heppy/commit/e64b3e8
[1328fcb]: https://github.com/hiqdev/heppy/commit/1328fcb
[3c6c3f4]: https://github.com/hiqdev/heppy/commit/3c6c3f4
[bf2fba6]: https://github.com/hiqdev/heppy/commit/bf2fba6
[2cfde17]: https://github.com/hiqdev/heppy/commit/2cfde17
[c63ac63]: https://github.com/hiqdev/heppy/commit/c63ac63
[24b8f95]: https://github.com/hiqdev/heppy/commit/24b8f95
[17a065f]: https://github.com/hiqdev/heppy/commit/17a065f
[f97e797]: https://github.com/hiqdev/heppy/commit/f97e797
[8d9777c]: https://github.com/hiqdev/heppy/commit/8d9777c
[60ccaaf]: https://github.com/hiqdev/heppy/commit/60ccaaf
[ce81052]: https://github.com/hiqdev/heppy/commit/ce81052
[d4067df]: https://github.com/hiqdev/heppy/commit/d4067df
[f22fd94]: https://github.com/hiqdev/heppy/commit/f22fd94
[d7717e4]: https://github.com/hiqdev/heppy/commit/d7717e4
[879323f]: https://github.com/hiqdev/heppy/commit/879323f
[66ee295]: https://github.com/hiqdev/heppy/commit/66ee295
[c2bdbac]: https://github.com/hiqdev/heppy/commit/c2bdbac
[a5f58a6]: https://github.com/hiqdev/heppy/commit/a5f58a6
[1c0f485]: https://github.com/hiqdev/heppy/commit/1c0f485
[d49e9f0]: https://github.com/hiqdev/heppy/commit/d49e9f0
[e16d03d]: https://github.com/hiqdev/heppy/commit/e16d03d
[1f364a7]: https://github.com/hiqdev/heppy/commit/1f364a7
[b34b71d]: https://github.com/hiqdev/heppy/commit/b34b71d
[9a8d427]: https://github.com/hiqdev/heppy/commit/9a8d427
[9bd74f7]: https://github.com/hiqdev/heppy/commit/9bd74f7
[26f9b2c]: https://github.com/hiqdev/heppy/commit/26f9b2c
[0aed840]: https://github.com/hiqdev/heppy/commit/0aed840
[5fa56c3]: https://github.com/hiqdev/heppy/commit/5fa56c3
[d926653]: https://github.com/hiqdev/heppy/commit/d926653
[3bad9e9]: https://github.com/hiqdev/heppy/commit/3bad9e9
[7268e1f]: https://github.com/hiqdev/heppy/commit/7268e1f
[18d750e]: https://github.com/hiqdev/heppy/commit/18d750e
