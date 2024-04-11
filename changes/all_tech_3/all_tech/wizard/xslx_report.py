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

        product_data = {}
        for item in sale_items:
            product = item.product_id
            if product not in product_data:
                product_data[product] = {
                    'quantity_sold': 0,
                    'total_earnings': 0,
                    'quantity_in_stock': product.quantity
                }
            product_data[product]['quantity_sold'] += item.quantity
            product_data[product]['total_earnings'] += item.total_price

        result = []
        for product, data in product_data.items():
            result.append({
                'product': product.product,
                'quantity_sold': data['quantity_sold'],
                'quantity_in_stock': data['quantity_in_stock'],
                'total_earnings': data['total_earnings']
            })

        return self.env.ref('all_tech.action_report_product_st').report_action(None, data=result)





