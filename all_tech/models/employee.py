from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Employee(models.Model):
    _name = 'all_tech.employee'
    _description = 'Employee'

    name = fields.Char(string='Name', required=True)
    email = fields.Char(string='email')
    phone = fields.Char(string='Phone Number', required=True, default='121541541')
    department = fields.Many2one('all_tech.department', string='Department', required=True)
    email_len = fields.Integer(string='Email Length', compute='_compute_email_len', store=True)

    _sql_constraints = [
        ('name', 'unique (name)', 'The name code must be unique!'),
        ('phone', 'unique (phone)', 'The phone code must be unique!'),
    ]

    @api.constrains('phone')
    def _check_phone(self):
        for record in self:
            if len(record.phone) > 10:
                raise ValidationError("Phone number must be less than 10")

    @api.depends('email')
    def _compute_email_len(self):
        for record in self:
            record.email_len = len(record.email) if record.email else 0

    @api.onchange('department')
    def _onchange_department(self):
        self.name = self.department.name

    def set_default_department(self):
        department = self.env['all_tech.department'].search([('name', 'ilike', 'test')], limit=1)
        if department.exists():
            self.department = department.id
        else:
            self.department = self.env['all_tech.department'].create({'name': 'test'}).id

    @api.model
    def create(self, values):
        # Add code here
        rec = super(Employee, self).create(values)

        return rec

    def write(self, values):
        # Add code here
        rec = super(Employee, self).write(values)

        return rec

    def unlink(self):
        rec = super(Employee, self).unlink()
        return rec
