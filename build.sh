#!bin/bash

set -e 

pyinstaller --noconsole --onefile --name "PDF Merger" main.py
