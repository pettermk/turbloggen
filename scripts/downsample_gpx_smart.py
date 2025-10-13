#!/usr/bin/env python3
import os
import glob
from pathlib import Path
import sys
import shutil

try:
    import gpxpy
    import gpxpy.gpx
except ImportError:
    print("gpxpy library not found. Please install it with:")
    print("python3 -m pip install gpxpy")
    sys.exit(1)

def downsample_gpx_smart(input_file, output_file, tolerance=0.0001):
    """Downsample GPX file using Ramer-Douglas-Peucker algorithm"""
    try:
        # Parse GPX file
        with open(input_file, 'r') as f:
            gpx = gpxpy.parse(f)

        # Simplify using Ramer-Douglas-Peucker algorithm
        # Note: max_distance is in meters for gpxpy
        gpx.simplify(max_distance=tolerance)

        # Save simplified GPX
        with open(output_file, 'w') as f:
            f.write(gpx.to_xml())

    except Exception as e:
        print(f"  Error processing {os.path.basename(input_file)}: {e}")

def process_directory(directory, tolerance=0.0001):
    """Process all GPX files in the given directory"""
    gpx_files = glob.glob(os.path.join(directory, "*.gpx"))
    print(gpx_files)
    
    if not gpx_files:
        return
    
    print(f"Processing directory: {directory}")
    print(f"Using tolerance: {tolerance} (smaller = more points kept)")
    
    for gpx_file in gpx_files:
        filename = os.path.basename(gpx_file)
        
        # Skip files that already have -resampled in the name
        if "-resampled" in filename:
            print(f"  Skipping {filename} (already resampled)")
            continue

        if filename.endswith(".orig"):
            print(f"  Skipping {filename} (is an original backup)")
            continue
        
        # Create backup by renaming to .gpx.orig
        orig_file = gpx_file + ".orig"
        if not os.path.exists(orig_file):
            shutil.copy(gpx_file, orig_file)
            print(f"  Copied {filename} to {filename}.orig")
        else:
            orig_file = gpx_file
            print(f"  Backup already exists for {filename}")
        
        # Create resampled version
        base_name = os.path.splitext(filename)[0]
        resampled_file = os.path.join(directory, f"{base_name}-resampled.gpx")
        
        print(f"  Processing {filename}...")
        downsample_gpx_smart(gpx_file, resampled_file, tolerance)
        os.remove(gpx_file)

def main():
    tolerance = 0.0001  # Default tolerance (smaller = more points kept)
    target_dir = None
    
    # Parse command line arguments
    i = 1
    while i < len(sys.argv):
        if sys.argv[i] == "--tolerance" or sys.argv[i] == "-t":
            if i + 1 < len(sys.argv):
                tolerance = float(sys.argv[i + 1])
                i += 2
            else:
                print("Error: --tolerance requires a value")
                sys.exit(1)
        else:
            target_dir = sys.argv[i]
            i += 1
    
    if not target_dir:
        # Default to looking for GPX files in the content/posts directory structure
        script_dir = Path(__file__).parent
        project_root = script_dir.parent
        content_dir = project_root / "content" / "posts"
        target_dir = str(content_dir)
    
    if not os.path.exists(target_dir):
        print(f"Directory {target_dir} does not exist")
        return
    
    print(f"Smart GPX Downsampling using Ramer-Douglas-Peucker Algorithm")
    print(f"Tolerance: {tolerance} (adjust with --tolerance <value>)")
    print(f"  - Smaller tolerance = more points kept, better accuracy")
    print(f"  - Larger tolerance = fewer points kept, more compression")
    print()
    
    # Process all subdirectories that contain GPX files
    for root, dirs, files in os.walk(target_dir):
        gpx_files = [f for f in files if f.endswith('.gpx')]
        if gpx_files:
            process_directory(root, tolerance)
    
    print("\nDone!")

if __name__ == "__main__":
    main()
