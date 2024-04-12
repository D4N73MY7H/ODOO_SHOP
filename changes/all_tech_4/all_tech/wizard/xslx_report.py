from odoo import models, fields, api


class Productreport(models.TransientModel):
    _name = 'all_tech.product.report'
    _description = 'Product Report'

    product_id = fields.Many2one('all_tech.product', string='Product')
    date = fields.Date('Start Date')
    till = fields.Date('End Date')

    def report_product(self):
        sale_items = self.env['all_tech.sale_item'].search([
            ('invoice_id.type', '=', 'sell'),
            ('invoice_id.state', '=', 'paid'),
            ('sale_date', '>=', self.date),
            ('sale_date', '<=', self.till)
        ])

        product_data = []
        for item in sale_items:
            product_data.append({
                'product': item.product_id.product,
                'quantity_sold': item.quantity,
                'quantity_in_stock': item.product_id.quantity,
                'total_earnings': item.total_price
            })

        return self.env.ref('all_tech.action_report_product_st').report_action(self, data={'products': product_data,
                                                                                           'date': self.date,
                                                                                           'till': self.till})
