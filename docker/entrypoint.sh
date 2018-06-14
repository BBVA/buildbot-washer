#!/bin/sh
export BASEDIR="/washer"
export PYTHONHOME="/washer"
export LD_LIBRARY_PATH="/washer"
/washer/ld-linux-x86-64.so.2 /washer/buildbot-worker "$@" --unset PYTHONHOME --unset LD_LIBRARY_PATH
