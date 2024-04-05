from odoo import models, fields, api


class Department(models.Model):
    _name = 'all_tech.department'
    _description = 'Departments'
    _rec_name = 'department'

    department = fields.Char(string='Department', required=True)
    description = fields.Text(string='Description')
    employee_ids = fields.One2many(comodel_name='all_tech.employee', inverse_name='department', string='Employees')


