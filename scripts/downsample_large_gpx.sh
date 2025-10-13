#!/bin/sh
set -e

# Downsample GPX files larger than specified size
SIZE_THRESHOLD=${1:-300000}  # Default 300KB
TOLERANCE=${2:-10}  # Default 10 meters

echo "Checking for GPX files larger than $SIZE_THRESHOLD bytes..."

find content/posts -name "*.gpx" -type f | while read -r gpx_file; do
    # Use wc -c for busybox compatibility (counts bytes)
    file_size=$(wc -c < "$gpx_file")

    if [ "$file_size" -gt "$SIZE_THRESHOLD" ]; then
        size_kb=$(awk "BEGIN {printf \"%.1f\", $file_size / 1024}")
        echo "Downsampling $gpx_file ($size_kb KB)..."
        cd scripts && uv run downsample_gpx_smart.py --tolerance "$TOLERANCE" --in-place "../$gpx_file" && cd ..
    fi
done

echo "Done!"
