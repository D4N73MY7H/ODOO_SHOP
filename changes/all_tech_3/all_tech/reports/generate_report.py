# from reportlab.lib.pagesizes import letter
# from reportlab.pdfgen import canvas
# # from reportlab.lib.utils import ImageReader
# from io import BytesIO
# from datetime import date
# # import base64
# from reportlab.pdfbase import pdfmetrics
# from reportlab.pdfbase.ttfonts import TTFont
# from reportlab.platypus import Table, TableStyle
# from reportlab.lib import colors
#
# pdfmetrics.registerFont(TTFont('Vera', 'Vera.ttf'))
# pdfmetrics.registerFont(TTFont('VeraBd', 'VeraBd.ttf'))
#
#
# def generate_pdf(info, extra):
#     data = [['NO.', 'DATE', 'CUSTOMER', 'REMAINING TOTAL', 'Total', 'State']]
#     data += info.get('invoices', [])
#
#     extra_data = [['NUM', 'DRAFT', 'PAYING', 'PAID', 'CANCELLED', 'REMAINING', 'TOTAL']]
#     extra_data += extra.get('extras', [])
#
#     buffer = BytesIO()
#     c = canvas.Canvas(buffer, pagesize=letter)
#
#     c.setFont("Helvetica", 12)
#     width, height = (612.0, 792.0)
#     y = 710
#     c.setFont("VeraBd", 12)
#     c.drawString(width / 2 - len('REPORT') * 4, y, "REPORT")
#     y -= 30
#     c.setFont("Vera", 11)
#     c.drawString(450, y, f"ON: {date.today()}")
#     y -= 40
#     c.setFont("Helvetica", 11)
#     c.drawString(width / 2 - len(f"Report from {info.get('date')} to {info.get('till')}: {info.get('name')}") * 2.5, y,
#                  f"Report from {info.get('date')} to {info.get('till')}:")
#     y -= 25
#     c.drawString(width / 2 - len(f"Name: {info.get('name')}, ID: {info.get('id')}") * 2.5, y,
#                  f"Name: {info.get('name')}, ID: {info.get('id')}")
#     rows = len(data)
#     table = Table(data, colWidths=[50, 100, 100, 100, 100, 100], rowHeights=[30] * rows)
#     style = TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.red),
#                         ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
#                         ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
#                         ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
#                         ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
#                         ('BACKGROUND', (0, 1), (-1, -1), colors.white),
#                         ('GRID', (0, 0), (-1, -1), 0.5, colors.grey)])
#     table.setStyle(style)
#     table.wrapOn(c, width, height)
#     table.drawOn(c, 5, y-550)
#
#     c.showPage()
#     rows_ex = len(extra_data)
#     table = Table(extra_data, colWidths=[50, 50, 50, 50, 50, 100, 100], rowHeights=[30] * rows_ex)
#     style = TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.lightcyan),
#                         ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
#                         ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
#                         ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
#                         ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
#                         ('BACKGROUND', (0, 1), (-1, -1), colors.white),
#                         ('GRID', (0, 0), (-1, -1), 0.5, colors.grey)])
#     table.setStyle(style)
#     table.wrapOn(c, width, height)
#     table.drawOn(c, 5, 100)
#
#
#     c.save()
#     pdf_bytes = buffer.getvalue()
#     buffer.close()
#     return pdf_bytes

# ===========================================================================================================================================


# from reportlab.lib.units import mm
# from reportlab.lib.pagesizes import letter
# from reportlab.pdfgen import canvas
# from io import BytesIO
# from datetime import date
# from reportlab.pdfbase import pdfmetrics
# from reportlab.pdfbase.ttfonts import TTFont
# from reportlab.platypus import Table, TableStyle, SimpleDocTemplate, PageBreak
# from reportlab.lib import colors
#
# # Register fonts
# # pdfmetrics.registerFont(TTFont('OpenSans', 'OpenSans-Regular.ttf'))
# # pdfmetrics.registerFont(TTFont('OpenSansBd', 'OpenSans-Bold.ttf'))
# pdfmetrics.registerFont(TTFont('Vera', 'Vera.ttf'))
# pdfmetrics.registerFont(TTFont('VeraBd', 'VeraBd.ttf'))


# def generate_pdf(info, extra):
#     buffer = BytesIO()
#     doc = SimpleDocTemplate(buffer, pagesize=letter)
#     elements = []
#     width, height = letter  # Letter size
#
#     def add_page_number(canvas, doc):
#         page_number_text = f"Page {canvas.getPageNumber()}"
#         canvas.drawRightString(200 * mm, 20 * mm, page_number_text)
#
#     # Custom method to draw header, footer, and report info
#     def on_new_page(canvas, doc):
#         canvas.setFont("VeraBd", 16)
#         canvas.drawCentredString(width / 2, height - 60, "Employee Report")
#
#         canvas.setFont("Vera", 11)
#         report_info = f"Report Period: {info.get('date')} to {info.get('till')} - Employee: {info.get('name')} (ID: {info.get('id')})"
#         canvas.drawCentredString(width / 2, height - 80, report_info)
#
#         add_page_number(canvas, doc)
#
#     doc.build(elements, onFirstPage=on_new_page, onLaterPages=on_new_page)
#
#     # Switch to using canvas for dynamic content
#     c = canvas.Canvas(buffer, pagesize=letter)
#     c.setFont("Vera", 10)
#     y_position = height - 100  # Starting Y position for the first table
#
#     # Table 1: Invoices
#     invoices_data = [['No.', 'Date', 'Customer', 'Remaining Total', 'Total', 'State']] + info.get('invoices', [])
#     invoices_table = Table(invoices_data, colWidths=[50, 100, 150, 100, 100, 100])
#     invoices_table_style = TableStyle([
#         ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
#         ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
#         ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
#         ('FONTNAME', (0, 0), (-1, -1), 'Vera'),
#         ('GRID', (0, 0), (-1, -1), 1, colors.lightblue)])
#     invoices_table.setStyle(invoices_table_style)
#
#     # Table 2: Extras
#     extras_data = [['Num', 'Draft', 'Paying', 'Paid', 'Cancelled', 'Remaining', 'Total']] + extra.get('extras', [])
#     extras_table = Table(extras_data, colWidths=[50, 50, 50, 50, 100, 100, 100])
#     extras_table_style = TableStyle([
#         ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
#         ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
#         ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
#         ('FONTNAME', (0, 0), (-1, 0), 'VeraBd'),
#         ('GRID', (0, 0), (-1, -1), 1, colors.grey)])
#     extras_table.setStyle(extras_table_style)
#
#     for table in [invoices_table, extras_table]:
#         table_height = table.wrap(0, 0)[1]
#         if y_position - table_height < 50:
#             c.showPage()
#             y_position = height - 100
#             on_new_page(c, doc)
#         table.drawOn(c, 5, y_position - table_height)
#         y_position -= table_height + 10
#
#     c.save()
#     pdf_bytes = buffer.getvalue()
#     buffer.close()
#     return pdf_bytes

