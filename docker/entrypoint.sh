#!/bin/sh
export BASEDIR="/washer" 
/washer/ld-linux-x86-64.so.2 /washer/buildbot-worker "$@" --unset BASEDIR
