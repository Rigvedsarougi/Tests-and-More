from PyPDF2 import PdfReader, PdfWriter, Transformation

def overlay_receipt_on_letterhead(receipt_path, letterhead_path, output_path, 
                                  up=0, down=0, left=0, right=0, 
                                  scale_increase=0.0, scale_decrease=0.0):
    """
    Overlays each page of a multi-page receipt PDF onto corresponding pages of a letterhead PDF 
    with custom positioning and size adjustments.

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
        # Use a blank page if a PDF has fewer pages than max_pages
        if i < len(receipt_pdf.pages):
            receipt_page = receipt_pdf.pages[i]
        else:
            # Create a blank page with the same size as the first letterhead page
            receipt_page = PdfWriter().add_blank_page(
                width=letterhead_pdf.pages[0].mediabox.width,
                height=letterhead_pdf.pages[0].mediabox.height
            )

        if i < len(letterhead_pdf.pages):
            letterhead_page = letterhead_pdf.pages[i]
        else:
            # Create a blank page with the same size as the first receipt page
            letterhead_page = PdfWriter().add_blank_page(
                width=receipt_page.mediabox.width,
                height=receipt_page.mediabox.height
            )

        # Apply transformations to the receipt page
        transformation = Transformation().scale(scale).translate(x_position, y_position)
        receipt_page.add_transformation(transformation)

        # Merge the transformed receipt onto the letterhead page
        letterhead_page.merge_page(receipt_page)

        # Add the merged page to the writer
        writer.add_page(letterhead_page)

    # Save the resulting combined PDF
    with open(output_path, "wb") as output_file:
        writer.write(output_file)
