from odoo import models, fields, api


class Product(models.Model):
    _name = 'all_tech.product'
    _description = 'Product'
    _rec_name = 'product'

    product = fields.Char(string='Product', required=True)
    description = fields.Char(string='Description', required=True)
    unit_price = fields.Char(string='Unit Price', required=True)
    quantity = fields.Char(string='Quantity in Stock', required=True)
    image = fields.Binary(string='Book Image', attachment=True)