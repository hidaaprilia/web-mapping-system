import streamlit as st

def show_navbar():
    st.set_page_config(layout="wide")

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
        </style>
    """, unsafe_allow_html=True)

    # Inisialisasi state halaman
    if "page" not in st.session_state:
        st.session_state.page = "Peta_Blok_Sensus"

    with st.container():
        # Inisialisasi state
        if 'page' not in st.session_state:
            st.session_state.page = "Peta_Blok_Sensus"
            
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