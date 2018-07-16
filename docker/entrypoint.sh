#!/bin/sh
export BASEDIR="/washer" 
export PYTHONHOME="/washer"
/washer/ld-linux-x86-64.so.2 /washer/buildbot-worker "$@" --unset PYTHONHOME
