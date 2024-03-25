from odoo import models, fields, api


class Category(models.Model):
    _name = 'all_tech.category'
    _description = 'Product Category'
    _rec_name = 'category'

    category = fields.Char(string='Category', required=True)
    description = fields.Char(string='Description', required=True)