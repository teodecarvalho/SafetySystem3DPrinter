#!/bin/bash
rm -r *.py *.kv __pyc*
cp -r /media/psf/Home/Documents/SafetySystem3DPrinter/* .
buildozer android debug deploy run
adb logcat | grep python
