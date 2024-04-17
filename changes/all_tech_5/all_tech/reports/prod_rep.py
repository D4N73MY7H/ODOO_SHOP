# from odoo import models
#
#
# class ProdReport(models.AbstractModel):
#     _name = 'report.all_tech.product_report'
#     _inherit = 'report.report_xlsx.abstract'
#
#
#     def generate_xlsx_report(self, workbook, data, assets):
#         worksheet = workbook.add_worksheet('Products Report')
#
#         header_format = workbook.add_format({'bold': True, 'align': 'center', 'bg_color': '#D3D3D3'})
#         header_labels = ['Product', 'Quantity Sold', 'Quantity In Stock', 'Total Earnings']
#         for col, label in enumerate(header_labels):
#             worksheet.write(0, col, label, header_format)
#
#         prods = data['products']
#
#         # Write data rows
#         row = 1
#         for a in prods:
#             worksheet.write(row, 0, a['product'])
#             worksheet.write(row, 1, a['quantity_sold'])
#             worksheet.write(row, 2, a['quantity_in_stock'])
#             worksheet.write(row, 3, a['total_earnings'])
#             row += 1
#
#         # Auto-adjust column width
#         worksheet.set_column(0, len(header_labels) - 1, 15)
#         workbook.close()

# ==============================================================================================================================
# ==============================================================================================================================
# ==============================================================================================================================
# ==============================================================================================================================
# ==============================================================================================================================


# from odoo import models
#
#
# class ProdReport(models.AbstractModel):
#     _name = 'report.all_tech.product_report'
#     _inherit = 'report.report_xlsx.abstract'
#
#
#     def generate_xlsx_report(self, workbook, data, assets):
#         worksheet = workbook.add_worksheet('Products Report')
#
#         # Define formats
#         header_format = workbook.add_format({'bold': True, 'align': 'center', 'bg_color': '#D3D3D3'})
#         data_format = workbook.add_format({'align': 'center'})
#         money_format = workbook.add_format({'num_format': '$#,##0.00'})
#
#         # Write header labels
#         header_labels = ['Product', 'Quantity Sold', 'Quantity In Stock', 'Total Earnings']
#         for col, label in enumerate(header_labels):
#             worksheet.write(0, col, label, header_format)
#
#         # Write data rows
#         prods = data['products']
#         for row, product_data in enumerate(prods, start=1):
#             worksheet.write(row, 0, product_data['product'], data_format)
#             worksheet.write(row, 1, product_data['quantity_sold'], data_format)
#             worksheet.write(row, 2, product_data['quantity_in_stock'], data_format)
#             worksheet.write(row, 3, product_data['total_earnings'], money_format)
#
#         # Auto-adjust column width
#         worksheet.set_column(0, len(header_labels) - 1, 20)
#
#         workbook.close()


# ==============================================================================================================================
# ==============================================================================================================================
# ==============================================================================================================================
# ==============================================================================================================================
# ==============================================================================================================================


from odoo import models
from datetime import datetime

