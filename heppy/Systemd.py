#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import time


class Systemd:
    def __init__(self, name, num, exec_start, work_dir = None):
        self.name = name
        self.num = num
        self.exec_start = exec_start
        self.work_dir = work_dir

    def dump(self):
        print(self.service_name(self.num))

    def call(self, name, args):
        if hasattr(self, name):
            getattr(self, name)()
        else:
            self.runcmd_all(name)

    def up(self):
        self.setup()
        self.runcmd_all('enable')
        self.runcmd_all('start')

    def down(self):
        self.setup()
        self.runcmd_all('stop')
        self.runcmd_all('disable')

    def status(self):
        self.unsafe_all('status')

    def tail(self):
        names = ' -u '.join(self.service_names())
        self.unsafe('journalctl -f -u %s' % names)

    def runcmd_all(self, command):
        for name in self.service_names():
            self.runcmd('systemctl %s %s' % (command, name))

    def unsafe_all(self, command):
        for name in self.service_names():
            self.unsafe('systemctl %s %s' % (command, name))

    def runcmd(self, command):
        ret = self.unsafe(command)
        if ret:
            raise Exception('failed ' + command)

    def unsafe(self, command):
        print(command)
        return os.system(command)

    def setup(self):
        path = self.service_path()
        new  = self.service_config()
        try:
            with open(path, 'r') as file:
                old = file.read()
        except Exception as e:
            old = ''
        if old != new:
            with open(path, 'w') as file:
                file.write(new)

    def service_path(self):
        return '/etc/systemd/system/' + self.service_name()

    def service_names(self):
        if not hasattr(self, 'names'):
            self.names = []
            for i in range(self.num):
                self.names.append(self.service_name(i))
        return self.names

    def service_name(self, no = ''):
        return '%s@%s.service' % (self.name, no)

    def service_config(self):
        return '''\
[Unit]
Description={name} %i
StopWhenUnneeded=true
After=rabbitmq-server.service

[Service]
WorkingDirectory={work_dir}
ExecStart={exec_start}
Restart=always
User=root
Group=root

[Install]
WantedBy=multi-user.target
'''.format(
            name=self.name,
            work_dir=self.work_dir,
            exec_start=self.exec_start
        )

