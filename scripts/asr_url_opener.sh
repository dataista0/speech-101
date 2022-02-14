#!/bin/sh
# Run from the scripts/ path as ./asr_url_opener.sh
# Make sure you are in the environment with speech_recognition installed!
python -u ../src/asr_url_opener.py  >> ../logs/asr_url_opener.log 2>&1 & 
