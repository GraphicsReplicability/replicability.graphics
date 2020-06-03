#!/bin/bash
set -e

## $1 is the Altmetric API key

echo "========= Init =========="
sudo apt-get install -y graphicsmagick
if [ -d tmp ]; then
  echo "tmp folder already exists"
else
  mkdir tmp        
fi

echo "========= Downloading the data =========="
if [ ! -d tmp ]; then
    if [ ! -d .git ]; then
        rm -rf ./*
    fi
    git clone --depth 1 https://github.com/GraphicsReplicability/replicability.graphics.git tmp
fi
cd tmp
git checkout gh-pages
cd ..
cp -R website-source/* tmp/

echo "========= Concatenate the JSON =========="
scripts/concatenateJSON.sh

echo "========= Fetching the data =========="
python3 scripts/fetchData.py tmp/consolidated.json $1

echo "========= Generate pages ================"
python3 scripts/generatePagesFromConsolidatedJSON.py tmp/consolidated.json
cd tmp

echo "========= main page =================="
./concat.sh core.html

echo "========= Data cache =================="
#At least one PDF
touch papers/hop.pdf
find "papers/" -name "*.pdf" | xargs rm -v 
echo "========= Bye  =================="
