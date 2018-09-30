Start EPP client:

```sh
./bin/heppyd epp.verisign-grs.com start
```

Start with systemd:

```sh
./bin/heppyd verisign/epp.json systemd up
```

Register domain:

```sh
./bin/heppyc epp.verisign-grs.com domain:create '-name=xn----0tbbnc0a.com' -pw=23_sA:d34 -period=1 -extensions.1=idnLang:tag -idnLang.tag=RUS -extensions.0=namestoreExt:subProduct -namestoreExt.subProduct=COM
```