class ProdReport(models.AbstractModel):
    _name = 'report.all_tech.product_report'
    _inherit = 'report.report_xlsx.abstract'

    # def generate_xlsx_report(self, workbook, data, assets):
    #     worksheet = workbook.add_worksheet('Products Report')
    #
    #     # Define formats
    #     title_format = workbook.add_format({'bold': True, 'font_size': 14})
    #     header_format = workbook.add_format({'bold': True, 'align': 'center', 'bg_color': '#FF0000', 'font_color': '#FFFFFF'})
    #     data_format = workbook.add_format({'align': 'center'})
    #     money_format = workbook.add_format({'num_format': '$#,##0.00', 'align': 'center'})
    #     total_label_format = workbook.add_format({'bg_color': '#ADD8E6', 'bold': True})
    #     total_value_format = workbook.add_format({'bg_color': '#ADD8E6', 'num_format': '$#,##0.00', 'bold': True})
    #
    #     # Titles
    #     date = datetime.strptime(data['date'], '%Y-%m-%d').strftime('%d.%m.%y')
    #     till = datetime.strptime(data['till'], '%Y-%m-%d').strftime('%d.%m.%y')
    #
    #     worksheet.merge_range('A1:D1', 'Products Sold', title_format)
    #     worksheet.merge_range('A2:D2', f"{date} to {till}", title_format)
    #
    #     # Write header labels
    #     header_labels = ['Product', 'Quantity Sold', 'Quantity In Stock', 'Total Earnings']
    #     for col, label in enumerate(header_labels):
    #         worksheet.write(3, col, label, header_format)
    #
    #     # Write data rows and calculate total earnings
    #     prods = data['products']
    #     total_earnings = 0
    #     max_lengths = [len(label) for label in header_labels]
    #     for row, product_data in enumerate(prods, start=4):
    #         worksheet.write(row, 0, product_data['product'], data_format)
    #         worksheet.write(row, 1, product_data['quantity_sold'], data_format)
    #         worksheet.write(row, 2, product_data['quantity_in_stock'], data_format)
    #         worksheet.write(row, 3, product_data['total_earnings'], money_format)
    #         total_earnings += product_data['total_earnings']
    #
    #     # Total table
    #     last_row = len(prods) + 4
    #     worksheet.merge_range(last_row, 0, last_row, 2, 'Total', total_label_format)
    #     worksheet.write(last_row, 3, total_earnings, total_value_format)
    #
    #     # Auto-adjust column width
    #     worksheet.set_column(0, len(header_labels) - 1, 30)
    #
    #     workbook.close()

    def generate_xlsx_report(self, workbook, data, assets):
        worksheet = workbook.add_worksheet('Products Report')

        # Define formats
        title_format = workbook.add_format({'bold': True, 'font_size': 14})
        header_format = workbook.add_format(
            {'bold': True, 'align': 'center', 'bg_color': '#FF0000', 'font_color': '#FFFFFF'})
        data_format = workbook.add_format({'align': 'center'})
        money_format = workbook.add_format({'num_format': '$#,##0.00', 'align': 'center'})
        total_label_format = workbook.add_format({'bg_color': '#ADD8E6', 'bold': True})
        total_value_format = workbook.add_format({'bg_color': '#ADD8E6', 'num_format': '$#,##0.00', 'bold': True})

        # Titles
        date = datetime.strptime(data['date'], '%Y-%m-%d').strftime('%d.%m.%y')
        till = datetime.strptime(data['till'], '%Y-%m-%d').strftime('%d.%m.%y')

        worksheet.merge_range('A1:D1', 'Products Sold', title_format)
        worksheet.merge_range('A2:D2', f"{date} to {till}", title_format)

        # Write header labels
        header_labels = ['Product', 'Quantity Sold', 'Quantity In Stock', 'Total Earnings']
        for col, label in enumerate(header_labels):
            worksheet.write(3, col, label, header_format)

        # Write data rows and calculate total earnings
        prods = data['products']
        total_earnings = 0

        # Find the length of the longest product name
        max_product_length = max(len(product_data['product']) for product_data in prods)

        # Write data rows
        for row, product_data in enumerate(prods, start=4):
            worksheet.write(row, 0, product_data['product'], data_format)
            worksheet.write(row, 1, product_data['quantity_sold'], data_format)
            worksheet.write(row, 2, product_data['quantity_in_stock'], data_format)
            worksheet.write(row, 3, product_data['total_earnings'], money_format)
            total_earnings += product_data['total_earnings']

        # Total table
        last_row = len(prods) + 4
        worksheet.merge_range(last_row, 0, last_row, 2, 'Total', total_label_format)
        worksheet.write(last_row, 3, total_earnings, total_value_format)

        # Set column widths
        worksheet.set_column(0, 0, max(20, min(50, max_product_length * 1.1)))  # Product column width
        for col in range(1, len(header_labels)):
            worksheet.set_column(col, col, 20)  # Width for other columns

        workbook.close()


