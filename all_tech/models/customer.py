from odoo import models, fields, api


class Customer(models.Model):
    _name = 'all_tech.customer'
    _description = 'Customer'

    name = fields.Char(string='First Name', required=True)
    l_name = fields.Char(string='Last Name', required=True)
    email = fields.Char(string='E-Mail', required=True)
    phone = fields.Char(string='Phone', required=True)
    country = fields.Char(string='Country', required=True)
    city = fields.Char(string='City', required=True)
    image = fields.Binary(string='Book Image', attachment=True)

