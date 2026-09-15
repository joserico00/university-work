#!/bin/bash

while IFS= read -r url; do
    # Convert the URL into a safe filename by replacing special characters
    filename=$(echo "$url" | sed 's/[^a-zA-Z0-9]/_/g').txt

    # Run pa11y and save the report to the filename
    pa11y "$url" > "$filename"
done < urls.txt
