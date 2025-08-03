import streamlit as st
import geopandas as gpd
import pandas as pd
import leafmap.foliumap as leafmap
from folium.features import GeoJsonTooltip

st.set_page_config(layout="wide")

# Path ke file GeoJSON
geojson_path = "data/gabungan_output_sls.geojson"

# Baca file GeoJSON
try:
    geojson_data = gpd.read_file(geojson_path)
    # st.success("File GeoJSON berhasil dimuat.")
except Exception as e:
    st.error(f"Error saat membaca GeoJSON: {e}")

# Layout untuk tiga bagian: kiri, tengah, kanan
col1, col2, col3 = st.columns([1, 2, 1])

# Variabel global untuk nama kecamatan dan nama desa yang dipilih, variabel pengganti bs
selected_nmkec = []
selected_nmdesa = []
search_idsls = []
replacement_results = []

# Inisialisasi session_state jika belum ada
if "replacement_results" not in st.session_state:
    st.session_state.replacement_results = []


# Kolom kiri (Input Upload dan Filter)
with col1:
    st.header("Upload dan Filter")

    # --- FITUR PENCARIAN DAN FILTER ---
    st.markdown("### Filter Tanpa Upload File")

    # Input teks untuk cari idsls langsung
    search_idsls = st.text_input("Cari idsls:")

    # Ambil daftar unik kecamatan dan desa dari geojson_data
    all_kecamatan = geojson_data["nmkec"].dropna().unique().tolist()
    all_kecamatan.sort()
    selected_nmkec = st.multiselect("Filter Kecamatan:", options=all_kecamatan, default=[])

    # Filter awal berdasarkan kecamatan jika dipilih
    filtered_geojson = geojson_data.copy()
    if selected_nmkec:
        filtered_geojson = filtered_geojson[filtered_geojson["nmkec"].isin(selected_nmkec)]

    # Ambil daftar desa dari hasil filter kecamatan
    all_desa = filtered_geojson["nmdesa"].dropna().unique().tolist()
    all_desa.sort()
    selected_nmdesa = st.multiselect("Filter Desa:", options=all_desa, default=[])

    # Filter lanjutan berdasarkan desa
    if selected_nmdesa:
        filtered_geojson = filtered_geojson[filtered_geojson["nmdesa"].isin(selected_nmdesa)]

    # Filter berdasarkan pencarian idsls (mengandung string dari input)
    if search_idsls:
        filtered_geojson = filtered_geojson[filtered_geojson["idsls"].astype(str).str.contains(search_idsls)]

    # Upload file Excel atau CSV
    uploaded_file = st.file_uploader("Upload file dengan kolom 'idsls':", type=["xlsx", "csv"])

    # Jika file diunggah, baca data dan ekstrak kolom 'idsls'
    if uploaded_file:
        if uploaded_file.name.endswith(".xlsx"):
            uploaded_data = pd.read_excel(uploaded_file)
        elif uploaded_file.name.endswith(".csv"):
            uploaded_data = pd.read_csv(uploaded_file)
        
        if "idsls" in uploaded_data.columns:
            # Cocokkan 'idsls' dengan data GeoJSON
            matched_geojson = geojson_data[geojson_data["idsls"].isin(uploaded_data["idsls"])]
            
            # Ambil daftar nama kecamatan unik dari hasil yang cocok
            nmkec_list = matched_geojson["nmkec"].unique().tolist()
            nmkec_list.sort()

            # Filter berdasarkan kecamatan
            if selected_nmkec:
                filtered_geojson = matched_geojson[matched_geojson["nmkec"].isin(selected_nmkec)]
            else:
                filtered_geojson = matched_geojson

            # Ambil daftar nama desa berdasarkan hasil filter kecamatan
            nmdesa_list = filtered_geojson["nmdesa"].unique().tolist()
            nmdesa_list.sort()

            # Filter akhir berdasarkan desa jika ada
            if selected_nmdesa:
                final_geojson = filtered_geojson[filtered_geojson["nmdesa"].isin(selected_nmdesa)]
            else:
                final_geojson = filtered_geojson

        else:
            st.error("Kolom 'idsls' tidak ditemukan di file yang diunggah.")
    else:
        st.warning("Silakan unggah file untuk memulai.")

    # Simpan ke dalam final_geojson jika tidak upload
    if not uploaded_file:
        final_geojson = filtered_geojson.copy()

