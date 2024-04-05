from odoo import models, fields, api


class Supplier(models.Model):
    _name = 'all_tech.supplier'
    _description = 'Supplier'

    name = fields.Char(string='Name', required=True)
    contact_person = fields.Char(string='Contact Person', required=True)
    email = fields.Char(string='E-Mail', required=True)
    phone = fields.Char(string='Phone', required=True)
    country = fields.Char(string='Country', required=True)
    city = fields.Char(string='City', required=True)
    image = fields.Binary(string='Image', attachment=True)
