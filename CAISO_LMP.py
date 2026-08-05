"""
Developed by Greg Miller, grmiller@ucdavis.edu
Version 2 (refactor by Dawson Verley, verley@berkeley.edu)
Last Updated July 2026

Purpose: To create a shapefile and CSV file of Locational Marginal Pricing (LMP) Nodes
in CAISO and the Western Energy Imbalance Market (WEIM) footprint. 

Data from the CAISO price contour map, available at the following URL:
http://wwwmobile.caiso.com/Web.Service.Chart/pricecontourmap.html
"""

from pathlib import Path
import geopandas as gpd
import pandas as pd
import requests

# Hard-coded configuration
PRICE_MAP_URL = "http://wwwmobile.caiso.com/Web.Service.Chart/api/v3/ChartService/PriceContourMap1"
LMP_CSV = Path.cwd() / "LMP_coordinates.csv"
LMP_SHP = Path.cwd() / "LMP/caiso_lmp.shp"

def clean_coordinates(coord_array):
    """
    Cleans coordinate pairs to ensure standard [latitude, longitude] ordering
    where latitude is positive and longitude is negative.
    """
    val0 = float(coord_array[0])
    val1 = float(coord_array[1])
    
    if val0 > 0 and val1 < 0:
        lat = val0
        lon = val1
    elif val0 < 0 and val1 > 0:
        lat = val1
        lon = val0
    elif val0 > 0 and val1 > 0:
        if val0 > val1:
            lat = val1
            lon = -val0
        else:
            lat = val0
            lon = -val1
    else:
        lat = abs(val0)
        lon = -abs(val1)
        
    return lat, lon

def get_lmp_loc():
    """
    Returns a list of dictionaries containing node data.
    Each dictionary has the following attributes:
    {
        'node_id': <name of the node>,
        'latitude': <latitude of the node>,
        'longitude': <longitude of the node>,
        'area': <control area the node belongs to>,
        'node_type': <node type>
    }
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
    }
    
    # Get JSON from the CAISO price map URL
    response = requests.get(PRICE_MAP_URL, headers=headers, timeout=20)
    response.raise_for_status()
    json_obj = response.json()

    # Parse the json to create the node location list
    node_entries = json_obj['l'][2]['m']
    
    return_list = []
    for entry in node_entries:
        if 'n' in entry and 'c' in entry and len(entry['c']) >= 2:
            lat, lon = clean_coordinates(entry['c'])
            return_list.append({
                'node_id': str(entry['n']),
                'latitude': lat,
                'longitude': lon,
                'area': str(entry['a']),
                'node_type': str(entry['p'])
            })
    return return_list

def main():
    try:
        print("Fetching LMP data from CAISO...")
        lmp_dict = get_lmp_loc()
        df_lmp = pd.DataFrame.from_dict(lmp_dict)
        
        # Reorder columns to match original: area, latitude, longitude, node_id, node_type
        column_order = ['area', 'latitude', 'longitude', 'node_id', 'node_type']
        df_lmp = df_lmp.reindex(columns=column_order)
        
        # Write CSV
        print(f"Writing CSV to {LMP_CSV}...")
        LMP_CSV.parent.mkdir(parents=True, exist_ok=True)
        df_lmp.to_csv(LMP_CSV, index=False, lineterminator='\n')
        
        # Write Shapefile using GeoPandas
        print(f"Writing Shapefile to {LMP_SHP}...")
        LMP_SHP.parent.mkdir(parents=True, exist_ok=True)
        
        # Convert to GeoDataFrame (WGS84 EPSG:4326)
        gdf = gpd.GeoDataFrame(
            df_lmp,
            geometry=gpd.points_from_xy(df_lmp['longitude'], df_lmp['latitude']),
            crs="EPSG:4326"
        )
        
        # Select and rename columns to match the original shapefile schema
        gdf_shp = gdf[['area', 'node_id', 'node_type', 'geometry']].rename(
            columns={
                'area': 'AREA',
                'node_id': 'NODE_ID',
                'node_type': 'TYPE'
            }
        )
        
        gdf_shp.to_file(LMP_SHP, driver="ESRI Shapefile", engine="pyogrio")
        print("CSV and Shapefile successfully created.")
    
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
