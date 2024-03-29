from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import date

class Patient(models.Model):
    _name = 'hospital.patient'
    _description = 'Hospital Patient'
    _rec_name = 'full_name'

    # for the chatter
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Name', required=True, tracking=True)
    l_name = fields.Char(string='Surname', required=True)
    full_name = fields.Char(string='Full Name', compute='_compute_full_name', store=True)
    ref = fields.Char(string='Reference', required=True, store=True)
    date_of_birth = fields.Date(string='Date of Birth')
    age = fields.Integer(string='Age', store=True, compute='_compute_age')
    gender = fields.Selection([('male', 'Male'), ('female', 'Female')], string='Gender')
    image = fields.Image(string='Image')
    active = fields.Boolean(string='Active', default=True)
    app_count = fields.Integer(string='Appointment Count', compute='_compute_app_count')

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

    @api.depends('name', 'l_name')
    def _compute_full_name(self):
        for record in self:
            if record.name and record.l_name:
                record.full_name = f"{record.name} {record.l_name}"
            else:
                record.full_name = record.name or record.l_name

    def _compute_app_count(self):
        print(self)
        for a in self:
            print(a.age)
            a.app_count = self.env['hospital.appointment'].search_count([('patient_id', '=', a.id)])

    @api.model
    def create(self, vals):
        print(vals)
        vals['ref'] = self.env['ir.sequence'].next_by_code('hospital.appointment.sequence')
        return super(Patient, self).create(vals)
