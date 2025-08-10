import streamlit as st
import base64

# Baca file PDF
pdf_file = open("document/Panduan penggunaan web mapping system.pdf", "rb")
pdf_bytes = pdf_file.read()

# Encode ke base64
base64_pdf = base64.b64encode(pdf_bytes).decode('utf-8')

# Buat iframe HTML
pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="800" type="application/pdf"></iframe>'
st.markdown(pdf_display, unsafe_allow_html=True)
