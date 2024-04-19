from odoo import models, fields, api


class Productreport(models.TransientModel):
    _name = 'all_tech.product.report'
    _description = 'Product Report'

    product_id = fields.Many2one('all_tech.product', string='Product')
    date = fields.Date('Start Date')
    till = fields.Date('End Date')

    def report_product(self):
        products = self.env['all_tech.product'].search([])

        product_data = []
        for product in products:
            sale_items = self.env['all_tech.sale_item'].search([
                ('product_id', '=', product.id),
                ('invoice_id.type', '=', 'sell'),
                ('invoice_id.state', '=', 'paid'),
                ('sale_date', '>=', self.date),
                ('sale_date', '<=', self.till)
            ])
            total_earnings = sum(item.total_price for item in sale_items)
            total_quantity_sold = sum(item.quantity for item in sale_items)
            product_data.append({
                'product': product.product,
                'quantity_sold': total_quantity_sold,
                'quantity_in_stock': product.quantity,
                'total_earnings': total_earnings
            })

        return self.env.ref('all_tech.action_report_product_st').report_action(self, data={'products': product_data,
                                                                                           'date': self.date,
                                                                                           'till': self.till})
