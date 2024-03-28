from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import date
import random

class Patient(models.Model):
    _name = 'hospital.patient'
    _description = 'Hospital Patient'

    # for the chatter
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Name', required=True, tracking=True)
    l_name = fields.Char(string='Surname', required=True)
    ref = fields.Char(string='Reference', required=True, store=True)
    date_of_birth = fields.Date(string='Date of Birth')
    age = fields.Integer(string='Age', store=True, compute='_compute_age')
    gender = fields.Selection([('male', 'Male'), ('female', 'Female')], string='Gender')
    image = fields.Image(string='Image')
    active = fields.Boolean(string='Active', default=True)

    _sql_constraints = [
        ('ref', 'unique (ref)', 'Reference must be unique')
    ]

    @api.constrains('gender')
    def _check_gender(self):
        for patient in self:
            if patient.gender not in ['male', 'female']:
                raise ValidationError("Gender must be either 'Male' or 'Female'.")

    @api.depends('date_of_birth')
    def _compute_age(self):
        today = date.today()
        for patient in self:
            if patient.date_of_birth:
                patient.age = today.year - patient.date_of_birth.year - ((today.month, today.day) < (patient.date_of_birth.month, patient.date_of_birth.day))

    @api.onchange('ref', 'date_of_birth')
    def onchange_ref(self):
        if self.date_of_birth:
            self.ref = f"REF{self.age}{self.date_of_birth.year}{random.randint(1,10)}"
