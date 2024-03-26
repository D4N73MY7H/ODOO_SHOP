from odoo import models, fields, api


class Customer(models.Model):
    _name = 'all_tech.customer'
    _description = 'Customer'

    name = fields.Char(string='First Name', required=True)
    l_name = fields.Char(string='Last Name', required=True)
    email = fields.Char(string='E-Mail', required=True)
    phone = fields.Char(string='Phone', required=True)
    type = fields.Selection([('registered', 'Registered'), ('new', 'New')], required=True, string='Type')
    image = fields.Binary(string='Image', attachment=True)