# Kolom tengah (Peta)
with col2:
    st.header("Peta SLS")

    # Dropdown untuk memilih basemap
    tooltip_fields = ["idsls", "kdsls", "nmsls", "nmdesa", "nmkec", "luas", "kk", "bstt", "bstt_k", "bsbtt", "muatan", "dom_sls"]
    basemap_options = list(leafmap.basemaps.keys())
    basemap = st.selectbox("Pilih Basemap:", basemap_options, index=basemap_options.index("SATELLITE"))

    # Inisialisasi peta
    m = leafmap.Map(
        locate_control=True, latlon_control=True, draw_export=True, minimap_control=True
    )

    if search_idsls:
        data_to_display = filtered_geojson
    elif selected_nmdesa:
        data_to_display = final_geojson
    elif selected_nmkec:
        data_to_display = filtered_geojson
    elif uploaded_file:
        data_to_display = matched_geojson
    else:
        data_to_display = geojson_data   

    # Filter GeoDataFrame untuk tooltip
    columns_to_keep = tooltip_fields + ["geometry"]
    gdf_for_map = data_to_display[columns_to_keep]

    # Tambahkan ke peta dengan tooltip sebagai bagian dari style
    m.add_gdf(
        gdf_for_map,
        layer_name="SLS Terfilter",
        info_mode="on_hover",  # Sudah cukup untuk hover info default
    )

    if "replacement_results" in st.session_state and st.session_state.replacement_results:
        df_replace_df = pd.DataFrame(st.session_state.replacement_results)
        idsls_pengganti_list = df_replace_df["IDSLS Pengganti"].dropna().unique().tolist()

        # Filter GeoJSON untuk mendapatkan geometri SLS pengganti
        gdf_pengganti = geojson_data[geojson_data["idsls"].isin(idsls_pengganti_list)]
        gdf_for_map = gdf_pengganti[columns_to_keep]

        if not gdf_pengganti.empty:
            m.add_gdf(
                gdf_for_map,
                layer_name="SLS Pengganti",
                style={"color": "red", "fillColor": "red", "fillOpacity": 0.5},
                info_mode="on_hover",
            )
    
    m.add_basemap(basemap)
    m.to_streamlit(height=600)

