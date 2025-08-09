import base64
import streamlit as st
import importlib.util

# Konfigurasi halaman
st.set_page_config(page_title="Web Mapping System", layout="wide")

# CSS: Sembunyikan sidebar dan ubah font
st.markdown("""
    <style>
        [data-testid="stSidebar"] {
            display: none;
        }

        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');

        html, body, [class*="css"] {
            font-family: 'Inter', sans-serif;
        }
            
        div.stButton > button {
            background-color: none;
            color: black;
            border: none;
            border-radius: 1px;
            padding: 2px 0px; /* lebih kecil */
            margin-bottom: 0px;
            font-size: 14px;
            font-weight: 500;
            line-height: 1.2; /* lebih rapat */
        }

        h5 {
            margin: 0; /* hilangkan margin bawaan */
        }

        hr {
            margin-top: 0px; /* jarak ke atas kecil */
            margin-bottom: 0px; /* jarak ke bawah kecil */
        }

        .explore-button {
            background-color: #FFD60A;
            color: black;
            padding: 0.5rem 1.2rem;
            font-weight: bold;
            border: none;
            border-radius: 8px;
            font-size: 16px;
            cursor: pointer;
        }

        .left-text {
            padding-left: 30px;
            padding-top: 30px;
        }

        .right-img {
            display: flex;
            justify-content: flex-end;
            overflow: visible;
        }

        .right-img img {
            width: 100%;
            max-width: none;
            margin: 0;
            padding: 0;
            object-fit: contain;
        }


        @media (max-width: 768px) {
            .right-img img {
                float: none;
                margin: auto;
            }
        }
            
        .fitur-box {
            background-color: #F0FFFF;
            padding: 1.5rem;
            border-radius: 1.25rem;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: start;
            height: 100%;
            min-height: 220px;
            box-sizing: border-box;
            text-align: center;
            padding: 20px;
            border-radius: 12px;
            transition: background-color 0.2s ease;
        }
        .fitur-box:hover {
            background-color: #CFF6F4;
        }
        .fitur-title {
            font-size: 16px;
            font-weight: bold;
            margin-top: 10px;
        }
        .fitur-desc {
            font-size: 13px;
            color: #555;
        }

    </style>
""", unsafe_allow_html=True)

# Inisialisasi state halaman
if "page" not in st.session_state:
    st.session_state.page = "Home"

with st.container():
    # Inisialisasi state
    if 'page' not in st.session_state:
        st.session_state.page = "Home"
        
    logo, nav_title, nav1, nav2, nav3, nav4 = st.columns([0.3, 3.7, 1, 1.4, 1, 1])

    with logo:
        st.image("images/4.png", width=40)

    with nav_title:
        st.markdown("<h5 style='margin:0px;'>Web Mapping System</h5>", unsafe_allow_html=True)

    with nav1:
        if st.button("Home"):
            st.session_state.page = "Home"

    with nav2:
        if st.button("Peta Blok Sensus"):
            st.session_state.page = "Peta_Blok_Sensus"

    with nav3:
        if st.button("Peta SLS"):
            st.session_state.page = "Peta_SLS"

    with nav4:
        if st.button("Panduan"):
            st.session_state.page = "Panduan"

    st.markdown("---")

# Halaman HOME
if st.session_state.page == "Home":
    def image_to_base64(path):
        with open(path, "rb") as f:
            data = f.read()
            return base64.b64encode(data).decode()
        
    img1 = image_to_base64("images/1.png")
    img2 = image_to_base64("images/2.png")
    img3 = image_to_base64("images/3.png")
    header = image_to_base64("images/header.png")

    # Layout
    col1, col2 = st.columns([1, 1.2])

    with col1:
        st.markdown("""
            <div class="left-text">
                <h2>Web Mapping System</h2>
                <p>Aplikasi ini dirancang untuk mempermudah proses identifikasi dan pengelolaan wilayah kerja statistik secara spasial. 
                Dengan antarmuka interaktif, pengguna dapat mengunggah data sampel, menampilkan peta blok sensus atau SLS, memfilter wilayah, 
                melihat detail atribut, serta mengusulkan penggantian wilayah berdasarkan analisis sistem.</p>
                <button class="explore-button">Let’s explore</button>
            </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div style="width: 100%; display: flex; justify-content: flex-end; margin: 0; padding: 0;">
            <img src="data:image/png;base64,{header}" style="width: 40vw; max-width: none; margin: 0; padding: 0;" />
        </div>
        """, unsafe_allow_html=True)


    st.markdown("### ")

    query_params = st.query_params
    if "page" in query_params:
        if query_params["page"] == "Peta_BS":
            st.switch_page("pages/Peta_Blok_Sensus.py")
        elif query_params["page"] == "Peta_SLS":
            st.switch_page("pages/Peta_SLS.py") 
        elif query_params["page"] == "Panduan":
            st.switch_page("pages/Panduan.py")  
            
    fitur1, fitur2, fitur3 = st.columns(3)

    with fitur1:
        st.markdown(f"""
            <a href="?page=Peta_BS" style="text-decoration: none; color: inherit;">
                <div class="fitur-box" style="cursor: pointer;">
                    <img src="data:image/png;base64,{img1}" width="90"/>
                    <div class="fitur-title" style="color: black;">Peta Blok Sensus</div>
                    <div class="fitur-desc">Menampilkan Peta Blok Sensus</div>
                </div>
            </a>
            """, unsafe_allow_html=True)
        
    with fitur2:
        st.markdown(f"""
            <a href="?page=Peta_SLS" style="text-decoration: none; color: inherit;">
                <div class="fitur-box" style="cursor: pointer;">
                    <img src="data:image/png;base64,{img2}" width="90"/>
                    <div class="fitur-title" style="color: black;">Peta SLS</div>
                    <div class="fitur-desc">Menampilkan Peta Satuan Lingkungan Setempat</div>
                </div>
            </a>
            """, unsafe_allow_html=True)
        

    with fitur3:
        st.markdown(f"""
            <a href="?page=Panduan" style="text-decoration: none; color: inherit;">
                <div class="fitur-box" style="cursor: pointer;">
                    <img src="data:image/png;base64,{img3}" width="90"/>
                    <div class="fitur-title" style="color: black;">Panduan</div>
                    <div class="fitur-desc">Petunjuk dan Panduan Penggunaan</div>
                </div>
            </a>
            """, unsafe_allow_html=True)

# Fungsi untuk load file Python dari folder /pages
def load_page(page_name):
    file_path = f"pages/{page_name}.py"
    spec = importlib.util.spec_from_file_location("page", file_path)
    page = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(page)

# Load halaman sesuai pilihan
if st.session_state.page in ["Peta_Blok_Sensus", "Peta_SLS", "Panduan"]:
    load_page(st.session_state.page)
    
# Halaman PANDUAN
elif st.session_state.page == "Panduan":
    st.header("📘 Panduan Penggunaan")
    st.write("""
    Berikut adalah panduan penggunaan aplikasi pemetaan blok sensus:
    
    1. Klik "Peta Blok Sensus" untuk melihat seluruh blok dalam satu wilayah.
    2. Gunakan filter wilayah untuk melihat blok tertentu.
    3. Gunakan "Peta SLS" untuk melihat detail satuan lingkungan setempat.
    4. Gunakan fitur interaktif untuk merekomendasikan penggantian BS.
    """)

