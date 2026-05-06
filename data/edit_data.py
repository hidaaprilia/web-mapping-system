import pandas as pd
import geopandas as gpd

# 1. Baca data GeoJSON
gdf = gpd.read_file("data/final_sls_202311507.geojson")

# 2. Baca file Excel
df_excel = pd.read_excel("data/Data_Hasil_Identifikasi_DSSLS.xlsx")  # ganti dengan nama filenya

# 3. Pastikan kolom `idsls` berupa string (agar cocok saat merge)
gdf["idsls"] = gdf["idsls"].astype(str)
df_excel["idsls"] = df_excel["idsls"].astype(str)

# 4. Gabungkan berdasarkan kolom `idsls`
gdf_merged = gdf.merge(df_excel, on="idsls", how="left")

# 5. Simpan hasilnya jika perlu
gdf_merged.to_file("data/gabungan_output_sls.geojson", driver="GeoJSON")
