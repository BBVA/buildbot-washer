#!/bin/sh
export BASEDIR="/washer"
export LD_LIBRARY_PATH="/washer"
/washer/ld-linux-x86-64.so.2 /washer/buildbot-worker "$@" --unset LD_LIBRARY_PATH --unset PYTHONHOME 
