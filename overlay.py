from PyPDF2 import PdfReader, PdfWriter, Transformation

def overlay_receipt_on_letterhead(receipt_path, letterhead_path, output_path, 
                                  up=0, down=0, left=0, right=0, 
                                  scale_increase=0.0, scale_decrease=0.0):
    """
    Overlays each page of a multi-page receipt PDF onto corresponding pages of a letterhead PDF 
    with custom positioning and size adjustments, ensuring the letterhead background appears 
    on all pages.

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
    # Load PDFs
    receipt_pdf = PdfReader(receipt_path)
    letterhead_pdf = PdfReader(letterhead_path)
    writer = PdfWriter()

    # Calculate transformations
    x_position = right - left
    y_position = up - down
    scale = 1.0 + scale_increase - scale_decrease

    # Determine the maximum number of pages to overlay
    max_pages = max(len(receipt_pdf.pages), len(letterhead_pdf.pages))

    for i in range(max_pages):
        # Select the current page for the receipt, or a blank page if out of pages
        if i < len(receipt_pdf.pages):
            receipt_page = receipt_pdf.pages[i]
        else:
            receipt_page = PdfWriter().add_blank_page(
                width=letterhead_pdf.pages[0].mediabox.width,
                height=letterhead_pdf.pages[0].mediabox.height
            )

        # Select the corresponding letterhead page, or reuse the last letterhead page if out of pages
        if i < len(letterhead_pdf.pages):
            letterhead_page = letterhead_pdf.pages[i]
        else:
            letterhead_page = letterhead_pdf.pages[-1]

        # Apply transformations to the receipt page
        transformation = Transformation().scale(scale).translate(x_position, y_position)
        receipt_page.add_transformation(transformation)

        # Create a copy of the letterhead page to avoid altering the original
        merged_page = letterhead_page.copy()

        # Merge the transformed receipt onto the letterhead page copy
        merged_page.merge_page(receipt_page)

        # Add the merged page to the writer
        writer.add_page(merged_page)

    # Save the resulting combined PDF
    with open(output_path, "wb") as output_file:
        writer.write(output_file)
