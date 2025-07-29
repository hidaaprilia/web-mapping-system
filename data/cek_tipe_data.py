import geopandas as gpd

# Baca file GeoJSON
gdf = gpd.read_file("data/gabungan_output_sls.geojson")

# Tampilkan tipe data tiap kolom
print(gdf.dtypes)

print(gdf['idsls'].head())
