#!/bin/sh
export PYTHONHOME="/washer"
export LD_LIBRARY_PATH="/washer"
/washer/launch-worker --unset PYTHONHOME --unset LD_LIBRARY_PATH