# Kolom kanan (Detail Data)
with col3:
    st.header("Detail Data")
    tab1, tab2, tab3 = st.tabs(["Detail SLS", "List SLS", "Ganti SLS"])

    with tab1:
        st.subheader("Detail Atribut SLS")
        if search_idsls:
            st.dataframe(filtered_geojson)
        elif selected_nmdesa:
            st.dataframe(final_geojson)
        elif selected_nmkec:
            st.dataframe(filtered_geojson)
        elif uploaded_file:
            st.dataframe(matched_geojson)
        else:
            st.dataframe(geojson_data.head(10))
    
    with tab2:
        st.subheader("List BS")
        if search_idsls:
            st.write(filtered_geojson["idsls"].tolist())
        elif selected_nmdesa:
            st.write(final_geojson["idsls"].tolist())
        elif selected_nmkec:
            st.write(filtered_geojson["idsls"].tolist())
        elif uploaded_file:
            st.write(matched_geojson["idsls"].tolist())
        else:
            st.write(geojson_data["idsls"].tolist())

    with tab3:
        st.subheader("Ganti SLS (Batch Mode)")
        from sklearn.ensemble import RandomForestClassifier
        from sklearn.preprocessing import StandardScaler

        # Tentukan list idsls yang akan jadi opsi multiselect
        if uploaded_file is not None and "idsls" in matched_geojson:
            idsls_options = matched_geojson["idsls"].unique()
        elif filtered_geojson is not None and "idsls" in filtered_geojson:
            idsls_options = filtered_geojson["idsls"].unique()
        elif final_geojson is not None and "idsls" in final_geojson:
            idsls_options = final_geojson["idsls"].unique()
        else:
            idsls_options = []

        # Ambil daftar idsls dan filter jika ada pencarian
        idsls_selected = st.multiselect(
            "Pilih beberapa SLS yang ingin diganti:",
            options=idsls_options
        )

        # 2. PILIH METODE PENGGANTIAN
        replace_method = st.radio("Pilih Metode:", ["Pilih Manual", "Rekomendasi Sistem"])

        # 4. METODE MANUAL
        if replace_method == "Pilih Manual":
            st.markdown("### Input Manual untuk Pengganti")
            idsls_pengganti = []
            for i, idsls in enumerate(idsls_selected):
                new_idsls = st.selectbox(f"Pengganti untuk {idsls}:", geojson_data["idsls"].unique(), key=f"manual_{i}")
                idsls_pengganti.append({
                    "IDSLS Lama": idsls,
                    "IDSLS Pengganti": new_idsls,
                    "Metode": "Manual",
                    "Keterangan": "Dipilih manual"
                })
            st.session_state.replacement_results = idsls_pengganti

        # 5. METODE REKOMENDASI SISTEM
        elif replace_method == "Rekomendasi Sistem" and st.button("Cari Rekomendasi"):
            st.session_state.replacement_results = []

            try:
                feature_cols = ["kdkec", "kddesa", "luas"]  # Kolom numerik, sesuaikan

                # Filter & bersihkan data
                all_bs = geojson_data.dropna(subset=["idsls"]).copy()
                X = all_bs[feature_cols].copy()
                for col in feature_cols:
                    X[col] = pd.to_numeric(X[col], errors="coerce")
                X = X.dropna()
                valid_index = X.index
                y = all_bs.loc[valid_index, "idsls"]

                scaler = StandardScaler()
                X_scaled = scaler.fit_transform(X)

                model = RandomForestClassifier(n_estimators=100, random_state=42)
                model.fit(X_scaled, y)

                for idsls in idsls_selected:
                    bs_ganti_row = all_bs[all_bs["idsls"] == idsls]
                    bs_X = bs_ganti_row[feature_cols].copy()
                    for col in feature_cols:
                        bs_X[col] = pd.to_numeric(bs_X[col], errors="coerce")

                    if bs_X.isnull().values.any() or bs_X.empty:
                        st.session_state.replacement_results.append({
                            "IDSLS Lama": idsls,
                            "IDSLS Pengganti": "-",
                            "Metode": "Sistem",
                            "Keterangan": "Data tidak lengkap"
                        })
                        continue

                    bs_scaled = scaler.transform(bs_X)
                    probs = model.predict_proba(bs_scaled)[0]
                    classes = model.classes_

                    sorted_idx = probs.argsort()[::-1]
                    rekomendasi = [cls for cls in classes[sorted_idx] if cls != idsls]

                    if rekomendasi:
                        st.session_state.replacement_results.append({
                            "IDSLS Lama": idsls,
                            "IDSLS Pengganti": rekomendasi[0],
                            "Metode": "Sistem",
                            "Keterangan": "Rekomendasi berdasarkan kemiripan"
                        })
                    else:
                        st.session_state.replacement_results.append({
                            "IDSLS Lama": idsls,
                            "IDSLS Pengganti": "-",
                            "Metode": "Sistem",
                            "Keterangan": "Tidak ada rekomendasi"
                        })

            except Exception as e:
                st.error(f"Terjadi kesalahan saat memproses rekomendasi: {e}")

        # 6. TAMPILKAN TABEL RINGKASAN
        if st.session_state.replacement_results:
            st.markdown("### Tabel Ringkasan Penggantian SLS")
            df_replace = pd.DataFrame(st.session_state.replacement_results)
            st.dataframe(df_replace, use_container_width=True)

            # Export button
            csv = df_replace.to_csv(index=False).encode('utf-8')
            st.download_button("📥 Download Tabel Penggantian", data=csv, file_name="penggantian_bs.csv", mime='text/csv')
