from odoo import models, fields, api
import re
from odoo.exceptions import ValidationError

regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'


class Customer(models.Model):
    _name = 'all_tech.customer'
    _description = 'Customer'
    _rec_name = 'full_name'

    name = fields.Char(string='First Name', required=True)
    last_name = fields.Char(string='Last Name', required=True)
    full_name = fields.Char(string='Full Name', compute='_compute_full_name', store=True)
    email = fields.Char(string='E-Mail', required=True)
    phone = fields.Char(string='Phone', required=True)
    image = fields.Binary(string='Image', attachment=True)
    ref = fields.Char(string='Reference', readonly=True)

    _sql_constraints = [
        ('phone', 'unique (phone)', 'The phone must be unique!'),
        ('email', 'unique (email)', 'The email must be unique!'),
    ]

    @api.depends('name', 'last_name')
    def _compute_full_name(self):
        for record in self:
            if record.name and record.last_name:
                record.full_name = f"{record.name} {record.last_name}"
            else:
                record.full_name = record.name or record.last_name

    @api.constrains('phone')
    def _check_phone(self):
        for record in self:
            if len(record.phone) != 11:
                raise ValidationError("Phone number must be less than 11")

    @api.constrains('email')
    def _check_email_format(self):
        for record in self:
            if record.email:
                if not re.fullmatch(regex, self.email):
                    raise ValidationError("Invalid email format")

    @api.model
    def create(self, vals):
        print(vals)
        vals['ref'] = self.env['ir.sequence'].next_by_code('tech.customer.seq')
        return super(Customer, self).create(vals)
