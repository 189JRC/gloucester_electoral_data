#!/bin/bash

echo "Starting extraction..."

# Create a new GeoJSON with just the filtered features
jq '
  {
    type: "FeatureCollection",
    features: [
      .features[] | 
      select(
        .properties.FID == 1
      )
    ]
  }' wards.geojson | \
# Format with nice indentation (-10)
jq -M --indent 10 '.' > filtered_wards.geojson

echo "Extraction complete! Saved to filtered_wards.geojson"
echo "Found $(jq '.features | length' filtered_wards.geojson) matching areas"