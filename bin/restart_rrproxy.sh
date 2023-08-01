#!/bin/sh

RES=`/home/sol/prj/epp/heppy/bin/heppyc /home/sol/prj/epp/heppy/etc/rrpproxy/epp.json epp:hello | grep 'Broken pipe'`
if [ "$?" = "0" ]; then
    /home/sol/prj/epp/heppy/bin/heppyd /home/sol/prj/epp/heppy/etc/rrpproxy/epp.json systemd restart
fi

