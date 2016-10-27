# Examples

## Fee

Check:

```sh
./bin/reppyc centralnic domain:check -names.0=some.host -names.1=expensive.host -extension=fee:check
```

Register:

```sh
./bin/reppyc centralnic domain:create -name=some.host -pw=zZz -period=1 -registrant=EVN_1014727N -tech=EVN_1014727N -billing=EVN_1014727N -admin=EVN_1014727N -extension=fee:create -fee_fee=3000
```

## Namestore

Info:

```sh
./bin/reppyc comnet domain:info -extensions.0=namestoreExt:subProduct -subProduct=COM -name=some.com
Namestore
