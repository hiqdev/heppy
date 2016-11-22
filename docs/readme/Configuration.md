### etc/epp.verisign-grs.com.json

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
