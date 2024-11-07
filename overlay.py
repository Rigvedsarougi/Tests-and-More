# overlay.py
from PyPDF2 import PdfReader, PdfWriter, Transformation

def overlay_receipt_on_letterhead(receipt_path, letterhead_path, output_path, 
                                  up=0, down=0, left=0, right=0, 
                                  scale_increase=0.0, scale_decrease=0.0):
    """
    Overlays a receipt PDF onto a letterhead PDF with custom positioning and size adjustments.

    Parameters:
        receipt_path (str): Path to the receipt PDF.
        letterhead_path (str): Path to the letterhead PDF.
        output_path (str): Path to save the output PDF.
        up (float): Amount to move up in points.
        down (float): Amount to move down in points.
        left (float): Amount to move left in points.
        right (float): Amount to move right in points.
        scale_increase (float): Factor to increase the scale (e.g., 0.1 for 10%).
        scale_decrease (float): Factor to decrease the scale (e.g., 0.1 for 10%).
    """
    receipt_pdf = PdfReader(receipt_path)
    letterhead_pdf = PdfReader(letterhead_path)
    writer = PdfWriter()

    x_position = right - left
    y_position = up - down
    scale = 1.0 + scale_increase - scale_decrease

    if len(receipt_pdf.pages) > 0 and len(letterhead_pdf.pages) > 0:
        letterhead_page = letterhead_pdf.pages[0]
        receipt_page = receipt_pdf.pages[0]

        transformation = Transformation().scale(scale).translate(x_position, y_position)
        receipt_page.add_transformation(transformation)

        letterhead_page.merge_page(receipt_page)
        writer.add_page(letterhead_page)

    with open(output_path, "wb") as output_file:
        writer.write(output_file)
