#!/bin/bash
set -e

## $1 is the Altmetric API key


echo "========= Init =========="
sudo apt-get install -y graphicsmagick
if [ -d tmp ]; then
    echo "tmp folder already exists, cleaning it"
    rm  -rf tmp
fi

echo "========= Downloading the data =========="
git clone --depth 1 -b gh-pages https://github.com/GraphicsReplicability/replicability.graphics.git tmp

## removing the .git in the clone
cd tmp
rm -rf .git/
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

echo "========= Generate GRSI page ================"
python3 scripts/scripts/exportGRSI.py tmp/consolidated.json > tmp/GRSI.html

echo "========= Data cache =================="
#At least one PDF
touch papers/hop.pdf
find "papers/" -name "*.pdf" | xargs rm -v
echo "========= Bye  =================="
