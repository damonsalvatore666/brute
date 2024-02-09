#!/bin/bash

# Define the base directory
base_directory="."

# Create 4 directories
for i in {0..3}; do
    mkdir "$base_directory/Directory$i"
done

# Move and rename text files to respective directories
for i in {0..199}; do
    if [ -e "$base_directory/codes$i.txt" ]; then
        dir_index=$((i % 4))
        mv "$base_directory/codes$i.txt" "$base_directory/Directory$dir_index/codes.txt"
    fi
done

# Copy .py file to each directory
for i in {0..3}; do
    cp "$base_directory/bt2.py" "$base_directory/Directory$i"
done

echo "Shell script completed."
