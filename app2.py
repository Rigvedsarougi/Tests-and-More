# app.py (modifications for target page input)
import streamlit as st
from overlay1 import overlay_receipt_on_letterhead
import tempfile
import os

# Streamlit application
st.title("PDF Overlay Application")

receipt_file = st.file_uploader("Upload Receipt PDF", type="pdf")
letterhead_file = st.file_uploader("Upload Letterhead PDF (optional)", type="pdf")

up_movement = st.number_input("Up Movement", value=0)
down_movement = st.number_input("Down Movement", value=170)
left_movement = st.number_input("Left Movement", value=0)
right_movement = st.number_input("Right Movement", value=0)
scale_increase = st.number_input("Scale Increase", value=0.05)
scale_decrease = st.number_input("Scale Decrease", value=0.0)
target_page = st.number_input("Target Page (leave blank for all pages)", min_value=1, value=1)

if st.button("Generate PDF") and receipt_file:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as receipt_temp, \
         tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as output_temp:

        receipt_temp.write(receipt_file.read())
        receipt_temp.close()

        letterhead_path = DEFAULT_LETTERHEAD_PATH
        if letterhead_file:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as letterhead_temp:
                letterhead_temp.write(letterhead_file.read())
                letterhead_temp.close()
                letterhead_path = letterhead_temp.name

        overlay_receipt_on_letterhead(
            receipt_path=receipt_temp.name,
            letterhead_path=letterhead_path,
            output_path=output_temp.name,
            up=up_movement,
            down=down_movement,
            left=left_movement,
            right=right_movement,
            scale_increase=scale_increase,
            scale_decrease=scale_decrease,
            target_page=target_page if target_page else None
        )

        with open(output_temp.name, "rb") as result_pdf:
            st.download_button("Download Output PDF", data=result_pdf, file_name="output.pdf", mime="application/pdf")

    os.remove(receipt_temp.name)
    if letterhead_file:
        os.remove(letterhead_temp.name)
    os.remove(output_temp.name)
