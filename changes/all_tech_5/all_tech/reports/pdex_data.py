from odoo import api, fields, models
from odoo.exceptions import UserError
from odoo.tools import format_date


class InvoiceReports(models.AbstractModel):
    _name = "report.all_tech.pdex_data"
    _inherit = 'report.report_xlsx.abstract'
    _description = "Pdex Data Report"

    def get_data(self, data):
        start_date = data.get("date", False)
        end_date = data.get("till", False)

        invoices = self.env['all_tech.invoice'].search([
            ('date', '>=', start_date),
            ('date', '<=', end_date),
            ('type', '=', 'sell'),
        ])

        report_data = []

        for i in invoices:
            invoice_data = {
                'num': i.invoice_num,
                'date': i.date,
                'invoice_lines': [],
                'total': round(i.total, 3)
            }

            for line in i.sale_items_ids:
                line_data = {
                    'product': line.product_id.product,
                    'quantity_sold': line.quantity,
                    'price': line.price,
                    'total': line.total_price
                }
                invoice_data['invoice_lines'].append(line_data)
            report_data.append(invoice_data)
        return report_data

    @api.model
    def _get_report_values(self, docids, data=None):
        report_data = self.get_data(data)

        return {
            'doc_ids': docids,
            'docs': report_data,
        }

    def generate_xlsx_report(self, workbook, data, assets):
        report_data = self.get_data(data)

        sheet = workbook.add_worksheet('Invoice Report')

        headers = ['INVOICE', 'DATE', '', '', '', '', 'Total']
        header_format = workbook.add_format({'bg_color': 'red', 'font_color': 'white', 'bold': True})
        sheet.write_row(0, 0, headers, header_format)

        row = 1
        max_widths = [len(header) for header in headers]

        for invoice_data in report_data:
            invoice_num = invoice_data.get('num', '')
            invoice_date = format_date(self.env, invoice_data.get('date', ''))
            invoice_total = invoice_data.get('total', '')
            sheet.write(row, 0, invoice_num)
            sheet.write(row, 1, invoice_date)
            sheet.write(row, 6, invoice_total)
            max_widths[0] = max(max_widths[0], len(invoice_num))
            max_widths[1] = max(max_widths[1], len(invoice_date))
            max_widths[6] = max(max_widths[6], len(str(invoice_total)))

            for line in invoice_data.get('invoice_lines', []):
                row += 1
                product = line.get('product', '')
                quantity = line.get('quantity_sold', '')
                price = line.get('price', '')
                total = line.get('total', '')
                sheet.write(row, 2, product)
                sheet.write(row, 3, quantity)
                sheet.write(row, 4, price)
                sheet.write(row, 5, total)
                max_widths[2] = max(max_widths[2], len(product))
                max_widths[3] = max(max_widths[3], len(str(quantity)))
                max_widths[4] = max(max_widths[4], len(str(price)))
                max_widths[5] = max(max_widths[5], len(str(total)))

            row += 1

        for col, width in enumerate(max_widths):
            sheet.set_column(col, col, width + 2)

        if not report_data:
            raise UserError('No data found for the selected criteria.')

        workbook.close()
