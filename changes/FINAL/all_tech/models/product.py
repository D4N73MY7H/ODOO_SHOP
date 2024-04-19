from odoo import models, fields, api


class Product(models.Model):
    _name = 'all_tech.product'
    _description = 'Product'
    _rec_name = 'product'

    product = fields.Char(string='Product', required=True)
    description = fields.Text(string='Description', required=True)
    unit_price = fields.Float(string='Unit Price', required=True)
    price = fields.Float(string='Price', required=True)
    quantity = fields.Integer(string='Quantity in Stock', required=True)
    image = fields.Binary(string='Image', attachment=True)

    category_ids = fields.Many2many('all_tech.category', string='Categories', required=True)
