# Examples

## Fee extension

Domain check:

```sh
./bin/reppyc centralnic domain:check -names.0=some.host -names.1=expensive.host -extension=fee:check
```

Domain create:

```sh
./bin/reppyc centralnic domain:create -name=some.host -pw=zZz -period=1 -registrant=EVN_1014727N -tech=EVN_1014727N -billing=EVN_1014727N -admin=EVN_1014727N -extension=fee:create -fee.fee=3000
```

Domain renew:

```sh
./bin/reppyc centralnic domain:renew -name=some.host -curExpDate=2016-10-10 -period=1 -extension=fee:renew -fee.fee=111
```

## Namestore extension

Domain info:

```sh
./bin/reppyc comnet domain:info -extensions.0=namestoreExt:subProduct -subProduct=COM -name=some.com
```

