import folium
from folium.plugins import Fullscreen
import geopandas as gpd
import json
from shapely.geometry import Polygon
from shapely.validation import explain_validity, make_valid


#For each geometry in the GeoDataFrame, check validity, log the issue if invalid, and attempt to fix it using make_valid
def validate_and_fix_geometries(gdf, log):
    for idx, row in gdf.iterrows(): # iterate over each row in the GeoDataFrame
        fid = row.get("fid", idx)
        geom = row.geometry
        if not geom.is_valid:
            issue = explain_validity(geom) # exploring the problem with geometry
            log.write(f"⚠️ Polygon fid `{fid}` is invalid: {issue}")
            fixed = make_valid(geom) # attempt to fix the geometry
            if fixed.is_valid:
                log.write(f"✅ Polygon fid `{fid}` geometry was fixed.")
                gdf.at[idx, "geometry"] = fixed
            else:
                log.write(f"❌ Polygon fid `{fid}` remains invalid. Keeping original.")
    return gdf


# Comparing polygon geometries and dropping duplicates
def remove_exact_duplicates(gdf, log):
    seen = [] # list to keep track of seen geometries
    duplicates = set() # set to keep track of duplicates
    for i, row1 in gdf.iterrows():
        fid1 = row1.get("fid", i)
        geom1 = row1.geometry
        for j in seen:
            fid2 = gdf.iloc[j].get("fid", j)
            geom2 = gdf.iloc[j].geometry
            if geom1.equals(geom2):
                log.write(f"🗑️Removing polygon fid `{fid1}` - duplicate of polygon fid `{fid2}`")
                duplicates.add(i)
                break
        seen.append(i)
    return gdf.drop(index=list(duplicates)).reset_index(drop=True)


# Finding polygons that are almost identical using a tolerance value and removing them
def remove_near_duplicates(gdf, log, tolerance=0.007):
    near_duplicates = set() # set to keep track of near duplicates
    for i in range(len(gdf)):
        for j in range(i + 1, len(gdf)):
            poly1 = gdf.geometry.iloc[i]
            poly2 = gdf.geometry.iloc[j]
            fid1 = gdf.iloc[i].get("fid", i)
            fid2 = gdf.iloc[j].get("fid", j)

            if isinstance(poly1, Polygon) and isinstance(poly2, Polygon):
                if poly1.equals_exact(poly2, tolerance):
                    log.write(f"🗑️Removing polygon fid `{fid2}` - nearly identical to polygon fid `{fid1}` with {tolerance} degrees tolerance")
                    near_duplicates.add(j)

    return gdf.drop(index=list(near_duplicates)).reset_index(drop=True)


# Read uploaded GeoJSON to GeoDataFrame and get original filename and CRS
def read_geojson_to_gdf(uploaded_file):
    original_json_str = uploaded_file.read().decode("utf-8")
    original_json = json.loads(original_json_str)
    original_name = original_json.get("name", "GeoJSON")

    uploaded_file.seek(0) # Reset pointer
    gdf = gpd.read_file(uploaded_file)
    original_crs = gdf.crs

    return original_name, gdf, original_crs, original_json


# Prepare cleaned GeoJSON dictionary with CRS and proper key order
def export_cleaned_geojson(gdf, original_crs, original_name):
    gdf.set_crs(original_crs, inplace=True)
    cleaned_data = json.loads(gdf.to_json())
    cleaned_data["crs"] = {"type": "name", "properties": { "name": str(original_crs.to_string())} }

    output = {
        "type": cleaned_data.get("type", "FeatureCollection"),
        "name": original_name,
        "crs": cleaned_data["crs"],
        "features": cleaned_data.get("features", [])
    }

    return json.dumps(output)


# Create a folium map with polygons from the GeoDataFrame
def add_folium_map(gdf, center):
    m = folium.Map(location=center, zoom_start=16, tiles="Esri.WorldImagery")

    # Add polygons from processed gdf and style them
    folium.GeoJson(gdf,
                   style_function=lambda x: {"fillColor": "orange", "color": "orange", "weight": 1},
                   tooltip=folium.GeoJsonTooltip(fields=["fid", "producttype"], aliases=["FID:", "Product:"]),
    ).add_to(m)

    # Add fullscreen button
    Fullscreen(position="topleft", title="Expand", title_cancel="Exit Fullscreen").add_to(m)

    return m