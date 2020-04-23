#!/bin/sh

jq -s . data/**/*.json >  tmp/consolidated.json
