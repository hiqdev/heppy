Start EPP client:

```sh
./bin/heppyd etc/comnet/epp.json start
```

Register domain:

```sh
./bin/heppyc etc/comnet/epp.json domain:create '-name=xn----0tbbnc0a.com' -pw=23_sA:d34 -period=1 -extensions.1=idnLang:tag -idnLang.tag=RUS -extensions.0=namestoreExt:subProduct -namestoreExt.subProduct=COM
```
