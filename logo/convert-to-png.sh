#!/bin/sh
base="electruth-logo"
source="$base".svg
size="$1"

if [ ! "$size" ]; then
    echo "usage: $0 SIZE (example: $0 64 returns a png of 64x64 pixels)"
else
    newpng="$base-$1.png"
    echo "Converting $source to $newpng..."
    inkscape "--export-png=$newpng" "--export-width=$size" \
        "--export-height=$size" "$source"
fi
