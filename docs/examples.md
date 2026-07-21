# Examples

## Fee extension

Domain check:

```sh
./bin/heppyc etc/centralnic/epp.json domain:check -names.0=advanced.host -extensions.0.command=fee:check -extensions.0.name=advanced.host -extensions.0.currency=USD -extensions.0.action=renew -extensions.0.period=1
```

Domain create:

```sh
./bin/heppyc etc/centralnic/epp.json domain:create -name=some.host -pw=zZz -period=1 -registrant=EVN_1014727N -tech=EVN_1014727N -billing=EVN_1014727N -admin=EVN_1014727N -extensions.0.command=fee:create -extensions.0.fee=3000
```

Domain renew:

```sh
./bin/heppyc etc/centralnic/epp.json domain:renew -name=some.host -curExpDate=2016-10-10 -period=1 -extensions.0.command=fee:renew -extensions.0.fee=111
```

## Namestore extension

Domain info:

```sh
./bin/heppyc etc/epp.verisign-grs.com               domain:info -extensions.0.command=namestoreExt -extensions.0.subProduct=dotCOM -name=some.com

./bin/heppyc etc/namestoressl.verisign-grs.com.json domain:info -extensions.0.command=namestoreExt -extensions.0.subProduct=dotCC -name=some.cc
```

## DNSSEC

```sh
./bin/heppyc etc/namestoressl.verisign-grs.com.json domain:update -name=some.cc -extensions.0.command=namestoreExt -extensions.0.subProduct=dotCC -extensions.1.command=secDNS:update -extensions.1.add.keyTag=23185 -extensions.1.add.digestAlg=8 -extensions.1.add.digestType=1 -extensions.1.add.digest=E326B89D105D7533D1C3FCC1B02841CA26D73A99

./bin/heppyc etc/namestoressl.verisign-grs.com.json domain:update -name=some.cc -extensions.0.command=namestoreExt -extensions.0.subProduct=dotCC -extensions.1.command=secDNS:update -extensions.1.add.keyTag=23185 -extensions.1.add.digestAlg=8 -extensions.1.add.digestType=1 -extensions.1.add.digest=E326B89D105D7533D1C3FCC1B02841CA26D73A99 -extensions.1.add.flags=257 -extensions.1.add.protocol=3 -extensions.1.add.keyAlg=8 -extensions.1.add.pubKey='AwEAAdaImq0YbvjNnK03ZeeZa4VxKUzrjVGw3jdHv3gEX748tUabgOCbpLiYvalT+FFBBLSLL5/uPhiOcL1slFlVchP7GdXwmuXWhdt/KsdSaeXeFEkIfYJS64LFVnLmCnSRs24M5m+OygvjJjL3dgwXmSu0S+NDp87/dsgSYj/z2g5XnlGnoVmXNlqflJEfXOOHrKN3ufDyyUEwPqDMKMViwv3MuzH6h8AHpXGtwUT6NA12t8EAQd9YiXqSxdWpv/DaRnLHTeWBEJ546dZ9/m64nT2U+FReu3E42DaGsKBXze8YPafV3P7dOWOp/K5QoGsVF1QHXD/ilLAqBaFU+Odw11U='
```

Domain create with a DS record straight away (no separate update needed):

```sh
./bin/heppyc etc/google/ote3.json domain:create -name=example.google-ga -period=1 -pw=Password_1a -nss.0=ns1.example.com -nss.1=ns2.example.com -extensions.0.command=secDNS:create -extensions.0.keyTag=2371 -extensions.0.digestAlg=13 -extensions.0.digestType=2 -extensions.0.digest=BDDC580D4B2E21A5DEBC43FC43DE20D50DB87A81F3162C6A2BE31871629C9779
```

## Host management

Create hosts, then attach them to a domain as glue records (IPv4 + IPv6):

```sh
./bin/heppyc etc/google/ote3.json host:create -name=ns1.example.google-ga -ips.0=88.208.5.2 -ips.1='2a02:b49:4:14:1::1'
./bin/heppyc etc/google/ote3.json host:create -name=ns2.example.google-ga -ips.0=88.208.36.16 -ips.1='2a02:b49:4:3:1::1'
./bin/heppyc etc/google/ote3.json host:info -name=ns1.example.google-ga

./bin/heppyc etc/google/ote3.json domain:update -name=example.google-ga -add.0.nss.0=ns1.example.google-ga -add.0.nss.1=ns2.example.google-ga -rem.0.nss.0=ns1.example.com -rem.0.nss.1=ns2.example.com
```

Update a host's IP addresses, then remove it:

```sh
./bin/heppyc etc/google/ote3.json host:update -name=ns1.example.google-ga -rem.0.ips.0=88.208.5.2 -add.0.ips.0=46.229.175.55
./bin/heppyc etc/google/ote3.json host:delete -name=ns1.example.google-ga
```

## Launch extension (claims & sunrise)

Claims notice: `launch:check` returns a `claimKey`, which is exchanged for a `noticeID`/`notAfter` at the TMCH's claims-notice service (CNIS), then passed into `launch:create`:

```sh
./bin/heppyc etc/google/ote3.json domain:check -names.0=example.google-ga -extensions.0.command=launch:check -extensions.0.phase=claims

# CLAIM_KEY parsed out of the reply above, then resolved to NOTICE_ID/NOT_AFTER via
# https://(test.)tmcnis.org/cnis/<CLAIM_KEY>.xml (see ote-test/google/google_test_24.sh)

./bin/heppyc etc/google/ote3.json domain:create -name=example.google-ga -period=1 -pw=Password_1 -extensions.0.command=launch:create -extensions.0.phase=claims -extensions.0.notice_id=$NOTICE_ID -extensions.0.not_after=$NOT_AFTER -extensions.0.accepted_date=$ACCEPTED_DATE -extensions.0.validator_id=tmch
```

Sunrise: create with an encoded Signed Mark Data (SMD) obtained from the TMCH — the domain label must match the mark in the SMD:

```sh
./bin/heppyc etc/google/ote1.json domain:check -names.0=example.google-sunrise -extensions.0.command=launch:check

./bin/heppyc etc/google/ote1.json domain:create -name=example.google-sunrise -period=1 -pw=Password_1 -extensions.0.command=launch:create -extensions.0.phase=sunrise -extensions.0.encoded_signed_mark=$ENCODED_SMD
```

## Poll messages

Fetch the next poll message, and acknowledge it if there is one (`result_code` `1301` means a message was returned):

```sh
./bin/heppyc etc/google/ote3.json epp:poll
./bin/heppyc etc/google/ote3.json epp:poll -op=ack -msgID=12345
```

## Domain transfer

Transfer is driven from both the gaining (`ote4`) and losing (`ote3`) registrar's clients:

```sh
# gaining registrar requests the transfer
./bin/heppyc etc/google/ote4.json domain:transfer -name=example.google-ga -pw=Password_1a

# either side can poll the pending request
./bin/heppyc etc/google/ote4.json domain:transfer -name=example.google-ga -pw=Password_1a -op=query
./bin/heppyc etc/google/ote3.json domain:transfer -name=example.google-ga -op=query

# losing registrar approves (or -op=reject / -op=cancel from the gaining side instead)
./bin/heppyc etc/google/ote3.json domain:transfer -name=example.google-ga -op=approve
```

## RGP restore

Request restoration of a domain still within its redemption grace period:

```sh
./bin/heppyc etc/google/ote3.json domain:restore -name=example.google-ga -extensions.0.command=rgp:request
```
