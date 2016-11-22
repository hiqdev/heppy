# systemd usage

## Target files

### `/etc/systemd/system/heppy.target`

```ini
[Install]
WantedBy=multi-user.target
```

### `/etc/systemd/system/heppy@.service`

```ini
[Unit]
Description=hEPPy %i
StopWhenUnneeded=true

[Service]
ExecStart=/home/sol/prj/evonames/evoplus-heppy/bin/heppyd %i start
Restart=always
User=heppy
Group=heppy

[Install]
WantedBy=heppy.target
```

## Enable new registry

```sh
systemctl enable heppy@epp.afilias.net:01.service
```
