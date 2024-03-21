from odoo import models, fields

class Employee(models.Model):
    _name = 'all_tech.employee'
    _description = 'Employee'

    name = fields.Char(string='Name', required=True)
    email = fields.Char(string='email')
    phone = fields.Char(string='Phone Number', required=True)
