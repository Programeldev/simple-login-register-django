#!/bin/bash

python -m venv .env
source .env/bin/activate
pip install -r requirements.txt

echo "######################################"
echo "#########  BUILD COMPLETED  ##########"
echo "######################################"
