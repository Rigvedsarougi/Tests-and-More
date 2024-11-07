# app.py
import streamlit as st
from overlay import overlay_receipt_on_letterhead
import tempfile
import os

# Streamlit application
st.title("PDF Overlay Application")

# File upload for the receipt and letterhead
receipt_file = st.file_uploader("Upload Receipt PDF", type="pdf")
letterhead_file = st.file_uploader("Upload Letterhead PDF", type="pdf")

# Display default transformation values and allow user customization
up_movement = st.number_input("Up Movement", value=0)
down_movement = st.number_input("Down Movement", value=170)
left_movement = st.number_input("Left Movement", value=0)
right_movement = st.number_input("Right Movement", value=0)
scale_increase = st.number_input("Scale Increase", value=0.05)
scale_decrease = st.number_input("Scale Decrease", value=0.0)

# Button to generate the overlay
if st.button("Generate PDF") and receipt_file and letterhead_file:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as receipt_temp, \
         tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as letterhead_temp, \
         tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as output_temp:

        # Write uploaded files to temporary files
        receipt_temp.write(receipt_file.read())
        letterhead_temp.write(letterhead_file.read())
        
        # Close files so they can be re-opened by the overlay function
        receipt_temp.close()
        letterhead_temp.close()

        # Perform overlay operation
        overlay_receipt_on_letterhead(
            receipt_path=receipt_temp.name,
            letterhead_path=letterhead_temp.name,
            output_path=output_temp.name,
            up=up_movement,
            down=down_movement,
            left=left_movement,
            right=right_movement,
            scale_increase=scale_increase,
            scale_decrease=scale_decrease
        )

        # Allow user to download the output file
        with open(output_temp.name, "rb") as result_pdf:
            st.download_button("Download Output PDF", data=result_pdf, file_name="output.pdf", mime="application/pdf")

    # Clean up temporary files
    os.remove(receipt_temp.name)
    os.remove(letterhead_temp.name)
    os.remove(output_temp.name)