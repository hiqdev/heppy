#!/usr/bin/env python

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
        print self.service_name(self.num)

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

    def runcmd_all(self, command):
        for i in range(self.num):
            self.runcmd('systemctl %s %s' % (command, self.service_name(i)))

    def unsafe_all(self, command):
        for i in range(self.num):
            self.unsafe('systemctl %s %s' % (command, self.service_name(i)))

    def runcmd(self, command):
        ret = self.unsafe(command)
        if ret:
            raise Exception('failed ' + command)

    def unsafe(self, command):
        print command
        return os.system(command)

    def setup(self):
        with open(self.service_path(), 'r+') as file:
            old = file.read()
            new = self.service_config()
            if old != new:
                file.seek(0)
                file.truncate()
                file.write(new)

    def service_path(self):
        return '/etc/systemd/system/' + self.service_name()

    def service_name(self, no = ''):
        return '%s@%s.service' % (self.name, no)

    def service_config(self):
        return '''\
[Unit]
Description={name} %i
StopWhenUnneeded=true

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

