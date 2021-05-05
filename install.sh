#!/usr/bin/env bash

sudo apt update 
sudo apt install postgresql

virtualenv -p python venv

source venv/bin/activate

pip install -r requirements.txt

deactivate


