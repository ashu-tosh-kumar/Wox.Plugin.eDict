#!/bin/bash

# Handle dependencies
# pyperclip
rm -rf lib
mkdir tmp
pip download --dest tmp pyperclip
cd tmp
for file in *.tar.gz; do tar -xvf "$file"; done
mkdir lib
mv */* lib
rm -rf lib/docs
rm -rf lib/tests
rm -rf lib/src/pyperclip.egg-info
mv lib ../
cd ..
rm -rf tmp

# Define the output zip file
OUTPUT_ZIP="Wox.Plugin.eDict.wox"

# Delete the existing zip file if it exists
if [ -f "$OUTPUT_ZIP" ]; then
    rm "$OUTPUT_ZIP"
fi

# Define the filenames and folder
FILES=("spell.py" "plugin.json" "main.py" "dictionary_compact_with_words.zip")
ICON_FOLDER="icons"
LIB_FOLDER="lib"

# Create a new zip file and add files
zip -r "$OUTPUT_ZIP" "${FILES[@]}" "$ICON_FOLDER" "$LIB_FOLDER"
