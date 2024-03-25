from odoo import models, fields

class Department(models.Model):
    _name = 'all_tech.department'
    _description = 'Departments'

    name = fields.Char(string='Name', required=True)
    description = fields.Char(string='Description')
    employee_ids = fields.One2many(comodel_name='all_tech.employee', inverse_name='department', string='Employees')

