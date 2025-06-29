import streamlit as st
from streamlit_folium import st_folium
import requests
from io import BytesIO
from utils import (read_geojson_to_gdf, validate_and_fix_geometries, remove_exact_duplicates, remove_near_duplicates,
                   export_cleaned_geojson, add_folium_map)


# Set app layout to wide screen mode
st.set_page_config(layout="wide")

st.title("GeoJSON Cleaning Dashboard")

# 📂 Upload file or use sample
st.markdown("## 📂 Upload your GeoJSON file or use a sample GeoJSON")

col2, col1 = st.columns([0.1, 0.9], gap="small", vertical_alignment="center")

with col1:
    uploaded_file = st.file_uploader("Upload GeoJSON file", type=["geojson"])

with col2:
    use_sample = st.button("📄 Use sample file")

# Initialize session state for sample file
if "sample_file" not in st.session_state:
    st.session_state["sample_file"] = None

# Load sample file if selected
if use_sample:
    sample_url = "https://raw.githubusercontent.com/viktor-ko/GeoJSON_Cleaner_Dashboard/refs/heads/master/Farm_file.geojson"
    response = requests.get(sample_url)
    if response.status_code == 200:
        sample_file = BytesIO(response.content)
        sample_file.name = "Sample_Farm_file.geojson"
        st.session_state["sample_file"] = sample_file
    else:
        st.error("❌ Failed to fetch sample file.")


file_to_process = uploaded_file or st.session_state["sample_file"]

if file_to_process:
    original_name, gdf, original_crs, original_json = read_geojson_to_gdf(file_to_process)

    logs = st.expander("📝 Show Cleaning Logs", expanded=True)

    with logs:
        st.success("✅ File uploaded. Processing...")

        st.markdown("#### Validating and fixing polygons geometry...")
        gdf = validate_and_fix_geometries(gdf, st)

        st.markdown("#### Removing duplicate polygons...")
        gdf = remove_exact_duplicates(gdf, st)

        st.markdown("#### Removing nearly identical polygons...")
        gdf = remove_near_duplicates(gdf, st)

        st.success("✅ Cleaning complete!")

    cleaned_json_str = export_cleaned_geojson(gdf, original_crs, file_to_process.name)

    #Oranise the dashboard in two equal columns for tables and map
    tables, leaflet_map = st.columns([1, 1])

    with tables:
        st.subheader("Original GeoJSON:")
        try:
            original_features = original_json.get("features", [])
            if original_features:
                # Extract properties for display from uploaded GeoJSON
                original_table_data = [f.get("properties", {}) for f in original_features]
                st.dataframe(original_table_data, use_container_width=True)
            else:
                st.warning("No features found in uploaded file.")
        except Exception as e:
            st.error(f"Failed to extract features from uploaded GeoJSON: {e}")

        st.subheader("GeoJSON after cleaning:")
        try:
            # exclude id and geometry columns for more clean look
            display_gdf = gdf.drop(columns=["id", "geometry"], errors="ignore")

            st.dataframe(display_gdf, use_container_width=True, hide_index=True)
        except Exception as e:
            st.error(f"Failed to display cleaned data: {e}")

        # Add option to download cleaned GeoJSON
        st.download_button(
            label="💾 Download cleaned GeoJSON",
            data=cleaned_json_str,
            file_name="cleaned_polygons.geojson",
        )

    with leaflet_map:
        # Add a dropdown menu for zooming to a specific polygon from list
        index_options = gdf.index.tolist()
        selected_idx = st.selectbox("Select a polygon to zoom to", label_visibility="hidden", options=index_options,
                                    format_func=lambda x: f"Zoom to polygon fid {gdf.iloc[x].fid}")

        # Use selected feature's centroid to center the map
        centroid = gdf.geometry.iloc[selected_idx].centroid
        center = [centroid.y, centroid.x]

        #Add map with polygons
        m = add_folium_map(gdf, center=center)
        st_folium(m, width=700, height=500)