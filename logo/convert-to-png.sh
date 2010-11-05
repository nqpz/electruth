#!/bin/sh
base="electruth-logo"
source="$base".svg
width="$1"

if [ ! "$width" ]; then
    echo "usage: $0 WIDTH (example: $0 500 returns a png of 500x320 pixels)"
else
    newpng="$base-$1.png"
    echo "Converting $source to $newpng..."
    inkscape "--export-png=$newpng" "--export-width=$width" \
        "$source"
fi
