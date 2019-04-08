# Examples

## Fee extension

Domain check:

```sh
./bin/heppyc etc/centralnic/epp.json domain:check -names.0=some.host -names.1=expensive.host -extensions.0.command=fee:check
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
./bin/heppyc etc/namestoressl.verisign-grs.com.json domain:update -name=some.cc -extensions.0.command=namestoreExt -extensions.0.subProduct=dotCC -extensions.1.command=secDNS:update -extensions.1.add.keyTag=23158 -extensions.1.add.digestAlg=8 -extensions.1.add.digestType=1 -extensions.1.add.digest=E326B89D105D7533D1C3FCC1B02841CA26D73A99

./bin/heppyc etc/namestoressl.verisign-grs.com.json domain:update -name=oshq.cc -extensions.0.command=namestoreExt -extensions.0.subProduct=dotCC -extensions.1.command=secDNS:update -extensions.1.add.flags=257 -extensions.1.add.protocol=3 -extensions.1.add.keyAlg=8 '-extensions.1.add.pubKey=AwEAAdaImq0YbvjNnK03ZeeZa4VxKUzrjVGw3jdHv3gEX748tUabgOCbpLiYvalT+FFBBLSLL5/uPhiOcL1slFlVchP7GdXwmuXWhdt/KsdSaeXeFEkIfYJS64LFVnLmCnSRs24M5m+OygvjJjL3dgwXmSu0S+NDp87/dsgSYj/z2g5XnlGnoVmXNlqflJEfXOOHrKN3ufDyyUEwPqDMKMViwv3MuzH6h8AHpXGtwUT6NA12t8EAQd9YiXqSxdWpv/DaRnLHTeWBEJ546dZ9/m64nT2U+FReu3E42DaGsKBXze8YPafV3P7dOWOp/K5QoGsVF1QHXD/ilLAqBaFU+Odw11U='
```