# def generate_pdf(info, extra):
#     buffer = BytesIO()
#     doc = SimpleDocTemplate(buffer, pagesize=letter)
#     elements = []
#     width, height = letter  # Letter size
#
#     def add_page_number(canvas, doc):
#         page_number_text = f"Page {canvas.getPageNumber()}"
#         canvas.drawRightString(200 * mm, 20 * mm, page_number_text)
#
#     def on_new_page(canvas, doc):
#         canvas.setFont("VeraBd", 16)
#         canvas.drawString(width / 2, height - 60, "Employee Report")
#
#         canvas.setFont("Vera", 11)
#         report_info = f"Report Period: {info.get('date')} to {info.get('till')} - Employee: {info.get('name')} (ID: {info.get('id')})"
#         canvas.drawString(width / 2, height - 80, report_info)
#
#         add_page_number(canvas, doc)
#
#     doc.build(elements, onFirstPage=on_new_page, onLaterPages=on_new_page)
#
#     # Switch to using canvas for dynamic content
#     c = canvas.Canvas(buffer, pagesize=letter)
#     c.setFont("Vera", 10)
#     y_position = height - 300  # Starting Y position for the first table
#
#     # Table 1: Invoices
#     invoices_data = [['No.', 'Date', 'Customer', 'Remaining Total', 'Total', 'State']] + info.get('invoices', [])
#     invoices_table = Table(invoices_data, colWidths=[50, 100, 150, 100, 100, 100])
#     invoices_table_style = TableStyle([
#         ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
#         ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
#         ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
#         ('FONTNAME', (0, 0), (-1, -1), 'Vera'),
#         ('GRID', (0, 0), (-1, -1), 1, colors.lightblue)])
#     invoices_table.setStyle(invoices_table_style)
#
#     # Table 2: Extras
#     extras_data = [['Num', 'Draft', 'Paying', 'Paid', 'Cancelled', 'Remaining', 'Total']] + extra.get('extras', [])
#     extras_table = Table(extras_data, colWidths=[50, 50, 50, 50, 100, 100, 100])
#     extras_table_style = TableStyle([
#         ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
#         ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
#         ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
#         ('FONTNAME', (0, 0), (-1, 0), 'VeraBd'),
#         ('GRID', (0, 0), (-1, -1), 1, colors.grey)])
#     extras_table.setStyle(extras_table_style)
#
#     for table in [invoices_table, extras_table]:
#         table_height = table.wrap(0, 0)[1]
#         if y_position - table_height < 50:
#             c.showPage()
#             y_position = height - 100
#             on_new_page(c, doc)
#         table.drawOn(c, 5, y_position - table_height)
#         y_position -= table_height + 10
#
#     c.save()
#     pdf_bytes = buffer.getvalue()
#     buffer.close()
#     return pdf_bytes

# ===========================================================================================================================================
# ===========================================================================================================================================
# ===========================================================================================================================================
# ===========================================================================================================================================

from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import mm
from io import BytesIO
from datetime import datetime

def generate_pdf(info, extra):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    elements = []

    # Current Date for the header
    current_date = datetime.now().strftime("%d-%m-%Y")

    # Header elements
    header = Paragraph(f"<font size=12><b>Employee Report</b></font>", styles['Title'])
    report_info = Paragraph(f"Report Period: {info.get('date')} to {info.get('till')} - Employee: {info.get('name')} (ID: {info.get('id')})", styles['Normal'])
    date_info = Paragraph(f"<font size=9>Date: {current_date}</font>", styles['Normal'])

    elements.append(date_info)
    elements.append(Spacer(1, 12))
    elements.append(header)
    elements.append(Spacer(1, 12))
    elements.append(report_info)
    elements.append(Spacer(1, 12))

    # Invoice Data Table
    invoice_data = [['NUM', 'DATE', 'CUSTOMER', 'REMAINING TOTAL', 'TOTAL', 'STATUS']] + info.get('invoices', [])
    invoice_table = Table(invoice_data)
    invoice_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
    ]))
    elements.append(invoice_table)
    elements.append(Spacer(1, 12))

    # Stats Table
    stats_data = [['Num', 'Draft', 'Paying', 'Paid', 'Cancelled', 'Remaining', 'Total']] + extra.get('extras', [])
    stats_table = Table(stats_data)
    stats_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
    ]))
    elements.append(stats_table)

    doc.build(elements)

    pdf_bytes = buffer.getvalue()
    buffer.close()
    return pdf_bytes