from odoo import models, fields, api
import re
from odoo.exceptions import ValidationError


class Employee(models.Model):
    _name = 'all_tech.employee'
    _description = 'Employee'

    name = fields.Char(string='Name', required=True)
    last_name = fields.Char(string='Last Name', required=True)
    email = fields.Char(string='E-mail')
    phone = fields.Char(string='Phone Number', required=True)
    department = fields.Many2one('all_tech.department', string='Department', required=True)
    image = fields.Binary(string='Image', attachment=True)

    _sql_constraints = [
        ('phone', 'unique (phone)', 'The phone code must be unique!'),
    ]

    @api.constrains('phone')
    def _check_phone(self):
        for record in self:
            if len(record.phone) != 11:
                raise ValidationError("Phone number must be less than 11")

    @api.constrains('email')
    def _check_email(self):
        for record in self:
            if not re.match(r"^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$", record.email):
                raise ValidationError("Invalid email format")

    # @api.depends('email')
    # def _compute_email_len(self):
    #     for record in self:
    #         record.email_len = len(record.email) if record.email else 0

    # @api.onchange('department')
    # def _onchange_department(self):
    #     self.name = self.department.department

    # def set_default_department(self):
    #     department = self.env['all_tech.department'].search([('department', 'ilike', 'test')], limit=1)
    #     if department.exists():
    #         self.department = department.id
    #     else:
    #         self.department = self.env['all_tech.department'].create({'department': 'test'}).id
    #
    # @api.model
    # def create(self, values):
    #     # Add code here
    #     rec = super(Employee, self).create(values)
    #
    #     return rec
    #
    # def write(self, values):
    #     # Add code here
    #     rec = super(Employee, self).write(values)
    #
    #     return rec
    #
    # def unlink(self):
    #     rec = super(Employee, self).unlink()
    #     return rec
