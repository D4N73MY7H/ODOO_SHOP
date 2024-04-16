from odoo import api, fields, models


class InvoiceReports(models.AbstractModel):
    _name = "report.all_tech.pdex_data"
    _inherit = 'report.report_xlsx.abstract'
    _description = "Pdex Data Report"

    @api.model
    def _get_report_values(self, docids, data=None):

        name = "Invoice Report"

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
                'total': i.total
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

        return {
            'doc_ids': docids,
            'docs': report_data,
            'r_name': name
        }