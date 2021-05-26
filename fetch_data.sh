#!/bin/bash
mkdir DB && cd DB

wget https://raw.githubusercontent.com/StebF2000/yeswebike/main/db_build.sh

wget -O data.zip https://www.dropbox.com/sh/p7utjsf1i0ur8hy/AACOXiJHiRDKRgC1Use29JTma\?dl=1

mkdir data

unzip data.zip -d data -x /
rm data.zip

exit 1
