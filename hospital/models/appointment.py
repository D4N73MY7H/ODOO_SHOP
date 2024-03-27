from odoo import models, fields, api

class Appointment(models.Model):
    _name = 'hospital.appointment'
    _description = 'Hospital Appointment'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'ref'

    patient_id = fields.Many2one('hospital.patient', string='Patient')
    gender = fields.Selection(related='patient_id.gender')
    time = fields.Datetime(string='Time', required=True, default=fields.Datetime.now)
    date = fields.Date(string='Date', required=True, default=fields.Date.context_today)
    ref = fields.Char(string='Reference', readonly=True, store='True')
    prescription = fields.Html(string='Prescription')
    priority = fields.Selection([
        ('0', 'Very Low'),
        ('1', 'Low'),
        ('2', 'Normal'),
        ('3', 'High'),
        ('4', 'High'),
        ('5', 'Maximal')], string="Priority")
    state = fields.Selection([
        ('draft', 'Draft'),
        ('inConsultation', 'In Consultation'),
        ('done', 'Done'),
        ('4cancel', 'Cancelled')], default='draft',string="Status", required=True)

    # @api.constrains('patient_id')
    # def onchange_patient_id(self):
    #     if self.patient_id:
    #         year = self.patient_id.date_of_birth.year if self.patient_id.date_of_birth else 'Unknown'
    #         self.ref = f"REF{self.patient_id.id}{year}"
    #
    # @api.onchange('ref', 'patient_id')
    # def onchange_patient_id(self):
    #     if self.patient_id:
    #         year = self.patient_id.date_of_birth.year if self.patient_id.date_of_birth else 'Unknown'
    #         self.ref = f"REF{self.patient_id.id}{year}"
